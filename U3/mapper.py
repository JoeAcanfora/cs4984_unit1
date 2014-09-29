#!/usr/bin/env python2

"""
Mapper

takes each line as a filename,
hashes filename to a number mod # reducers
print hash and filename
"""

import sys

for line in sys.stdin:
	line = line.strip()
	value = hash(line)%9
	print '%s\t%s' % (value, line)



