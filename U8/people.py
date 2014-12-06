#!/usr/bin/env python

import re
import sys
from numpy import median

regex_num = "((\d,?)+(\s+[a-z]illions?)?)"


def find_num(text, keywords):
    # find things that say "X missing" with 5 words possibly in between
    keywords = "(" + "|".join(keywords) + ")"
    matches = re.findall(
            "(" + regex_num + "\s+([a-zA-Z]+\s+){0,5}" + keywords + ")",
            text, flags=re.IGNORECASE)

    if len(matches) > 0:
        nums = [match[1].replace(",", "") for match in matches]

        # return the median
        return nums

    else:
        return None

 
def find_missing(text):
    return find_num(text, ["missing"])


def find_injured(text):
    return find_num(text, ["injured", "harmed"])


def find_killed(text):
    return find_num(text, 
            [   "killed", 
                "dea(d|ths)", 
                "bod(y|ies)",
                "casualt(ies|y)",
                "fatalit(ies|y)"    ])


def find_relocated(text):
    return find_num(text, [ "affect(ed|s)?", ])


if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        text = file.read()
        print("Missing: " + str(find_missing(text)))
        print("injured: " + str(find_injured(text)))
        print("killed: " + str(find_killed(text)))
        print("relocated: " + str(find_relocated(text)))
