import math
import data_structure as data
import helper_functions as helper

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
                            self.nodes[(X,Xx),(X1,Xx1),('class',Yy)] = self.calc_P({X:Xx,X1:Xx1,'class':Yy},None) #P(Xx,Xx1,Yy)
                    
class Information:

    def __init__(self,trn):
        self.trn = trn
        self.info = data.Nodes() 
        self.prims = data.Nodes() 

    def assign_cond_mut_info(self):
        attr_keys = list(self.trn.dataset.attr_val_set.keys())
        attr_keys.remove('class')

        for X in attr_keys:
            sub_attr_keys = list(attr_keys)
            sub_attr_keys.remove(X)
            for X1 in sub_attr_keys:
                IXX1_Y = 0
                for Xx in self.trn.dataset.attr_val_set[X]:
                    for Xx1 in self.trn.dataset.attr_val_set[X1]:
                        for Yy in self.trn.dataset.attr_val_set['class']:
                            X_Xx,X1_Xx1,Y_Yy = (X,Xx),(X1,Xx1),('class',Yy)
                            Ixx1_y = self.calc_cond_mut_info(X_Xx,X1_Xx1,Y_Yy)
                            IXX1_Y = IXX1_Y + Ixx1_y
                self.info[X][X1] = IXX1_Y 

    def calc_cond_mut_info(self,X_Xx,X1_Xx1,Y_Yy):
        Pxx1y = self.trn.nodes[(X_Xx,X1_Xx1,Y_Yy)]

        Pxx1_y =  self.trn.nodes[(X_Xx,X1_Xx1)][Y_Yy]

        Px_y = self.trn.nodes[(X_Xx)][Y_Yy]
        Px1_y = self.trn.nodes[(X1_Xx1)][Y_Yy]
        Px_yPx1_y = helper.log_mult(Px_y,Px1_y)  
        return Pxx1y*math.log(Pxx1_y/Px_yPx1_y,2)


    def prims_tree(self):
        attributes = self.trn.dataset.instances[0].attribute_names[:]
        init_vertex = attributes[0] #first attribute from arff
        attributes.remove('class')

        V_new = [init_vertex]
        V_cur = attributes[:]
        V_cur.remove(init_vertex)
        E_new = []
        while len(V_new) != len(attributes):
            uv_names = []
            uv = []
            for u in V_new:
                for v in V_cur:
                    uv_names.append((u,v))
                    uv.append(self.info[(u,v)])
                    
            uv_name = self.prims_max_edge(uv_names,uv)
            self.prims[uv_name]
            V_new.append(uv_name[1])
            V_cur.remove(uv_name[1])

    def prims_max_edge(self,uv_names,UV):
        #TODO test this with more examples
        attributes = self.trn.dataset.instances[0].attribute_names[:]
        attributes.remove('class')
        
        maxval = max(UV)
        max_uv_names = [uv_names[i] for i,uv in enumerate(UV) if uv == maxval]
        # choose first
        first_u = []
        for attribute in attributes:
            for uv_name in max_uv_names: 
                if uv_name[0] == attribute:
                    for _uv_name in max_uv_names: 
                        if _uv_name[0] == attribute:
                            first_u.append(uv_name)
                    break

        for attribute in attributes:
            for uv_name in first_u: 
                if uv_name[1] == attribute:
                    return uv_name


        
        

