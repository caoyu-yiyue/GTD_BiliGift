"""GTD Manager abstract class for all the Managers.
"""
from abc import ABC, abstractmethod


class GTDManager(ABC):
    @abstractmethod
    def post_task():
        pass
