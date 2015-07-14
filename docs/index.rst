.. enki documentation master file, created by
   sphinx-quickstart on Tue Oct 16 11:21:34 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to enki's documentation!
==========================================

This small library will help you to analyze your PyBossa_ projects results.

.. _PyBossa: http://dev.pybossa.com

Install
-------

You can install enki using **pip**, preferably while working in a 
`virtualenv <http://www.virtualenv.org/en/latest/index.html>`_::

    $ pip install enki

Usage
-----

Setup::

    >>> import enki

    # setup the server connection
    >>> e = enki.Enki(api_key='your-key', endpoint='http://server',
                      project_short_name='your-project-short-name')
    # Get all completed tasks and its associated task runs
    >>> e.get_all()

The previous command, loads all **completed** tasks and task runs into four variables:

 * **e.tasks** a list of tasks
 * **e.task_runs** a dictionary of task runs, where the keys are the
   project task IDs
 * **e.tasks_df** a Pandas_ list of data frames for the tasks
 * **e.task_runs_df** a Pandas_ dictionary of data frame for the task runs,
   where the keys are the project task IDs

Now that you have downloaded all the tasks and task runs, you can start
analyzing them using Pandas_::

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
    
.. _Pandas: http://pandas.pydata.org/

Enki explodes the task_run info field if it is a dictionary (a JSON
object). This will help you to analyze more easily for example, all the
keys of the object via Pandas_ statistical solutions. All you have to do is
to access the key and use Pandas_ methods.

Package overview
---------------

.. automodule:: enki
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
