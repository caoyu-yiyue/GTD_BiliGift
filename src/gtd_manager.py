"""
GTD Manager abstract class for all the Managers.
Author: caoyu-yiyue
Github URL: https://github.com/caoyu-yiyue/GTD_BiliGift/
"""
from abc import ABC, abstractmethod


class GTDManager(ABC):
    @abstractmethod
    def post_task():
        pass
