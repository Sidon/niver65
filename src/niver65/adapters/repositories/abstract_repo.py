import abc
import logging

logger = logging.getLogger(__name__)


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, instance):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, instance):
        raise NotImplementedError
