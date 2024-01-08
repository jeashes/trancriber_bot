from abc import ABC, abstractmethod


class Transcriber(ABC):
    @abstractmethod
    def __init__(self, model: str, device: str, compute_type: str = 'int8') -> None:
        ...
