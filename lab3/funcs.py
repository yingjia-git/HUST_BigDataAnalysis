'''
funcs.py
By: YingjiaWang 
From: HUST
Date: 2020.12.16
'''
import numpy as np
import pandas as pd
import itertools, copy

def combine(l, n):
    '''
    给定n-1阶频繁项列表，返回待选n阶频繁项列表
    '''
    if n == 2:
        return list(itertools.combinations(l, n))
    if n > 2:
        tmp = []
        for i in range(len(l)-1):
            for j in range(i+1, len(l)):
                s = set(l[i]) & set(l[j])
                if s and len(list(s)) == n - 2:
                    tmp.append(tuple(sorted(set(l[i])|set(l[j]))))
        
        return list(set(tmp)) # 去重

def reduceFreq(groups_n, n, data, data_num, min_support):
    '''
    计算n阶频繁项及支持度
    '''
    support_n = {g:0 for g in groups_n}

    if n == 1:
        for i in range(data_num):
            if i % 100 == 0:
                print('reduceFreq1 %d/%d...' % (i+1, data_num))
            for j in range(len(data[i])):
                k = data[i][j]
                support_n[k] = support_n[k] + 1.0 / data_num
    else:
        for i in range(data_num):
            if i % 100 == 0:
                print('reduceFreq%d %d/%d...' % (n, i+1, data_num))
            for g in groups_n:
                if set(g).issubset(set(data[i])):
                    support_n[g] = support_n[g] + 1.0 / data_num

    # 对于低于支持度的频繁项集舍弃
    for i in list(support_n.keys()):
        if support_n[i] < min_support:
            del support_n[i] 
    
    return support_n
    

def hash(x, y, nBuckets):
    '''
    返回hash值
    '''
    return int(str(x)+str(y)) % nBuckets


def PCY(nSub1Freq, n, data, data_num, min_support, nBuckets):
    '''
    计算2阶频繁项及支持度(经过PCY算法改进)
    '''
    cnt = [0] * nBuckets
    bitmap = [0] * nBuckets
    pairs = []
    pairs2hash = {}

    # Pass 1
    for i in range(data_num):
        for j in range(len(data[i])-1):
            for k in range(j+1, len(data[i])):
                g = tuple([data[i][j], data[i][k]])
                f = hash(g[0], g[1], nBuckets)
                cnt[f] += 1
                if g[0] in nSub1Freq and g[1] in nSub1Freq and g not in pairs:
                    pairs.append(g)
                    pairs2hash[g] = f
    
    pairs = sorted(pairs) # 对pairs排序

    # Pass 2
    min_cnt = min_support * data_num
    bitmap = [1 if cnt[i] >= min_cnt else 0 for i in range(nBuckets)]
    print(bitmap)

    candidateFreq = []
    for i in range(len(pairs)):
        g = pairs[i]
        if bitmap[pairs2hash[g]] == 1:
            candidateFreq.append(pairs[i])

    support_2 = {}
    support_2_backup = {}
    candidateFreq_num = len(candidateFreq)
    for i in range(candidateFreq_num):
        if i % 100 == 0:
            print('reduceFreq2 %d/%d...' % (i+1, candidateFreq_num))
        support = 0
        for j in range(data_num):
            if set(candidateFreq[i]).issubset(set(data[j])):
                support += 1.0 / data_num
        if support >= min_support:
            support_2[candidateFreq[i]] = support
    
    return support_2

def generateRules(support, min_confidence):
    '''
    生成关联规则
    ''' 
    rules = {}
    keys = list(support.keys())
    for k in keys:
        if type(k) != int: # 不必考虑单元素
            rules = {**rules, **appendRule([set(k), set()], support, min_confidence)}

    return rules

def appendRule(k, support, min_confidence):
    '''
    对列表k生成全部高于置信度的关联规则
    '''
    if len(k[0]) == 1:
        return {}
    rules = {}
    union = tuple(sorted(k[0] | k[1]))
    if union not in support.keys():
        return {}
    for i in k[0]:
        tmp = copy.deepcopy(k)
        tmp[0].remove(i)
        tmp[1].add(i)
        tmp[0], tmp[1] = tuple(sorted(tmp[0])), tuple(sorted(tmp[1]))

        # 将单元素元组转化为int作为键
        tmp[0] = tmp[0][0] if len(tmp[0]) == 1 else tmp[0]
        tmp[1] = tmp[1][0] if len(tmp[1]) == 1 else tmp[1]

        if tmp[0] not in support.keys():
            continue
        
        confidence = support[union] / support[tmp[0]]
        if confidence >= min_confidence - 1e-6: # 很重要！！！！
            rules[(tmp[0], tmp[1])] = confidence
            tmp[0] = tuple([tmp[0]]) if type(tmp[0]) == int else tmp[0]
            tmp[1] = tuple([tmp[1]]) if type(tmp[1]) == int else tmp[1]

            rules = {**rules, **appendRule([set(tmp[0]), set(tmp[1])], support, min_confidence)}
    
    return rules
