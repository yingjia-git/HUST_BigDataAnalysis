'''
kmeans.py
By: YingjiaWang 
From: HUST
Date: 2020.12.16
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# 宏参数
clusters = 3
chooseRandomly = False
max_times = 100

#　数据预处理
columns = ['label'] + ['dim'+str(i) for i in range(13)]
data = pd.read_csv('ProcessData.csv', names=columns)
label = data['label']
del data['label']

# 返回x和y的欧式距离
def dist(x, y): 
    return np.sqrt(np.sum((x-y)**2))

# 随机选择三个初始点
data_num = len(data)
dim_num = len(data.loc[0])
if chooseRandomly:
    initialChoices = random.sample([i for i in range(data_num)], clusters)
else:
    initialChoices = [20, 70, 150]
centralPoints = [data.loc[initialChoices[i]] for i in range(clusters)]

# 开始kmeans迭代
ans = np.zeros(data_num)
for i in range(clusters):
    ans[initialChoices[i]] = i + 1 # 分配初始编号1-n

i = 0
while True:
    change = False
    tmp = [np.zeros(dim_num)] * clusters
    cnt = [0] * clusters
    for j in range(data_num):
        dists = []
        for k in range(clusters):
            dists.append(dist(data.loc[j], centralPoints[k]))

        min_index = dists.index(min(dists))
        tmp[min_index] += data.loc[j]
        cnt[min_index] += 1
        if min_index + 1 != ans[j]:
            ans[j] = min_index + 1
            change = True
        
    #np.seterr(all='ignore')
    for j in range(clusters):
        centralPoints[j] = tmp[j] / cnt[j]

    i += 1
    if i > max_times or not change: # 超过最大次数或聚类结果不再改变时退出
        break

# 输出结果
print('After %d rounds...' % i)
acc = np.sum(ans == label)/data_num * 100
print('Acc = %.2f%%' % acc)
dists = []
for i in range(data_num):
    dists.append(dist(data.loc[i], centralPoints[int(ans[i])-1]))
sse = np.sum(dists)

output = pd.DataFrame(dists, columns=['dist'])
output.to_csv('output.csv')

# 图形化展示
first_dim = 'dim5'
second_dim = 'dim6'
fd, sd = data[first_dim], data[second_dim]
map_dict = {0:'r', 1:'g', 2:'b'} # clusters=3
ans = [map_dict[ans[i]-1] for i in range(data_num)]

plt.xlabel(first_dim)
plt.ylabel(second_dim)
plt.title('SSE=%.2f Acc=%.2f%%' % (sse, acc))
plt.scatter(fd, sd, c=ans)
for i in range(clusters):
    tmp = centralPoints[i]
    x, y = tmp[int(first_dim[-1])],tmp[int(second_dim[-1])]
    plt.plot(x, y, color=map_dict[i], marker='v', markersize=10)
plt.show()
