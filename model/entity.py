from abc import abstractmethod


class Entity:
    @abstractmethod
    def get_id(self):
        raise NotImplementedError

    @abstractmethod
    def set_id(self, entity_id):
        raise NotImplementedError
