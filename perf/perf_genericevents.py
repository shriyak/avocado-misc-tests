#!/usr/bin/env python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
#
# Copyright: 2017 IBM
# Author: Athira Rajeev<atrajeev@linux.vnet.ibm.com>
# Author: Shriya Kulkarni <shriyak@linux.vnet.ibm.com>

import os
import re
from avocado import Test
from avocado import main


def generic_events(x):
    return {
        'cpu-cycles': "0x1e",
        'stalled-cycles-frontend': "0x100f8",
        'stalled-cycles-backend': "0x4000a",
        'instructions': "0x02",
        'branch-instructions': "0x10068",
        'branch-misses': "0x400f6",
        'cache-references': "0x100ee",
        'cache-misses': "0x3e054",
        'L1-dcache-load-misses': "0x3e054",
        'L1-dcache-loads': "0x100ee",
        'L1-dcache-prefetches': "0xd8b8",
        'L1-dcache-store-misses': "0x300f0",
        'L1-icache-load-misses': "0x200fd",
        'L1-icache-loads': "0x4080",
        'L1-icache-prefetches': "0x408e",
        'LLC-load-misses': "0x300fe",
        'LLC-loads': "0x4c042",
        'LLC-prefetches': "0x4e052",
        'LLC-store-misses': "0x17082",
        'LLC-stores': "0x17080",
        'branch-load-misses': "0x400f6",
        'branch-loads': "0x10068",
        'dTLB-load-misses': "0x300fc",
        'iTLB-load-misses': "0x400fc"
    }.get(x, 9)


class test_generic_events(Test):
    """
    This tests Display event codes for Generic HW (PMU) events.
    This test will read content of each file from
    /sys/bus/event_source/devices/cpu/events
    and compare the raw event code for each generic event
    """

    def test(self):
        nfail = 0
        dir = "/sys/bus/event_source/devices/cpu/events"
        os.chdir(dir)
        for file in os.listdir(dir):
            events_file = open(file, "r")
            event_code = events_file.readline()
            val = generic_events(file)
            raw_code = event_code.split('=', 2)[1].rstrip()
            if raw_code != val:
                nfail += 1
                self.warn('FAIL : Expected value is %s but got'
                          '%s' % (val, raw_code))
            self.log.info('FILE in %s is %s' % (dir, file))
            self.log.info('PASS : Expected value: %s and got'
                          '%s' % (val, raw_code))
        if nfail != 0:
            self.fail('Failed to verify generic PMU event codes')


if __name__ == "__main__":
    main()
