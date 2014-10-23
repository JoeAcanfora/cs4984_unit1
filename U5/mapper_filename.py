#!/usr/bin/env python2

"""
Mapper

takes each line as a filename,
hashes filename to a number mod # reducers
print hash and filename
"""

import sys
import os.path

for line in sys.stdin:
    filename = line.strip()
    if os.path.exists(filename):
        value = hash(filename) % 100
        print '%s\t%s' % (value, filename)
