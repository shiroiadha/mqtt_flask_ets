import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="atmin_mqtt",
        password="masadmin_masadmin#1234",
        database="mysensor_db"
    )
