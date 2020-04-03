import abc


class Uploader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def upload(self, path_to_file: str) -> None:
        raise NotImplementedError
