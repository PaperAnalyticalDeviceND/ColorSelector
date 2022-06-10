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
import math

#### PLS version of concentration
class pls:
    def __init__(self, coefficients_file):
        try:
            # load coeffs
            self.coeff = {}
            with open(coefficients_file) as csvcoeffs:
                csvcoeffreader = csv.reader(csvcoeffs)
                #i=0
                for row in csvcoeffreader:
                    elmts = []
                    for j in range(1,len(row)):
                        elmts.append(float(row[j]))
                    self.coeff[row[0]] = elmts
        except Exception as e:
            print("Error",e, "loading pls coefficients", coefficients_file)

    def quantity(self, in_file, drug):
        try:
            # grab image
            img = cv.imread(in_file)

            # pls dictionary
            f = {}
            f = regionRoutine.fullRoutine(img, regionRoutine.intFind.findMaxIntensitiesFiltered, f, True, 10)

            # drug?
            # continue if no coefficients
            if drug.lower() not in self.coeff:
                return 0.

            drug_coeff = self.coeff[drug.lower()] #coeff['amoxicillin'] #

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
        except Exception as e:
            print("Error",e, "pls analyzing image", in_file, "with", drug)
            return -1.

#### NN version of concentration
class pad_neural_network:
    def __init__(self, model_file):
        try:
            # Load the TFLite model and allocate tensors.
            self.interpreter =  tf.contrib.lite.Interpreter(model_path=model_file)
            self.interpreter.allocate_tensors()

            # get labels
            with ZipFile(model_file, 'r') as zipObject:
                zipObject.extract("labels.txt", './')
                with open("labels.txt") as f:
                    self.labels = f.readlines()

            # get sizes
            # Get input and output tensors.
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.HEIGHT_INPUT, self.WIDTH_INPUT, self.DEPTH = self.input_details[0]["shape"][1:]
            #print("input", self.input_details[0], self.output_details) #["shape"], HEIGHT_INPUT)
        except Exception as e:
            print("Error",e, "loading model", model_file)


    def catagorize(self, im_file):
        try:
            # Load png file using the PIL library
            img = PIL.Image.open(im_file)

            #crop out active area
            img = img.crop((71, 359, 71+636, 359+490))
        
            # resize
            img = img.resize((self.HEIGHT_INPUT,self.WIDTH_INPUT), PIL.Image.ANTIALIAS)

            #reshape the image as numpy
            im = np.asarray(img).flatten().reshape(1, self.HEIGHT_INPUT, self.WIDTH_INPUT, self.DEPTH).astype(np.float32)

            #print("shape/type:", im.shape, im.dtype)
            # input_shape = input_details[0]['shape']
            # input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
            self.interpreter.set_tensor(self.input_details[0]['index'], im)

            # predict
            self.interpreter.invoke()

            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            concentration = self.labels[np.argmax(output_data[0])]

            # softmax
            if np.sum(output_data[0]) < 0.99 or np.sum(output_data[0]) > 1.01:
                exps = np.exp(output_data[0])
                exps = exps/np.sum(exps)
                confidence = exps[np.argmax(output_data[0])]
            else: # alreasy softmax
                confidence = output_data[0][np.argmax(output_data[0])]

            return concentration[:-1], float(confidence)

        except Exception as e:
            print("Error",e, "catagorizing image", im_file)
            return "", -1.

