
# 🚗 Car Rental Management System

A full-stack **DBMS project** built using **Flask (Python) + MySQL**, designed to manage car rentals, customers, billing, and payments efficiently.

---

## 📌 Features

* 👤 Add and manage customers
* 🚘 Add and manage cars
* 📅 Rent cars with start & end date
* 🔁 Return cars with validation
* 💰 Automatic rent calculation
* ⏱ Late fee calculation (₹500/day)
* 💳 Payment method selection (Cash / Online / Card)
* 🧾 Professional invoice generation
* 📊 Total revenue calculation (returned cars only)
* 🔒 Date validation (no future / invalid return dates)

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS
* **Backend:** Flask (Python)
* **Database:** MySQL
* **Tools:** VS Code, MySQL Workbench

---

## 📂 Project Structure

```
DBMS Project/
│── app.py              # Main Flask application
│── db_config.py        # Database connection
│── templates/
│   ├── index.html      # Main UI
│   ├── bill.html       # Invoice page
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/car-rental-system.git
cd car-rental-system
```

---

### 2️⃣ Install Dependencies

```
pip install flask mysql-connector-python
```

---

### 3️⃣ Setup Database

Open MySQL Workbench and run:

```
CREATE DATABASE car_rental;

USE car_rental;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(50),
    price_per_day INT,
    status VARCHAR(20) DEFAULT 'Available'
);

CREATE TABLE rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    car_id INT,
    start_date DATE,
    end_date DATE,
    return_date DATE,
    total_cost INT,
    payment_method VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (car_id) REFERENCES cars(id)
);
```

---

### 4️⃣ Configure Database

Edit `db_config.py`:

```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="car_rental"
    )
```

---

### 5️⃣ Run Application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 📊 Key Functionalities

### 🚘 Rent Car

* Select customer & car
* Choose start & end date
* Cost calculated automatically

### 🔁 Return Car

* Select return date
* Choose payment method
* Late fee applied if delayed

### 🧾 Invoice

* Shows customer, car, dates
* Displays late fee & total amount
* Includes payment method

---

## 🔐 Validation Rules

* Return date must be between **start date and current date**
* No future return allowed
* Minimum rental = 1 day

---

## 🎯 Future Enhancements

* 🔐 Login system
* 📊 Dashboard with graphs
* 📄 PDF invoice download
* 🔍 Search & filter
* 📱 Responsive UI

---

## 👨‍💻 Author

**Krish**
B.Tech CSE

---


