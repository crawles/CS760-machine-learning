import information as info
import data_structure as data
import tree 
import copy
import random
import numpy as np
import matplotlib.pyplot as plt

m = 4
#part 2
train_set = data.read_arff_file('heart_train.arff.txt')
default_class = train_set.instances[0].attribute['class']
test_set = data.read_arff_file('heart_test.arff.txt')

M = tree.Metrics(train_set,test_set,default_class,m)
strata = M.create_strata()
sub_sample = M.stratified_ds(50)

curve = []
for s in 25, 50, 100:
    res = M.test_train_set(s)
    curve.append(res)
#200 case
tt = tree.Tree(train_set,default_class,m)
tt_dict = tt.get_children()
tt1 = tree.Tree(test_set,default_class)
res = [tt1.test_all_instances(tt_dict)] * 3
curve.append(res)

curve_array = np.zeros([4,3])
for i,s in enumerate(curve):
    curve_array[i,:] = s

x=np.array([25,50,100,200])
#plot min
p1,=plt.plot(x,curve_array[:,0],'o')
#plot max
p3,=plt.plot(x,curve_array[:,2],'o')
#plot mean
p2,=plt.plot(x,curve_array[:,1],'o')
plt.ylabel('percent correct')
plt.xlabel('num of training examples')
legend([p1,p2,p3], ["min","mean","max"])

#part 3
m_curve = []
m_vals = [2,5,10,20]
for m in m_vals:
    tt = tree.Tree(train_set,default_class,m)
    tt_dict = tt.get_children()
    tt1 = tree.Tree(test_set,default_class)
    res = tt1.test_all_instances(tt_dict)
    m_curve.append(res)

plt.plot(m_vals,m_curve,'o')
plt.plot(m_vals,m_curve)
plt.ylabel('percent correct')
plt.xlabel('value of m')
#instance = train_set.instances[0]
#
#
#a = info.Information(train_set)
#first_attribute = a.calc_max_gain()[0] 
#
#tt = tree.Tree(train_set,default_class,m)
#tt_dict = tt.get_children()
#tt.print_tree('',first_attribute,tt_dict)
#tt1 = tree.Tree(test_set,default_class)
#tt1.test_all_instances(tt_dict)



