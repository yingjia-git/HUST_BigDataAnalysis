'''
funcs.py
By: YingjiaWang 
From: HUST
Date: 2020.12.9
'''
import threading
import os
from collections import OrderedDict

# 文件地址
source_url = 'source/source0'
map_url = 'map/map0'
reduce_url = 'reduce/reduce0'
final_url = 'wordcount'

def Map(index, upgrade=False):
    '''
    实现mapreduce中的map功能，可选择combine&shuffle模式
    '''
    url = source_url + str(index)
    with open(url, 'r') as f:
        if upgrade: # 如果是combine和shuffle模式用有序词典OrderedDict来保存
            d = OrderedDict()
            for line in f:
                for word in line.split():
                    word = word.strip(',')
                    d[word] = d.setdefault(word, 0) + 1
        else:
            words = []
            for line in f:           
                words += [word.strip(',') for word in line.split()]

    url = map_url + str(index)
    if not os.path.exists('map'):
        os.mkdir('map')
    
    with open(url, 'w') as f:
        if upgrade:
            for key in d.keys():
                f.write(key + ' ' + str(d[key]) + '\n')
        else:
            for word in words:
                f.write(word + ' 1\n')

def Reduce(index, upgrade=False):
    '''
    实现mapreduce中的reduce功能
    '''
    if upgrade:
        d = OrderedDict()
    else:
        d = {}
    for i in index:
        url = map_url + str(i)
        with open(url, 'r') as f:
            if upgrade:
                for line in f:
                    word, cnt = line.split()
                    d[word] = d.setdefault(word, 0) + int(cnt)
            else:
                for line in f:
                    word, _ = line.split()
                    d[word] = d.get(word, 0) + 1
    
    url = reduce_url + str(int((index[0]-1)/3))
    if not os.path.exists('reduce'):
        os.mkdir('reduce')
    with open(url, 'w') as f:
        for key in d.keys():
            f.write(key + ' ' + str(d[key]) + '\n')

def Merge(upgrade=False):
    '''
    整合reduce节点的结果
    '''
    if upgrade:
        d = OrderedDict()
    else:
        d = {}
    for i in range(3):
        url = reduce_url + str(i)
        with open(url, 'r') as f:
            if upgrade:
                for line in f:
                    word, cnt = line.split()
                    d[word] = d.setdefault(word, 0) + int(cnt)
            else:
                for line in f:
                    word, cnt = line.split()
                    d[word] = d.get(word, 0) + int(cnt)
    
    with open(final_url, 'w') as f:
        for key in d.keys():
            f.write(key + ' ' + str(d[key]) + '\n')   

def multiThreads(threads):
    '''
    实现多线程处理
    '''
    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join() # 线程全部运行完程序才能结束