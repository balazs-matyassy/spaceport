from db import get_db
from model.product import Product

default_table = None


def init(table='product'):
    global default_table
    default_table = table


def find_all(table=None):
    table = _get_table(table)
    db = get_db()

    query = f"""
        SELECT *
            FROM {table}
            ORDER BY id
    """
    result = db.execute(query).fetchall()

    return [_row_to_entity(row) for row in result]


def find_all_by_name(name, table=None):
    table = _get_table(table)
    db = get_db()

    query = f"""
        SELECT *
            FROM {table}
            WHERE name LIKE ?
            ORDER BY id
    """
    result = db.execute(query, ('%' + name + '%',)).fetchall()

    return [_row_to_entity(row) for row in result]


def find_one_by_id(product_id, table=None):
    table = _get_table(table)
    db = get_db()

    query = f"""
        SELECT *
            FROM {table}
            WHERE id = ?
    """
    row = db.execute(query, (product_id,)).fetchone()

    return _row_to_entity(row) if row is not None else None


def save(product, table=None):
    table = _get_table(table)

    if product.product_id is None:
        # CREATE
        return _create(product, table)
    else:
        # UPDATE
        return _update(product, table)


def delete(product_id, table=None):
    table = _get_table(table)
    db = get_db()

    query = f"""
        DELETE FROM {table}
            WHERE id = ?
    """
    rowcount = db.execute(query, (product_id,)).rowcount
    db.commit()

    return rowcount


def validate(product):
    errors = []

    if product.name is None \
            or len(product.name.strip()) == 0:
        errors.append('Name missing.')

    if product.unit_price < 0:
        errors.append('Unit price must be a non-negative number.')

    if product.discount < 0 or product.discount > 100:
        errors.append('Unit price must be a number between 0 and 100.')

    return errors


def _row_to_entity(row):
    return Product(row['id'], row['name'], row['unit_price'], row['discount'])


def _create(product, table):
    db = get_db()

    query = f"""
        INSERT INTO {table} (name, unit_price, discount)
            VALUES (?, ?, ?)
    """
    product.product_id = db.execute(
        query,
        (product.name, product.unit_price, product.discount)
    ).lastrowid
    db.commit()

    return product


def _update(product, table):
    db = get_db()

    query = f"""
        UPDATE {table} SET
            name = ?,
            unit_price = ?,
            discount = ?
        WHERE id = ?
    """
    rowcount = db.execute(
        query,
        (product.name, product.unit_price, product.discount, product.product_id)
    ).rowcount

    if rowcount == 1:
        db.commit()
        return product
    else:
        return None


def _get_table(table=None):
    return table if table is not None else default_table
