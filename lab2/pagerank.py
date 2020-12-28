'''
pagerank.py
By: YingjiaWang 
From: HUST
Date: 2020.12.9
'''
import numpy as np
import pandas as pd

# 读取数据
data = pd.read_csv('source/sent_receive.csv')
sent, receive = data['sent_id'], data['receive_id']

# 提取有向边并按入结点排序
edges = []
for row in zip(sent, receive):
    e = (row[0], row[1])
    if e not in edges: # 不考虑重复边
        edges.append(e)

edges = sorted(edges)

# 提取结点个数
nodes = list(set([node for e in edges for node in e]))
node_num = len(nodes)

# 初始化转移矩阵M
M = np.zeros((node_num, node_num), dtype=float)

for n in nodes:
    end = []
    check = False
    for e in edges:
        if e[0] == n:
            end.append(e[1])
            check = True
        else:
            if check: # 由于边是按序排序，check帮助提前退出，提高效率
                break
    
    end_num = len(end)
    for i in end:
        M[nodes.index(n)][nodes.index(i)] = 1.0 / end_num

M = M.T # 转置

# 初始化w
value = 1.0 / node_num
w = np.array([value for _ in range(node_num)], dtype=float)
w = w.T #转置

# 参数
beta = 0.85
w0 = w.copy()

# 开始迭代
error = 1
round = 0

while error > 1e-8:
    new_w = beta * np.matmul(M, w) + (1 - beta) * w0  # 带阻尼系数，阻尼系数为0.85
    error = np.sum(w - new_w)
    w = new_w
    round = round + 1

w = w / np.sum(w)

# 输出结果
print('After', round, 'rounds...')
ans = pd.DataFrame({'id':nodes, 'pagerank':w})
ans.to_csv('output/pagerank.csv', index=False)
print('done.')








