import cv2 as cv
import numpy as np
import math

BLACK_THRESH_S = 35
BLACK_THRESH_V = 70

#Takes a HSV image and returns a list of the most intense pixels in it
def findMaxIntensities(img):
  imgS = img[:,:,1]
  maxI = 0
  maxSet = []
  for i in range(imgS.shape[0]):
    for j in range(imgS.shape[1]):
      if imgS[i,j] > maxI:
        maxI = imgS[i,j]
        maxSet = [(i,j)]
      elif imgS[i,j] == maxI:
        maxSet.append((i,j))
  #print(maxI)
  return maxSet

#Takes a HSV image and returns a list of the most intense pixels in it, 
# after applying filtering to minimize black bars on the edges
def findMaxIntensitiesFiltered(img):
  imgS = img[:,:,1]
  imgV = img[:,:,2]
  maxI = 0
  maxSet = []
  centerX = imgS.shape[0]/2
  centerY = imgS.shape[1]/2
  for i in range(imgS.shape[0]):
    dX = abs(centerX-i)
    for j in range(imgS.shape[1]):
      dY = abs(centerY-j)
      sF = cosCorrectFactor(dX,dY,centerX,centerY)
      cS = sF*imgS[i,j]
      cV = sF*imgV[i,j]
      if cS <= BLACK_THRESH_S and cV <= BLACK_THRESH_V:
        pass
      elif cS > maxI:
        maxI = imgS[i,j]
        maxSet = [(i,j)]
      elif cS == maxI:
        maxSet.append((i,j))
  return maxSet

#Takes a distance from a center and returns a weight between 0 and 1
# determined by cosine such that a point at the cetner has weight 1,
# and a point at the extremes has weight ~0.
def cosCorrectFactor(dx, dy, centerX, centerY):
  relevantD = max((dx/centerX), dy/centerY)
  relevnatDRads = (math.pi/2) * relevantD
  return math.cos(relevnatDRads)

if __name__ == '__main__':
  print(cosCorrectFactor(0,0,50,100))
  print(cosCorrectFactor(50,0,50,100))
  print(cosCorrectFactor(20,50,50,100))
  '''
  img = cv.imread('../cards/42398')
  imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
  findMaxIntensities(imgHSV)
  cv.imshow("out", imgHSV[:,:,1])
  cv.waitKey()'''