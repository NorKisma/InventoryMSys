from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Ensure you use a secure key in production

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="std"
)
mycursor = mydb.cursor()

@app.route('/index')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        flash('You need to login first', 'danger')
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        # Fetch user
        mycursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = mycursor.fetchone()

        # Check if user exists and the password is correct
        if user and check_password_hash(user[4], password):  # Assuming password is in the 5th column
            session['user_id'] = user[0]  # Assuming ID is in the 1st column
            session['email'] = user[3]  # Assuming email is in the 4th column
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

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
            sql = "INSERT INTO users (ful_name, tel, email, password, role, DateT) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (full_name, tel, email, password, role, DateT)

        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        return redirect(url_for('register_user'))

    # Fetch all users
    mycursor.execute("SELECT * FROM users")
    data = mycursor.fetchall()
    return render_template('Register.html', data=data)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        sql = "DELETE FROM users WHERE id = %s"
        mycursor.execute(sql, (id,))
        mydb.commit()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
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

        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        return redirect(url_for('add_customer'))

    # Fetch all customers
    data = fetch_customers()
    return render_template('customers.html', data=data)

@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    try:
        sql = "DELETE FROM customers WHERE id = %s"
        mycursor.execute(sql, (id,))
        mydb.commit()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    return redirect(url_for('add_customer'))

def fetch_customers():
    mycursor.execute("SELECT * FROM customers")
    return mycursor.fetchall()

if __name__ == "__main__":
    app.run(debug=True)
