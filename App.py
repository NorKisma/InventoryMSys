from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import hashlib
from functools import wraps
import os
from Crud_M import Supplier
from Crud_M import CustomerCRUD
import mysql.connector  

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Database connection
from db_con.db import mydb 

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
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

#end login and logout System
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
@app.route('/index')
def index():
    return render_template('index.html')

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




@app.route('/pur_lists')
def pur_lists():
    return render_template('pur_lists.html')

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    return render_template('purOrder.html')

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

        # Handle image upload
        image_file = request.files.get('userImage')
        image_filename = None
        if image_file and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Hash the password if it's being set
        password = request.form.get('userPassword')
        if password:
            password = hashlib.md5(password.encode()).hexdigest()

        if user_id:
         
            sql = """UPDATE users 
                     SET ful_name = %s, tel = %s, email = %s,  role = %s, status = %s, DateT = %s, image = %s
                     WHERE id = %s"""
            val = (full_name, tel, email, role, status, date_t, image_filename, user_id)
        else:
            sql = """INSERT INTO users (ful_name, tel, email, password, role, status, DateT, image) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (full_name, tel, email, password, role, status, date_t, image_filename)

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
@admin_required
def delete_user(id):
    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("DELETE FROM users WHERE id = %s", (id,))
            mydb.commit()
        flash('User deleted successfully.', 'success')
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'danger')
    return redirect(url_for('add_user'))

customer_crud = CustomerCRUD(mydb)

@app.route('/customers', methods=['GET', 'POST'])
@admin_required
def add_customer():
    return customer_crud.add_customer()

@app.route('/delete_customer/<int:id>', methods=['POST'])
@admin_required
def delete_customer(id):
    return customer_crud.delete_customer(id)


supplier_crud = Supplier(mydb)

@app.route('/suppliers', methods=['GET', 'POST'])
@admin_required
def add_supplier():
    return supplier_crud.add_supplier()

@app.route('/delete_supplier/<int:id>', methods=['POST'])
@admin_required
def delete_supplier(id):
    return supplier_crud.delete_supplier(id)

if __name__ == '__main__':
    app.run(debug=True)
