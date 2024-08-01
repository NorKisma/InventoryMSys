from flask import Flask, render_template
from blueprints.auth import auth_bp
from blueprints.users import users_bp
from blueprints.customers import customers_bp
from db_con.db import mydb

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(customers_bp, url_prefix='/customers')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
