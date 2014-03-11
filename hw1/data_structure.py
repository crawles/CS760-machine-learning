import information as info

def read_arff_file(file_name):
    attributes = []
    instances = []
    arff_attr_val_set = {}
    d = Dataset()          
    for row in open(file_name):
        row_split = row.split()
        if row[0] == "@" and row[1:10] == "attribute":
#            d.add_attribute(row_split[1][1:-1])
            attr_name = (row_split[1][1:-1])
            attributes.append(attr_name)                    
            try:
                arff_attr_val_set[attr_name] = set(find_between(row,'{','}').split(', '))
            except:
                pass
        elif row[0] != "@":
           attribute_values = row.split(',') 
#           d.add_instance(Instance(attributes,attribute_values))
           instances.append(Instance(attributes,attribute_values))
    d.add_attributes(attributes)
    d.add_instances(instances)
    d.arff_attr_val_set = arff_attr_val_set
    return d

#parse possible attribute values
def find_between(s,first,last):
    start = s.index( first ) + len( first ) +1
    end = s.index( last, start )
    return s[start:end]

class Dataset:

        def __init__(self):
            self.instances = []
            self.attributes = []
            self.attr_val_set = {}
            self.arff_attr_val_set = {}
            self.attr_midpoints = {}
            self.arff_val = {}

#        def add_attribute(self,attribute):
#            self.attributes.append(attribute)
#
#        def add_instance(self,instance):
#            self.instances.append(instance)

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
            for attribute_name in self.attributes:
                self.attr_val_set[attribute_name] = []
            for instance in instances:
                for attribute_name in self.attributes:
                    attribute_value = instance.attribute[attribute_name]
                    self.attr_val_set[attribute_name] = [attribute_value] + self.attr_val_set[attribute_name]
            # remove duplicates AND create midpoint list
            for attribute_name in self.attributes:
                self.attr_val_set[attribute_name] = set(self.attr_val_set[attribute_name])
                # midpoint list
                if info.numeric_att(self,attribute_name):
                    mp = info.Midpoint(self,attribute_name)
                    m_pts = mp.find_midpoints(attribute_name)
                    self.attr_midpoints[attribute_name] = m_pts
                    #if len(m_pts) == 0:
                    #    self.attributes.remove(attribute_name)

        def pop_attribute_mp(self,attr_mp):
            attr = attr_mp[0]
            mp = attr_mp[1]
            self.attr_midpoints[attr].remove(mp)

        def remove_node():
            pass

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
