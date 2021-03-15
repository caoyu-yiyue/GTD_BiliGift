#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The Router to record gift message in Bilibili.com Live room to GTD Softwares.
将 Bilibili 直播间中的礼物信息自动记录入 GTD 软件的转发器。
Author: caoyu-yiyue
Github URL: https://github.com/caoyu-yiyue/GTD_BiliGift/
"""
import asyncio
from datetime import datetime

from bilibili_api.live import LiveDanmaku
from aiohttp import ClientSession

from src.todoist_manager import TodoistManager


class BiliGiftRouter(object):
    """
    Router Object for Forwarding gift messages to GTD Software.
    转发礼物信息到 GTD 软件的路由对象。
    """
    def __init__(self, room_display_id: int):
        """
        BiliGiftRouter object.
        -----------
        Parameters:
        -----------
        room_display_id: Bilibili live room display id, you can find it in the
        room url. Bilibili 直播间的显示直播间号，可以在直播间 URL 中找到。
        """

        self.__event_loop = asyncio.get_event_loop()
        self.__session = self.__event_loop.run_until_complete(
            self.__creat_session())
        self.__room = LiveDanmaku(room_display_id=room_display_id)
        self.__gift_filter = {}
        self.__gtd_managers = []

    async def __creat_session(self):
        return ClientSession()

    async def __close_session(self):
        await self.__session.close()

    @staticmethod
    def parse_gtd_managers(gtd_settings: list):
        """
        Parameters:
        -----------
        gtd_setting: The list of 'gtd_setting' in 'config.py'.
        """
        gtd_managers = []
        for setting in gtd_settings:
            # skip the setting if is not enabled.
            if not setting['enable']:
                continue

            gtd_type = setting['type'].lower()
            if gtd_type == 'todoist':
                gtd_manager = TodoistManager(
                    token=setting['token'],
                    gift_project_name=setting['project_name'])
                gtd_managers.append(gtd_manager)

        return gtd_managers

    def add_gtd_managers(self, gtd_managers: list):
        """
        Add GTD Managers to the router.
        Parameters:
        -----------
        gtd_managers: GTDManager or list of GTDManager
        The GTDManager object(s) to append to the BiliGiftRouter object.
        """
        gtd_managers = list(gtd_managers)
        self.__gtd_managers.extend(gtd_managers)

    def set_gift_filter(self, gift_filter: set):
        self.__gift_filter = gift_filter

    # =================== Callback Functions Start =================== #
    async def gift_sender(self, gift_msg: dict):
        """
        Callback function for gift send.
        -----------
        Parameters:
        -----------
        gift_msg: The message which bilibili_api send to the callback.
        """
        gift_data = gift_msg['data']['data']
        gift_name = gift_data['giftName']
        if gift_name in self.__gift_filter:
            return
        user_name = gift_data['uname']
        gift_num = gift_data['num']
        gift_timestamp = gift_data['timestamp']

        gtd_msg = '🎁【{}】赠送的 {} 个【{}】'.format(user_name, gift_num, gift_name)
        gtd_date = datetime.fromtimestamp(gift_timestamp)
        gtd_due_str = gtd_date.strftime('%Y-%m-%d')

        await asyncio.gather(*[
            gtd_manager.post_task(
                session=self.__session, task_msg=gtd_msg, due_str=gtd_due_str)
            for gtd_manager in self.__gtd_managers
        ])

    async def guard_sender(self, guard_msg: dict):
        """
        Callback function for gurad buy.
        -----------
        Parameters:
        -----------
        guard_msg: The message which bilibili_api send to the callback.
        """
        user_name = guard_msg['data']['data']['username']
        guard_type = guard_msg['data']['data']['gift_name']
        guard_timestamp = guard_msg['data']['data']['start_time']

        gtd_msg = '🚢【{}】上了【{}】'.format(user_name, guard_type)
        gtd_date = datetime.fromtimestamp(guard_timestamp)
        gtd_due_str = gtd_date.strftime('%Y-%m-%d')

        await asyncio.gather(*[
            gtd_manager.post_task(
                session=self.__session, task_msg=gtd_msg, due_str=gtd_due_str)
            for gtd_manager in self.__gtd_managers
        ])

    async def sc_sender(self, sc_msg: dict):
        """
        Callback funtion for Super Chat.
        Parameters:
        sc_msg: The message which bilibili_api send to the callback.
        """
        user_name = sc_msg['data']['data']['user_info']['uname']
        sc_content = sc_msg['data']['data']['message']
        sc_content_jp = sc_msg['data']['data'].get('message_jpn', '')
        sc_price = sc_msg['data']['data']['price']
        sc_timestamp = sc_msg['data']['data']['start_time']

        gtd_msg = '💬【{}】的 SC({})：{}'.format(user_name, sc_price, sc_content)
        if sc_content_jp:
            # sc_msg sent jp trans.
            gtd_msg += '｜{}'.format(sc_content_jp)
        gtd_date = datetime.fromtimestamp(sc_timestamp)
        gtd_due_str = gtd_date.strftime('%Y-%m-%d')

        await asyncio.gather(*[
            gtd_manager.post_task(
                session=self.__session, task_msg=gtd_msg, due_str=gtd_due_str)
            for gtd_manager in self.__gtd_managers
        ])

    # =================== Callback Functions End =================== #

    def start(self, tranlate_sc=False):
        """
        Start forwarding gift messages to GTD Softwares.
        ----------
        Parameters:
        ----------
        translate_sc: Whether use Japanese translate in the gtd task.
        """
        if not self.__gtd_managers:
            return "No GTD Manager is Activied, Please Check Your Setting."
        self.__room.add_event_handler('SEND_GIFT', self.gift_sender)
        self.__room.add_event_handler('GUARD_BUY', self.guard_sender)
        if not tranlate_sc:
            self.__room.add_event_handler('SUPER_CHAT_MESSAGE', self.sc_sender)
        else:
            self.__room.add_event_handler('SUPER_CHAT_MESSAGE_JPN',
                                          self.sc_sender)
        self.__room.connect()

    def stop(self):
        """Stop forwarding."""
        self.__room.disconnect()
        self.__event_loop.run_until_complete(self.__close_session())
