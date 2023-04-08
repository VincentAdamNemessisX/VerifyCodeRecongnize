"""
# File       : opencv2Andtesseract2Recognize.py
# Time       : 12:33 PM
# Author     : vincent
# version    : python 3.8
# Description:
"""
import cv2
import pytesseract as tess
from PIL import Image

# 验证码识别
img = cv2.imread('test.png')
img = cv2.blur(img, (1, 1))
cv2.imshow('yzm', img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_TRIANGLE)
kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 4))
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 6))
open1 = cv2.erode(binary, kernel=kernel1)
open2 = cv2.morphologyEx(open1, cv2.MORPH_OPEN, kernel=kernel2)
cv2.imshow('detect', open2)
cv2.bitwise_not(open2, open2)
textimg = Image.fromarray(open2)
text = tess.image_to_string(textimg)
print("验证码为:%s" % text)
cv2.waitKey(0)
