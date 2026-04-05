from flask import Flask, render_template, request, redirect
from db_config import get_db_connection
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM cars WHERE status='Available'")
    cars = cursor.fetchall()

    cursor.execute("""
SELECT r.id, c.name, ca.brand, ca.model, 
       r.start_date, r.end_date, r.return_date, 
       r.total_cost, r.payment_method   -- 🔥 ADD THIS
FROM rentals r
JOIN customers c ON r.customer_id = c.id
JOIN cars ca ON r.car_id = ca.id
""")
    rentals = cursor.fetchall()

    # 🔥 ADD THIS PART (TOTAL CALCULATION)
    total_returned = 0
    for r in rentals:
        if r['return_date'] is not None:
            total_returned += r['total_cost']

    conn.close()

    return render_template(
        "index.html",
        customers=customers,
        cars=cars,
        rentals=rentals,
        total_returned=total_returned   # 👈 send to HTML
    )


@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
        (data['name'], data['email'], data['phone'])
    )

    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/add_car', methods=['POST'])
def add_car():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO cars (brand, model, price_per_day) VALUES (%s, %s, %s)",
        (data['brand'], data['model'], data['price'])
    )

    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/rent_car', methods=['POST'])
def rent_car():
    data = request.form

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    start = datetime.strptime(data['start'], "%Y-%m-%d")
    end = datetime.strptime(data['end'], "%Y-%m-%d")

    days = (end - start).days

    cursor.execute("SELECT price_per_day FROM cars WHERE id=%s", (data['car_id'],))
    price = cursor.fetchone()['price_per_day']

    total = days * price

    cursor.execute("""
        INSERT INTO rentals (customer_id, car_id, start_date, end_date, total_cost)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['customer_id'], data['car_id'], data['start'], data['end'], total))

    cursor.execute("UPDATE cars SET status='Rented' WHERE id=%s", (data['car_id'],))

    conn.commit()
    conn.close()

    return redirect('/')


# 🔥 Show return form
# @app.route('/return_form/<int:rental_id>')
# def return_form(rental_id):
#     return render_template("return.html", rental_id=rental_id)


# 🔥 Handle return logic
from datetime import datetime, date

@app.route('/return_car', methods=['POST'])
def return_car():

    rental_id = request.form['rental_id']
    return_date = datetime.strptime(request.form['return_date'], "%Y-%m-%d").date()
    payment_method = request.form['payment_method']
    today = date.today()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rentals WHERE id=%s", (rental_id,))
    rental = cursor.fetchone()

    start_date = rental['start_date']

    # 🔥 FINAL VALIDATION
    if not (start_date <= return_date <= today):
        return "❌ Return date must be between start date and today"

    # -------------------------

    cursor.execute("SELECT price_per_day FROM cars WHERE id=%s", (rental['car_id'],))
    price = cursor.fetchone()['price_per_day']

    days = (return_date - start_date).days
    if days <= 0:
        days = 1

    total_cost = days * price

    # late fee
    if return_date > rental['end_date']:
        late_days = (return_date - rental['end_date']).days
        total_cost += late_days * 500

    # update
    cursor.execute("""
    UPDATE rentals 
    SET return_date=%s, total_cost=%s, payment_method=%s
    WHERE id=%s
""", (return_date, total_cost, payment_method, rental_id))

    cursor.execute("UPDATE cars SET status='Available' WHERE id=%s", (rental['car_id'],))

    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/bill/<int:rental_id>')
def bill(rental_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
SELECT r.*, c.name, c.email, c.phone,
       ca.brand, ca.model, ca.price_per_day
FROM rentals r
JOIN customers c ON r.customer_id = c.id
JOIN cars ca ON r.car_id = ca.id
WHERE r.id=%s
""", (rental_id,))

    data = cursor.fetchone()

    # calculate late fee
    if data['return_date'] and data['return_date'] > data['end_date']:
        late_days = (data['return_date'] - data['end_date']).days
        late_fee = late_days * 500
    else:
        late_fee = 0

    conn.close()

    return render_template("bill.html", data=data, late_fee=late_fee)
if __name__ == '__main__':
    app.run(debug=True)