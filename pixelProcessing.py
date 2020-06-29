import cv2 as cv
import numpy as np

#Takes a list of pixels and a BGR image and returns the average
# RGB pixel values
def avgPixels(pixels, img):
  totalB = 0
  totalG = 0
  totalR = 0
  for pixel in pixels:
    x = pixel[0]
    y = pixel[1]
    b,g,r = img[x,y,:]
    totalB += b
    totalG += g
    totalR += r
  if len(pixels) != 0:
    totalB /= len(pixels)
    totalG /= len(pixels)
    totalR /= len(pixels)
  return totalR, totalG, totalB

#Takes a list of pixels and a BGR image and returns the average
# HSV pixel values
def avgPixelsHSV(pixels, img):
  workingImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
  totalH = 0
  totalS = 0
  totalV = 0
  for pixel in pixels:
    x = pixel[0]
    y = pixel[1]
    h, s, v = workingImg[x,y,:]
    totalH += h
    totalS += s
    totalV += v
  if len(pixels) != 0:
    totalH /= len(pixels)
    totalS /= len(pixels)
    totalV /= len(pixels)
  return totalH, totalS, totalV

#Takes a list of pixels and a BGR image and returns the average
# Lab pixel values
def avgPixelsLAB(pixels, img):
  workingImg = cv.cvtColor(img, cv.COLOR_BGR2Lab)
  totalL = 0
  totalA = 0
  totalB = 0
  for pixel in pixels:
    x = pixel[0]
    y = pixel[1]
    l, a, b = workingImg[x,y,:]
    totalL += l
    totalA += a
    totalB += b
  if len(pixels) != 0:
    totalL /= len(pixels)
    totalA /= len(pixels)
    totalB /= len(pixels)
  return totalL, totalA, totalB