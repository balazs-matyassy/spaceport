from flask import Blueprint, request, render_template, flash, redirect, url_for

from auth import fully_authenticated
from db import get_product_repository
from model.product import Product

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/')
def products_list():
    product_repository = get_product_repository()
    name = request.args.get('name')

    if name is not None:
        products = product_repository.find_all_by_column('name', name)
    else:
        products = product_repository.find_all()

    return render_template('products/list.html', products=products, name=name)


@bp.route('/create', methods=("GET", "POST"))
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
            return redirect(url_for('products.products_list'))

    return render_template(
        'products/edit.html',
        product=product,
        errors=errors,
        create=True
    )


@bp.route('/<int:product_id>/edit', methods=("GET", "POST"))
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


@bp.route('/<int:product_id>/delete', methods=["POST"])
@fully_authenticated
def products_delete(product_id):
    product_repository = get_product_repository()
    if product_repository.delete(product_id) is not None:
        flash('Product deleted.')

    return redirect(url_for('products.products_list'))
