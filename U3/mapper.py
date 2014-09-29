#!/usr/bin/env python2

"""
Mapper

takes each line as a filename,
hashes filename to a number mod # reducers
print hash and filename
"""

import sys
import zipimport


try:
    importer = zipimport.zipimporter('nltk.mod')
    nltk = importer.load_module("nltk")
    nltk.data.path += ["./nltkData/"]
except zipimport.ZipImportError:
    import nltk

sys.path.append("..")
import TextUtils as tu

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize import sent_tokenize

from cPickle import load


