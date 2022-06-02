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

# defines
url = 'http://pad.crc.nd.edu'
dest = './temp.png'
coefficients_file = "pls_coefficients_ios.csv" #"PLS_COEFS_LAST_10_REG_RGB_FULL.csv" #"pls_coefficients.csv"
# PLS_COEFS_FIRST_10_REG_RGB_FULL.csv, PLS_COEFS_LAST_10_REG_RGB_FULL.csv, PLS_COEFS_MID_10_REG_RGB_FULL.csv
output_file = 'conc_05_31_2022notes.csv'
pad_card_list_file = "FHIwPics_05_31_2022.csv" #"FHIwPics.csv"

##################################################
#### test calculation ############################
##################################################
#img = cv.imread('../cards/40314.png')
#cv.imshow("img", img)
#cv.waitKey()


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
    # if i==0:
    #   print(row)
    #   i = 1
    #   print(len(elmts),elmts)

with open(output_file,'w') as myFile:

  # loop through CSV
  with open(pad_card_list_file, 'r', encoding='utf-8', errors='ignore') as csvsamples:
    csvsamplereader = csv.reader(csvsamples)
    for row in csvsamplereader:
      #print("Error",row[5],row[9])
      if 'iOS app.' not in row[3]: # or row[9] == '':
        continue
      #time.sleep(1)
      try:
        urllib.request.urlretrieve(url + row[5], dest)
        #time.sleep(1)
        img = cv.imread(dest)
        #print("OK",row[5],row[9])
          # get pixel analysis

        f = regionRoutine.fullRoutine(img, regionRoutine.intFind.findMaxIntensitiesFiltered, f, True, 10)

        # drug?
        #if row[9] == '':
        drug = row[3].split('.')[0].lower() #row[9].lower()

        if drug not in coeff:
          print("Drug not in notes", drug, row[9])
          drug = row[9].lower()

        drug_coeff = coeff[drug] #coeff['amoxicillin'] #

        # start with offst
        concentration = drug_coeff[0]

        coeff_index = 1

        for letter in ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
          for region in range(10):
            for color_letter in ['R', 'G', 'B']:
              pixval = f[letter + str(region + 1) + '-' + color_letter]
              concentration += float(pixval) * drug_coeff[coeff_index]
              coeff_index += 1

        # for f_elt in f:
        #   #print(f_elt)
        #   concentration += float(f[f_elt]) * drug_coeff[coeff_index]
        #   coeff_index += 1

        print("Drug/Concentration:",drug, concentration, row[10], row[3])#, row[5])
        myFile.write(row[0] + ',' + row[1] + ',' + drug + ',' + str(float(int(concentration))) + ',' + row[10] + ',(' + row[3].replace(',', ';') + ')\n')

      except Exception as e:
        print("Error",e, row[5],row[9])
        myFile.write(row[0] + ',' + row[1] + ',' + row[9] + ',' + 'PLS,' + row[10] + ',' + row[3] + '\n')

myFile.close()
      



