import copy
import data_structure as data
import information as info
import sys
import random

class Tree:

    def __init__(self,dataset,default_class,m=2):
        self.dataset = dataset
        self.default_class = default_class
        self.m = m

    def pop_attribute(self,sn,attr_mp):
        """ if numeric, remove mp value (and attribute name is len(mps)=0)
        if string, remove attribute name"""
        attr = attr_mp[0]
        mp = attr_mp[1]
        attr_index = sn.attributes.index(attr)
        #if numeric attribute
        if mp:
            sn.pop_attribute_mp(attr_mp)
            if len(sn.attr_midpoints(attr))==0:
                sn.attributes.pop(attr_index)
        else:
            sn.attributes.pop(attr_index)
            #self.dataset.attr_val_set.pop(attr)
            
    def split_tree_numeric(self,attr_mp):
        """ returns 2 new datasets split using mp """

        attribute_name = attr_mp[0]
        split_pt = attr_mp[1]
        ds_under = data.Dataset()
        ds_under.add_attributes(copy.deepcopy(self.dataset.attributes))
        ds_under.arff_attr_val_set = copy.deepcopy(self.dataset.arff_attr_val_set)
        ds_over = data.Dataset()
        ds_over.add_attributes(copy.deepcopy(self.dataset.attributes))
        ds_over.arff_attr_val_set = copy.deepcopy(self.dataset.arff_attr_val_set)
        over_instances = []
        under_instances = []
            
        for instance in self.dataset.instances:
            attr_val = float(instance.attribute[attribute_name])
            if attr_val <= float(split_pt):
                under_instances.append(copy.deepcopy(instance))   
            else:
                over_instances.append(copy.deepcopy(instance))   

        ds_under.add_instances(under_instances) 
        ds_over.add_instances(over_instances) 
        return (ds_under,ds_over)

    def split_tree_string(self,attr_mp):
        attribute_name = attr_mp[0]
        attr_vals = copy.deepcopy(self.dataset.arff_attr_val_set[attribute_name])
        datasets = []
        for attr_val in attr_vals:
            ds = data.Dataset()
            ds.add_attributes(copy.deepcopy(self.dataset.attributes))
            ds.arff_attr_val_set = copy.deepcopy(self.dataset.arff_attr_val_set)
            ds_instances = []
            for instance in self.dataset.instances:
                attr_val_inst = instance.attribute[attribute_name]
                if attr_val == attr_val_inst:
                    ds_instances.append(copy.deepcopy(instance))
            if not ds_instances:
                ds.arff_val = attr_val


            ds.add_instances(ds_instances)
            datasets.append(ds)        
        return datasets
                
    def leaf_node(self):
        inf = info.Information(self.dataset)
        if len(self.dataset.attr_val_set['class']) == 1:
            return True
        elif len(self.dataset.instances) < self.m:
            return True
        #no attributes, just class
        elif len(self.dataset.attributes) == 1:
            return True
        elif inf.calc_max_gain() <= 0:
            return True
        return False

    def get_leaf_class(self):
        if len(self.dataset.instances) == 0:
            return self.default_class
        class_vals = list(self.dataset.attr_val_set['class'])
        class0 = class_vals[0]
        i = 0.
        for instance in self.dataset.instances:
            if instance.attribute['class'] == class0:
                i = i + 1
        if i > len(self.dataset.instances)/2:
            return class0
        elif i == len(self.dataset.instances)/2:
            return self.default_class
        return class_vals[1]

    def get_children(self):
        if self.leaf_node():
            #attr_val = list(self.dataset.attr_val_set['ca'])[0] 
#            print attr_val,'=',self.get_leaf_class(),len(self.dataset.instances)
#            print 'LEAF'
#            raw_input()
            return self.get_leaf_class()
        else:
            inf = info.Information(self.dataset)
            attr_mp = inf.calc_max_gain()
            branches = {}
            node = {}
            node[attr_mp[0]] = branches
            if attr_mp[1]:
                sub_nodes = self.split_tree_numeric(attr_mp)
                j = 0
                for sn,op in zip(sub_nodes,(' <= ',' > ')):
                    sn_tree = Tree(sn,self.default_class,self.m)
                    branches[op+str(attr_mp[1])] = sn_tree.get_children()
            else:
                sub_nodes = self.split_tree_string(attr_mp)
                for sn in sub_nodes:
                    try:
                        attr_val = list(sn.attr_val_set[attr_mp[0]])[0] 
                    except:
                        attr_val = sn.arff_val
                    self.pop_attribute(sn,attr_mp)

                    sn_tree = Tree(sn,self.default_class,self.m)
                    branches[' = '+attr_val] = sn_tree.get_children()
            return node

    def print_tree(self,tabs,node,tree_dict):
        class_list = list(self.dataset.attr_val_set['class'])
        if tree_dict == class_list[0] or tree_dict == class_list[1]:
            sys.stdout.write(' : '+tree_dict)
        elif tree_dict[node] == class_list[0] or tree_dict[node] == class_list[1]:
            sys.stdout.write(' : '+tree_dict[node])
        else:
            node_name = node
            tabs = tabs + '\t' 
            if node in self.dataset.attributes and len(tabs) > 1:
                pass
            else:
                tabs = tabs[:-1] + '|'
            for subnode in sorted(tree_dict[node]):
                if node in self.dataset.attributes:
                    print ''
                    new_line = tabs+node_name+subnode
                    sys.stdout.write(new_line[1:])
                    
                self.print_tree(tabs,subnode,tree_dict[node])
            
    def test_instance(self,instance,tree_dict):
        class_list = list(self.dataset.attr_val_set['class'])
        if tree_dict == class_list[0] or tree_dict == class_list[1]:
            return tree_dict
        else:
            if tree_dict.keys()[0] in self.dataset.attributes:
                attribute_name = tree_dict.keys()[0]
                attr_val = instance.attribute[attribute_name]
                for dict_val in tree_dict[attribute_name].keys():
                    dv = dict_val.split()[1]
                    op = dict_val.split()[0]
                    if op == '=':
                        op = op + '='
                    a = eval("'"+attr_val+"'"+op+"'"+dv+"'")
                    if a:
                        td = tree_dict[attribute_name][dict_val]
                        return self.test_instance(instance,td)

            
    def test_all_instances(self,tree_dict):
        num_correct = 0
        for instance in self.dataset.instances:
            pred_label = self.test_instance(instance,tree_dict) 
            act_label = instance.attribute_vals[-1]
            if pred_label == act_label:
                num_correct = num_correct + 1
            print pred_label, act_label
        print num_correct, len(self.dataset.instances)
        return float(num_correct)/len(self.dataset.instances)
        
class Metrics:

    def __init__(self,train_set,test_set,default_class,m=2):
        self.train_set = train_set
        self.test_set = test_set
        self.default_class = default_class
        self.m = m

    def create_strata(self):
        val1_list = []
        val2_list = []
        class_vals = self.train_set.attr_val_set['class']
        val1 = list(class_vals)[0]
        val2 = list(class_vals)[1]
        for instance in self.train_set.instances:
            if instance.attribute['class'] == val1:
                val1_list.append(copy.deepcopy(instance))
            else:
                val2_list.append(copy.deepcopy(instance))
        len_inst = len(self.train_set.instances)*1.
        return {len(val1_list)/len_inst:val1_list,len(val2_list)/len_inst:val2_list}


    def stratified_ds(self,ds_size):
        strata = self.create_strata()
        sub_train_set = copy.deepcopy(self.train_set)
        sub_train_set.instances = []
        instances = []
        for k in strata:
            num_sample = int(round(k * ds_size)) 
            rand_inst = random.sample(strata[k],num_sample)
            instances = instances + rand_inst
        sub_train_set.add_instances(instances[0:ds_size])
        return sub_train_set
            
    def test_train_set(self,ds_size):
        accur_results = []
        for i in range(10):
            #train
            sub_train_set = self.stratified_ds(ds_size)
            t = Tree(sub_train_set,self.default_class,self.m)
            t_dict = t.get_children()
            #test
            tt = Tree(self.test_set,self.default_class,self.m)
            accur_results.append(tt.test_all_instances(t_dict))
        a = min(accur_results)
        #average
        b = sum(accur_results) / float(len(accur_results))  
        c = max(accur_results)
        return [a,b,c]
        
