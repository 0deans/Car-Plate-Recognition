import cv2 as cv
import numpy as np

img = cv.imread('source/car4.jpg', cv.IMREAD_GRAYSCALE)
kernel = np.ones((10, 10), np.uint8)

blackhat = cv.morphologyEx(img, cv.MORPH_BLACKHAT, kernel)

res = cv.resize(blackhat, (600, 600))

cv.imshow('Blackhat', res)

cv.waitKey(0)