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

import pandas


def create_task_run_data_frames(tasks, task_runs):
    task_runs_df = {}
    for task in tasks:
        task_runs_df[task.id] = create_data_frame(task_runs[task.id])
    return task_runs_df


def create_data_frame(item):
    data = [explode_info(tr) for tr in item]
    index = [tr.__dict__['data']['id'] for tr in item]
    return pandas.DataFrame(data, index)


def explode_info(item):
    item_data = item.__dict__['data']
    protected = item_data.keys()
    if type(item.info) == dict:
        keys = item_data['info'].keys()
        for k in keys:
            if k in protected:
                item_data["_" + k] = item_data['info'][k]
            else:
                item_data[k] = item_data['info'][k]
    return item_data
