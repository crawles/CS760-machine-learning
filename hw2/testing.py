import helper_functions as helper
#from collections import defaultdict
#
#def tree(): return defaultdict(tree)
#
#users = tree()
#users['harold']['username'] = 'hrldcpr'
#users['handler']['username'] = 'matthandlersux'
#
#n = data.Nodes()
#n.node['key1'] = 'val1'
#n.node['val1']['subkey1'] = 'subval2' 
#n.node['val1']['subval2']['subval3'] = 'subval3' 
#
ci = 0
ai = 0
for i in train_set:
    if i['class'] == 'metastases':
        ci = ci + 1
        if i['by_pass'] == 'no':
            ai = ai + 1
float(ci)/len(train_set)

instance = train_set[4]
instance_keys = instance.attr_val_set.keys()
instance_keys.remove('class')


clas_key_val = ('class','metastases')
result = 1
for key in instance_keys:
    key_val = (key,instance[key])
    cond_prob =  trn.nodes[key_val][clas_key_val]
    result = helper.log_mult(result,cond_prob)

clas_key_val = ('class','malign_lymph')
result0 = 1
for key in instance_keys:
    key_val = (key,instance[key])
    cond_prob =  trn.nodes[key_val][clas_key_val]
    result0 = helper.log_mult(result0,cond_prob)

print result0/(result+result0)
print result/(result+result0)

attributes = trn.dataset[0].attribute_names

