import time
import sys
import csv
import json

import colorama

from sklearn.externals import joblib

import redis

from dfitools import RedisCsvChannel as Rcc

# * POWERFUL PICKLE * ##############
# Peder G. Landsverk - 2018 ########
# For use with DFI #################

"""
Loads a pickled pipeline
and uses it to predict outcome
using text in dat[tgtCol]
"""

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

pl = joblib.load(plFile)

# Classification ###################

m1 = time.time()

while True: 
    ch = rcc.getChunk()
    if ch == []:
        break
    else:
        predictions = pl.predict([row[tgtIndex] for row in ch])
        for i,p in enumerate(predictions):
            ch[i].append(p)
        rcc.writeChunk(ch) 


m2 = time.time()
print((colorama.Fore.BLUE + 'Time elapsed: ' + str(m2 - m1) + ' seconds'))

rcc.header.append('prediction')

# Data output ######################

rcc.commit()

