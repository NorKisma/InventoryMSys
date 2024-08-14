
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import hashlib
from functools import wraps
import os
import mysql.connector  

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Database connection
from db_con.db import mydb 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Example of storing settings in the session

def store_settings_in_session(settings):

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
    cursor.execute('SELECT * FROM company_settings LIMIT 1 ORDER BY Datet DESC')
    settings = cursor.fetchone()
    cursor.close()


    # Handle case where no settings are present
    if settings is None:
        settings = ['', '', '', '', '', '', '', '']

    # Store fetched settings in session
    store_settings_in_session(settings)

    return render_template('settings.html', settings=settings)
