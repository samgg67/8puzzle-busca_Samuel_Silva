from abc import ABC, abstractmethod
from puzzle.state import State
from puzzle.result import SearchResult


class BaseSearch(ABC):
    @abstractmethod
    def search(self, initial: State) -> SearchResult:
        ...
