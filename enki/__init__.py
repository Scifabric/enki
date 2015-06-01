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
"""
Enki module for analyzing the results of a PyBossa project.

This module exports:
    * Enki Class: to import an project, its tasks and task runs

"""
import pandas
import pbclient
import json
from pynq import From
from exceptions import ProjectNotFound, ProjectError, \
    ProjectWithoutTasks, ProjectWithoutTaskRuns


class Enki(object):

    """General class for Enki."""

    def __init__(self, api_key, endpoint, project_short_name):
        """Initiate."""
        self.api_key = api_key
        self.endpoint = endpoint
        self.project = None
        self.pbclient = pbclient
        self.pbclient.set('api_key', self.api_key)
        self.pbclient.set('endpoint', self.endpoint)
        if self.project is None:
            self.project = self.get_project(project_short_name)

    def get_project(self, project_short_name):
        """Return project object."""
        project = self.pbclient.find_project(short_name=project_short_name)
        if (len(project) == 1):
            return project[0]
        else:
            raise ProjectNotFound(project_short_name)

    def explode_info(self, item):
        """Return the a dict of the object but with info field exploded."""
        tmp = item.__dict__['data']
        if type(item.info) == dict:
            keys = tmp['info'].keys()
            for k in keys:
                tmp[k] = tmp['info'][k]
        return tmp

    def get_tasks(self, task_id=None, state='completed', json_file=None):
        """Load all project Tasks."""
        if task_id:
            offset = 0
            limit = 1
        else:
            offset = 0
            limit = 100
        self.tasks = []
        if self.project and task_id:
            query = dict(project_id=self.project.id,
                         state=state,
                         id=task_id,
                         limit=limit,
                         offset=offset)
        elif self.project and task_id is None:
            query = dict(project_id=self.project.id,
                         state=state,
                         limit=limit,
                         offset=offset)
        else:
            raise ProjectError()

        tmp = self.pbclient.find_tasks(**query)
        if json_file:
            json_file_data = open(json_file).read()
            tmp_tasks = json.loads(json_file_data)
            for t in tmp_tasks:
                self.tasks.append(pbclient.Task(t))
        else:
            while(len(tmp) != 0):
                self.tasks += tmp
                offset += limit
                query['offset'] += limit
                tmp = self.pbclient.find_tasks(**query)

        # Create the data frame for tasks
        try:
            self.tasks[0]
            data = [self.explode_info(t) for t in self.tasks]
            index = [t.__dict__['data']['id'] for t in self.tasks]
            self.tasks_df = pandas.DataFrame(data, index)
        except:
            raise ProjectWithoutTasks

    def get_task_runs(self, json_file=None):
        """Load all project Task Runs from Tasks."""
        self.task_runs = {}
        self.task_runs_file = []
        self.task_runs_df = {}

        if json_file:
            json_file_data = open(json_file).read()
            tmp_task_runs = json.loads(json_file_data)
            for tr in tmp_task_runs:
                self.task_runs_file.append(pbclient.TaskRun(tr))

        if self.project:
            for t in self.tasks:
                offset = 0
                limit = 100
                self.task_runs[t.id] = []
                if json_file:
                    query = "item.project_id == %s and item.task_id == %s" % \
                        (self.project.id, t.id)
                    self.task_runs[t.id] = From(self.task_runs_file)\
                        .where(query).select_many()
                else:
                    tmp = self.pbclient.find_taskruns(project_id=self.project.id,
                                                      task_id=t.id,
                                                      limit=limit,
                                                      offset=offset)
                    while(len(tmp) != 0):
                        self.task_runs[t.id] += tmp
                        offset += limit
                        tmp = self.pbclient.find_taskruns(
                            project_id=self.project.id,
                            task_id=t.id,
                            limit=limit,
                            offset=offset)

                if len(self.task_runs[t.id]) > 0:
                    data = [self.explode_info(tr)
                            for tr in self.task_runs[t.id]]
                    index = [tr.__dict__['data']['id'] for tr in
                             self.task_runs[t.id]]
                    self.task_runs_df[t.id] = pandas.DataFrame(data, index)
                else:
                    raise ProjectWithoutTaskRuns
        else:
            raise ProjectError()

    def get_all(self):  # pragma: no cover
        """Get task and task_runs from project."""
        self.get_tasks()
        self.get_task_runs()

    def describe(self, element):  # pragma: no cover
        """Return tasks or task_runs Panda describe."""
        if (element == 'tasks'):
            return self.tasks_df.describe()
        elif (element == 'task_runs'):
            return self.task_runs_df.describe()
        else:
            return "ERROR: %s not found" % element
