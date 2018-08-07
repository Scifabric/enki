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


class ServerTasksLoader(object):

    def __init__(self, project_id, task_id=None, state='completed', all=0):
        self.query = self._build_query(project_id, task_id, state, all)

    def load(self):
        self.tasks = pbclient.find_tasks(**self.query)
        last_fetched_tasks = self.tasks
        del self.query['offset']
        while self._tasks_not_exhausted(last_fetched_tasks):
            self.query['last_id'] = last_fetched_tasks[-1].id
            last_fetched_tasks = pbclient.find_tasks(**self.query)
            self.tasks += last_fetched_tasks
        return self.tasks

    def _build_query(self, project_id, task_id, state, all):
        if task_id is not None:
            query = dict(project_id=project_id,
                         id=task_id,
                         limit=1,
                         offset=0,
                         all=all)
        else:
            query = dict(project_id=project_id,
                         state=state,
                         limit=100,
                         offset=0,
                         all=all)
        return query

    def _tasks_not_exhausted(self, last_fetched_tasks):
        return (len(last_fetched_tasks) != 0
                and len(last_fetched_tasks) == self.query['limit']
                and self.query.get('id') is None)


class JsonTasksLoader(object):

    def __init__(self, json_file, project_id, task_id=None, state=None):
        self.json_file = json_file
        self.project_id = project_id
        self.task_id = task_id
        self.state = state

    def load(self):
        json_file_data = open(self.json_file).read()
        file_tasks = json.loads(json_file_data)
        if self.task_id is None:
            return [pbclient.Task(t) for t in file_tasks
                    if (not self.project_id or self.project_id == t['project_id'])
                    and (not self.state or self.state == t['state'])]
        return [pbclient.Task(t) for t in file_tasks if t['id'] == self.task_id]


def create_tasks_loader(project_id, task_id, state, json_file, all=0):
    if json_file is not None:
        return JsonTasksLoader(json_file, project_id, task_id, state)
    return ServerTasksLoader(project_id, task_id, state, all)
