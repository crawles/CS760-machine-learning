import information as info
import data_structure as data
import tree 
import copy
import random
import sys

train_set_file = sys.argv[1]
test_set_file = sys.argv[2]
m = int(sys.argv[3])

train_set = data.read_arff_file(train_set_file)
test_set = data.read_arff_file(test_set_file)
default_class = train_set.instances[0].attribute['class']

a = info.Information(train_set)
first_attribute = a.calc_max_gain()[0] 

tt = tree.Tree(train_set,default_class,m)
tt_dict = tt.get_children()
tt.print_tree('',first_attribute,tt_dict)
print ''
#tt1 = tree.Tree(test_set,default_class)
tt1 = tree.Tree(test_set,default_class)
tt1.test_all_instances(tt_dict)


