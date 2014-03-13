import math
import helper_functions as helper

class Test():

    def __init__(self,dataset,trn):
        self.dataset = dataset
        self.nodes = trn.nodes

    def naive_bayes(self):
        class_val1 = self.dataset.attr_val_set['class'][0]
        labels = []
        for instance in self.dataset:
            numer = self.cond_product(instance,[class_val1])
            denom = self.cond_product(instance,self.dataset.attr_val_set['class'])
            labels.append([class_val1,numer/denom])

        class_val2 = self.dataset.attr_val_set['class'][1]
        for i,class_prob in enumerate(labels):
            if class_prob[1]<.5:
                class_prob[0] = class_val2
                class_prob[1] = 1-class_prob[1]
                labels[i] = class_prob
            labels[i][1]= str(class_prob[1])
        return labels

    def print_naive(self):
        labels = self.naive_bayes()
        num_correct = 0
        for line,instance in zip(labels,self.dataset):
            print line[0],instance['class'],line[1]
            if line[0]==instance['class']:
                num_correct = num_correct + 1
        print num_correct

    def cond_product(self,instance,Y):
        """ calc add_sum(P(Yyi)*mult_sum(P(Xxi|Yyi))) """
        #TODO could use this for info gain
        attr_keys = list(instance.attr_val_set.keys())
        attr_keys.remove('class')
        sum_result = 0
        for Yy in Y:
            mult_result = 1.0
            prob = self.nodes[('class',Yy)] #calc P(Yy) 
            mult_result = helper.log_mult(mult_result,prob)
            for X in attr_keys:
                cond_prob = self.nodes[(X,instance.attr_val_set[X])][('class',Yy)]
                mult_result = helper.log_mult(mult_result,cond_prob)
            sum_result = sum_result + mult_result

        return sum_result

        
