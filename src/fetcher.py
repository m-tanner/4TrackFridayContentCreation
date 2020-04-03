import abc
from typing import List

from src.subscriber import Subscriber


class Fetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_real_subscribers(self) -> List[Subscriber]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_test_subscribers(self) -> List[Subscriber]:
        raise NotImplementedError
