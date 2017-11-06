# Dead simple Python package for analyzing PYBOSSA project's results
[![Build Status](https://travis-ci.org/Scifabric/enki.svg)](https://travis-ci.org/Scifabric/enki) [![Coverage Status](https://coveralls.io/repos/Scifabric/enki/badge.svg)](https://coveralls.io/r/Scifabric/enki)
[![PyPi Downloads Version](https://img.shields.io/pypi/v/enki.svg)](https://pypi.python.org/pypi/enki/)
[![PyPi Downloads Month](https://img.shields.io/pypi/dm/enki.svg)](https://pypi.python.org/pypi/enki/)

Makes it easy to statistically analyze [PYBOSSA](http://pybossa.com>) project results.

## Install

You can install enki using **pip**, preferably while working in a 
[virtualenv](http://www.virtualenv.org/en/latest/index.html):

```bash
    $ pip install enki
```

## Requirements

[PYBOSSA server](http://pybossa.com) >= v1.2.0.

## Usage

It is really simple:

```python
    >>> import enki

    # setup the server connection
    >>> e = enki.Enki(api_key='your-key', endpoint='http://server',
                      project_short_name='your-project-short-name')
    # Get all completed tasks and its associated task runs
    >>> e.get_all()
```

The previous command, loads all **completed** tasks and task runs into four variables:

 * **e.tasks** a list of tasks
 * **e.task_runs** a dictionary of task runs, where the keys are the
   project task IDs
 * **e.tasks_df** a [Pandas](http://pandas.pydata.org/) list of data frames for the tasks
 * **e.task_runs_df** a  [Pandas](http://pandas.pydata.org/) dictionary of data frame for the task runs,
   where the keys are the project task IDs

Now that you have downloaded all the tasks and task runs, you can start
analyzing them using Pandas_:

```python
    # For example, for a given task of your project:
    >>> task = e.tasks[0]
    # Let's analyze it (note: if the answer is a simple string like 'Yes' or 'No'):
    >>> e.task_runs_df[task.id]['info'].describe()
    count       1
    unique      1
    top       Yes
    freq        1
    dtype: object

    # Otherwise, if the answer in info is a dict: info = {'x': 32, 'y': 24}
    # Enki explodes the info field, using its keys (x, y) for new data frames:
    >>> e.task_runs_df[task.id]['x'].describe()
    count    100.000000
    mean     265.640000
    std        4.358945
    min      235.000000
    25%      264.000000
    50%      266.000000
    75%      268.000000
    max      278.000000
    dtype: float64
```
    
Enki explodes the task_run info field if it is a dictionary (a JSON
object). This will help you to analyze more easily for example, all the
keys of the object via [Pandas](http://pandas.pydata.org/) statistical solutions. All you have to do is
to access the key and use [Pandas](http://pandas.pydata.org/) methods.

**WARNING**: If a task or taskrun has inside the *info* field a key that is protected, it will be escaped.
For example, if exists task.info.id == 13, then, enki will escape it to **_id**. Enki will do it with all the
protected attributes of Tasks and TaskRuns.

**NOTE**: if you want to load partial results, you can do it. Instead of using e.get_all() method, use the following code:

```python
e.get_tasks(state='ongoing')
e.get_task_runs()
```
That will get the partial results. Then you can proceed with the analysis as before.

# Using PYBOSSA JSON files

PYBOSSA exports the tasks and task runs as ZIP files in JSON format. You can pass those files to Enki, and
avoid using the API for a faster analysis. If that's the case, download both files (task and task runs) and import them:

```python
    >>> import enki

    # setup the server connection
    >>> e = enki.Enki(api_key='your-key', endpoint='http://server',
                  project_short_name='your-project-short-name')
    # Get all completed tasks and its associated task runs
    e.get_tasks(json_file='path/to/your/tasks.json')
    e.get_task_runs(json_file='path/to/your/task_runs.json')
```

Then you can do the analysis as before. 

**NOTE**: If you want to anlayze a project from another person in the same server,
then you can use the all=1 parameter when creating the Enki object:

```python
    >>> import enki

    # setup the server connection
    >>> e = enki.Enki(api_key='your-key', endpoint='http://server',
                  project_short_name='your-project-short-name', all=1)
    # Get all completed tasks and its associated task runs
    e.get_all()
```
This will ensure that Enki will search across all projects in PYBOSSA.

# Contributing

Please, see [CONTRIBUTING file](CONTRIBUTING.md)

## Copyright
2016 Copyrigth [Scifabric LTD](http://scifabric.com).

## License

AGPLv3.0 see [COPYING](COPYING) file.
