import operator
import copy
import math
from itertools import groupby
import numpy as np

def numeric_att(dataset,attribute_name):
    #print attribute_name
    #raw_input()
    try:
        float(dataset.instances[0].attribute[attribute_name])
        return True
    except:
        pass
    return False

class Information:

    def __init__(self,dataset):
        self.dataset = dataset

    def calc_cond_prob(self,attribute_name,attribute_value,class_val):
        """ P(Y=y|X=x) """
        pXn = 0.
        pXYn = 0.
        for instance in self.dataset.instances:
            if instance.attribute[attribute_name] == attribute_value:
                pXn = pXn + 1
                if instance.attribute['class'] == class_val:
                    pXYn = pXYn + 1
        pXd = pXYd = len(self.dataset.instances)
        pX = pXn/pXd
        pXY = pXYn/pXYd
        if pX == 0:
            return 0
        return pXY/pX

    def calc_spec_cond_entropy(self,attribute_name,attribute_value):
        """ H(Y,X=x), i.e P(Y=y|X=x)*log2(P(Y=y|X=x)) """
        spec_cond_entropy = 0.
        for c in self.dataset.attr_val_set['class']:
            cond_prob = self.calc_cond_prob(attribute_name,attribute_value,c)
            if cond_prob == 0:
                pass
            else:
                spec_cond_entropy = (- cond_prob*math.log(cond_prob,2) +   
                                    spec_cond_entropy)
        return spec_cond_entropy

    def calc_cond_entropy_string(self,attribute_name):
        """ H(Y|X) for string attributes"""
        cond_entropy = 0.
        for av in self.dataset.attr_val_set[attribute_name]:
            #calc pX
            pXn = 0.
            for instance in self.dataset.instances:
                if instance.attribute[attribute_name] == av:
                    pXn = pXn + 1
            pXd = len(self.dataset.instances)
            pX = pXn/pXd
            #calc
            spec_cond_entropy = self.calc_spec_cond_entropy(attribute_name,av)
            cond_entropy = cond_entropy + pX*spec_cond_entropy
        return cond_entropy

    def calc_cond_entropy_at_split(self,attribute_name,split_pt):
        """ H(Y|X) for numeric attribute using one split point"""
        ds = copy.deepcopy(self.dataset)
        attribute_index = ds.instances[0].attribute_names.index(attribute_name)
        for instance in ds.instances:
            attr_val = float(instance.attribute[attribute_name])
            if attr_val <= float(split_pt):
                bin_value = 'under'
            else:
                bin_value = 'over'
            instance.attribute[attribute_name] = bin_value
            instance.attribute_vals[attribute_index] = bin_value
        ds.attr_val_set = {}
        ds.get_attribute_values(ds.instances)
        info_ds = Information(ds)
        cond_entropy = info_ds.calc_cond_entropy_string(attribute_name)
        return cond_entropy

    def calc_cond_entropy_numeric(self,attribute_name):
        """ max(H(Y|X)) for numeric attribute testing all split points"""
        midpoints = self.dataset.attr_midpoints[attribute_name]
        if not midpoints:
            return (0,1)
        mpt_entropies = []
        for mpt in midpoints:
            mpt_entropy = self.calc_cond_entropy_at_split(attribute_name,mpt)
            mpt_entropies.append(mpt_entropy)
        min_i = mpt_entropies.index(min(mpt_entropies))
        return (midpoints[min_i],min(mpt_entropies)) 
            
        
    def calc_gain(self,attribute_name):
        i = 0.
        class_vals = self.dataset.attr_val_set['class']
        for instance in self.dataset.instances:
            if instance.attribute['class'] == list(class_vals)[0]:
                i = i + 1
        pr = i/(len(self.dataset.instances))
        if pr == 1:
            current_entropy = -((pr)*math.log(pr,2))
        else:
            current_entropy = -((pr)*math.log(pr,2)) - ((1-pr)*math.log(1-pr,2));
        if not numeric_att(self.dataset,attribute_name):
            cond_entropy = self.calc_cond_entropy_string(attribute_name)
            mp = None
        else:
            mp_cond_entropy = self.calc_cond_entropy_numeric(attribute_name)
            mp = mp_cond_entropy[0]
            cond_entropy = mp_cond_entropy[1]
        gain = current_entropy - cond_entropy
        return (mp,gain)

    def is_number(self):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def calc_max_gain(self):
        attrs = []
        gains = []
        midpoints = []
        possible_attributes = copy.deepcopy(self.dataset.attributes)
        possible_attributes.remove('class')
        for i,att in enumerate(possible_attributes):
            attrs.append(att)
            mp_g = self.calc_gain(att)
            mp = mp_g[0]
            g = mp_g[1]
            gains.append(g)
            midpoints.append(mp)
        max_i = gains.index(max(gains))
        return (attrs[max_i],midpoints[max_i])

class Midpoint:

    def __init__(self, dataset, attribute_name):
        self.dataset = dataset
        self.midpoints = self.find_midpoints(attribute_name)

    def sort_numeric_attribute(self, attribute_name):
        """ returns sort key_val list """
        att_class = []
        for instance in self.dataset.instances:
            numeric_val = float(instance.attribute[attribute_name])
            instance_class = instance.attribute['class']
            key_val = att_class.append((numeric_val,instance_class))
        att_class.sort(key=operator.itemgetter(0))
        return att_class

    def group_numeric_attribute(self,att_class):
        """ return list of key_val groups """
        grouped_numeric = []
        for key, group in groupby(att_class,lambda x:x[0]):
            val_classes=[]
            val_classes.append(key)
            for c in group:
                val_classes.append(c[1])
            grouped_numeric.append(val_classes)
        return grouped_numeric

    def unanimous_class(self,val_classes):
        """ input list of [attribute_value,instance_class1,...,instance_class_n] 
        output: class if unanimous else: None """
        x = val_classes[1:]
        if (x.count(x[0]) == len(x)):
            return x[0]
        return False

    def split(self,val1,val2):
        return (val1 + val2)/2.
    
    def find_midpoints(self,attribute_name):
        sorted_numeric = self.sort_numeric_attribute(attribute_name)
        grouped_numeric = self.group_numeric_attribute(sorted_numeric)
        midpoints = []
        for i in range(len(grouped_numeric)-1):
            val_class1 = grouped_numeric[i]
            val_class2 = grouped_numeric[i+1]
            if (self.unanimous_class(val_class1) and self.unanimous_class(val_class2) 
                 and self.unanimous_class(val_class1) == self.unanimous_class(val_class2)):
                pass
            else:
                split_pt = self.split(val_class1[0],val_class2[0])
                midpoints.append(split_pt)
        return midpoints
