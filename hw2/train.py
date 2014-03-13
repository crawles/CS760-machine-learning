import data_structure as data

class Train():

    def __init__(self,dataset):
        self.dataset = dataset
        self.nodes = data.Nodes()

    def calc_all_naive(self):
        len_all = 0
        for att in self.dataset.attr_val_set.values():
            print att
            len_all = len_all + len(att)
        return (len_all-2)

    def calc_P(self,Xx,Yy):
        """ P(Xx|Yy) = P(Xx,Yy)/P(Yy)  e.g ({'no_of_nodes_in':'5'},{'class':'metastases'}) """
        #print Xx,Yy
        total = float(len(self.dataset))
        if Yy:
            #conditional
            lap = len(self.dataset.attr_val_set[Xx.keys()[0]])
            num_Yy = total - self.key_val_not_in_dataset(Yy) + lap
        else:
            #not conditioned. i.e P(Yy)
            num_Yy = total + 2 #2 classes
            Yy = {}
        num_Xx = total - self.key_val_not_in_dataset(dict(Xx.items() + Yy.items()))
        #TODO check this
        return (num_Xx+1)/(num_Yy) #laplace

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
            #P(Yy)
            self.nodes[('class',Yy)] = self.calc_P({'class':Yy},None)
            for X in attr_keys:
                for Xx in self.dataset.attr_val_set[X]:
                    #P(Xx|Yy)
                    self.nodes[(X,Xx)][('class',Yy)] = self.calc_P({X:Xx},{'class':Yy}) 
                    for X1 in attr_keys:
                        for Xx1 in self.dataset.attr_val_set[X1]:
                            #P(Xx,Xx1,|Yy)
                            #TODO need this for TAN
                            #self.nodes[((X,Xx),(X1,Xx1))][('class',Yy)] = self.calc_P({X:Xx},{X:Xx1,'class':Yy}) 
                            pass
                    

