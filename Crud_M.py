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
                'supplierName': request.form.get('supp_name'),
                'supplierContact': request.form.get('suppContact'),
                'supplierEmail': request.form.get('suppEmail'),
                'supplierCompany': request.form.get('suppCompany'),
                'supplierAddress': request.form.get('suppAddress'),
                'supplierDate': request.form.get('dateAdded'),
                'supplierId': request.form.get('suppId')
            }

            if supplier_data['supplierId']:
                sql = """UPDATE suppliers 
                         SET supp_name = %s, supp_contact = %s, supp_email = %s, supp_company = %s, supp_address = %s, date_added = %s 
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

            return redirect(url_for('add_supplier'))

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




  





  

class CategoryCRUD:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_category(self):
        if request.method == 'POST':
            category_name = request.form.get('category_name')
          
           
            # Insert a new category
            sql = "INSERT INTO category (category_name) VALUES (%s)"
            val = (category_name,)
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
           
            # Update category SQL query
            sql = "UPDATE category SET category_name = %s  WHERE category_Id  = %s"
            val = (category_name, category_Id)
            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()  # Commit the changes
                flash('Category updated successfully.', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('categories'))
    def delete_category(self, category_Id):
        try:
            with self.mydb.cursor() as mycursor:
                mycursor.execute("DELETE FROM category WHERE category_Id  = %s", (category_Id,))
                self.mydb.commit()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('categories'))

    def fetch_categories(self):
     try:
        with self.mydb.cursor() as mycursor:
            # Ensure that both category_Id and category_name are being selected
            mycursor.execute("SELECT category_Id, category_name FROM category")
            return mycursor.fetchall()
     except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
        return []
        
class ProductCRUD:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_product(self):
        if request.method == 'POST':
            product_unit = request.form.get('product_unit')
            product_name = request.form.get('product_name')
            category_name = request.form.get('category_name')  # Get category_id from form
            price = request.form.get('price')
            description = request.form.get('description')

           
            # SQL query to insert a new product
            sql = """
            INSERT INTO product_list (category_name, product_unit, name, price, description) 
            VALUES (%s, %s, %s, %s, %s)
            """
            val = (category_name, product_unit, product_name, price, description)

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
            # Fetch form data
            product_unit = request.form.get('product_unit')
            product_name = request.form.get('product_name')
            category_name = request.form.get('category_name')
            price = request.form.get('price')
            description = request.form.get('description')

            # Ensure category_id is an integer before updating the database
          
            # Update product SQL query
            sql = """
            UPDATE product_list 
            SET category_name = %s, product_unit = %s, name = %s, price = %s, description = %s 
            WHERE id = %s
            """
            val = (category_name, product_unit, product_name, price, description, product_id)

            try:
                with self.mydb.cursor() as mycursor:
                    mycursor.execute(sql, val)
                    self.mydb.commit()  # Commit the changes to the database
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
            with self.mydb.cursor() as cursor:
                query = ("SELECT *  FROM product_list ")
                cursor.execute(query)
                products = cursor.fetchall()
                return products
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []

class OrderCRUD:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_order(self, request):
        if request.method == 'POST':
            invoice_number = request.form.get('invoice_number')
            supplier = request.form.get('supplier')
            product_name = request.form.get('product_name')
            product_unit = request.form.get('product_unit')
            qty = request.form.get('qty')
            price = request.form.get('price')
            subtotal = request.form.get('subtotal')
            status = request.form.get('status')
            date_order = request.form.get('date_order')
            order_id = request.form.get('order_id') 
            stock_from = 'purchase'

            if order_id:
                return self.update_order(order_id, invoice_number, supplier, product_name, product_unit, qty, price, subtotal, status, date_order)
            else:
                return self.insert_order(invoice_number, supplier, product_name, product_unit, qty, price, subtotal, status, date_order)

    def insert_order(self, invoice_number, supplier, product_name, product_unit, qty, price, subtotal, status, date_order):
        sql = """
            INSERT INTO purchase (invoice_number, supp_id, product_id, product_unit, qty, price, 
                subtotal, status, date_order, date_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        val = (invoice_number, supplier, product_name, product_unit, qty, price, subtotal, status, date_order)
        
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(sql, val)
                self.mydb.commit()
                flash('Order added successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return redirect(url_for('add_order'))
        
        return redirect(url_for('pur_lists'))

    def update_order(self, order_id, invoice_number, supplier, product_name, product_unit, qty, price, subtotal, status, date_order):
        sql = """
            UPDATE purchase 
            SET invoice_number = %s, supp_id = %s, product_id = %s, product_unit = %s, qty = %s, 
                price = %s, subtotal = %s, status = %s, date_order = %s, date_updated = NOW()
            WHERE order_id = %s
        """
        val = (invoice_number, supplier, product_name, product_unit, qty, price, subtotal, status, date_order, order_id)
        
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(sql, val)
                self.mydb.commit()
                flash('Order updated successfully.', 'success')

                # Update inventory if the order is completed
                if status == 'Received':
                    self.update_inventory(product_name, qty)
            return redirect(url_for('pur_lists'))
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return redirect(url_for('pur_lists', order_id=order_id))
        return redirect(url_for('edit_order'))

    def update_inventory(self, product_name, qty):
        # Check if the product exists in the inventory
        check_sql = "SELECT qty FROM inventory WHERE product_id = %s"
        update_sql = "UPDATE inventory SET qty = qty + %s, date_updated = NOW() WHERE product_id = %s"
        insert_sql = "INSERT INTO inventory (product_id, qty, stock_from, date_updated) VALUES (%s, %s, 'purchase', NOW())"
        
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(check_sql, (product_name,))
                result = cursor.fetchone()

                if result:
                    # Update the existing quantity
                    cursor.execute(update_sql, (qty, product_name))
                else:
                    # Insert a new inventory record
                    cursor.execute(insert_sql, (product_name, qty ))
                
                self.mydb.commit()
                flash('Inventory updated successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred while updating inventory: {err}', 'danger')

    def delete_order(self, order_id):
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute("DELETE FROM purchase WHERE order_id = %s", (order_id,))
                self.mydb.commit()
                flash('Order deleted successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('pur_lists'))

    def fetch_purchases(self):
        try:
            with self.mydb.cursor() as cursor:
                query = """
                    SELECT p.order_id, p.invoice_number,  s.supp_name,  pl.name,
                        p.product_unit, p.qty, p.price, p.subtotal, p.date_order, p.status
                    FROM purchase p
                    JOIN suppliers s ON p.supp_id  = s.supp_id 
                    JOIN product_list pl ON p.product_id = pl.id
                """
                cursor.execute(query)
                orders = cursor.fetchall()
                return orders if orders else []
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')  
            return []

    def get_products(self):
        query = "SELECT id, name, product_unit FROM product_list"
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(query)
                products = cursor.fetchall()
                return products if products else []
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []

    def fetch_suppliers(self):
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute("SELECT supp_id, supp_Name FROM suppliers")
                suppliers = cursor.fetchall()
                return suppliers if suppliers else []
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []
   


class SalesCRUD:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_sale(self, request):
        if request.method == 'POST':
            
            customer_id = request.form.get('customer_id')
            product_name = request.form.get('product_name')
          
            qty = request.form.get('qty')
            price_sale = request.form.get('price_sale')
            subtotal = request.form.get('subtotal')
            payment_method = request.form.get('payment_method')
            paid_status = request.form.get('paid_status')
            date_sale = request.form.get('date_sale')
            sale_id = request.form.get('sale_id')

            if sale_id:
                return self.update_sale(sale_id, customer_id, product_name,  qty, price_sale, subtotal, payment_method, paid_status, date_sale)
            else:
                return self.insert_sale(customer_id, product_name,  qty, price_sale, subtotal, payment_method, paid_status, date_sale)

    def insert_sale(self,  customer_id, product_name,  qty, price_sale, subtotal, payment_method, paid_status, date_sale):
        sql = """
            INSERT INTO sales ( cust_id, product_id,  qty, price_sale, 
                subtotal, payment_method, paid_status, date_sale, date_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s,  %s, NOW())
        """
        val = ( customer_id, product_name,  qty, price_sale, subtotal, payment_method, paid_status, date_sale)
        
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(sql, val)
                self.mydb.commit()
                flash('Sale added successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return redirect(url_for('add_sale'))
        
        return redirect(url_for('sales_list'))

    def update_sale(self, sale_id, customer_id, product_name,  qty, price_sale, subtotal, payment_method, paid_status, date_sale):
        sql = """
            UPDATE sales 
            SET cust_id = %s, product_id = %s,  qty = %s, 
                price_sale = %s, subtotal = %s, payment_method = %s, paid_status = %s, date_sale = %s, date_updated = NOW()
            WHERE sale_id = %s
        """
        val = (customer_id, product_name, qty, price_sale, subtotal, payment_method, paid_status, date_sale, sale_id)
        
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(sql, val)
                self.mydb.commit()
                flash('Sale updated successfully.', 'success')

                # Update inventory if necessary (e.g., reduce stock after sale)
                self.update_inventory(product_name, -qty)
            return redirect(url_for('sales_list'))
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return redirect(url_for('sales_list', sale_id=sale_id))

    def update_inventory(self, product_name, qty_change):
        # Check if the product exists in the inventory
        check_sql = "SELECT qty FROM inventory WHERE product_id = %s"
        update_sql = "UPDATE inventory SET qty = qty - %s, date_updated = NOW() WHERE product_id = %s"
        
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(check_sql, (product_name,))
                result = cursor.fetchone()

                if result:
                    # Update the existing quantity in inventory
                    cursor.execute(update_sql, (qty_change, product_name))
                
                self.mydb.commit()
                flash('Inventory updated successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred while updating inventory: {err}', 'danger')

    def delete_sale(self, sale_id):
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute("DELETE FROM sales WHERE sale_id = %s", (sale_id,))
                self.mydb.commit()
                flash('Sale deleted successfully.', 'success')
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        return redirect(url_for('sales_list'))

    def fetch_sales(self):
        try:
            with self.mydb.cursor() as cursor:
                query = """
                    SELECT s.sale_id,  c.customer_name, p.name,
                       s.qty, s.price_sale, s.subtotal, s.date_sale, s.payment_method, s.paid_status
                    FROM sales s
                    JOIN customers c ON s.cust_id = c.id 
                    JOIN product_list p ON s.product_id = p.id
                """
                cursor.execute(query)
                sales = cursor.fetchall()
                return sales if sales else []
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')  
            return []

    def get_products(self):
        query = "SELECT id, name, price FROM product_list"
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(query)
                products = cursor.fetchall()
                return products if products else []
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []
    def get_inventor(self):
        query = "SELECT inventory_id,  qty FROM inventory"
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute(query)
                products = cursor.fetchall()
                return products if products else []
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []

    def fetch_customers(self):
        try:
            with self.mydb.cursor() as cursor:
                cursor.execute("SELECT id, Customer_Name FROM customers")
                customers = cursor.fetchall()
                return customers if customers else []
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return []
