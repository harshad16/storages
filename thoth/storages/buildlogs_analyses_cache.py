#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Harshad Reddy Nalla
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Adapter for retrieving and storing hashes for fast buildlog lookups."""

from .ceph_cache import CephCache


class BuildLogsAnalysesCacheStore(CephCache):
    """Adapter for retrieving and storing hashes for fast buildlog lookups.

    This adapter is used to store simple files on Ceph so that there can be quickly checked whether the given buildlog
    was analyzed based in its SHA and which analysis corresponds to the analyzed buildlogs.
    """

    RESULT_TYPE = "buildlogs-analysis-cache"
