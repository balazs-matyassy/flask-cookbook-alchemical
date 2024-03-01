from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_entity_cls():
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def find_all():
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def find_by_id(entity_id):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def save(entity):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def delete_by_id(entity_id):
        raise NotImplementedError()
