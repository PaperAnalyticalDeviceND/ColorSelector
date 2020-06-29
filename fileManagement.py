import os
import sys
import warnings
import pandas as pd
import cv2 as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

SAVE_DIR = './Data/'
REQS = {'ORIG_DIR':'Original_Images',
  'CSV_DIR':'CSV_Data',
  'PROC_DIR':'Cartoon_Images',
  'LOG':'log.txt',
  'MASTER':'master.csv'}
MASTER_INDEX = ['Image', 'Contains', 'PAD S#', 'Image Use', 'Aceta%', 'Cipro%',
       'CBlk-R', 'CBlk-G', 'CBlk-B', 'CR-R', 'CR-G', 'CR-B', 'Cblu-R',
       'Cblu-G', 'Cblu-B', 'CG-R', 'CG-G', 'CG-B', 'CW-R', 'CW-G', 'CW-B',
       'A1-R', 'A1-G', 'A1-B', 'A2-R', 'A2-G', 'A2-B', 'A3-R', 'A3-G', 'A3-B',
       'B1-R', 'B1-G', 'B1-B', 'B2-R', 'B2-G', 'B2-B', 'B3-R', 'B3-G', 'B3-B',
       'C1-R', 'C1-G', 'C1-B', 'C2-R', 'C2-G', 'C2-B', 'C3-R', 'C3-G', 'C3-B',
       'D1-R', 'D1-G', 'D1-B', 'D2-R', 'D2-G', 'D2-B', 'D3-R', 'D3-G', 'D3-B',
       'E1-R', 'E1-G', 'E1-B', 'E2-R', 'E2-G', 'E2-B', 'E3-R', 'E3-G', 'E3-B',
       'F1-R', 'F1-G', 'F1-B', 'F2-R', 'F2-G', 'F2-B', 'F3-R', 'F3-G', 'F3-B',
       'G1-R', 'G1-G', 'G1-B', 'G2-R', 'G2-G', 'G2-B', 'G3-R', 'G3-G', 'G3-B',
       'H1-R', 'H1-G',
       'H1-B', 'H2-R', 'H2-G', 'H2-B', 'H3-R', 'H3-G', 'H3-B', 'I1-R', 'I1-G',
       'I1-B', 'I2-R', 'I2-G', 'I2-B', 'I3-R', 'I3-G', 'I3-B', 'J1-R', 'J1-G',
       'J1-B', 'J2-R', 'J2-G', 'J2-B', 'J3-R',
       'J3-G', 'J3-B', 'K1-R', 'K1-G', 'K1-B', 'K2-R', 'K2-G', 'K2-B', 'K3-R',
       'K3-G', 'K3-B', 'L1-R', 'L1-G', 'L1-B', 'L2-R', 'L2-G', 'L2-B', 'L3-R',
       'L3-G', 'L3-B']
COLORS = ['R', 'G', 'B']
#COLORS = ['L','a','b']

def convertToDF(file, sampleNumber, index, regions=3):
  df = pd.read_csv(file)
  ret = {}
  for i in MASTER_INDEX:
    ret[i] = 'N/A'
  ret['Image'] = sampleNumber
  ret['PAD S#'] = sampleNumber
  i = 0
  for letter in ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
    for j in range(1,regions+1):
      for color in COLORS:
        tempStr = letter+str(j)+'-'+color
        ret[tempStr] = df.loc[i][color]
      i+=1
  return ret

def genIndex(regions, ColorList = ['R', 'G', 'B']):
  index = ['Image', 'Contains', 'Drug %', 'PAD S#']
  for letter in ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
    for j in range(1,regions+1):
      for color in ColorList:
        tempStr = letter+str(j)+'-'+color
        index.append(tempStr)
  return index

def compressCSVs(masterName=SAVE_DIR+'/master.csv', target=SAVE_DIR+REQS['CSV_DIR'], regions=3):
  try:
    masterDF = pd.read_csv(masterName, index_col=0)
    print(masterDF.index)
  except Exception as e:
    masterDF = None
  index = genIndex(regions)
  for item in os.listdir(target):
    if item[-4:] == '.csv':
      number = item[:-4]
      data = convertToDF(target+'/'+item, number, index, regions)
      if masterDF is None:
        masterDF = pd.DataFrame(data, columns=index, index=[data['Image']])
      else:
        if number in masterDF.index:
          pass
        else:
          tempDF = pd.DataFrame(data, columns=index, index=[data['Image']])
          masterDF = pd.concat([masterDF, tempDF])
  if masterDF is not None:
    masterDF.to_csv(masterName)

def readLanes(target=SAVE_DIR+'/master.csv', regions=3, req=None, targetPercent=0, reqName=None):
  try:
    masterDF = pd.read_csv(target, index_col=0)
  except Exception as e:
    print(e)
    return
  nameList = []
  laneHash = {'A':{},'B':{},'C':{}, 'D':{}, 'E':{}, 'F':{}, 'G':{}, 'H':{}, 'I':{}, 'J':{}, 'K':{}, 'L':{}, 'All':{}}
  for item in masterDF.index:
    if req is not None:
      targetVal = masterDF.loc[item][req]
      if str(targetVal) != str(targetPercent):
        continue
      else:
        nameList.append(item)
    if reqName is not None:
      if item not in reqName:
        continue
    for letter in ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
      for j in range(1,regions+1):
        cColor = [0,0,0]
        i = 0
        for color in ['L','a','b']:
          tempStr = letter+str(j)+'-'+color
          cColor[i] = masterDF.loc[item][tempStr]
          i += 1
        cColor = tuple(cColor)
        if cColor not in laneHash[letter].keys():
          laneHash[letter][cColor] = 0
        if cColor not in laneHash['All'].keys():
          laneHash['All'][cColor] = 0
        laneHash[letter][cColor] += 1
        laneHash['All'][cColor] += 1
  return laneHash, nameList

def graphLanes(laneHash, lane = 'A'):
  colors = laneHash[lane]
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.set_xlabel('R')
  ax.set_ylabel('G')
  ax.set_zlabel('B')
  name = 'Lane '+lane+' colorMap'
  ax.set_title(name)
  for (r, g, b) in colors.keys():
    s = colors[(r, g, b)]
    r /= 255.0
    g /= 255.0
    b /= 255.0
    ax.scatter3D(r, g, b, c=[r, g, b], s=s)
  plt.savefig(SAVE_DIR+name+'.png')
  plt.show()

def graphComparison(laneList, lane = 'A', name='Aceta'):
  fig = plt.figure()
  i = 1
  keys = list(laneList.keys())
  keys.sort(key=int)
  for item in keys:
    colors = laneList[item][lane]
    ax = fig.add_subplot(1, len(laneList), i, projection='3d')
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    for (r, g, b) in colors.keys():
      s = colors[(r, g, b)]
      r /= 255.0
      g /= 255.0
      b /= 255.0
      ax.scatter3D(r, g, b, c=[r, g, b], s=s)
    ax.set_title(item)
    i+=1
  fig.canvas.set_window_title(name)

def outputFile(file, origImg, dataframe, processedImg, saveOrig=False, saveProc=False, targetDir = SAVE_DIR):
  fileName = stripSuffix(file)
  checkFormating(targetDir)
  errors = open(targetDir+REQS['LOG'], 'a')
  checkFormating(targetDir)
  saveString = targetDir+REQS['ORIG_DIR']+'/'+str(fileName)+'.jpg'
  saveString2 = targetDir+REQS['CSV_DIR']+'/'+str(fileName)+'.csv'
  saveString3 = targetDir+REQS['PROC_DIR']+'/'+str(fileName)+'.jpg'
  i = 0
  while os.path.isfile(saveString3):
    i += 1
    saveString = targetDir+REQS['ORIG_DIR']+'/'+str(fileName)+'_'+str(i)+'.jpg'
    saveString2 = targetDir+REQS['CSV_DIR']+'/'+str(fileName)+'_'+str(i)+'.csv'
    saveString3 = targetDir+REQS['PROC_DIR']+'/'+str(fileName)+'_'+str(i)+'.jpg'
  if 0 != i:
    errorString = str.format("Existing item %s, saving as %s.\n" %(str(fileName), str(fileName)+'_'+str(i)))
    errors.write(errorString)
    warnings.warn(errorString)
  if(saveOrig):
    cv.imwrite(saveString, origImg)
  dataframe.to_csv(saveString2)
  if(saveProc):
    cv.imwrite(saveString3, processedImg)
  errors.close()

def stripSuffix(file):
  ret = file.replace(".jpg", "")
  return ret

def checkFormating(dir=SAVE_DIR, errorsFile=None):
  if not os.path.isdir(dir):
    os.mkdir(dir)
  if errorsFile is None:
    errors = open(dir+REQS['LOG'], 'a')
  else:
    errors = errorsFile
  files = os.listdir(dir)
  #print(files)
  for item in REQS.values():
    if item not in files:
      errorString = str.format("Required file %s not found, creating.\n" %(item))
      errors.write(errorString)
      warnings.warn(errorString)
      if item is REQS['MASTER'] or item is REQS['LOG']:
        temp = open(dir+item, 'w')
        temp.close()
      else:
        os.mkdir(dir+item)
  if errorsFile is None:
    errors.close()

def build4Comp(target, target2, name, lane):
  laneHash1, nameList1 = readLanes(target, name, 0.0)
  laneHash2, nameList2  = readLanes(target, name, 50.0)
  laneHash3, nameList3  = readLanes(target, name, 80.0)
  laneHash4, nameList4  = readLanes(target, name, 100.0)
  graphComparison({'0':laneHash1, '50':laneHash2, '80':laneHash3, '100':laneHash4}, lane=lane, name=name+' FHI')
  laneHash1, nameList1 = readLanes(target2, None, 0, nameList1)
  laneHash2, nameList2  = readLanes(target2, None, 0, nameList2)
  laneHash3, nameList3  = readLanes(target2, None, 0, nameList3)
  laneHash4, nameList4  = readLanes(target2, None, 0, nameList4)
  graphComparison({'0':laneHash1, '50':laneHash2, '80':laneHash3, '100':laneHash4}, lane=lane, name=name+' GB')

def showBeforeAfter(target, group=''):
  img1 = cv.imread(SAVE_DIR+REQS['ORIG_DIR']+'/'+target+".jpg")
  img2 = cv.imread(SAVE_DIR+REQS['PROC_DIR']+'/'+target+".jpg")
  img3 = np.hstack([img1, img2])
  return img3

def showGroup(members, title):
  rets = []
  for member in members:
    rets.append(showBeforeAfter(str(member), title))
  ret = np.vstack(rets)
  cv.imwrite(SAVE_DIR+title, ret)

def MLDemo():
  t1 = "0%.jpg"
  m1 = [40127, 40144, 40145, 40156, 40157]
  t2 = "50%.jpg"
  m2 = [40121, 40130, 40131, 40133, 40138]
  t3 = "80%.jpg"
  m3 = [40122, 40128, 40140, 40167, 40178]
  t4 = "100%.jpg"
  m4 = [40136, 40142, 40143, 40150, 40180]
  showGroup(m1, t1)
  showGroup(m2, t2)
  showGroup(m3, t3)
  showGroup(m4, t4)

if __name__ == '__main__':
  '''build4Comp('/Users/Diyogon/Documents/ND/ColorSelector/FHIData/tmp/r.csv', '/Users/Diyogon/Documents/ND/ColorSelector/Data/master.csv', 'Cipro%', 'L')
  build4Comp('/Users/Diyogon/Documents/ND/ColorSelector/FHIData/tmp/r.csv', '/Users/Diyogon/Documents/ND/ColorSelector/Data/master.csv', 'Cipro%', 'D')
  build4Comp('/Users/Diyogon/Documents/ND/ColorSelector/FHIData/tmp/r.csv', '/Users/Diyogon/Documents/ND/ColorSelector/Data/master.csv', 'Aceta%', 'K')
  plt.show()'''
  #compressCSVs('./FHI2020/10_region_lab/master.csv', './FHI2020/10_region_lab/'+REQS['CSV_DIR'], 10)
  compressCSVs('./FHI2020/10_region_rgb/master.csv', './FHI2020/10_region_rgb/'+REQS['CSV_DIR'], 10)