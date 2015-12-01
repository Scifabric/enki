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
This package contains a set of Exceptions for Enki.

The module exports:
    * Error: a generic class for the exceptions
    * ProjectNotFound: an exception for not found projects
    * ProjectError: an exception for a PyBossa project object not created

"""



class Error(Exception):

    """Base class for Enki errors."""

    pass


class ProjectNotFound(Error):

    """Exception raised for PyBossa project not found."""

    def __init__(self, value):
        """Init method."""
        self.value = value
        self.msg = " short_name: %s not found" % self.value

    def __str__(self):
        """String representation."""
        print self.msg  # pragma: no cover


class ProjectError(Error):

    """Exception raised for PyBossa project object not created."""

    def __init__(self):
        """Init method."""
        self.msg = " object not created"

    def __str__(self):  # pragma: no cover
        """String representation."""
        print self.msg


class ProjectWithoutTasks(Error):

    """Exception raised for PyBossa project without tasks."""

    def __init__(self):
        """Init method."""
        self.msg = " this project does not have tasks"

    def __str__(self):
        """String representation."""
        print self.msg  # pragma: no cover


class ProjectWithoutTaskRuns(Error):

    """Exception raised for PyBossa project without task runs."""

    def __init__(self):
        """Init method."""
        self.msg = " this project does not have task runs"

    def __str__(self):
        """String representation."""
        print self.msg  # pragma: no cover


class PyBossaServerNoKeysetPagination(Error):

    """Exception raised for PyBossa server when no keyset pagination."""

    def __init__(self):
        """Init method."""
        self.msg = " PyBossa server does not support keyset pagination. \
                     Upgrade PyBossa server to version v1.2.0"

    def __str__(self):
        """String representation."""
        print self.msg  # pragma: no cover
