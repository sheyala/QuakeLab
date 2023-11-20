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

import shakelab.signals.metadata as slmd

# example using metadata for station CIMO of network OX;
# it has many channels and multiple working intervals  
# (corresponding to different instrumental responses)
#------------------------------------------------------------
# example file n.1: metadata for station OX.CIMO, in UTC time
file_in_utc = 'shakelab/signals/data/CIMO_UTC.xml'

# load all the information contained in input files at level 'response'
#----------------------------------------------------------------------
md_utc = slmd.Metadata(mdfile=file_in_utc, level='response')


# check that timezone handling was correct
#------------------------------------------------------------
# example file n.2: metadata for station OX.CIMO, in CET time
file_in_cet = 'shakelab/signals/data/CIMO_CET.xml'
md_cet = slmd.Metadata(mdfile=file_in_cet, level='response')
print(md_utc.data == md_cet.data)


# create new Metadata() objects using different selections:
#----------------------------------------------------------
# all available information for HHE channels
md_utc_HHE_all = md_utc.select('OX.CIMO..HHE')

# information for HHE channels, at a given time
time = '2019-10-08T18:30:00.000000Z'
md_utc_HHE_time = md_utc.select('OX.CIMO..HHE', time=time)

# information for HHE channels with locationcode 01 (if present)
md_utc_HHE_01 = md_utc.select('OX.CIMO.01.HHE')

# the same dictionary stored in md_utc_HHE_time.data can also be accessed using 
# select_nslc
md_utc_HHE_select = slmd.Metadata()
md_utc_HHE_select.data = slmd.select_nslc(md_utc.data, 'OX.CIMO..HHE', time=time)
print(md_utc_HHE_select.data == md_utc_HHE_time.data)

# to access the data at level 'channel' now we can use __getitem__
chan_info = md_utc_HHE_time['Channel']
print(chan_info)



##########

'2014-12-31T23:59:59.000000'
'2015-01-01T00:00:00.000000'
from shakelab.libutils.time import sec_to_date, Date
def test_date(dd):
    if not isinstance(dd, Date):
        dd = Date(dd)
    print(sec_to_date(dd.seconds))