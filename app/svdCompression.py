import numpy as np
import cv2
def svdCompression(path):
  r = 20
  img = cv2.imread(path, 0)
  U, S, VT = np.linalg.svd(img, full_matrices = False)
  S = np.diag(S)
  Xapprox = U[:,:r] @ S[0:r, : r] @ VT[:r,:]
  return Xapprox