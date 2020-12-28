'''
kmeans(sklearn).py
By: YingjiaWang 
From: HUST
Date: 2020.12.16
'''
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans

columns = ['label'] + ['dim'+str(i) for i in range(13)]
data = pd.read_csv('ProcessData.csv', names=columns)
label = data['label']
del data['label']

km = KMeans(n_clusters=3, random_state=42)
pred = km.fit_predict(data)
print('Acc = %.2f%%' % (np.sum(pred==label)/len(pred) * 100))

