import os
import mysql.connector
from app.constants import ALL, ONE, VALUE

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        autocommit=True)

def execute(query, operation=None, params=(), value=None):
    result = None
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    if operation == ALL:
        result = cursor.fetchall()
    if operation == ONE:
        result = cursor.fetchone()
    if operation == VALUE:
        result = cursor.fetchone()[value]
    cursor.close()
    connection.close()
    return result

