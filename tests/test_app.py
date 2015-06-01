# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2013 SF Isle of Man Limited
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
from enki.exceptions import ProjectNotFound, ProjectError, \
    ProjectWithoutTasks, ProjectWithoutTaskRuns
from mock import patch
from base import TestEnki
from nose.tools import raises


class Test(TestEnki):
    @raises(ProjectNotFound)
    @patch('pbclient.requests.get')
    def test_00_get_project_not_found(self, Mock):
        """Test project not found works."""
        # App does not exist returns an empty list
        Mock.return_value = self.create_fake_request(data=[], status=200)
        enki.Enki(api_key='key', endpoint='http://localhost:5000',
                  project_short_name='non-exists')

    @patch('pbclient.requests.get')
    def test_01_get_project_found(self, Mock):
        """Test project found works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        assert e.project.id == self.project['id'], e.project
        assert e.project.short_name == self.project['short_name'], e.project

    @patch('pbclient.requests.get')
    def test_explode_info_without_info_dict(self, Mock):
        """Test explode_info method works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        Mock.side_effect = [self.create_fake_request([self.task], 200),
                            self.create_fake_request([], 200)]
        e.get_tasks()
        result = e.explode_info(e.tasks[0])
        err_msg = "This item should not be exploded"
        assert result.keys() == self.task.keys(), err_msg

    @patch('pbclient.requests.get')
    def test_explode_info_with_info_dict(self, Mock):
        """Test explode_info method works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        Mock.side_effect = [self.create_fake_request([self.task2], 200),
                            self.create_fake_request([], 200)]
        e.get_tasks()
        result = e.explode_info(e.tasks[0])
        err_msg = "This item should be exploded"
        assert 'key' in result.keys(), err_msg

    @patch('pbclient.requests.get')
    def test_explode_info_with_info_dict_file(self, Mock):
        """Test explode_info method with a file works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        e.get_tasks(json_file='test_task.json')
        print e.tasks[0]
        result = e.explode_info(e.tasks[0])
        err_msg = "This item should be exploded"
        assert 'key' in result.keys(), err_msg

    @raises(ProjectError)
    @patch('pbclient.requests.get')
    def test_get_tasks_project_error(self, Mock):
        """Test get_tasks without project works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        # Make it fail
        e.project = None
        Mock.side_effect = [self.create_fake_request([], 200)]
        e.get_tasks()

    @raises(ProjectWithoutTasks)
    @patch('pbclient.requests.get')
    def test_get_tasks_empty(self, Mock):
        """Test get_tasks without tasks works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        Mock.side_effect = [self.create_fake_request([], 200)]
        e.get_tasks()

    @patch('pbclient.requests.get')
    def test_get_tasks_for_one_id(self, Mock):
        """Test get_tasks with only one task works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        Mock.side_effect = [self.create_fake_request([self.task], 200),
                            self.create_fake_request([], 200)]
        e.get_tasks(task_id=self.task['id'])
        desc = e.tasks_df['info'].describe()
        err_msg = "Pandas describe is wrong"
        assert e.tasks_df['id'].count() == 1, err_msg
        assert desc['count'] == 1, err_msg
        assert desc['unique'] == 1, err_msg
        assert desc['top'] == self.task['info'], err_msg
        assert desc['freq'] == 1, err_msg


    @patch('pbclient.requests.get')
    def test_get_tasks(self, Mock):
        """Test get_tasks with tasks works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        Mock.side_effect = [self.create_fake_request([self.task], 200),
                            self.create_fake_request([], 200)]
        e.get_tasks()
        desc = e.tasks_df['info'].describe()
        err_msg = "Pandas describe is wrong"
        assert e.tasks_df['id'].count() == 1, err_msg
        assert desc['count'] == 1, err_msg
        assert desc['unique'] == 1, err_msg
        assert desc['top'] == self.task['info'], err_msg
        assert desc['freq'] == 1, err_msg

    @raises(ProjectError)
    @patch('pbclient.requests.get')
    def test_get_task_runs_project_error(self, Mock):
        """Test get_task_runs without task runs works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        Mock.side_effect = [self.create_fake_request([self.task], 200),
                            self.create_fake_request([], 200)]
        e.get_tasks()
        # Make it fail
        e.project = None
        Mock.side_effect = [self.create_fake_request([], 200)]
        e.get_task_runs()

    @raises(ProjectWithoutTaskRuns)
    @patch('pbclient.requests.get')
    def test_get_task_runs_empty(self, Mock):
        """Test get_task_runs without task runs works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        Mock.side_effect = [self.create_fake_request([self.task], 200),
                            self.create_fake_request([], 200)]
        e.get_tasks()

        Mock.side_effect = [self.create_fake_request([], 200)]
        e.get_task_runs()

    @patch('pbclient.requests.get')
    def test_get_task_runs(self, Mock):
        """Test get_task_runs with task_runs works."""
        Mock.return_value = self.create_fake_request([self.project], 200)
        e = enki.Enki(api_key='key', endpoint='http://localhost:5000',
                      project_short_name=self.project['short_name'])
        Mock.side_effect = [self.create_fake_request([self.task], 200),
                            self.create_fake_request([], 200)]
        e.get_tasks()
        Mock.side_effect = [self.create_fake_request([self.taskrun], 200),
                            self.create_fake_request([], 200)]
        e.get_task_runs()

        desc = e.task_runs_df[e.tasks[0].id]['info'].describe()
        err_msg = "Pandas describe is wrong"
        assert desc['count'] == 1, err_msg
        assert desc['unique'] == 1, err_msg
        assert desc['top'] == self.task['info'], err_msg
        assert desc['freq'] == 1, err_msg
