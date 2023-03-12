import os

from flask import Flask, render_template, request

import repository.products as product_repository

app = Flask(__name__)

os.makedirs(app.instance_path, exist_ok=True)
product_repository.init(app.instance_path)


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


if __name__ == '__main__':
    app.run()
