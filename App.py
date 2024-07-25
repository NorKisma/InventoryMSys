# app.py (Example Flask application)
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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if 'id' in request.form:
            # Handle user edit
            user_id = request.form['id']
            ful_name = request.form['name']
            tel = request.form['tel']
            email = request.form['email']
            gender = request.form['gender']
            sql = """UPDATE users 
                     SET ful_name = %s, tel = %s, email = %s, gender = %s 
                     WHERE id = %s"""
            val = (ful_name, tel, email, gender, user_id)
            mycursor.execute(sql, val)
        else:
            # Handle user registration
            ful_name = request.form['name']
            tel = request.form['tel']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])
            role = request.form['role']
            sql = "INSERT INTO users (ful_name, tel, email, password, role) VALUES (%s, %s, %s, %s, %s)"
            val = (ful_name, tel, email, password, role)
            mycursor.execute(sql, val)
        
        mydb.commit()
        return redirect(url_for('signup'))
    
    # Fetch all users
    mycursor.execute("SELECT * FROM users")
    data = mycursor.fetchall()
    return render_template('signup.html', data=data)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    # Handle user deletion
    sql = "DELETE FROM users WHERE id = %s"
    mycursor.execute(sql, (id,))
    mydb.commit()
    return redirect(url_for('signup'))

@app.route('/customers', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':

    # Retrieve form data
        name = request.form.get('customerName')
        tel = request.form.get('customerTel')
        gender = request.form.get('customerGender')
        email = request.form.get('customerEmail')
        customer_id = request.form.get('customerId')

        if customer_id:
            # Edit customer
            sql = "UPDATE customers SET name = %s, tel = %s, email = %s, gender = %s WHERE id = %s"
            val = (name, tel, email, gender, customer_id)
        else:
            # Add new customer
            sql = "INSERT INTO customers (name, tel, email, gender) VALUES (%s, %s, %s, %s)"
            val = (name, tel, email, gender)
        
        mycursor.execute(sql, val)
        mydb.commit()
    # Fetch all customers
    data = fetch_customers()
    return render_template('customers.html', data=data)

@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    sql = "DELETE FROM customers WHERE id = %s"
    mycursor.execute(sql, (id,))
    mydb.commit()
    return redirect(url_for('customers'))

def fetch_customers():
    mycursor.execute("SELECT * FROM customers")
    return mycursor.fetchall()
