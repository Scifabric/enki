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
"""
Enki module for analyzing the results of a PyBossa project.

This module exports:
    * Enki Class: to import an project, its tasks and task runs

"""
import pbclient
from task_loaders import create_tasks_loader
from task_run_loaders import create_task_runs_loader
import dataframer
from exceptions import ProjectNotFound, ProjectError, \
    ProjectWithoutTasks, ProjectWithoutTaskRuns


class Enki(object):

    """General class for Enki."""

    def __init__(self, api_key, endpoint,
                 project_short_name, all=0):
        """Initiate."""
        self.project = None
        self.all = all
        pbclient.set('api_key', api_key)
        pbclient.set('endpoint', endpoint)
        if self.project is None:
            self.project = self.get_project(project_short_name)

    def get_project(self, project_short_name):
        """Return project object."""
        project = pbclient.find_project(short_name=project_short_name,
                                        all=self.all)
        if (len(project) == 1):
            return project[0]
        else:
            raise ProjectNotFound(project_short_name)

    def explode_info(self, item):
        """Return the a dict of the object but with info field exploded."""
        return dataframer.explode_info(item)

    def get_tasks(self, task_id=None, state='completed', json_file=None):
        """Load all project Tasks."""
        if self.project is None:
            raise ProjectError

        loader = create_tasks_loader(self.project.id, task_id,
                                     state, json_file, self.all)
        self.tasks = loader.load()

        self._check_project_has_tasks()
        self.tasks_df = dataframer.create_data_frame(self.tasks)

    def get_task_runs(self, json_file=None):
        """Load all project Task Runs from Tasks."""
        if self.project is None:
            raise ProjectError
        loader = create_task_runs_loader(self.project.id, self.tasks,
                                         json_file, self.all)
        self.task_runs, self.task_runs_file = loader.load()

        self._check_project_has_taskruns()
        self.task_runs_df = dataframer.create_task_run_data_frames(self.tasks, self.task_runs)

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

    def _check_project_has_tasks(self):
        if len(self.tasks) == 0:
            raise ProjectWithoutTasks

    def _check_project_has_taskruns(self):
        count_task_runs = lambda total, task_runs: total + len(task_runs)
        total_task_runs = reduce(count_task_runs, self.task_runs.values(), 0)
        if total_task_runs == 0:
            raise ProjectWithoutTaskRuns
