'''
wordcount.py
By: YingjiaWang 
From: HUST
Date: 2020.12.9
'''

from funcs import Map, Reduce, Merge, multiThreads
import threading
from time import time

upgrade = True
if upgrade:
    print('In combine and shuffle mode...')
else:
    print('In common mode...')

# map
start = time()

threads = []
for i in range(1, 10):
    threads.append(threading.Thread(target=Map, args=(str(i), upgrade,)))

multiThreads(threads)

end = time()
mapTime = end - start
print('Map done. Time Cost = %.2fs' % mapTime)

# reduce
start = time()

threads = []
for i in range(3):
    index = 3 * i + 1
    threads.append(threading.Thread(target=Reduce, args=([index, index+1, index+2], upgrade,)))

multiThreads(threads)
Merge(upgrade)

end = time()
reduceTime = end - start
print('Reduce done. Time Cost = %.2fs' % reduceTime)
print('timeSum = %.2fs' % (mapTime + reduceTime))
