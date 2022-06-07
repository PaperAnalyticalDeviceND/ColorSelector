#!/usr/bin/python
from urllib.parse import DefragResultBytes
import MySQLdb
from PIL import Image, ImageEnhance, ImageStat
import json
import MySQLdb
import numpy as np
import tensorflow as tf
from tensorflow import keras
import PIL
import urllib.request
from zipfile import ZipFile
import regionRoutine
import cv2 as cv
import csv
import pad_analysis

# NN
methods = ['fhi360_small_lite','fhi360_conc_large_lite','pls_fhi360_conc']

# grab image other defines
url = 'http://pad.crc.nd.edu'
dest = './temp.png'

output_file = 'accuracy_conc_1b.csv'

# drug labels
cat_labels = ['Albendazole','Amoxicillin','Ampicillin','Azithromycin','Benzyl','Penicillin','Ceftriaxone','Chloroquine','Ciprofloxacin','Doxycycline','Epinephrine','Ethambutol','Ferrous,Sulfate','Hydroxychloroquine','Isoniazid','Promethazine','Hydrochloride','Pyrazinamide','Rifampicin','RIPE','Sulfamethoxazole','Tetracycline','Distractor']

# set lite model
cat_model_file = '/var/www/html/joomla/neuralnetworks/tf_lite/fhi360_small_lite/1.0/fhi360_small_1_21.tflite'
conc_model_file = '/var/www/html/joomla/neuralnetworks/tf_lite/fhi360_conc_large_lite/1.0/fhi360_conc_large_1_21.tflite'

# pls
coefficients_file = "/var/www/html/joomla/neuralnetworks/pls/fhi360_concentration/1.0/pls_fhi360_conc_coefficients.csv"

# create cat nn
cat_nn = pad_analysis.pad_neural_network(cat_model_file)

# create conc nn
conc_nn = pad_analysis.pad_neural_network(conc_model_file)

# create pls
pls_conc = pad_analysis.pls(coefficients_file)

# setup query
QUERY1 = 'SELECT `id`,`date_of_creation`,`notes`,`processed_file_location` FROM `card` WHERE `category`="FHI2022"' 

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

# get list of samples
cur.execute(QUERY1)


count = 0

doBreak = True

# loop
for row in cur.fetchall() :
    #print(row[0])
    count += 1

    # grab image from server
    urllib.request.urlretrieve(url + row[3], dest)

    # do analysis
    pred_drug, conf = cat_nn.catagorize(dest)

    nn_concentration, conc_conf = conc_nn.catagorize(dest)

    pls_concentration = pls_conc.quantity(dest, pred_drug)

    # arrays
    results = [pred_drug, nn_concentration, '{0:.2f}'.format(pls_concentration)]
    confs = [conf, conc_conf, 1.0]

    # get notes text
    notes_json = json.loads(row[2])

    # get data
    app_device_type = notes_json["App type"]
    #print(count,"Device", app_device_type, "NN cat", row[0], pred_drug, conf,"PLS", pls_concentration, "NN conc", nn_concentration, "Db", row[2])

    # cal_nn = notes_json["Neural net"]
    # cal_result = notes_json["Predicted drug"]
    # cal_confidence = notes_json["Prediction score"]

    # pls_result = notes_json["Quantity PLS"]

    # conc_result = notes_json["Quantity NN"]

    # print(device_type, cal_nn, cal_result, cal_confidence, pls_result, conc_result)
    # create query

    for i in range(3):
        QUERY2 = 'INSERT INTO analysis(`id`, `device_type`, `method`, `version`, `result`, `confidence`) VALUES (%d,%s,%s,%s,%s,%.3f)' % \
            (row[0], "\""+app_device_type+"\"", "\""+methods[i]+"\"", "\"1.0\"", "\""+results[i]+"\"", confs[i])

        print(QUERY2)

        try:
            # execute query
            cur.execute(QUERY2)

            # commit your changes
            db.commit()

            print("Inserted", QUERY2)
        except MySQLdb.IntegrityError:
            print("Could not insert", QUERY2)

    # if count > 1:
    #     break

#
# Close all cursors
cur.close()
# Close all databases
db.close()
