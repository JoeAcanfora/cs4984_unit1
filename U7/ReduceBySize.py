__author__ = 'joeacanfora'
import os
import re
import string

filedir = '/Users/joeacanfora/Desktop/Virginia Tech/Capstone/cs4984_unit1-master/U1/china_flood'


for file in os.listdir(filedir):
        statinfo = os.stat(filedir + '/' + file)
        if statinfo.st_size < 2 * 1024:
            os.remove(filedir + '/' + file)




