from model.product import Product
from repository.repository import Repository


class ProductRepository(Repository):
    def __init__(self, db, table='product'):
        super().__init__(db, table)

    def validate(self, product):
        errors = []

        if product.name is None \
                or len(product.name.strip()) == 0:
            errors.append('Name missing.')

        if product.unit_price < 0:
            errors.append('Unit price must be a non-negative number.')

        if product.discount < 0 or product.discount > 100:
            errors.append('Unit price must be a number between 0 and 100.')

        return errors

    def _row_to_entity(self, row):
        return Product(row['id'], row['name'], row['unit_price'], row['discount'])

    def _create(self, product):
        query = f"""
            INSERT INTO {self.table} (name, unit_price, discount)
                VALUES (?, ?, ?)
        """
        product.product_id = self.db.execute(
            query,
            (product.name, product.unit_price, product.discount)
        ).lastrowid
        self.db.commit()

        return product

    def _update(self, product):
        query = f"""
            UPDATE {self.table} SET
                name = ?,
                unit_price = ?,
                discount = ?
            WHERE id = ?
        """
        rowcount = self.db.execute(
            query,
            (product.name, product.unit_price, product.discount, product.product_id)
        ).rowcount

        if rowcount == 1:
            self.db.commit()
            return product
        else:
            return None
