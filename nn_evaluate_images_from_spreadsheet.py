# imports
import numpy as np
import tensorflow as tf
from tensorflow import keras
import PIL

import cv2 as cv
import numpy as np
import fileManagement as fm
import intensityFind as intFind
import pixelProcessing as px
import pandas as pd
import os
import csv
import urllib.request
import warnings
import math
from datetime import datetime
import time
import regionRoutine
import json
import MySQLdb

# defines
url = 'http://pad.crc.nd.edu'
dest = './temp.png'
coefficients_file = "pls_coefficients_ios.csv"
output_file = 'conc_NN_PLS_all_test2.csv'
pad_card_list_file = "FHIwPics_part.csv" #"FHIwPics_06_02_2022.csv"

# Training Image Set properties
IMG_SHAPE = (227, 227,3)
HEIGHT_INPUT, WIDTH_INPUT, DEPTH = IMG_SHAPE
NUM_CHANNELS = DEPTH; 
NUM_CLASSES = 4

# set lite model
model_file = '/var/www/html/joomla/neuralnetworks/tf_lite/fhi360_conc_large_lite/1.0/fhi360_conc_large_1_21.tflite'

conc = [100,80,50,20]

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

##################################################
#### test calculation ############################
##################################################

f = {}

# get coeff file
coeff = {}
with open(coefficients_file) as csvcoeffs:
  csvcoeffreader = csv.reader(csvcoeffs)
  i=0
  for row in csvcoeffreader:
    elmts = []
    for j in range(1,len(row)):
      elmts.append(float(row[j]))
    coeff[row[0]] = elmts

with open(output_file,'w') as myFile:

  # loop through CSV
  with open(pad_card_list_file, 'r', encoding='utf-8', errors='ignore') as csvsamples:
    csvsamplereader = csv.reader(csvsamples)
    for row in csvsamplereader:
      #print("Error",row[5],row[9])
      if 'iOS app.' not in row[3]: # or row[9] == '':
        continue

      # drug = row[9].lower()

      # # continue if no coefficients
      # if drug in coeff:
      #   continue

      # print(row[0], row[1])
      # #continue
      #### PLS version of concentration
      try:
        urllib.request.urlretrieve(url + row[5], dest)

        img = cv.imread(dest)
        #print("OK",row[5],row[9])
          # get pixel analysis

        f = regionRoutine.fullRoutine(img, regionRoutine.intFind.findMaxIntensitiesFiltered, f, True, 10)

        # drug?
        #if row[9] == '':
        # drug = row[3].split('.')[0].lower() #row[9].lower()

        # if drug not in coeff:
        #   print("Drug not in notes", drug, row[9])
        drug = row[9].lower()

        # continue if no coefficients
        if drug not in coeff:
          continue

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

      except Exception as e:
        print("Error",e, row[5],row[9])
        continue
      #drug = row[9]

      #### NN version of concentration
      try:
        # get pixel analysis
        #Load png file using the PIL library
        img = PIL.Image.open(dest)

        #crop out active area
        img = img.crop((71, 359, 71+636, 359+490))

        #resize
        img = img.resize((227,227), PIL.Image.ANTIALIAS)

        #reshape the image as numpy
        im = np.asarray(img).flatten().reshape(1, HEIGHT_INPUT, WIDTH_INPUT, DEPTH).astype(np.float32)
        #print("shape/type:", im.shape, im.dtype)


        # Load the TFLite model and allocate tensors.
        interpreter =  tf.contrib.lite.Interpreter(model_path=model_file)
        interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        #print("input", input_details[0])

        # Test the model on random input data.
        input_shape = input_details[0]['shape']
        input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
        interpreter.set_tensor(input_details[0]['index'], im)

        # predict
        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = interpreter.get_tensor(output_details[0]['index'])

        concentration = conc[np.argmax(output_data[0])]
        confidence = output_data[0][np.argmax(output_data[0])]
        #print("Result:", conc[np.argmax(output_data[0])])

        print("Drug/Concentrations:", drug, pls_concentration, concentration, row[10])
        myFile.write(row[0] + ',' + row[1] + ',' + drug + ',' + str(float(int(pls_concentration))) + ',' + str(float(int(concentration))) + ',' + row[10] + '\n')

      except Exception as e:
        print("Error",e, row[5],row[9])
        continue
        #myFile.write(row[0] + ',' + row[1] + ',' + drug + ',' + '-1.0,' + row[10] + '\n')

      #### Sort out notes
      notes_split = row[3].split('.')
      #print(row[0], row[1], "|", "|"+notes_split[0]+"|", notes_split[1], notes_split[2], "|"+notes_split[3][7:]+"|")

      json_string = {}
      json_string["Predicted drug"] = notes_split[0]
      json_string["User"] = notes_split[3][7:]
      json_string["App type"] = "iOS"
      json_string["Quantity NN"] = concentration
      json_string["Prediction score"] = round(float(confidence), 3)
      json_string["Quantity PLS"] = round(pls_concentration, 1)
      json_string["Notes version"] = 0
      json_string["Neural net"] = "fhi360_small_lite"
      json_string["Notes"] = ""

      QUERY1 =  'UPDATE `card` SET `notes` = \'%s\' WHERE `id`=%s' % \
                (json.dumps(json_string), row[1])

      print(row[1],QUERY1)

      cur.execute(QUERY1)

      # commit your changes
      db.commit()

      #break

myFile.close()
      



