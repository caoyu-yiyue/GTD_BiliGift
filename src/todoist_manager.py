"""
Manager for Todoist.
Author: caoyu-yiyue
Github URL: https://github.com/caoyu-yiyue/GTD_BiliGift/
"""
from logging import warning
import uuid

import todoist
from aiohttp import ClientSession

from src.gtd_manager import GTDManager


class TodoistManager(GTDManager):
    gtd_type = "todoist"

    def __init__(self, token: str, gift_project_name: str = 'Bilibili Gift'):
        """
        Manager for projects and tasks for todoist.
        管理 Todoist 项目管理、任务上传的对象
        ----------
        Parameter:
        ----------
        todoist_token: API token for todoist, at Todoist Settings ->
        Integrations -> API token. Todoist 的 API Token，在设置 -> 关联应用 -> API置换符中。

        gift_project_name: The todoist Project name for saving gift infomation,
        Default 'Bilibili Gift'. 存储礼物任务的 Todoist 项目名称，默认为 Bilibili Gift。
        """

        self._todoist_api = todoist.TodoistAPI(token=token)
        self.gift_project_name = gift_project_name
        self.gift_project_id = None

        self.prepare_todoist()

    def _todoist_sync(self) -> None:
        """Sync todoist data with todoist sync api."""
        self._todoist_api.sync()

    def _prepare_todoist_project(self) -> None:
        """Find the project name in todoist, else creat it."""
        projects = self._todoist_api.state['projects']
        project_names = [project['name'] for project in projects]

        # check if there's a project name, use it or creat it.
        if self.gift_project_name not in project_names:
            gift_project = self._todoist_api.projects.add(
                self.gift_project_name)
            self._todoist_api.commit()
        else:
            gift_project = projects[project_names.index(
                self.gift_project_name)]
        self.gift_project_id = gift_project['id']

    def prepare_todoist(self) -> None:
        """Prepare all the things for todoist."""
        self._todoist_sync()
        self._prepare_todoist_project()

    async def post_task(self, session: ClientSession, task_msg: str,
                        due_str: str, **kwargs):
        """Add task to todoist.
        -----------
        Parameters:
        -----------
        session: Aiohttp.ClientSession. The session for task posting.
        task_msg: The message of the task in todoist.
        due_str: A str for the task due. Using English in natural language and
        todoist will pharse it.
        """
        if not self.gift_project_id:
            warning('No project id provided, use Inbox')

        post_json = {
            'content': task_msg,
            'due_string': due_str,
            'due_lang': 'en',
            'project_id': self.gift_project_id
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': 'Bearer {}'.format(self._todoist_api.token)
        }
        async with session.post(url='https://api.todoist.com/rest/v1/tasks',
                                json=post_json,
                                headers=headers) as resp:
            resp.raise_for_status()
            if resp.status == 200:
                print('Success for ' + task_msg)
