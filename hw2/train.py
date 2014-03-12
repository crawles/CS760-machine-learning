import data_structure as data

class Train():

    def __init__(self,dataset):
        self.dataset = dataset
        self.nodes = data.Nodes()

    def calc_P(self,Xx,Yy):
        """ P(Xx|Yy) e.g ({'no_of_nodes_in':'5'},{'class':'metastases'}) """
        total = float(len(self.dataset))
        if Yy:
            num_Yy = total - self.key_val_not_in_dataset(Yy)    
        else:
            num_Yy = total
            Yy = {}

        num_Xx = total - self.key_val_not_in_dataset(dict(Xx.items() + Yy.items()))
        return num_Xx/num_Yy

    def key_val_not_in_dataset(self,key_vals):
        """ P(!Xx,!Yy,...) """
        n = 0
        for instance in self.dataset:
            for key in key_vals:
                if instance[key] != key_vals[key]:
                    n = n + 1
                    break
        return n

    def get_key_val(self,key):
        return {key:self.dataset.attr_val_set(key)}

    def calc_all_cond_prob(self):
        """ calc both P(Xx|Yy) and P(Xx,Xx1,|Yy) 
        where Xx = attributes, Yy = class_vals """
        attr_keys = list(self.dataset.attr_val_set.keys())
        attr_keys.remove('class')
        for Yy in self.dataset.attr_val_set['class']:
            print 1111
            self.nodes[('class',Yy)] = self.calc_P({'class':Yy},None)
            for X in attr_keys:
                for Xx in self.dataset.attr_val_set[X]:
                    self.nodes[{(X,Xx)}][('class',Yy)] = self.calc_P({X:Xx},{'class':Yy})
                    for X1 in attr_keys:
                        for Xx1 in self.dataset.attr_val_set[X1]:
                            self.nodes[{(X,Xx),(X1,Xx1)}][('class',Yy)] = self.calc_P({X:Xx},{X:Xx1},{'class':Yy})
                    
