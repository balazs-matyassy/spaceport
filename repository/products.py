import os

default_path = None
default_delimiter = None


def init(folder, filename='products.csv', delimiter=';'):
    global default_path
    global default_delimiter

    default_path = os.path.join(folder, filename)
    default_delimiter = delimiter

    if not os.path.isfile(default_path):
        with open(default_path, 'w', encoding='utf-8') as file:
            header = _get_header(default_delimiter)
            file.write(f'{header}\n')

    return default_path


def find_all(path=None, delimiter=None):
    path = _get_path(path)
    delimiter = _get_delimiter(delimiter)

    products = []

    with open(path, encoding='utf-8') as file:
        file.readline()

        for line in file:
            product = _line_to_entity(line, delimiter)
            products.append(product)

        return products


def find_all_by_name(name, path=None, delimiter=None):
    path = _get_path(path)
    delimiter = _get_delimiter(delimiter)

    products = find_all(path, delimiter)
    filtered = []

    for product in products:
        if name.strip().lower() in product['name'].lower():
            filtered.append(product)

    return filtered


def find_one_by_id(product_id, path=None, delimiter=None):
    path = _get_path(path)
    delimiter = _get_delimiter(delimiter)

    products = find_all(path, delimiter)

    for product in products:
        if product['id'] == product_id:
            return product

    return None


def save(product, path=None, delimiter=None):
    path = _get_path(path)
    delimiter = _get_delimiter(delimiter)

    if 'id' not in product or product['id'] is None:
        # CREATE
        return _create(product, path, delimiter)
    else:
        # UPDATE
        return _update(product, path, delimiter)


def delete(product_id, path=None, delimiter=None):
    path = _get_path(path)
    delimiter = _get_delimiter(delimiter)

    products = find_all(path, delimiter)
    filtered = []
    deleted_product = None

    for product in products:
        if product['id'] != product_id:
            filtered.append(product)
        else:
            deleted_product = product

    if deleted_product is not None:
        _overwrite(filtered, path, delimiter)

    return deleted_product


def validate(product):
    errors = []

    if 'name' not in product \
            or product['name'] is None \
            or len(product['name'].strip()) == 0:
        errors.append('Name missing.')

    if 'unit_price' not in product \
            or not isinstance(product['unit_price'], int) \
            or product['unit_price'] < 0:
        errors.append('Unit price must be a non-negative number.')

    return errors


def _get_header(delimiter):
    return 'id' \
        + delimiter + 'name' \
        + delimiter + 'unit_price'


def _line_to_entity(line, delimiter):
    line = line.strip()
    parts = line.split(delimiter)

    if len(parts) >= 3:
        return {
            'id': int(parts[0].strip()),
            'name': parts[1].strip(),
            'unit_price': int(parts[2].strip())
        }
    else:
        return {
            'id': None,
            'name': parts[0].strip(),
            'unit_price': int(parts[1].strip())
        }


def _entity_to_line(product, delimiter):
    return str(product['id']) \
        + delimiter + product['name'] \
        + delimiter + str(product['unit_price'])


def _create(product, path, delimiter):
    products = find_all(path, delimiter)
    max_id = 0

    for stored_product in products:
        if stored_product['id'] > max_id:
            max_id = stored_product['id']

    product['id'] = max_id + 1

    with open(path, 'a', encoding='utf-8') as file:
        line = _entity_to_line(product, delimiter)
        file.write(f'{line}\n')

    return product


def _update(product, path, delimiter):
    products = find_all(path, delimiter)
    updated_product = None

    for i in range(len(products)):
        if products[i]['id'] == product['id']:
            products[i] = product
            updated_product = products[i]
            break

    if updated_product is not None:
        _overwrite(products, path, delimiter)

    return updated_product


def _get_path(path=None):
    return path if path is not None else default_path


def _get_delimiter(delimiter=None):
    return delimiter if delimiter is not None else default_delimiter


def _overwrite(products, path, delimiter):
    with open(path, 'w', encoding='utf-8') as file:
        header = _get_header(delimiter)
        file.write(f'{header}\n')

        for product in products:
            line = _entity_to_line(product, delimiter)
            file.write(f'{line}\n')
