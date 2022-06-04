#!/usr/bin/python
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

# set lite model
cat_model_file = '/var/www/html/joomla/neuralnetworks/tf_lite/fhi360_small_lite/1.0/fhi360_small_1_21.tflite'
conc_model_file = '/var/www/html/joomla/neuralnetworks/tf_lite/fhi360_conc_large_lite/1.0/fhi360_conc_large_1_21.tflite'

# cat_labels = ['Albendazole','Amoxicillin','Ampicillin','Azithromycin','Benzyl','Penicillin','Ceftriaxone','Chloroquine','Ciprofloxacin','Doxycycline','Epinephrine','Ethambutol','Ferrous,Sulfate','Hydroxychloroquine','Isoniazid','Promethazine','Hydrochloride','Pyrazinamide','Rifampicin','RIPE','Sulfamethoxazole','Tetracycline','Distractor']
# conc_labels = [100,80,50,20]

# pls
coefficients_file = "/var/www/html/joomla/neuralnetworks/pls/fhi360_concentration/1.0/pls_fhi360_conc_coefficients.csv"

#### Load PLS coefficients
def get_pls_coeff(coefficients_file):
    coeff = {}
    with open(coefficients_file) as csvcoeffs:
        csvcoeffreader = csv.reader(csvcoeffs)
        #i=0
        for row in csvcoeffreader:
            elmts = []
            for j in range(1,len(row)):
                elmts.append(float(row[j]))
            coeff[row[0]] = elmts
    return coeff

#### PLS version of concentration
def get_pls_quantity(file_url, coeff, drug):
    # grab image from server
    urllib.request.urlretrieve(url + file_url, dest)

    img = cv.imread(dest)
    #print("OK",row[5],row[9])
        # get pixel analysis
    f = {}
    f = regionRoutine.fullRoutine(img, regionRoutine.intFind.findMaxIntensitiesFiltered, f, True, 10)

    # drug?
    # continue if no coefficients
    if drug not in coeff:
        return 0.

    drug_coeff = coeff[drug] #coeff['amoxicillin'] #

    # start with offst
    pls_concentration = drug_coeff[0]

    coeff_index = 1

    for letter in ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
        for region in range(10):
            for color_letter in ['R', 'G', 'B']:
                pixval = f[letter + str(region + 1) + '-' + color_letter]
                pls_concentration += float(pixval) * drug_coeff[coeff_index]
                coeff_index += 1

    return pls_concentration

#### NN version of concentration
def get_nn_quantity(file_url, model_file):
    # fixed pads data
    url = 'http://pad.crc.nd.edu'
    dest = './temp.png'

    # grab image from server
    urllib.request.urlretrieve(url + file_url, dest)

    # Load png file using the PIL library
    img = PIL.Image.open(dest)

    #crop out active area
    img = img.crop((71, 359, 71+636, 359+490))
 
    # Load the TFLite model and allocate tensors.
    interpreter =  tf.contrib.lite.Interpreter(model_path=model_file)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    HEIGHT_INPUT, WIDTH_INPUT, DEPTH = input_details[0]["shape"][1:]
    print("input", input_details[0], output_details) #["shape"], HEIGHT_INPUT)

    # resize
    img = img.resize((HEIGHT_INPUT,WIDTH_INPUT), PIL.Image.ANTIALIAS)

    #reshape the image as numpy
    im = np.asarray(img).flatten().reshape(1, HEIGHT_INPUT, WIDTH_INPUT, DEPTH).astype(np.float32)

    #print("shape/type:", im.shape, im.dtype)
    # input_shape = input_details[0]['shape']
    # input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], im)

    # predict
    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # get labels
    with ZipFile(model_file, 'r') as zipObject:
        zipObject.extract("labels.txt", './')
        with open("labels.txt") as f:
            labels = f.readlines()
    #print("disp",labels)

    concentration = labels[np.argmax(output_data[0])]
    confidence = output_data[0][np.argmax(output_data[0])]

 
    return concentration[:-1], float(confidence)

# get coeff file for pls
coeff = get_pls_coeff(coefficients_file)

# do analysis
print(get_nn_quantity("/var/www/html/joomla/images/padimages/api/processed/Ampicillin-12LanePADKenya2015-1-132184838.processed.png", cat_model_file))

# # setup query
# QUERY1 = 'SELECT `sample_id`,`notes`,`id`,`processed_file_location` FROM `card` WHERE `category`="FHI2022" AND `notes` LIKE "%Predicted drug = %" AND `notes` NOT LIKE "%Notes version%"'
# # AND `notes` LIKE "%(pls%" 

# #get database credentials
# with open('credentials.txt') as f:
#     line = f.readline()
#     split = line.split(",")
# f.close()

# #open database
# db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                      user=split[0], # your username
#                       passwd=split[1], # your password
#                       db="pad") # name of the data base

# # you must create a Cursor object. It will let
# #  you execute all the queries you need
# cur = db.cursor()

# # get list of samples
# cur.execute(QUERY1)

# count = 0

# doBreak = True

# # loop through CSV
# # loop
# for row in cur.fetchall() :
#     #print(row[1])
#     count += 1
#     notes_split = row[1].split(',')
#     pred = notes_split[0][17:].split('(')
#     pred_drug = pred[0].strip()
#     pred_conf = pred[1][:-1]
#     quant = notes_split[1].strip()
#     quant_nn = notes_split[2].strip()[:-1]
#     quant_pls = notes_split[3][5:-2]
#     #print("4", notes_split[4])
#     #print("5", notes_split[5])
#     if quant_pls != "":
#         other = notes_split[5].split('.')
#     else:
#         other = notes_split[4].split('.')
#     safe = other[0].strip()[10:]
#     user = (other[1].strip())[6:]
#     nn = (other[2].strip())[12:]

#     #print(pred_drug, pred_conf, quant, quant_nn, quant_pls, safe, user, nn)
#     json_string = {}
#     json_string["Predicted drug"] = pred_drug
#     json_string["User"] = user
#     json_string["App type"] = "Android"
#     if quant_nn !="":
#         json_string["Quantity NN"] = float(quant_nn)
#     else:
#         json_string["Quantity NN"] = get_nn_quantity(row[3])
#     json_string["Prediction score"] = float(pred_conf)
#     if quant_pls != "":
#         json_string["Quantity PLS"] = float(quant_pls)
#     else:
#         json_string["Quantity PLS"] = round(get_pls_quantity(row[3], coeff, pred_drug.lower()), 1)
#     json_string["Notes version"] = 0
#     json_string["Neural net"] = nn
#     json_string["Notes"] = ""

#     QUERY1 =  'UPDATE `card` SET `notes` = \'%s\' WHERE `id`=%s' % \
#             (json.dumps(json_string), row[2])

#     print(QUERY1)

#     #cur.execute(QUERY1)

#     # commit your changes
#     #db.commit()
#     #break

    
# print("Count",count)

# # Close all cursors
# cur.close()
# # Close all databases
# db.close()
