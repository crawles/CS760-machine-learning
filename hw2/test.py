class Test():

    def __init__(self,dataset,train_nodes):
        self.dataset = dataset
        self.nodes = train_nodes

    def naive_bayes(self):
        pass

    def cond_product(self,instance,Y):
        attr_keys = list(instance.attr_val_set.keys())
        attr_keys.remove('class')
        result = 1.0
        for Yy in Y:
            #calc P(Yy)
            prob = self.nodes[(Y,Yy)]
            result = result*prob
            for X in attr_keys:
                cond_prob = self.nodes[(X,instance.attr_val_set(Xx))][(Y,Yy)]
                result = result*cond_prob

        
