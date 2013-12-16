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
"""
This package contains a set of Exceptions for Enki.

The module exports:
    * Error: a generic class for the exceptions
    * AppNotFound: an exception for not found applications
    * AppError: an exception for a PyBossa application object not created

"""


class Error(Exception):

    """Base class for Enki errors."""

    pass


class AppNotFound(Error):

    """Exception raised for PyBossa application not found."""

    def __init__(self, value):
        self.value = value
        self.msg = " short_name: %s not found" % self.value

    def __str__(self):
        print self.msg  # pragma: no cover


class AppError(Error):

    """Exception raised for PyBossa application object not created."""

    def __init__(self):
        self.msg = " object not created"

    def __str__(self):  # pragma: no cover
        print self.msg


class AppWithoutTasks(Error):

    """Exception raised for PyBossa application without tasks."""

    def __init__(self):
        self.msg = " this app does not have tasks"

    def __str__(self):
        print self.msg  # pragma: no cover


class AppWithoutTaskRuns(Error):

    """Exception raised for PyBossa application without task runs."""

    def __init__(self):
        self.msg = " this app does not have task runs"

    def __str__(self):
        print self.msg  # pragma: no cover
