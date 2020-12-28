'''
pagerank(networkx实现).py
By: YingjiaWang 
From: HUST
Date: 2020.12.9
'''
import numpy as np
import pandas as pd
import networkx as nx

data = pd.read_csv('source/sent_receive.csv')
sent, receive = data['sent_id'], data['receive_id']

edges = []
for row in zip(sent, receive):
    edge = (row[0], row[1])
    if edge not in edges:
        edges.append(edge)

graph = nx.DiGraph()
graph.add_edges_from(edges)

pagerank = nx.pagerank(graph)
pagerank = sorted(pagerank.items())

k = []
v = []
for i in pagerank:
    k.append(i[0])
    v.append(i[1])

ans = pd.DataFrame({'id':k, 'pagerank':v})
ans.to_csv('output/pagerank(networkx).csv', index=False)
print('done.')
