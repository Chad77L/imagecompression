from sklearn.cluster import KMeans
import cv2
import numpy as np

def KMeansCompressor(path_in):
    img= cv2.imread(path_in,0)
    w, h = img.shape
    X= img.copy().reshape((w*h))
    X= np.expand_dims(X,axis=1)
    kmeans = KMeans(n_clusters=20, random_state=0).fit(X)
    for i in range(0,len(X)):
        X[i]= kmeans.cluster_centers_[kmeans.labels_[i]][0]
    X= np.squeeze(X,axis=1)
    X=X.reshape((w, h))
    return X