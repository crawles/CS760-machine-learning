import information as info

#parse possible attribute values
def find_between(s,first,last):
    start = s.index( first ) + len( first ) +1
    end = s.index( last, start )
    return s[start:end]

class Dataset:

        def __init__(self):
            self.instances = []
            self.attributes = []
            #TODO remove val_set?
            self.attr_val_set = {}

        def add_attributes(self,attributes):
            """ add all attribtues at once 
            and get all possible attribute values """
            self.attributes =  self.attributes + attributes

        def add_instances(self,instances):
            """ add all instances at once """
            self.instances = self.instances + instances
            self.get_attribute_values(self.instances)

        def get_attribute_values(self,instances):
            """ get all possible attribute values,
            after you add all instances"""
            #attr_val_set keys
            for attribute_name in self.attributes:
                self.attr_val_set[attribute_name] = []
                print attribute_name
            #attr_val_set values
            #for instance in instances:
            #    for attribute_name in self.attributes:
            #        attribute_value = instance.attribute[attribute_name]
            #        self.attr_val_set[attribute_name] = [attribute_value] + self.attr_val_set[attribute_name]
            ## remove duplicates 
            #for attribute_name in self.attributes:
            #    self.attr_val_set[attribute_name] = set(self.attr_val_set[attribute_name])

class Instance:

    def __init__(self,attribute_names,attribute_vals):
        self.attribute_names = attribute_names
        self.attribute_vals = attribute_vals
        self.read_instance_line()

    def read_instance_line(self):
        """ assign feature/value to instance"""
        self.attribute = {}
        self.attribute_vals[-1] = self.attribute_vals[-1].strip()
        for att_name,att_val in zip(self.attribute_names, self.attribute_vals):
            self.attribute[att_name] = att_val

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
           #TODO revamp instance
           instances.append(Instance(attributes,attribute_values))
    d.add_attributes(attributes)
    d.add_instances(instances)
    d.attr_val_set = attr_val_set
    return d


