import os

from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import check_password_hash

from blueprints import users, products
from db import close_db, init_db_command, get_user_repository

app = Flask(__name__)
app.config['SECRET_KEY'] = '31f010a7-4ff4-49f9-9307-9fd04843a846'
app.config['DATABASE'] = os.path.join(app.instance_path, 'spaceport.sqlite')

app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)

app.register_blueprint(users.bp)
app.register_blueprint(products.bp)

os.makedirs(app.instance_path, exist_ok=True)


@app.before_request
def load_current_user():
    user_id = session.get('user_id')

    if user_id is not None:
        user_repository = get_user_repository()
        g.user = user_repository.find_one_by_id(user_id)
    else:
        g.user = None


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=("GET", "POST"))
def login():
    username = ''
    password = ''

    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password']

        user_repository = get_user_repository()
        user = user_repository.find_one_by_column('username', username)

        if user is not None and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.user_id
            flash('Login successful.')

            return redirect(url_for('home'))
        else:
            flash('Wrong username or password.')

    return render_template('login.html', username=username, password=password)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.')

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
