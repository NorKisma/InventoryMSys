from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
import mysql.connector
from db_con.db import mydb

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Ensure the upload folder exists
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = mydb()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pur_lists')
def pur_lists():
    return render_template('pur_lists.html')

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    return render_template('purOrder.html')

@app.route('/users', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        full_name = request.form.get('userName')
        tel = request.form.get('userTel')
        email = request.form.get('userEmail')
        role = request.form.get('userRole')
        status = request.form.get('userStatus')
        date_t = request.form.get('userDate')

        image_file = request.files.get('userImage')
        image_filename = None
        if image_file and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn = mydb()
        cursor = conn.cursor()

        if user_id:
            sql = """UPDATE users 
                     SET ful_name = %s, tel = %s, email = %s, role = %s, status = %s, DateT = %s, image = %s
                     WHERE id = %s"""
            val = (full_name, tel, email, role, status, date_t, image_filename, user_id)
        else:
            password = generate_password_hash(request.form.get('userPassword'))
            sql = """INSERT INTO users (ful_name, tel, email, password, role, status, DateT, image) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (full_name, tel, email, password, role, status, date_t, image_filename)

        try:
            cursor.execute(sql, val)
            conn.commit()
            flash('User saved successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('add_user'))

    conn = mydb()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users ORDER BY DateT")
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
        data = []
    finally:
        cursor.close()
        conn.close()

    return render_template('users.html', data=data)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    conn = mydb()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        flash('User deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
    finally:
        cursor.close()
        conn.close()

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

        conn = mydb()
        cursor = conn.cursor()

        if customer_id:
            sql = "UPDATE customers SET Customer_Name = %s, tel = %s, email = %s, gender = %s, DateT = %s WHERE id = %s"
            val = (name, tel, email, gender, DateT, customer_id)
        else:
            sql = "INSERT INTO customers (Customer_Name, tel, email, gender, DateT) VALUES (%s, %s, %s, %s, %s)"
            val = (name, tel, email, gender, DateT)

        try:
            cursor.execute(sql, val)
            conn.commit()
            flash('Customer saved successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('add_customer'))

    data = fetch_customers()
    return render_template('customers.html', data=data)

@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    conn = mydb()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM customers WHERE id = %s", (id,))
        conn.commit()
        flash('Customer deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('add_customer'))

def fetch_customers():
    conn = mydb()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM customers")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
        return []
    finally:
        cursor.close()
        conn.close()

@app.route('/suppliers', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        supp_Name = request.form.get('supplierName')
        supp_Contact = request.form.get('supplierContact')
        supp_Email = request.form.get('supplierEmail')
        supp_Company = request.form.get('supplierCompany')
        supp_Address = request.form.get('supplierAddress')
        date_added = request.form.get('supplierDate')
        supplier_id = request.form.get('supplierId')

        conn = mydb()
        cursor = conn.cursor()

        if supplier_id:
            sql = """UPDATE suppliers 
                     SET supp_Name = %s, supp_contact = %s, supp_email = %s, supp_company = %s, supp_address = %s, date_added = %s 
                     WHERE supp_id = %s"""
            val = (supp_Name, supp_Contact, supp_Email, supp_Company, supp_Address, date_added, supplier_id)
        else:
            sql = """INSERT INTO suppliers (supp_Name, supp_contact, supp_email, supp_company, supp_address, date_added) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            val = (supp_Name, supp_Contact, supp_Email, supp_Company, supp_Address, date_added)

        try:
            cursor.execute(sql, val)
            conn.commit()
            flash('Supplier saved successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('add_supplier'))

    data = fetch_suppliers()
    return render_template('suppliers.html', data=data)

@app.route('/delete_supplier/<int:id>', methods=['POST'])
def delete_supplier(supplier_id):
    conn = mydb()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM suppliers WHERE supp_id = %s", (supplier_id,))
        conn.commit()
        flash('Supplier deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('add_supplier'))

def fetch_suppliers():
    conn = mydb()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM suppliers")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
        return []
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
