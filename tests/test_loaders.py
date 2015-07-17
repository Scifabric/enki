# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2015 SF Isle of Man Limited
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.
import enki
import pbclient
from mock import patch, call
from base import TestEnki


class TestServerTasksLoader(TestEnki):

    @patch('pbclient.find_tasks')
    def test_load_one_task_if_task_id_is_given(self, fake_client):
        task_data = {'id': 1, 'project_id': 1, 'state': 'completed'}
        task = pbclient.Task(task_data)
        fake_client.side_effect = [[task]]
        project = pbclient.Project(self.project)
        query = dict(project_id=task.project_id, id=task.id, limit=1, offset=0)

        loader = enki.ServerTasksLoader(project.id, task.id)
        tasks = loader.load()

        assert tasks[0] == task
        fake_client.assert_called_once_with(**query)

    @patch('pbclient.find_tasks')
    def test_load_all_tasks_if_no_task_id_is_given(self, fake_client):
        project = pbclient.Project(self.project)
        query = dict(project_id=1, limit=100, offset=0, state='completed')
        response = [pbclient.Task({'id': n}) for n in range(2)]
        fake_client.side_effect = [response]

        loader = enki.ServerTasksLoader(project.id)
        tasks = loader.load()

        assert len(tasks) == len(response)
        fake_client.assert_called_with(**query)

    @patch('pbclient.find_tasks')
    def test_load_all_tasks_uses_keyset_pagination(self, fake_client):
        project = pbclient.Project(self.project)
        first_query = dict(project_id=1, limit=100, offset=0, state='completed')
        second_query = dict(project_id=1, limit=100, last_id=99, state='completed')

        first_response = [pbclient.Task({'id': n}) for n in range(100)]
        second_response = [pbclient.Task({'id': 100+n}) for n in range(2)]
        fake_client.side_effect = [first_response, second_response]

        loader = enki.ServerTasksLoader(project.id)
        tasks = loader.load()

        assert len(tasks) == 102
        assert fake_client.mock_calls == [call(**first_query), call(**second_query)]


class TestJsonTasksLoader(object):
    json_file = 'tests/different_tasks.json'

    def test_load_one_task_if_task_id_is_given(self):
        loader = enki.JsonTasksLoader(project_id=1, json_file=self.json_file,
                                     task_id=2)

        tasks = loader.load()

        assert len(tasks) == 1, tasks
        assert tasks[0].id == 2, tasks

    def test_load_returns_project_tasks_when_project_id_in_query(self):
        loader = enki.JsonTasksLoader(json_file=self.json_file, project_id=1)

        tasks = loader.load()

        assert len(tasks) == 2, tasks
        for task in tasks:
            assert task.project_id == 1

    def test_load_returns_tasks_with_state_in_query(self):
        loader = enki.JsonTasksLoader(project_id=1, json_file=self.json_file,
                                     state='ongoing')

        tasks = loader.load()

        assert len(tasks) == 2, tasks
        for task in tasks:
            assert task.project_id == 1
