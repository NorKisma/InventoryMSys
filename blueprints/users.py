from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from db_con.db import mydb

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users', methods=['GET', 'POST'])
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

        with mydb.cursor() as mycursor:
            mycursor.execute(sql, val)
            mydb.commit()
        flash('User saved successfully.', 'success')
        return redirect(url_for('users_bp.register_user'))

    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT * FROM users")
        data = mycursor.fetchall()
    return render_template('users.html', data=data)

@users_bp.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    with mydb.cursor() as mycursor:
        mycursor.execute("DELETE FROM users WHERE id = %s", (id,))
        mydb.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('users_bp.register_user'))
