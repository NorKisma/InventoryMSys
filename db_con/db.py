import mysql.connector


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Inventory_db"
    )
except mysql.connector.Error as err:
    print(f"Error: {err}")