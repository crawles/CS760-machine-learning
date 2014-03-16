import sys
import data_structure as data
import train
import test

train_set = data.read_arff_file(sys.argv[1])
test_set = data.read_arff_file(sys.argv[2])
trn = train.Train(train_set)
trn.calc_all_cond_prob()

I = train.Information(trn)
#trn.nodes['class','metastases']=.57
#trn.nodes['class','malign_lymph ']=1-.57

tst = test.Test(test_set,trn)
tst.print_naive()

