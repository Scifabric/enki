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

import json
import pbclient
from exceptions import Error, PyBossaServerNoKeysetPagination

class ServerTaskRunsLoader(object):

    def __init__(self, project_id, tasks, all=0):
        self.project_id = project_id
        self.tasks = tasks
        self.all = all

    def check_errors(self, data):
        """Check for errors on data payload."""

        if (type(data) == dict and 'status' in data.keys()
            and data['status'] == 'failed'):
            if data.get('exception_msg') and 'last_id' in data.get('exception_msg'):
                raise PyBossaServerNoKeysetPagination
            else:
                raise Error(data)
        return False

    def load(self):
        task_runs = {}

        for t in self.tasks:
            limit = 100
            task_runs[t.id] = []
            taskruns = pbclient.find_taskruns(project_id=self.project_id,
                                              task_id=t.id,
                                              limit=limit,
                                              offset=0,
                                              all=self.all)
            while(len(taskruns) != 0):
                self.check_errors(taskruns)
                task_runs[t.id] += taskruns
                last_id = taskruns[-1].id
                taskruns = pbclient.find_taskruns(
                    project_id=self.project_id,
                    task_id=t.id,
                    limit=limit,
                    last_id=last_id,
                    all=self.all)
        return (task_runs, None)


class JsonTaskRunsLoader(object):

    def __init__(self, project_id, tasks, json_file):
        self.project_id = project_id
        self.tasks = tasks
        self.json_file = json_file

    def load(self):
        self.task_runs = {}
        self.task_runs_file = []

        self._load_from_json()
        self._group_json_task_runs_by_task_id()
        return (self.task_runs, self.task_runs_file)

    def _load_from_json(self):
        json_file_data = open(self.json_file).read()
        file_task_runs = json.loads(json_file_data)
        for tr in file_task_runs:
            self.task_runs_file.append(pbclient.TaskRun(tr))

    def _group_json_task_runs_by_task_id(self):
        for t in self.tasks:
            self.task_runs[t.id] = [tr for tr in self.task_runs_file
                                    if (tr.task_id == t.id
                                    and tr.project_id == self.project_id)]


def create_task_runs_loader(project_id, tasks, json_file, all=0):
    if json_file is not None:
        return JsonTaskRunsLoader(project_id, tasks, json_file)
    return ServerTaskRunsLoader(project_id, tasks, all)
