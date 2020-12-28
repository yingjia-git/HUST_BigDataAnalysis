'''
Apriori(mlxtend).py
By: YingjiaWang 
From: HUST
Date: 2020.12.16
'''
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

data = pd.read_csv('Groceries.csv')['items']
data = [d.lstrip('{').rstrip('}').split(',') for d in data]
debug = False
if debug:
    data = data[:500]

te = TransactionEncoder()
te_data = te.fit_transform(data)
df = pd.DataFrame(te_data, columns=te.columns_)

# 求频繁项集
freq = apriori(df, min_support=0.005, use_colnames=True, max_len=4)
freq.sort_values(by='support', ascending=False, inplace=True)
print(len(freq))

# 求关联规则
rules = association_rules(freq,metric='confidence',min_threshold=0.5)
rules.sort_values(by='confidence', ascending=False, inplace=True) 
#rules.to_csv('rules.csv', index=False)
print(len(rules))