#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Saving Use Configs.
保存用户设置的各类信息
Author: caoyu-yiyue
Github URL: https://github.com/caoyu-yiyue/GTD_BiliGift/
"""
config = {
    # The bilibili live room id, Can find it in url。B 站直播间号，可以在直播间的 url 中找到。
    'liveroom_id':
    4138602,
    # Gift list in which don't forward to GTD software. 不需要转发进 GTD 软件的礼物名单。
    'gift_filter': {'辣条'},
    # Whether add Japanese translation of SuperChat. 是否带上 SC 的日语翻译。
    'translate_sc':
    False,
    # GTD API Settings. One Item is an instance for a GTD Client,
    # Can use several GTD instance at the same time.
    # GTD 软件的各类 API 设置。每个项目为一个 GTD 客户端，可以同时启用多个 GTD 客户端。
    'gtd_settings': [
        {
            'id': 'todoist1',  # Custom name for the setting.
            'enable': True,  # whether enable this instance.
            'type': 'todoist',  # Which GTD software for the instance.
            'token': '',  # Todoist API Token. At Todoist Settings ->
            # Integrations -> API token
            'project_name':
            'Bilibili Gift'  # The Project name for saving messages.
        },
        # More GTD Clients' Setting.
        {
            'id': 'todoist2',
            'enable': False,
            'type': 'todoist',
            'token': '',
            'project_name': 'Bilibili Gift'
        }
    ]
}
