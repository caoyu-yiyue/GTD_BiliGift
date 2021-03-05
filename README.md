# 转发 Bilibili 直播间礼物、舰长、SuperChat 信息到任务管理软件

将 Bilibili 直播间中的礼物、舰长、SuperChat 信息转发到 GTD（任务管理）软件中，方便主播管理。可以在直播中将感谢过的礼物等勾选完成，只留下还未感谢的礼物信息，方便区分和查找。另外通过任务管理软件的其它功能，如排序、过滤等，更易管理和记录礼物信息。

目前支持的 GTD 软件为 [Todoist](https://todoist.com/)。

## 使用方法

1. 首先需要安装有 [Python](https://www.python.org/downloads/) 环境（开发坏境为 Python 3.9.2）。
2. 下载或 Clone 该项目

    ```shell
    git clone https://github.com/caoyu-yiyue/GTD_BiliGift.git
    ```

3. 安装项目依赖。

    ```shell
    pip install-r requirements.txt 
    ```

4. 在 `config.py` 文件中设置需要监控的直播间号、GTD 软件的 API 等配置信息，详细配置请见文件中的注释说明。可以同时配置多个 GTD 客户端接收礼物信息。
5. 打开 Mac OS 上的终端（Terminal）或 Windows 上的 CMD 或 Powershell，通过 `cd` 命令将路径移动到下载本项目的路径，然后运行 `main.py`，程序将自动运行。

    ```shell
    cd <your path to this project>
    python3 main.py
    ```

6. 在终端中按 `Ctrl + C` 停止运行。

## 在 Python 中使用相关模块

项目通过 `GTDManager` 的子类管理 GTD 客户端对象，完成客户端信息的下载和任务上传等任务。通过 `BiliGiftRouter` 对象完成直播间信息抓取和转发。如不通过 `config.py` 文件指定配置信息，也可以在 Python 脚本中使用该对象手动创建礼物转发器。

使用方法如：

```python
from src.gift_router import BiliGiftRouter
from src.todoist_manager import TodoistManager

gift_router = BiliGiftRouter(room_display_id=4138602)   # 初始化路由对象
gtd_manager = TodoistManager(token=<API Token>, gift_projcet_name="Bilibili Gift")  # 初始化 GTD 管理器
gift_router.add_gtd_managers([gtd_manager]) # 添加 GTD 管理器，可以是 list 或单个对象。
gift_router.set_gift_filter({'辣条'})  # 添加无需记录的礼物名称。
try:
    gift_router.start(tranlate_sc=config['translate_sc'])   # 开始任务，并指定是否需要记录 SC 的日语翻译。
except KeyboardInterrupt:
    print('End Connection.')
finally:
    gift_router.stop()  # 任务结束时关闭连接。
```

转发器内部使用异步 IO 提高性能，需要注意结束任务时合理关闭连接。

项目鸣谢： [bilibili-api](https://github.com/Passkou/bilibili-api)。
