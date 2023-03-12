import os

from flask import Flask, render_template

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
    products = product_repository.find_all()
    return render_template('products/list.html', products=products)


if __name__ == '__main__':
    app.run()
