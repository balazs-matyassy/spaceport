import os

from flask import Flask, render_template, request, redirect, url_for, flash, current_app, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from auth import fully_authenticated, admin_granted
from db import close_db, init_db_command, get_product_repository, get_user_repository
from model.product import Product
from model.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '31f010a7-4ff4-49f9-9307-9fd04843a846'
app.config['DATABASE'] = os.path.join(app.instance_path, 'spaceport.sqlite')

app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)

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


@app.route('/products')
def products_list():
    product_repository = get_product_repository()
    name = request.args.get('name')

    if name is not None:
        products = product_repository.find_all_by_column('name', name)
    else:
        products = product_repository.find_all()

    return render_template('products/list.html', products=products, name=name)


@app.route('/products/create', methods=("GET", "POST"))
@fully_authenticated
def products_create():
    product_repository = get_product_repository()
    product = Product(None, '', 0, 0)
    errors = []

    if request.method == "POST":
        product.name = request.form['name']
        product.unit_price = int(request.form['unit_price'])
        product.discount = int(request.form['discount'])
        errors = product_repository.validate(product)

        if len(errors) == 0 and \
                product_repository.save(product) is not None:
            flash('Product created.')
            return redirect(url_for("products_list"))

    return render_template(
        'products/edit.html',
        product=product,
        errors=errors,
        create=True
    )


@app.route('/products/<int:product_id>/edit', methods=("GET", "POST"))
@fully_authenticated
def products_edit(product_id):
    product_repository = get_product_repository()
    product = product_repository.find_one_by_id(product_id)
    errors = []

    if request.method == "POST":
        product.name = request.form['name']
        product.unit_price = int(request.form['unit_price'])
        product.discount = int(request.form['discount'])
        errors = product_repository.validate(product)

        if len(errors) == 0 and \
                product_repository.save(product) is not None:
            flash('Product saved.')

    return render_template(
        'products/edit.html',
        product=product,
        errors=errors,
        create=False
    )


@app.route('/products/<int:product_id>/delete', methods=["POST"])
@fully_authenticated
def products_delete(product_id):
    product_repository = get_product_repository()
    if product_repository.delete(product_id) is not None:
        flash('Product deleted.')

    return redirect(url_for("products_list"))


@app.route('/users')
@admin_granted
def users_list():
    user_repository = get_user_repository()
    username = request.args.get('username')

    if username is not None:
        users = user_repository.find_all_by_column('username', username)
    else:
        users = user_repository.find_all()

    return render_template('users/list.html', users=users, username=username)


@app.route('/users/create', methods=("GET", "POST"))
@admin_granted
def users_create():
    user_repository = get_user_repository()
    user = User(None, '', '', 'USER')
    errors = []

    if request.method == "POST":
        user.username = request.form['username']
        user.admin = request.form['role'].upper() == 'ADMIN'

        if len(request.form['password']) > 0:
            user.password = generate_password_hash(request.form['password'])

        errors = user_repository.validate(user)

        if len(errors) == 0 and \
                user_repository.save(user) is not None:
            flash('User created.')
            return redirect(url_for("users_list"))

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors,
        create=True
    )


@app.route('/users/<int:user_id>/edit', methods=("GET", "POST"))
@admin_granted
def users_edit(user_id):
    user_repository = get_user_repository()
    user = user_repository.find_one_by_id(user_id)
    errors = []

    if request.method == "POST":
        user.username = request.form['username']
        user.admin = request.form['role'].upper() == 'ADMIN'

        if len(request.form['password']) > 0:
            user.password = generate_password_hash(request.form['password'])

        errors = user_repository.validate(user)

        if len(errors) == 0 and \
                user_repository.save(user) is not None:
            flash('User saved.')

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors,
        create=False
    )


@app.route('/users/<int:user_id>/delete', methods=["POST"])
@admin_granted
def users_delete(user_id):
    user_repository = get_user_repository()
    if user_repository.delete(user_id) is not None:
        flash('User deleted.')

    return redirect(url_for("users_list"))


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
