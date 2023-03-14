import functools
import os

from flask import Flask, render_template, request, redirect, url_for, flash, current_app, session, g

import repository.products as product_repository

app = Flask(__name__)
app.config['SECRET_KEY'] = '31f010a7-4ff4-49f9-9307-9fd04843a846'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'abc123'

os.makedirs(app.instance_path, exist_ok=True)
product_repository.init(app.instance_path)


def fully_authenticated(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_current_user():
    if session.get('username') is not None:
        g.user = {'username': session['username']}
    else:
        g.user = None


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/products')
def products_list():
    name = request.args.get('name')

    if name is not None:
        products = product_repository.find_all_by_name(name)
    else:
        products = product_repository.find_all()

    return render_template('products/list.html', products=products, name=name)


@app.route('/products/create', methods=("GET", "POST"))
@fully_authenticated
def products_create():
    product = {
        'name': '',
        'unit_price': 0
    }
    errors = []

    if request.method == "POST":
        product['name'] = request.form['name']
        product['unit_price'] = int(request.form['unit_price'])
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
    product = product_repository.find_one_by_id(product_id)
    errors = []

    if request.method == "POST":
        product['name'] = request.form['name']
        product['unit_price'] = int(request.form['unit_price'])
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
    if product_repository.delete(product_id) is not None:
        flash('Product deleted.')

    return redirect(url_for("products_list"))


@app.route('/login', methods=("GET", "POST"))
def login():
    user = {
        'username': '',
        'password': ''
    }

    if request.method == "POST":
        user['username'] = request.form['username'].strip()
        user['password'] = request.form['password']

        if user['username'].lower() == current_app.config['USERNAME'].lower() \
                and user['password'] == current_app.config['PASSWORD']:
            session.clear()
            session['username'] = user['username']
            flash('Login successful.')

            return redirect(url_for('home'))
        else:
            flash('Wrong username or password.')

    return render_template('login.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.')

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()