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
coefficients_file = "pls_coefficients.csv"
output_file = 'conc.csv'
pad_card_list_file = "FHIwPics.csv"

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
  for row in csvcoeffreader:
    elmts = []
    for j in range(1,len(row) - 1):
      elmts.append(float(row[j]))
    coeff[row[0]] = elmts

with open(output_file,'w') as myFile:

  # loop through CSV
  with open(pad_card_list_file, 'r', encoding='utf-8', errors='ignore') as csvsamples:
    csvsamplereader = csv.reader(csvsamples)
    for row in csvsamplereader:
      #print("Error",row[5],row[9])
      #time.sleep(1)
      try:
        urllib.request.urlretrieve(url + row[5], dest)
        #time.sleep(1)
        img = cv.imread(dest)
        #print("OK",row[5],row[9])
          # get pixel analysis

        f = regionRoutine.fullRoutine(img, regionRoutine.intFind.findMaxIntensitiesFiltered, f, True, 10)

        # drug?
        drug = row[9]
        drug_coeff = coeff[drug]

        concentration = 0.0

        coeff_index = 0;

        for f_elt in f:
          #print(f[f_elt])
          concentration += float(f[f_elt]) * drug_coeff[coeff_index]
          coeff_index += 1

        print("Drug/Concentration:",drug,concentration, row[10])
        myFile.write(row[0] + ',' + row[1] + ',' + drug + ',' + str(float(int(concentration)) / 100) + ',' + row[10] + '\n')

      except Exception as e:
        print("Error",e, row[5],row[9])
        myFile.write(row[0] + ',' + row[1] + ',' + drug + ',' + '-1.0,' + row[10] + '\n')

myFile.close()
      



