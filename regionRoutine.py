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

HORIZONTAL_BORDER = 12
VERTICAL_BORDER = 0
SAVE_DIR = './Data/'
REQS = {'ORIG_DIR':'Original_Images',
  'CSV_DIR':'CSV_Data',
  'PROC_DIR':'Cartoon_Images',
  'LOG':'log.txt',
  'MASTER':'PADData.csv'}

def regionGen(regions, region):
  start = 359
  totalLength = 273
  regionStart = start + math.floor(totalLength * (region/regions)) + VERTICAL_BORDER
  regionEnd = start + math.floor(totalLength * ((region+1)/regions)) - VERTICAL_BORDER
  return regionStart, regionEnd

'''
This is a major hack at this point. Eventually I could refactor it to work
nice and programatically, for now I'll revel in the hack.
'''
def fullRoutine_old(img, roiFunc, RGB=True, regions=3, display=False):
  imgC = img.copy()
  fImg = img.copy()
  rList = []
  gList = []
  bList = []
  imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
  if display:
    cv.imshow("in", imgC)
    cv.imshow("out", imgHSV[:,:,1])
    cv.waitKey()
  for lane in range(1,13):
    laneStart = 17 + (53*lane)+HORIZONTAL_BORDER
    laneEnd = 17 + (53*(lane+1))-HORIZONTAL_BORDER
    for region in range(regions):
      regionStart, regionEnd = regionGen(regions, region)
      roi = imgHSV[regionStart:regionEnd,laneStart:laneEnd,:]
      rgbROI = img[regionStart:regionEnd,laneStart:laneEnd,:]
      pixels = roiFunc(roi)
      r, g, b = px.avgPixels(pixels, rgbROI)
      l, a, blu = px.avgPixelsLAB(pixels, rgbROI)
      temp = np.zeros((regionEnd-regionStart,laneEnd-laneStart,3), dtype='uint8')
      #Switches between RGB and Lab
      if(RGB):
        rList.append(r)
        gList.append(g)
        bList.append(b)
      else:
        rList.append(l)
        gList.append(a)
        bList.append(blu)
      temp[:,:,0] = b
      temp[:,:,1] = g
      temp[:,:,2] = r
      outImg = imgC[regionStart:regionEnd,laneStart:laneEnd,:]
      for pixel in pixels:
        (y, x) = pixel
        #print(pixel)
        outImg = cv.circle(outImg, (x, y), 2, (255,0,0), 0)
        cv.imshow("pixels", outImg)
      fImg[regionStart:regionEnd,laneStart:laneEnd,:] = temp
      if display:
        print("lane %d region %d: %d, %d, %d" %(lane, region, r, g, b))
      cv.rectangle(imgC, (laneStart, regionStart), (laneEnd, regionEnd), (255,0,0))
      cv.imshow("in", imgC)
      cv.imshow("color swatch", temp)
      if display and cv.waitKey() & 0xFF == ord('q'):
        break
  if(RGB):
    data = {'B':bList,'G':gList,'R':rList}
    columns = ['R','G','B']
  else:
    data = {'b':bList,'a':gList,'L':rList}
    columns = ['L','a','b']
  index = []
  for letter in ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
    for region in range(regions):
      i = letter + " - Region " + str(region+1)
      index.append(i)
  if(pIndex is None):
    df = pd.DataFrame(data, columns = columns, index=index)
  else:
    buildData(data, pIndex)
  #df.to_csv(destination)
  cv.destroyAllWindows()
  return fImg, df

def fullRoutine(img, roiFunc, df, RGB=True, regions=3):
  letters = ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
  rList = []
  gList = []
  bList = []
  imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
  for lane in range(1,13):
    laneStart = 17 + (53*lane)+HORIZONTAL_BORDER
    laneEnd = 17 + (53*(lane+1))-HORIZONTAL_BORDER
    letter = letters[lane-1]
    for region in range(regions):
      regionStart, regionEnd = regionGen(regions, region)
      roi = imgHSV[regionStart:regionEnd,laneStart:laneEnd,:]
      rgbROI = img[regionStart:regionEnd,laneStart:laneEnd,:]
      pixels = roiFunc(roi)
      tempString = letter + str(region+1) + "-"
      #Switches between RGB and Lab
      if(RGB):
        r, g, b = px.avgPixels(pixels, rgbROI)
        df[tempString+'R'] = r
        df[tempString+'G'] = g
        df[tempString+'B'] = b
      else:
        l, a, blu = px.avgPixelsLAB(pixels, rgbROI)
        df[tempString+'L'] = l
        df[tempString+'a'] = a
        df[tempString+'b'] = blu
  return df

def directorySearch(target, RGB=True, regions=3, save_dir=SAVE_DIR):
  startTime = datetime.now()
  fm.checkFormating(save_dir)
  errors = open(save_dir+REQS['LOG'], 'a')
  files = os.listdir(target)
  panic = 0
  for file in files:
    print(file)
    try:
      img = cv.imread(target+file)
      if (1250, 730, 3) != img.shape and (1220, 730, 3) != img.shape:
        errorString = str.format("Error with file %s. Expected shape %s, found shape %s.\n" %(file, '(1250, 730, 3) or (1220, 730, 3)', str(img.shape)))
        errors.write(errorString)
        warnings.warn(errorString)
      else:
        res, df = fullRoutine(img, intFind.findMaxIntensitiesFiltered, RGB, regions)
        fm.outputFile(file, img, df, res, False, False, save_dir)
    except Exception as e:
      errorString = str.format("Error %s with file %s.\n" %(str(e), file))
      errors.write(errorString)
      warnings.warn(errorString)
  errors.close()
  endTime = datetime.now()
  print('Time: ',endTime-startTime)

def tempTest(target, regions):
  files = os.listdir(target)
  index = fm.genIndex(regions)
  for file in files[:5]:
    print(file)
    img = cv.imread(target+file)
    data = {}
    data = fullRoutine(img, intFind.findMaxIntensitiesFiltered, data, True, regions)
    data['Image'] = file
    df = pd.DataFrame(data, columns=index, index=[data['Image']])
    print(df)

def addIndex(runSettings):
  for setting in runSettings:
    regions = runSettings[setting]['regions']
    if(runSettings[setting]['RGB']):
      runSettings[setting]['Index'] = fm.genIndex(regions)
    else:
      runSettings[setting]['Index'] = fm.genIndex(regions, ['L','a','b'])
  return runSettings

def csvReader(target, runSettings, save_dir=SAVE_DIR):
  startTime = datetime.now()
  url = 'https://pad.crc.nd.edu'
  dest = './temp.png'
  fm.checkFormating(save_dir)
  errors = open(save_dir+REQS['LOG'], 'a')
  print("Starting...")
  with open(target) as csvfile:
    csvreader = csv.reader(csvfile)
    i = 0
    for row in csvreader:
      cTime = datetime.now()
      i+=1
      try:
        urllib.request.urlretrieve(url + row[7], dest)
        img = cv.imread(dest)
        if (1250, 730, 3) != img.shape and (1220, 730, 3) != img.shape:
          errorString = str.format("Error with file %s. Expected shape %s, found shape %s.\n" %(file, '(1250, 730, 3) or (1220, 730, 3)', str(img.shape)))
          errors.write(errorString)
          warnings.warn(errorString)
        else:
          for setting in runSettings:
            data = {}
            data = fullRoutine(img, intFind.findMaxIntensitiesFiltered, data, runSettings[setting]['RGB'], runSettings[setting]['regions'])
            data['Image'] = row[0]
            data['Contains'] = row[1]
            data['Drug %'] = row[18]
            data['PAD S#'] = row[17]
            df = pd.DataFrame(data, columns=runSettings[setting]['Index'], index=[data['Image']])
            if(not os.path.exists(save_dir+setting)):
              df.to_csv(save_dir+setting, mode='w', header=True)
            else:
              df.to_csv(save_dir+setting, mode='a', header=False)
          elapsedTime = datetime.now() - cTime
          print("Finished image ",row[0]," in ",elapsedTime)
      except Exception as e:
        errorString = str.format("Error %s with file %s.\n" %(str(e), row[0]))
        errors.write(errorString)
        warnings.warn(errorString)
      os.remove(dest)
    errors.close()
    endTime = datetime.now()
    regions = 3+12+20
    print('Time: ',endTime-startTime, ' time saved = ',i*regions*13/60.0)


if __name__ == '__main__':
  runs = {'3_region_lab_0.csv':{'RGB':False, 'regions':3},
            '3_region_rgb.csv':{'RGB':True, 'regions':3},
            '6_region_lab.csv':{'RGB':False, 'regions':6},
            '6_region_rgb.csv':{'RGB':True, 'regions':6},
            '10_region_lab.csv':{'RGB':False, 'regions':10},
            '10_region_rgb.csv':{'RGB':True, 'regions':10}}
  runs = {'3_region_rgb.csv':{'RGB':True, 'regions':3},
            '6_region_lab.csv':{'RGB':False, 'regions':6},
            '6_region_rgb.csv':{'RGB':True, 'regions':6},
            '10_region_lab.csv':{'RGB':False, 'regions':10},
            '10_region_rgb.csv':{'RGB':True, 'regions':10}}
  runs = addIndex(runs)
  csvReader('/Users/Diyogon/Downloads/card-10.csv', runs, save_dir='./FHI2020/')
  #tempTest('/Users/Diyogon/Downloads/FHI2020/', 3)
  #directorySearch('/Users/Diyogon/Downloads/FHI2020/', 10, './FHI2020/10_region_lab/')
  #directorySearch('/Users/Diyogon/Downloads/FHI2020/', 10, './FHI2020/10_region_rgb/')
  #directorySearch('/Users/Diyogon/Documents/ND/ColorSelector/Data/Original_Images/', 10, './10_region_data/')
  #img = cv.imread('../cards/40296')
  #img2 = cv.imread('../cards/40307')
  '''
  img = cv.imread('../cards/40314')
  f = fullRoutine(img, intFind.findMaxIntensities)
  f2 = fullRoutine(img, intFind.findMaxIntensitiesFiltered)
  cv.imshow("initial", img)
  cv.imshow("final", f)
  cv.imshow("final2", f2)
  cv.waitKey()'''
