import data_structure as data

class Train():

    def __init__(self,dataset):
        self.dataset = dataset
        self.nodes = data.Nodes()

    #def calc_all_naive(self):
    #    len_all = 0
    #    for att in self.dataset.attr_val_set.values():
    #        print att
    #        len_all = len_all + len(att)
    #    return (len_all-2)

    def laplace(self,key_vals):
        """ for numerator: 
            simulate P(X1,X2...) if NO data 
        """
        att_keys = key_vals.keys()
        result = 1
        for key in att_keys:
            result = result*len(self.dataset.attr_val_set[key])
        return result
        
    def calc_P(self,Xx,Yy):
        """ P(Xx|Yy) = P(Xx,Yy)/P(Yy)  e.g ({'no_of_nodes_in':'5'},{'class':'metastases'}) """
        #print Xx,Yy
        total = float(len(self.dataset))
        if Yy:
            #conditioned
            laplace = self.laplace(Xx)
            num_Yy = total - self.key_val_not_in_dataset(Yy) + laplace
        else:
            #not conditioned. i.e P(Yy)
            laplace = self.laplace(Xx)
            num_Yy = total + laplace #2 classes
            Yy = {}
        num_Xx = total - self.key_val_not_in_dataset(dict(Xx.items() + Yy.items()))
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
        """ build self.nodes
        calc both P(Xx|Yy) and P(Xx,Xx1,|Yy) 
        where Xx = attributes, Yy = class_vals """
        attr_keys = list(self.dataset.attr_val_set.keys())
        attr_keys.remove('class')
        for Yy in self.dataset.attr_val_set['class']:
            #P(Yy)
            self.nodes[('class',Yy)] = self.calc_P({'class':Yy},None)
            for X in attr_keys:
                sub_attr_keys = list(attr_keys)
                sub_attr_keys.remove(X)
                for Xx in self.dataset.attr_val_set[X]:
                    self.nodes[(X,Xx)][('class',Yy)] = self.calc_P({X:Xx},{'class':Yy}) #P(Xx|Yy)
                    for X1 in sub_attr_keys:
                        for Xx1 in self.dataset.attr_val_set[X1]:
                            self.nodes[((X,Xx),(X1,Xx1))][('class',Yy)] = self.calc_P({X:Xx,X1:Xx1},{'class':Yy}) #P(Xx,Xx1,|Yy)
                            self.nodes[(X,Xx)][(X1,Xx1),('class',Yy)] = self.calc_P({X:Xx},{X1:Xx1,'class':Yy}) #P(Xx|Xx1,Yy)
                    

