"""
Uses serialized sklearn models to make predictions about text.
"""

import time

import sys
import os

import re

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

import csv
import json
import colorama

from sklearn.externals import joblib
from lib.analyzers import *

import redis
from dfitools import RedisCsvChannel as Rcc

colorama.init(autoreset = True)

# Config ###########################

config = json.load(sys.stdin)
plFile = config['Path to pickle']
chunksize = config['chunksize']
rconf = config['redis']

tgtCol = 'body'

# Redis Stuff ######################

r = redis.Redis(host = rconf['hostname'],
                port = rconf['port'],
                db = rconf['db'])

rcc = Rcc.RedisCsvChannel(r,rconf['listkey'],chunksize)
tgtIndex = rcc.header.index(tgtCol)

# Load the pipeline ################

try:
    pl = joblib.load(plFile)
except AttributeError as e:
    print(e)
    print(colorama.Fore.RED + 'Loading model failed;')
    print(colorama.Fore.RED + 'dependencies not met?')
    a,b = re.findall('\'[^\']+\'',string = str(e))
    print(colorama.Fore.RED + b + ' not found in ' + a)
    sys.exit(1)

# Classification ###################

m1 = time.time()

rcc.appendCol('prediction')

while True: 
    ch = rcc.getChunk()
    if ch:
        predictions = pl.predict([row[tgtIndex] for row in ch])
        for i,p in enumerate(predictions):
            ch[i].append(p)
        rcc.writeChunk(ch) 

    else:
        break

rcc.commit(label = True)
m2 = time.time()

print((colorama.Fore.BLUE + 'Time elapsed: ' + str(m2 - m1) + ' seconds'))

