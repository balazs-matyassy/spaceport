from model.product import Product


class ProductRepository:
    def __init__(self, db, table='product'):
        self.db = db
        self.table = table

    def find_all(self):
        query = f"""
            SELECT *
                FROM {self.table}
                ORDER BY id
        """
        result = self.db.execute(query).fetchall()

        return [self._row_to_entity(row) for row in result]

    def find_all_by_name(self, name):
        query = f"""
            SELECT *
                FROM {self.table}
                WHERE name LIKE ?
                ORDER BY id
        """
        result = self.db.execute(query, ('%' + name + '%',)).fetchall()

        return [self._row_to_entity(row) for row in result]

    def find_one_by_id(self, product_id):
        query = f"""
            SELECT *
                FROM {self.table}
                WHERE id = ?
        """
        row = self.db.execute(query, (product_id,)).fetchone()

        return self._row_to_entity(row) if row is not None else None

    def save(self, product):
        if product.product_id is None:
            # CREATE
            return self._create(product)
        else:
            # UPDATE
            return self._update(product)

    def delete(self, product_id):
        query = f"""
            DELETE FROM {self.table}
                WHERE id = ?
        """
        rowcount = self.db.execute(query, (product_id,)).rowcount
        self.db.commit()

        return rowcount

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
