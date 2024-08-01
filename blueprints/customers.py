from flask import Blueprint, request, render_template, redirect, url_for
from db_con.db import mydb

customers_bp = Blueprint('customers_bp', __name__)

@customers_bp.route('', methods=['GET', 'POST'])
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

        with mydb.cursor() as mycursor:
            mycursor.execute(sql, val)
            mydb.commit()
        return redirect(url_for('customers_bp.add_customer'))

    data = fetch_customers()
    return render_template('customers.html', data=data)

@customers_bp.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    with mydb.cursor() as mycursor:
        mycursor.execute("DELETE FROM customers WHERE id = %s", (id,))
        mydb.commit()
    return redirect(url_for('customers_bp.add_customer'))

def fetch_customers():
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT * FROM customers")
        return mycursor.fetchall()
