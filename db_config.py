from dotenv import load_dotenv
import os
import pyodbc
from pyodbc import Error

load_dotenv()

def get_connection():
    try:
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE")
        driver = os.getenv("SQL_DRIVER")
        if not all([server, database, driver]):
            raise ValueError("Missing SQL Server Infor")
        conn = f"DRIVER={{{driver}}};SERVER={server};Database={database};Trusted_Connection=yes;"
        conn =pyodbc.connect(conn)
        return conn
    except Error  as e:
        print("Database connection failed. Check your connection")
        print(e)
        return None
    except Exception as e:
        print("Database connection failed. Check your connection")
        print(e)
        return None

def check_connection():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(version)
        conn.close()
    else:
        print("Database connection failed. Check your connection")

if __name__ == "__main__":
    check_connection()
