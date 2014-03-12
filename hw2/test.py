from collections import defaultdict

def tree(): return defaultdict(tree)

users = tree()
users['harold']['username'] = 'hrldcpr'
users['handler']['username'] = 'matthandlersux'

n = data.Nodes()
n.node['key1'] = 'val1'
n.node['val1']['subkey1'] = 'subval2' 
n.node['val1']['subval2']['subval3'] = 'subval3' 

t=train.Train(train_set)
n = 0
for i in train_set:
    if i['class'] == 'metastases':
        n = n + 1

train_set['class']
instance = train_set[0]

