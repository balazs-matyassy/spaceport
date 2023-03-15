from model.user import User
from repository.repository import Repository


class UserRepository(Repository):
    def __init__(self, db, table='user'):
        super().__init__(db, table)

    def validate(self, user):
        errors = []

        if user.username is None \
                or len(user.username.strip()) == 0:
            errors.append('Username missing.')

        if user.password is None \
                or len(user.password) == 0:
            errors.append('Password missing.')

        return errors

    def _row_to_entity(self, row):
        return User(row['id'], row['username'], row['password'], row['role'].upper() == 'ADMIN')

    def _create(self, user):
        query = f"""
            INSERT INTO {self.table} (username, password, role)
                VALUES (?, ?, ?)
        """
        user.product_id = self.db.execute(
            query,
            (user.username, user.password, 'ADMIN' if user.admin else 'USER')
        ).lastrowid
        self.db.commit()

        return user

    def _update(self, user):
        query = f"""
            UPDATE {self.table} SET
                username = ?,
                password = ?,
                role = ?
            WHERE id = ?
        """
        rowcount = self.db.execute(
            query,
            (user.username, user.password, 'ADMIN' if user.admin else 'USER', user.user_id)
        ).rowcount

        if rowcount == 1:
            self.db.commit()
            return user
        else:
            return None
