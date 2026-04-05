import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="singhal@2006",  
        database="car_rental"
    )