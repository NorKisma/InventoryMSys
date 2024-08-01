from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from db_con.db import mydb

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
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
                        return redirect(url_for('index'))
                    else:
                        flash('Invalid email or password', 'danger')
                else:
                    flash('Invalid email or password', 'danger')

        except mysql.connector.Error as err:
            flash(f'An error occurred: {err}', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_bp.login'))
