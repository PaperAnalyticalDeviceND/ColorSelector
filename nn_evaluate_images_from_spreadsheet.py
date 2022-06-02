# imports
import numpy as np
import tensorflow as tf
from tensorflow import keras
import PIL

import cv2 as cv
# import numpy as np
# import fileManagement as fm
# import intensityFind as intFind
# import pixelProcessing as px
# import pandas as pd
# import os
import csv
import urllib.request
# import warnings
# import math
# from datetime import datetime
# import time
# import regionRoutine

# defines
url = 'http://pad.crc.nd.edu'
dest = './temp.png'
#coefficients_file = "PLS_COEFS_LAST_10_REG_RGB_FULL.csv" #"pls_coefficients.csv"
# PLS_COEFS_FIRST_10_REG_RGB_FULL.csv, PLS_COEFS_LAST_10_REG_RGB_FULL.csv, PLS_COEFS_MID_10_REG_RGB_FULL.csv
output_file = 'conc_NN.csv'
pad_card_list_file = "FHIwPics_05_31_2022.csv"

# Training Image Set properties
IMG_SHAPE = (227, 227,3)
HEIGHT_INPUT, WIDTH_INPUT, DEPTH = IMG_SHAPE
NUM_CHANNELS = DEPTH; 
NUM_CLASSES = 4

# set lite model
model_file = '/var/www/html/joomla/neuralnetworks/tf_lite/fhi360_conc_large_lite/1.0/fhi360_conc_large_1_21.tflite'

conc = [100,80,50,20]

##################################################
#### test calculation ############################
##################################################
#img = cv.imread('../cards/40314.png')
#cv.imshow("img", img)
#cv.waitKey()


#f = {}

# get coeff file
#coeff = {}
# with open(coefficients_file) as csvcoeffs:
#   csvcoeffreader = csv.reader(csvcoeffs)
#   i=0
#   for row in csvcoeffreader:
#     elmts = []
#     for j in range(1,len(row)):
#       elmts.append(float(row[j]))
#     coeff[row[0]] = elmts
#     # if i==0:
#     #   print(row)
#     #   i = 1
#     #   print(len(elmts),elmts)

with open(output_file,'w') as myFile:

  # loop through CSV
  with open(pad_card_list_file, 'r', encoding='utf-8', errors='ignore') as csvsamples:
    csvsamplereader = csv.reader(csvsamples)
    for row in csvsamplereader:
      #print("Error",row[5],row[9])
      if 'iOS app.' not in row[3]: # or row[9] == '':
        continue

      drug = row[9]

      #time.sleep(1)
      try:
        urllib.request.urlretrieve(url + row[5], dest)
        #time.sleep(1)
        #img = cv.imread(dest)
        #print("OK",row[5],row[9])
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
        #print("Result:", conc[np.argmax(output_data[0])])

        print("Drug/Concentration:", drug, concentration, row[10])
        myFile.write(row[0] + ',' + row[1] + ',' + drug + ',' + str(float(int(concentration))) + ',' + row[10] + '\n')

      except Exception as e:
        print("Error",e, row[5],row[9])
        myFile.write(row[0] + ',' + row[1] + ',' + drug + ',' + '-1.0,' + row[10] + '\n')
      #break

myFile.close()
      



