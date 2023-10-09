from abc import ABC, abstractmethod


class Effect(ABC):
    @abstractmethod
    def apply(self) -> None: ...
