# ****************************************************************************
#
# Copyright (C) 2019-2020, ShakeLab Developers.
# This file is part of ShakeLab.
#
# ShakeLab is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# ShakeLab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# ****************************************************************************
"""
Module for basic waveform analysis - metadata handling
"""

import numpy as np


class Stage():
    """
    Class for generic stage representation
    """
    def __init__(self, number, stage_gain, decimation, input_units, output_units):
        pass
        







class Metadata(object):
    """
    Representation of metadata for a single sid; might cover different 
    time periods.
    """
    def __init__(self, id):
        self.sid = id
        self.response = []

    def __len__(self):
        return len(self.response)

    def append(self, record, enforce=False):
        """
        """
        if record.head.sid != self.sid:
            assert ValueError('Record ID mismatching')

        if not self.record:
            self.record = [record]
        else:
            if not self.record[-1].append(record, enforce=enforce):
                self.record.append(record) 





class MetadataCollection():
    """
    """
    def __init__(self):
        self.metadata = []

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, id):
        """
        """
        if isinstance(id, str):
            return self.metadata[self._idx(id)]
        else:
            return self.metadata[id]

    def _idx(self, id):
        """
        """
        sid_list = self.sid
        if id in sid_list:
            return sid_list.index(id)
        else:
            print('Id not found.')
            return None

    @property
    def sid(self):
        """
        """
        return [metadata.sid for metadata in self.metadata]
