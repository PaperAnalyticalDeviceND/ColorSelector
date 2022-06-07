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

# creat pls
pls_conc = pad_analysis.pls(coefficients_file)

# setup query
QUERY1 = 'SELECT `sample_name`,`processed_file_location`,`quantity`,`id`,`sample_id`  FROM `card` WHERE `category`="FHI2022"' # AND `notes` LIKE "%Predicted drug = %" AND `notes` NOT LIKE "%Notes version%"'
# AND `notes` LIKE "%(pls%" 

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

# setup for loop
drug_correct = {}
drug_total = {}

for drug in cat_labels:
    drug_correct[drug.lower()] = 0
    drug_total[drug.lower()] = 0

# drug_correct['distractor'] = 0
# drug_total['distractor'] = 0

count = 0

doBreak = True

# loop through CSV
with open(output_file,'w') as myFile:
    # loop
    for row in cur.fetchall() :
        #print(row[0])
        count += 1

        # increment Drugs
        if row[0].lower() in drug_correct:
            drug_total[row[0].lower()] += 1
        else:
            continue
            #drug_total['distractor'] += 1

        # grab image from server
        urllib.request.urlretrieve(url + row[1], dest)

        # do analysis
        pred_drug, conf = cat_nn.catagorize(dest)
        #print("NN", row[0], pred_drug, conf,)

        if row[0].lower() == pred_drug.lower():
            if row[0].lower() in drug_correct:
                drug_correct[row[0].lower()] += 1
            # else:
            #     drug_correct['distractor'] += 1

        nn_concentration, conc_conf = conc_nn.catagorize(dest)

        pls_concentration = pls_conc.quantity(dest, pred_drug)
        print(count,"NN cat", row[0], pred_drug, conf,"PLS", pls_concentration, "NN conc", nn_concentration, "Db", row[2])

        # save info
        myFile.write(str(row[4]) + ',' + str(row[3]) + ',' + row[0] + ',' + pred_drug + ',' + str(conf) + ',' + str(row[2]) + ',' + str(nn_concentration) + ',' + str(pls_concentration) + '\n')

        # if count > 10:
        #     break

# calculate ratios
drug_ratio = {}

for drug in cat_labels:
    if drug_total[drug.lower()] != 0:
        drug_ratio[drug.lower()] = float(drug_correct[drug.lower()]) / float(drug_total[drug.lower()])
    else:
        drug_ratio[drug.lower()] = 0.

# if drug_total['distractor'] != 0:
#     drug_ratio['distractor'] = float(drug_correct['distractor']) / float(drug_total['distractor'])
# else:
#     drug_ratio['distractor'] = 0.

print("Count",count, drug_ratio)
print(drug_correct, drug_total)

myFile.close()

# Close all cursors
cur.close()
# Close all databases
db.close()
