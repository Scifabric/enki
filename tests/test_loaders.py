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
"""Package to test Enki package."""
import enki
import pbclient
from enki.exceptions import ProjectNotFound, ProjectError, \
    ProjectWithoutTasks, ProjectWithoutTaskRuns
from mock import patch, call
from base import TestEnki
from nose.tools import raises


class TestServerTaskLoader(TestEnki):

    @patch('pbclient.find_tasks')
    def test_load_one_task_if_task_id_is_given(self, fake_client):
        task_data = {'id': 1, 'project_id': 1, 'state': 'completed'}
        task = pbclient.Task(task_data)
        fake_client.side_effect = [[task]]
        project = pbclient.Project(self.project)
        query = dict(project_id=task.project_id, id=task.id, limit=1, offset=0)

        loader = enki.ServerTaskLoader(project, task.id)
        tasks = loader.load()

        assert tasks[0] == task
        fake_client.assert_called_once_with(**query)

    @patch('pbclient.find_tasks')
    def test_load_all_tasks_if_no_task_id_is_given(self, fake_client):
        project = pbclient.Project(self.project)
        query = dict(project_id=1, limit=100, offset=0, state='completed')
        response = [pbclient.Task({'id': n}) for n in range(2)]
        fake_client.side_effect = [response]

        loader = enki.ServerTaskLoader(project)
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

        loader = enki.ServerTaskLoader(project)
        tasks = loader.load()

        assert len(tasks) == 102
        assert fake_client.mock_calls == [call(**first_query), call(**second_query)]
