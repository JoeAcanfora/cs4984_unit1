#!/usr/bin/env python2

""" 
Reducer
"""

import sys

current_length = None
current_count = 0
length = None

for line in sys.stdin:
    line = line.strip()
    length, count = line.split('\t', 1)

    try:
        count = int(count)
        length = int(length)
    except ValueError:
        continue

    if current_length == length:
        current_count += count
    else:
        if current_length:
            print("{0}\t{1}".format(current_length, current_count))
        current_count = count
        current_length = length

if current_length == length:
    print("{0}\t{1}".format(current_length, current_count))
