from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector  # Make sure to import mysql.connector

# Create Flask application instance
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Database connection
from db_con.db import mydb  # Ensure you have the correct path for db connection

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            with mydb.cursor() as mycursor:
                mycursor.execute('SELECT id, ful_name, email, password, status, role FROM users WHERE status="active" AND email = %s', (email,))
                user = mycursor.fetchone()
                
                if user:
                    if check_password_hash(user[3], password):
                        session['loggedin'] = True
                        session['user_id'] = user[0]
                        session['ful_name'] = user[1]
                        session['email'] = user[2]
                        session['role'] = user[5]
                        flash('Login successful!', 'success')
                        return redirect(url_for('index'))  # Update 'index' to your actual route
                    else:
                        flash('Invalid email or password', 'danger')
                else:
                    flash('Invalid email or password', 'danger')

        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Directly refer to 'login'

# Define the index route or any other routes here
@app.route('/')
def index():
     return render_template('index.html') 
 
 
 
@app.route('/users', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        full_name = request.form.get('userName')
        tel = request.form.get('userTel')
        email = request.form.get('userEmail')
        role = request.form.get('userRole')
        status = request.form.get('userStatus')
        DateT = request.form.get('userDate')

        if user_id:
            sql = """UPDATE users 
                     SET ful_name = %s, tel = %s, email = %s, role = %s, status = %s, DateT = %s
                     WHERE id = %s"""
            val = (full_name, tel, email, role, status, DateT, user_id)
        else:
            password = generate_password_hash(request.form.get('userPassword'))
            sql = "INSERT INTO users (ful_name, tel, email, password, role, status, DateT) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (full_name, tel, email, password, role, status, DateT)

        try:
            with mydb.cursor() as mycursor:
                mycursor.execute(sql, val)
                mydb.commit()
            flash('User saved successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('add_user'))

    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("SELECT * FROM users")
            data = mycursor.fetchall()
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
        data = []

    return render_template('users.html', data=data)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("DELETE FROM users WHERE id = %s", (id,))
            mydb.commit()
        flash('User deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
    return redirect(url_for('add_user'))
 
 
 
@app.route('/customers', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form.get('customerName')
        tel = request.form.get('customerTel')
        gender = request.form.get('customerGender')
        email = request.form.get('customerEmail')
        DateT = request.form.get('customerDate')
        customer_id = request.form.get('customerId')

        if customer_id:
            sql = "UPDATE customers SET name = %s, tel = %s, email = %s, gender = %s, DateT = %s WHERE id = %s"
            val = (name, tel, email, gender, DateT, customer_id)
        else:
            sql = "INSERT INTO customers (name, tel, email, gender, DateT) VALUES (%s, %s, %s, %s, %s)"
            val = (name, tel, email, gender, DateT)

        try:
            with mydb.cursor() as mycursor:
                mycursor.execute(sql, val)
                mydb.commit()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return redirect(url_for('add_customer'))

        flash('Customer saved successfully.', 'success')
        return redirect(url_for('add_customer'))

    data = fetch_customers()
    return render_template('customers.html', data=data)

@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("DELETE FROM customers WHERE id = %s", (id,))
            mydb.commit()
        flash('Customer deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
    return redirect(url_for('add_customer'))

def fetch_customers():
    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("SELECT * FROM customers")
            return mycursor.fetchall()
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
        return []
 
if __name__ == '__main__':
    app.run(debug=True)
