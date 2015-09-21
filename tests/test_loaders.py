# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2015 SciFabric LTD.
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
import pbclient
from mock import patch, call
from base import TestEnki
from enki.task_loaders import ServerTasksLoader, JsonTasksLoader
from enki.task_run_loaders import ServerTaskRunsLoader, JsonTaskRunsLoader


class TestServerTasksLoader(TestEnki):

    @patch('pbclient.find_tasks')
    def test_load_does_one_request_to_get_specified_task_if_id_given(self, fake_client):
        project_id = 1
        task_data = {'id': 1, 'project_id': project_id, 'state': 'completed'}
        task = pbclient.Task(task_data)
        fake_client.side_effect = [[task]]
        query = dict(project_id=task.project_id, id=task.id, limit=1, offset=0)

        loader = ServerTasksLoader(project_id, task.id)
        tasks = loader.load()

        assert tasks[0] == task
        fake_client.assert_called_once_with(**query)

    @patch('pbclient.find_tasks')
    def test_load_all_tasks_if_no_task_id_is_given(self, fake_client):
        project = pbclient.Project(self.project)
        query = dict(project_id=1, limit=100, offset=0, state='completed')
        response = [pbclient.Task({'id': n}) for n in range(2)]
        fake_client.side_effect = [response]

        loader = ServerTasksLoader(project.id)
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

        loader = ServerTasksLoader(project.id)
        tasks = loader.load()

        assert len(tasks) == 102
        assert fake_client.mock_calls[1] == call(**second_query)


class TestJsonTasksLoader(object):
    json_file = 'tests/different_tasks.json'

    def test_load_one_task_if_task_id_is_given(self):
        loader = JsonTasksLoader(project_id=1, json_file=self.json_file,
                                     task_id=2)

        tasks = loader.load()

        assert len(tasks) == 1, tasks
        assert tasks[0].id == 2, tasks

    def test_load_returns_project_tasks_when_project_id_in_query(self):
        loader = JsonTasksLoader(json_file=self.json_file, project_id=2)

        tasks = loader.load()

        assert len(tasks) == 2, tasks
        assert_all_tasks_belong_to_project(tasks, project_id=2)

    def test_load_returns_tasks_with_state_in_query(self):
        loader = JsonTasksLoader(project_id=1,
                                              json_file=self.json_file,
                                              state='ongoing')

        tasks = loader.load()

        assert len(tasks) == 2, tasks
        assert_all_tasks_belong_to_project(tasks, project_id=1)


class TestServerTaskRunsLoader(object):

    @patch('pbclient.find_taskruns')
    def test_load_returns_empty_dict_if_no_tasks(self, fake_client):
        loader = ServerTaskRunsLoader(project_id=1, tasks=[])
        fake_client.return_value = [pbclient.TaskRun({'id':1, 'project_id': 1})]

        task_runs, _ = loader.load()

        assert task_runs == {}

    @patch('pbclient.find_taskruns')
    def test_load_returns_dict_with_taskruns_for_each_task(self, fake_client):
        tasks = [pbclient.Task({'id': 1}), pbclient.Task({'id': 2})]
        loader = ServerTaskRunsLoader(project_id=1, tasks=tasks)
        fake_client.side_effect = [
            [pbclient.TaskRun({'id': 1, 'task_id': 1, 'project_id': 1}),
             pbclient.TaskRun({'id': 2, 'task_id': 1, 'project_id': 1})],
            [],
            [pbclient.TaskRun({'id': 3, 'task_id': 2, 'project_id': 1}),
             pbclient.TaskRun({'id': 4, 'task_id': 2, 'project_id': 1})],
            []]

        task_runs, _ = loader.load()

        assert len(task_runs) == 2
        assert_task_runs_grouped_by_task(task_runs)

    @patch('pbclient.find_taskruns')
    def test_load_uses_keyset_pagination(self, fake_client):
        tasks = [pbclient.Task({'id': 1})]
        loader = ServerTaskRunsLoader(project_id=1, tasks=tasks)
        fake_client.side_effect = [
            [pbclient.TaskRun({'id': 1, 'task_id': 1, 'project_id': 1}),
             pbclient.TaskRun({'id': 2, 'task_id': 1, 'project_id': 1})],
            []]
        first_query = dict(limit=100, offset=0, project_id=1, task_id=1)
        second_query = dict(last_id=2, limit=100, project_id=1, task_id=1)

        tasks = loader.load()

        assert fake_client.mock_calls == [call(**first_query), call(**second_query)]


class TestJsonTaskRunsLoader(object):
    json_file = 'tests/different_task_runs.json'

    def test_load_returns_empty_dict_if_no_tasks(self):
        loader = JsonTaskRunsLoader(project_id=1, tasks=[],
                                         json_file=self.json_file)

        task_runs, _ = loader.load()

        assert task_runs == {}, task_runs

    def test_load_returns_dict_with_taskruns_for_each_task(self):
        tasks = [pbclient.Task({'id': 1, 'project_id': 1}),
                 pbclient.Task({'id': 2, 'project_id': 1})]
        loader = JsonTaskRunsLoader(project_id=1, tasks=tasks,
                                         json_file=self.json_file)

        task_runs, _ = loader.load()

        assert len(task_runs) == 2
        assert_task_runs_grouped_by_task(task_runs)



def assert_all_tasks_belong_to_project(tasks, project_id):
    for task in tasks:
        assert task.project_id == project_id

def assert_task_runs_grouped_by_task(task_runs):
    for task in task_runs.keys():
        for task_run in task_runs[task]:
            assert task == task_run.task_id, task_runs
