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
"""Package to test Enki errors package."""
from enki.exceptions import check_errors
from enki.exceptions import Error, PyBossaServerNoKeysetPagination
from base import TestEnki
from nose.tools import raises


class TestErrors(TestEnki):
    @raises(PyBossaServerNoKeysetPagination)
    def test_keyset_pagination_works(self):
        """Test keyset error pagination works."""
        data = dict(status='failed', exception_msg='last_id')
        check_errors(data)

    def test_check_errors_works(self):
        """Test check_errors returns False when no error."""
        data = dict(status='failed', exception_msg='nothing')
        assert check_errors(data) is False

    @raises(Error)
    def test_check_generic_error_works(self):
        """Test check_errors raises Error."""
        data = dict(status='failed')
        check_errors(data)

    def test_check_errors_not_json_works(self):
        """Test check_errors only works for dicts."""
        data = [dict(status='failed')]
        print type(data)
        assert check_errors(data) is False, type(data)
