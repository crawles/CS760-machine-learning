from collections import defaultdict
import itertools

def Nodes(): return defaultdict(Nodes)
        
class Dataset:

    def __init__(self):
        self.instances = []
        self.attr_val_set = {}

    def __iter__(self):
        return iter(self.instances)

    def __getitem__(self,index):
        return self.instances[index]

    def __len__(self):
        return len(self.instances)

    def add_attributes(self,attributes):
        """ add all attribtues at once  """
        self.attributes =  self.attributes + attributes

    def add_instances(self,instances):
        """ add instance list """
        self.instances = self.instances + instances


class Instance:

    def __init__(self,attribute_names,attribute_vals):
        self.attribute_names = attribute_names
        self.attribute_vals = attribute_vals
        self.attr_val_set = self.read_instance_line()

    def __iter__(self):
        return iter(self.attr_val_set)

    def __getitem__(self,attribute):
        return self.attr_val_set[attribute]

    def read_instance_line(self):
        """ assign feature/value to instance"""
        attr_val_set = {}
        self.attribute_vals[-1] = self.attribute_vals[-1].strip()
        for att_name,att_val in zip(self.attribute_names, self.attribute_vals):
            attr_val_set[att_name] = att_val
        return attr_val_set

def read_arff_file(file_name):
    attributes = []
    instances = []
    attr_val_set = {}
    d = Dataset()          
    for row in open(file_name):
        row_split = row.split()
        if row[0] == "%":
            pass
        elif row[0] == "@" and row[1:10] == "attribute":
            attr_name = (row_split[1][1:-1]) #strip quotes
            attributes.append(attr_name)                    
            s = row
            attr_val_set[attr_name] = s[s.find("{")+1:s.find("}")].replace(" ","").split(',')
        elif row[0] != "@":
           attribute_values = row.split(',') 
           instances.append(Instance(attributes,attribute_values))
    d.add_instances(instances)
    d.attr_val_set = attr_val_set
    return d


