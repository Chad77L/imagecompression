import cv2 
import numpy as np
def fftCompression(path): 
  img = cv2.imread(path, 0)
  bimg = np.fft.fft2(img)
  Btsort = np.sort(np.abs(bimg.reshape(-1)))
  keep = 0.002
  thresh = Btsort[int(np.floor((1-keep)* len(Btsort)))]
  ind = np.abs(bimg) > thresh
  Atlow = bimg * ind
  Alow = np.fft.ifft2(Atlow).real
  return Alow