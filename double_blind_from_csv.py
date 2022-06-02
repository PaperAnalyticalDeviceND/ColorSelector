 #!/usr/bin/python
import datetime, os
import sys
import subprocess
import MySQLdb
import getopt
from PIL import Image, ImageEnhance, ImageStat
import random
import math
import csv

# setup query
#QUERY1 = 'SELECT `id`,`sample_actual`,`quantity_actual` FROM `double_blind` WHERE `project`="FHI360_2021_blinded" AND (`sample_name`<>`sample_actual` OR `quantity`<>`quantity_actual`)'

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

# # get list of samples
# cur.execute(QUERY1)

count = 0
with open('Non_match','w') as myFile:
    # loop through CSV
    with open('FHI360_2022_Deliverable_Unblinded_PADs_conc.csv', 'r', encoding='utf-8', errors='ignore') as csvsamples:
        csvsamplereader = csv.reader(csvsamples)
        for row in csvsamplereader:
            count += 1
            # miss headers
            if count == 1:
                continue
            # if count > 2:
            #     break

            # handle sample id
            #print("CSV",row[5],row[4])

            # run query
            QUERY1 = 'SELECT `id`,`sample_name`,`user_name`,`category`,`quantity` FROM `card` WHERE `sample_id`=%d' % (int(row[5]))
            cur.execute(QUERY1)

            # get matching records
            for rowdb1 in cur.fetchall() :
                #print(rowdb1[0], rowdb1[1])
                # check sample names check
                if row[1].lower().strip() == rowdb1[1].lower() or rowdb1[1].lower() == '' or row[1].lower() == 'blank' or rowdb1[1].lower() == 'distractor':
                    #continue
                    # get actual identity
                    actual_id = row[3].strip()

                    # # strip talc or lactose
                    # if 'talc' in actual_id or 'lactose' in actual_id:
                    #     actual_id = actual_id.split(' ')[0]
                    
                    # # remove + if starch
                    # if 'starch' in actual_id:
                    #     actual_id = actual_id.replace('+ ', '').replace('starch', 'Starch')

                    #print(actual_id)

                    # create query
                    QUERY2 = 'INSERT INTO `double_blind` (`id`,`sample_id`,`sample_name`,`sample_actual`,`quantity`,`quantity_actual`,`user_name`,`test_id`,`project`) VALUES (%d,%d,%s,%s,%d,%d,%s,%s,%s)' % \
                        (int(rowdb1[0]), int(row[5]), "\""+rowdb1[1]+"\"", "\""+actual_id+"\"", int(rowdb1[4]), int(float(row[4]) * 100), "\""+rowdb1[2]+"\"", "\""+row[2]+"\"", "\""+rowdb1[3]+"\"")

                    print(QUERY2)

                    try:
                        # execute query
                        cur2.execute(QUERY2)

                        # commit your changes
                        db.commit()

                        print("Inserted", QUERY2)
                    except MySQLdb.IntegrityError:
                        print("Could not insert", QUERY2)
                    
                else:
                    print("No sample_name match","|"+row[1]+"|","|"+rowdb1[1]+"|")
                    myFile.write(row[5] + ',' + row[1] + ',' + rowdb1[1] + '\n')
                #break
            #break