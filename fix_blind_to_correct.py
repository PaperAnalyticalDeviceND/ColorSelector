#!/usr/bin/python
import datetime, os
import sys
import subprocess
import MySQLdb
import getopt
from PIL import Image, ImageEnhance, ImageStat
import random
import math

# setup query
QUERY1 = 'SELECT `id`,`sample_actual`,`quantity_actual` FROM `double_blind` WHERE `project`="FHI2022" AND (`sample_name`<>`sample_actual` OR `quantity`<>`quantity_actual`)'

#get database credentials
with open('credentials.txt') as f:
    line = f.readline()
    split = line.split(",")
f.close()

#open database
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user=split[0], # your username
                      passwd=split[1], # your password
                      db="pad") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
cur2 = db.cursor()
cur3 = db.cursor()

# get list of samples
cur.execute(QUERY1)

count = 0

doBreak = True

# loop
for row in cur.fetchall() :
    count += 1

    print(row[0], row[1], row[2])
    QUERY2 = 'SELECT `id`,`sample_name`,`quantity` FROM `card` WHERE `id`=%s'  % \
                    (row[0])
    cur2.execute(QUERY2)
    for row2 in cur2.fetchall() :
        print(row2[1], row2[2])

        actual_id = row[1].strip()

        # strip talc or lactose
        if 'talc' in actual_id or 'lactose' in actual_id:
            actual_id = actual_id.split('+')[0].strip()
        

        # remove + if starch
        if 'starch' in actual_id:
            actual_id = actual_id.replace('+ ', '').replace('starch', 'Starch')

        if 'blank' in actual_id:
            actual_id = 'Blank'

        if row[1] != row2[1] or row[2] != row2[2]:
            print("Need to update", row2[1], "to", row[1], "or", row2[2], "to", row[2])

            QUERY3 =  'UPDATE `card` SET `sample_name` = "%s", `quantity`=%s  WHERE `id`=%s' % \
                            (actual_id, row[2], row[0])
            print(QUERY3)
            cur3.execute(QUERY3)

            # commit your changes
            db.commit()

            # break if test
            doBreak = True

    # if doBreak:
    #     break
    # if count > 1:
    #     break
    
print("Count",count)
# Close all cursors
cur.close()
# Close all databases
db.close()
