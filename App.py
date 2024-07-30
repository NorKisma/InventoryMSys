from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
import mysql.connector

app = Flask(__name__)

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="std"
)
mycursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        full_name = request.form.get('userName')
        tel = request.form.get('userTel')
        email = request.form.get('userEmail')
        role = request.form.get('userRole')
        DateT = request.form.get('userDate')

        if user_id:
            # Handle user edit
            sql = """UPDATE users 
                     SET ful_name = %s, tel = %s, email = %s, role = %s, DateT = %s
                     WHERE id = %s"""
            val = (full_name, tel, email, role, DateT, user_id)
        else:
            # Handle user registration
            password = generate_password_hash(request.form.get('userPassword'))
            sql = "INSERT INTO users (ful_name, tel, email, password, role,DateT) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (full_name, tel, email, password, role,DateT)

        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('register_user'))

    # Fetch all users
    mycursor.execute("SELECT * FROM users")
    data = mycursor.fetchall()
    return render_template('Register.html', data=data)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    # Handle user deletion
    sql = "DELETE FROM users WHERE id = %s"
    mycursor.execute(sql, (id,))
    mydb.commit()
    return redirect(url_for('register_user'))

@app.route('/customers', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('customerName')
        tel = request.form.get('customerTel')
        gender = request.form.get('customerGender')
        email = request.form.get('customerEmail')
        DateT = request.form.get('customerDate')
        customer_id = request.form.get('customerId')

        if customer_id:
            # Edit customer
            sql = "UPDATE customers SET name = %s, tel = %s, email = %s, gender = %s, DateT = %s WHERE id = %s"
            val = (name, tel, email, gender, DateT, customer_id)
        else:
            # Add new customer
            sql = "INSERT INTO customers (name, tel, email, gender, DateT) VALUES (%s, %s, %s, %s, %s)"
            val = (name, tel, email, gender, DateT)

        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('add_customer'))

    # Fetch all customers
    data = fetch_customers()
    return render_template('customers.html', data=data)

@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    sql = "DELETE FROM customers WHERE id = %s"
    mycursor.execute(sql, (id,))
    mydb.commit()
    return redirect(url_for('add_customer'))

def fetch_customers():
    mycursor.execute("SELECT * FROM customers")
    return mycursor.fetchall()
