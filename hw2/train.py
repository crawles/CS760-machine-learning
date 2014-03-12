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

    def calc_all_cond_prob(self):
        """ generate all P(Xx|Yy) where Yy = class_val1 or class_val2 or None """
        for Yy in self.dataset.attr_val_set['class'] + [None]:
             for Xx in self.dataset.
