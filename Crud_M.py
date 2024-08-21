from flask import Flask, request, render_template, redirect, url_for, flash, session,current_app
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import hashlib
from functools import wraps
import os

import mysql.connector  
class usersCRUD:
    def __init__(self, db, allowed_file_func):
        self.db = db
        self.allowed_file = allowed_file_func

    def add_user(self):
        if request.method == 'POST':
            user_id = request.form.get('userId')
            full_name = request.form.get('userName')
            tel = request.form.get('userTel')
            email = request.form.get('userEmail')
            role = request.form.get('userRole')
            status = request.form.get('userStatus')
            date_t = request.form.get('userDate')

            # Handle image upload
            image_file = request.files.get('userImage')
            image_filename = None
            if image_file and self.allowed_file(image_file.filename):
                image_filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))

            # Hash the password if it's being set
            password = request.form.get('userPassword')
            if password:
                password = hashlib.md5(password.encode()).hexdigest()

            if user_id:
                sql = """UPDATE users 
                         SET ful_name = %s, tel = %s, email = %s, role = %s, status = %s, DateT = %s, image = %s
                         WHERE id = %s"""
                val = (full_name, tel, email, role, status, date_t, image_filename, user_id)
            else:
                sql = """INSERT INTO users (ful_name, tel, email, password, role, status, DateT, image) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (full_name, tel, email, password, role, status, date_t, image_filename)

            try:
                with self.db.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.db.commit()
                flash('User saved successfully.', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
            return redirect(url_for('add_user'))

        data = self.fetch_users()
        return render_template('users.html', data=data)

    def delete_user(self, id):
        try:
            with self.db.cursor() as mycursor:
                mycursor.execute("DELETE FROM users WHERE id = %s", (id,))
                self.db.commit()
            flash('User deleted successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('add_user'))

    def fetch_users(self):
        try:
            with self.db.cursor() as mycursor:
                mycursor.execute("SELECT * FROM users")
                return mycursor.fetchall()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []

class Supplier:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_supplier(self):
        if request.method == 'POST':
            supplier_data = {
                'supplierName': request.form.get('supplierName'),
                'supplierContact': request.form.get('supplierContact'),
                'supplierEmail': request.form.get('supplierEmail'),
                'supplierCompany': request.form.get('supplierCompany'),
                'supplierAddress': request.form.get('supplierAddress'),
                'supplierDate': request.form.get('supplierDate'),
                'supplierId': request.form.get('supplierId')
            }

            if supplier_data['supplierId']:
                sql = """UPDATE suppliers 
                         SET supp_Name = %s, supp_contact = %s, supp_email = %s, supp_company = %s, supp_address = %s, date_added = %s 
                         WHERE supp_id = %s"""
                val = (supplier_data['supplierName'], supplier_data['supplierContact'], supplier_data['supplierEmail'],
                       supplier_data['supplierCompany'], supplier_data['supplierAddress'], supplier_data['supplierDate'],
                       supplier_data['supplierId'])
            else:
                sql = """INSERT INTO suppliers (supp_name, supp_contact, supp_email, supp_company, supp_address, date_added) 
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                val = (supplier_data['supplierName'], supplier_data['supplierContact'], supplier_data['supplierEmail'],
                       supplier_data['supplierCompany'], supplier_data['supplierAddress'], supplier_data['supplierDate'])

            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()
                flash('Supplier saved successfully.', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')

            return redirect(url_for('add_supplier_route'))

        # For GET requests, render the template with the data
        data = self.fetch_suppliers()
        return render_template('suppliers.html', data=data)

    def delete_supplier(self, supplier_id):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("DELETE FROM suppliers WHERE supp_id = %s", (supplier_id,))
                self.mydb.commit()
            flash('Supplier deleted successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')

        return redirect(url_for('add_supplier'))

    def fetch_suppliers(self):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("SELECT * FROM suppliers")
                return mycursor.fetchall()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []

     
class CustomerCRUD:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_customer(self):
        if request.method == 'POST':
            name = request.form.get('customerName')
            tel = request.form.get('customerTel')
            gender = request.form.get('customerGender')
            email = request.form.get('customerEmail')
            DateT = request.form.get('customerDate')
            customer_id = request.form.get('customerId')

            if customer_id:
                sql = """
                    UPDATE customers 
                    SET Customer_Name = %s, tel = %s, email = %s, gender = %s, DateT = %s 
                    WHERE id = %s
                """
                val = (name, tel, email, gender, DateT, customer_id)
            else:
                sql = """
                    INSERT INTO customers (Customer_Name, tel, email, gender, DateT) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                val = (name, tel, email, gender, DateT)

            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()
                flash('Customer saved successfully.', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
                return redirect(url_for('add_customer'))

            return redirect(url_for('add_customer'))

        data = self.fetch_customers()
        return render_template('customers.html', data=data)

    def delete_customer(self, id):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("DELETE FROM customers WHERE id = %s", (id,))
                self.mydb.commit()
            flash('Customer deleted successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('add_customer'))

    def fetch_customers(self):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("SELECT * FROM customers")
                return mycursor.fetchall()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []



class OrderCRUD:
    def __init__(self, mydb):
        self.mydb = mydb

    # Function to add a new order
    def add_order(self):
        if request.method == 'POST':
            invoice_number = request.form.get('invoice_number')
            supplier = request.form.get('supplier')
            product_name = request.form.get('product_name')
            qty = request.form.get('qty')
            price = request.form.get('price')
            subtotal = request.form.get('subtotal')
            status = request.form.get('status')
            date_order = request.form.get('date_order')

            # Insert a new order
            sql = """
                INSERT INTO purchase (invoice_number, supplier, product_name, qty, price, 
                                      subtotal, status, date_order, date_updated) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            val = (invoice_number, supplier, product_name, qty, price, subtotal, status, date_order)

            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
                return redirect(url_for('pur_lists'))

        return redirect(url_for('add_order'))

    # Function to edit an existing order
    def edit_order(self, purchase_id):
        if request.method == 'POST':
            invoice_number = request.form.get('invoice_number')
            supplier = request.form.get('supplier')
            product_name = request.form.get('product_name')
            qty = request.form.get('qty')
            price = request.form.get('price')
            subtotal = request.form.get('subtotal')
            status = request.form.get('status')
            date_order = request.form.get('date_order')

            # No need to check for invoice_number uniqueness since it’s an update
            sql = """
                UPDATE purchase 
                SET invoice_number = %s, supplier = %s, product_name = %s, qty = %s, 
                    price = %s, subtotal = %s, status = %s, date_order = %s, date_updated = NOW() 
                WHERE order_id = %s
            """
            val = ( invoice_number ,supplier, product_name, qty, price, subtotal, status, date_order, purchase_id)

            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
                return redirect(url_for('pur_lists', purchase_id=purchase_id))
        return redirect(url_for('pur_lists', purchase_id=purchase_id))

   
    def delete_order(self, purchase_id):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("DELETE FROM purchase WHERE order_id = %s", (purchase_id,))
                self.mydb.commit()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('pur_lists'))

    def fetch_purchases(self):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("SELECT * FROM purchase")
                return mycursor.fetchall()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []


class CategoryCRUD:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_category(self):
        if request.method == 'POST':
            category_name = request.form.get('category_name')
            category_unit = request.form.get('category_unit')
           
            # Insert a new category
            sql = "INSERT INTO category (category_name,category_unit) VALUES (%s,%s)"
            val = (category_name,category_unit,)
            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('categories'))

    def update_category(self, category_id):
        if request.method == 'POST':
            category_name = request.form.get('category_name')  # Get category name from the form
            category_unit = request.form.get('category_unit')
            # Update category SQL query
            sql = "UPDATE category SET category_name = %s ,category_unit= %s WHERE category_id = %s"
            val = (category_name,category_unit, category_id)
            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()  # Commit the changes
                flash('Category updated successfully.', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('categories'))
    def delete_category(self, category_id):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
                self.mydb.commit()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('categories'))

    def fetch_categories(self):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("SELECT * FROM category")
                return mycursor.fetchall()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []
        
class ProductCRUD:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_product(self):
        if request.method == 'POST':
            product_name = request.form.get('product_name')
            category_id = request.form.get('category_id')
            price = request.form.get('price')
            description = request.form.get('description')
            
            # Insert a new product
            sql = "INSERT INTO product_list (category_id, name, price, description) VALUES (%s, %s, %s, %s)"
            val = (category_id, product_name, price, description)
            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()
                flash('Product added successfully.', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('products'))

    def update_product(self, product_id):
        if request.method == 'POST':
            product_name = request.form.get('product_name')
            category_id = request.form.get('category_id')
            price = request.form.get('price')
            description = request.form.get('description')
            
            # Update product SQL query
            sql = "UPDATE product_list SET category_id = %s, name = %s, price = %s, description = %s WHERE id = %s"
            val = (category_id, product_name, price, description, product_id)
            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()  # Commit the changes
                flash('Product updated successfully.', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('products'))

    def delete_product(self, product_id):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("DELETE FROM product_list WHERE id = %s", (product_id,))
                self.mydb.commit()
            flash('Product deleted successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('products'))

    def fetch_products(self):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("SELECT * FROM product_list")
                return mycursor.fetchall()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []
       