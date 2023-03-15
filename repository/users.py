from model.user import User


class UserRepository:
    def __init__(self, db, table='user'):
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

    def find_all_by_username(self, username):
        query = f"""
            SELECT *
                FROM {self.table}
                WHERE username LIKE ?
                ORDER BY id
        """
        result = self.db.execute(query, ('%' + username + '%',)).fetchall()

        return [self._row_to_entity(row) for row in result]

    def find_one_by_id(self, user_id):
        query = f"""
            SELECT *
                FROM {self.table}
                WHERE id = ?
        """
        row = self.db.execute(query, (user_id,)).fetchone()

        return self._row_to_entity(row) if row is not None else None

    def find_one_by_username(self, username):
        query = f"""
            SELECT *
                FROM {self.table}
                WHERE username = ?
        """
        row = self.db.execute(query, (username,)).fetchone()

        return self._row_to_entity(row) if row is not None else None

    def save(self, user):
        if user.user_id is None:
            # CREATE
            return self._create(user)
        else:
            # UPDATE
            return self._update(user)

    def delete(self, user_id):
        query = f"""
            DELETE FROM {self.table}
                WHERE id = ?
        """
        rowcount = self.db.execute(query, (user_id,)).rowcount
        self.db.commit()

        return rowcount

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
