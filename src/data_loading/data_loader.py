from abc import ABC, abstractmethod

from organisation_utils.logging_config import logger_factory

from .data_container import DataContainer


class DataLoader(ABC):
    def __init__(self):
        self.logger = logger_factory.get_logger("__loader__")

    @abstractmethod
    def load(self, data_container: DataContainer) -> None:
        pass
