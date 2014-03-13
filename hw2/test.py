import math
import helper_functions as helper

class Test():

    def __init__(self,dataset,trn):
        self.dataset = dataset
        self.nodes = trn.nodes

    def naive_bayes(self):
        for instance in self.dataset:
            numer = self.cond_product(instance,[instance.attr_val_set['class']])
            denom = self.cond_product(instance,self.dataset.attr_val_set['class'])
            #print numer/denom

    def cond_product(self,instance,Y):
        """ calc add_sum(P(Yyi)*mult_sum(P(Xxi|Yyi))) """
        #TODO could use this for info gain
        attr_keys = list(instance.attr_val_set.keys())
        attr_keys.remove('class')
        sum_result = 0
        for Yy in Y:
            mult_result = 1.0
            #calc P(Yy)
            prob = self.nodes[('class',Yy)]
            mult_result = helper.log_mult(mult_result,prob)
            for X in attr_keys:
                cond_prob = self.nodes[(X,instance.attr_val_set[X])][('class',Yy)]
                #print X,instance.attr_val_set[X],'class',Yy,cond_prob
                mult_result = helper.log_mult(mult_result,cond_prob)
            sum_result = sum_result + mult_result
            #print Y,Yy,sum_result,mult_result
            #print mult_result

        return sum_result

        
