from flask import Flask, request, render_template, redirect, url_for, flash, session,current_app,jsonify  
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import hashlib
from functools import wraps

import os
from Crud_M import Supplier,CustomerCRUD,usersCRUD,OrderCRUD,CategoryCRUD,ProductCRUD

import mysql.connector  
from db_con.db import mydb 
app = Flask(__name__)
app.secret_key = 'your_secret_key'  


UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()




order_crud = OrderCRUD(mydb)
crud_users = usersCRUD(mydb, allowed_file)
customer_crud = CustomerCRUD(mydb)
supplier_crud = Supplier(mydb)
category_crud = CategoryCRUD(mydb)
product_crud = ProductCRUD(mydb)
#admin_required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('Admin access required.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
# Ensure the upload folder exists


@app.route('/index', methods=['GET'])
def index():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM users")
    user_count = mycursor.fetchone()[0]
    mycursor.close()

    return render_template('index.html', user_count=user_count)

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, ful_name, tel, email, password, role, status, image FROM users WHERE email = %s", (email,))
        user = mycursor.fetchone()

        # Fetch any remaining results to avoid the "Unread result found" error
        mycursor.fetchall()  # This ensures all results are read, even if you only need one

        mycursor.close()

        if user:
            # Check if the password matches
            if hashlib.md5(password.encode()).hexdigest() == user[4]:
                # Check if the account is active
                if user[6] == 'Active':
                    # Store user details in session
                    session['user_id'] = user[0]
                    session['ful_name'] = user[1]
                    session['tel'] = user[2]
                    session['email'] = user[3]
                    session['role'] = user[5]
                    session['status'] = user[6]
                    session['image'] = user[7]

                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Account is inactive', 'danger')
            else:
                flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
#end login and logout System


#Start profile Update
@app.route('/profile/<int:id>')
def profile(id):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = mycursor.fetchone()
    mycursor.close()

    if user:
        return render_template('profile.html', user=user)
    else:
        flash('User not found.', 'danger')
        return redirect(url_for('index'))
@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    tel = request.form['tel']
    email = request.form['email']
    mycursor = mydb.cursor()
    
    image_file = request.files.get('image')
    image_filename = None
    if image_file and allowed_file(image_file.filename):
        image_filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
    if image_filename:
        sql = "UPDATE users SET ful_name = %s, tel = %s, email  = %s, image = %s WHERE id = %s"
        values = (name, tel, email, image_filename, id)
    else:
        sql = "UPDATE users SET ful_name = %s, tel = %s, email  = %s WHERE id = %s"
        values = (name, tel, email, id)
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    flash('User details updated successfully.', 'success')
    return redirect(url_for('profile', id=id))
#End profile Update


# Example of storing settings in the session
def store_settings_in_session(settings):
    print("Settings tuple:", settings)  # Debugging line
    session['company_name'] = settings[1]
    session['short_name'] = settings[2]
    session['logo'] = settings[3] if len(settings) > 3 else None

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        company_name = request.form['company_name']
        short_name = request.form['short_name']
        address = request.form['address']
        email = request.form['email']
        tel = request.form['tel']
        website = request.form['website']
       

        logo = request.files.get('logo')
        logo_path = None  # Initialize logo_path
        if logo and allowed_file(logo.filename):
         filename = secure_filename(logo.filename)
         logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
         logo.save(logo_path)
        else:
            logo_path = request.form.get('existing_logo')
           
        try:
            company_name = request.form.get('company_name')
            short_name = request.form.get('short_name')
            cursor = mydb.cursor()
            cursor.execute('''
                INSERT INTO company_settings (company_name, shortName, logo, address, email, tel, website)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                company_name = VALUES(company_name),
                shortName = VALUES(shortName),
                logo = VALUES(logo),
                address = VALUES(address),
                email = VALUES(email),
                tel = VALUES(tel),
                website = VALUES(website)
            ''', (company_name, short_name, logo_path, address, email, tel, website))
            mydb.commit()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
        finally:
            cursor.close()

        # Store updated settings in session
        store_settings_in_session((company_name, short_name,logo_path))

        flash('Settings updated successfully.', 'success')
        return redirect(url_for('settings'))

    # Fetch existing settings
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM company_settings LIMIT 1')
    settings = cursor.fetchone()
    cursor.close()

    # Handle case where no settings are present
    if settings is None:
        settings = ['', '', '', '', '', '', '', '']

    # Store fetched settings in session
    store_settings_in_session(settings)

    return render_template('settings.html', settings=settings)




# Start change_password
@app.route('/change_password/<int:id>', methods=['GET', 'POST'])
def change_password(id):
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('change_password', id=id))

        user_id = session.get('user_id')
        if not user_id:
            flash('User not logged in.', 'danger')
            return redirect(url_for('login'))

        if user_id != id:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('change_password', id=id))
        # Get user data
        try:
            with mydb.cursor() as cursor:
                cursor.execute('SELECT password FROM users WHERE id = %s', (id,))
                user = cursor.fetchone()
        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')
            return redirect(url_for('change_password', id=id))

        if user:
            stored_password = user[0]
            if check_password_hash(stored_password, current_password):
                hashed_new_password = generate_password_hash(new_password)
                try:
                    with mydb.cursor() as cursor:
                        cursor.execute('UPDATE users SET password = %s WHERE id = %s', (hashed_new_password, id))
                        mydb.commit()
                    flash('Password updated successfully.', 'success')
                except mysql.connector.Error as err:
                    flash(f'An error occurred: {err}', 'danger')
            else:
                flash('Current password is incorrect.', 'danger')
        else:
            flash('User not found.', 'danger')

        return redirect(url_for('change_password', id=id))

    return render_template('change_password.html', id=id)
# End change_password



@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        result = crud_users.add_user()
        if isinstance(result, str):  
            flash(result, 'danger')
            return redirect(url_for('add_user'))
        return result
    return crud_users.add_user()  

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    result = crud_users.delete_user(id)
    if isinstance(result, str):  
        flash(result, 'danger')
        return redirect(url_for('list_users'))
    return result  # Assuming it returns a redirect response

@app.route('/users')
def list_users():
    data = crud_users.fetch_users()
    return render_template('users.html', data=data)

@app.route('/customers', methods=['GET', 'POST'])
@admin_required
def add_customer():
    return customer_crud.add_customer()

@app.route('/delete_customer/<int:id>', methods=['POST'])
@admin_required
def delete_customer(id):
    return customer_crud.delete_customer(id)



@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    return supplier_crud.add_supplier()

@app.route('/delete_supplier/<int:id>', methods=['POST'])
@admin_required
def delete_supplier(id):
    return supplier_crud.delete_supplier(id)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        return order_crud.add_order(request)
    suppliers = order_crud.fetch_suppliers()
    products = order_crud.get_products()
    return render_template('PurOrder.html', suppliers=suppliers, products=products)
   

@app.route('/pur_lists')
def pur_lists():
    data = order_crud.fetch_purchases() 
    return render_template('pur_lists.html', data=data) 

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    try:
        # Fetch all orders and find the one with the given order_id
        orders = order_crud.fetch_purchases()
        order = next((o for o in orders if o[0] == order_id), None)
        
        if not order:
            flash('Order not found.', 'danger')
            return redirect(url_for('pur_lists'))

        if request.method == 'POST':
            # Handle form submission to update the order
            order_crud.update_order(
                order_id=order_id,
                invoice_number=request.form.get('invoice_number'),
                supplier=request.form.get('supplier'),
                product_name=request.form.get('product_id'),
                product_unit=request.form.get('product_unit'),
                qty=request.form.get('qty'),
                price=request.form.get('price'),
                subtotal=request.form.get('subtotal'),
                status=request.form.get('status'),
                date_order=request.form.get('date_order')
            )
            return redirect(url_for('pur_lists'))

        # Fetch products and suppliers for the dropdowns
        products = order_crud.get_products()
        suppliers = order_crud.fetch_suppliers()

        return render_template('edit_order.html', order=order, products=products, suppliers=suppliers)

    except Exception as e:
        flash(f'An unexpected error occurred: {e}', 'danger')
        # Optionally log the error
        # app.logger.error(f'Error in edit_order route: {e}')
        return redirect(url_for('pur_lists'))

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order_crud.delete_order(order_id)
    return redirect(url_for('pur_lists'))




















   


 







@app.route('/products')
def products():
    products = product_crud.fetch_products()  # Fetch all products
    return render_template('products.html', data=products)  # Adjust template name as needed


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        return product_crud.add_product()
    return render_template('products.html')


@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
   
    return product_crud.update_product(product_id)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    
    return product_crud.delete_product(product_id)











if __name__ == '__main__':
    app.run(debug=True)
