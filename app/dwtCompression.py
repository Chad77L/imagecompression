import numpy as np
import pywt
import cv2
def dwtCompression(path):
 img = cv2.imread(path, 0)
 coeffs2 = pywt.dwt2(img, 'bior1.3')
 LL, (LH, HL, HH) = coeffs2
 print(LL.shape)
 print(img.shape)	
# return LL
 return cv2.resize(LL, img.shape)
