from abc import abstractmethod


class Repository:
    def __init__(self, db, table):
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

    def find_all_by_column(self, column, value):
        query = f"""
            SELECT *
                FROM {self.table}
                WHERE {column} LIKE ?
                ORDER BY id
        """
        result = self.db.execute(query, ('%' + value + '%',)).fetchall()

        return [self._row_to_entity(row) for row in result]

    def find_one_by_id(self, entity_id):
        query = f"""
            SELECT *
                FROM {self.table}
                WHERE id = ?
        """
        row = self.db.execute(query, (entity_id,)).fetchone()

        return self._row_to_entity(row) if row is not None else None

    def find_one_by_column(self, column, value):
        query = f"""
            SELECT *
                FROM {self.table}
                WHERE {column} = ?
            """
        row = self.db.execute(query, (value,)).fetchone()

        return self._row_to_entity(row) if row is not None else None

    def save(self, entity):
        if entity.get_id() is None:
            # CREATE
            return self._create(entity)
        else:
            # UPDATE
            return self._update(entity)

    def delete(self, entity_id):
        query = f"""
            DELETE FROM {self.table}
                WHERE id = ?
        """
        rowcount = self.db.execute(query, (entity_id,)).rowcount
        self.db.commit()

        return rowcount

    @abstractmethod
    def validate(self, product):
        raise NotImplementedError

    @abstractmethod
    def _row_to_entity(self, row):
        raise NotImplementedError

    @abstractmethod
    def _create(self, product):
        raise NotImplementedError

    @abstractmethod
    def _update(self, product):
        raise NotImplementedError
