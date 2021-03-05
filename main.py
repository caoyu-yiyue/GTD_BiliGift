#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Script to Run the App.
运行 App 的主脚本。
Author: caoyu-yiyue
Github URL: https://github.com/caoyu-yiyue/GTD_BiliGift/
"""
from src.gift_router import BiliGiftRouter
from config import config

# %%
if __name__ == '__main__':
    gift_router = BiliGiftRouter(room_display_id=config['liveroom_id'])
    gtd_managers = gift_router.parse_gtd_managers(
        gtd_settings=config['gtd_settings'])
    gift_router.add_gtd_managers(gtd_managers)
    gift_router.set_gift_filter(config['gift_filter'])
    try:
        gift_router.start(tranlate_sc=config['translate_sc'])
    except KeyboardInterrupt:
        print(' End Connection.')
    finally:
        gift_router.stop()
