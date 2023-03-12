import os

from flask import Flask

import repository.products as product_repository


def input_cmd():
    line = input('>> ').strip()
    parts = line.split(' ', 1)

    return {
        'name': parts[0].strip(),
        'param': parts[1] if len(parts) >= 2 else None
    }


def param_to_product(param):
    parts = cmd['param'].split(',')

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


app = Flask(__name__)

os.makedirs(app.instance_path, exist_ok=True)
product_repository.init(app.instance_path)

print('==================================================')
print('\tWelcome to SpacePort 0.1')
print('==================================================')

cmd = input_cmd()

while cmd['name'] != 'exit':
    if cmd['name'] == 'list':
        products = product_repository.find_all()

        print(f'{"ID":4} {"Name":32} {"Unit price":8}')

        for product in products:
            print(f'{product["id"]:4} {product["name"]:32} {product["unit_price"]:8}')
    elif cmd['name'] == 'find':
        product = product_repository.find_one_by_id(int(cmd['param']))
        print(f'{"ID":4} {"Name":32} {"Unit price":8}')
        print(f'{product["id"]:4} {product["name"]:32} {product["unit_price"]:8}')
    elif cmd['name'] == 'save':
        product = param_to_product(cmd['param'])
        create = product['id'] is None
        errors = product_repository.validate(product)

        if len(errors) > 0:
            for error in errors:
                print(f'Error: {error}')
        elif product_repository.save(product) is not None:
            if create:
                print('Product created.')
            else:
                print('Product updated.')
    elif cmd['name'] == 'delete':
        product_repository.delete(int(cmd['param']))
        print('Product deleted.')
    elif cmd['name'] == 'help':
        print('Available commands:')
        print('- list')
        print('- view [id]')
        print('- save [name],[unit_price]')
        print('\t-> create new product')
        print('- save [id],[name],[unit_price]')
        print('\t-> update existing product')
        print('- delete [id]')
        print('- help')
        print('- exit')
    else:
        print('Wrong command!')

    cmd = input_cmd()

print('Bye! :)')
exit()
