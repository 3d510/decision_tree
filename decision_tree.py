import math

examples   = []
attributes = [] # notice last element of attributes is the output to classify
tree_nodes = []

def readArffInput(filepath):
    # declarations
    examples = []
    attributes = []
    lines = []
    # file reading
    file = open(filepath, 'r')
    for line in file:
        lines.append(line)
    # find all attributes and examples
    data_start_line = lines.index("@DATA\n")+1
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("@ATTRIBUTE"):
            line = lines[i]
            data = line.split()
            if data[2] == "STRING":
                attributes.append([data[1],set()])
            else:
                attributes.append([[data[1]],data[2][1:-1].strip().split(",")])
        elif i>=data_start_line:
            examples.append(line.strip().split(","))
    return examples,attributes

def pre_process_string_data():
    for i in range(len(attributes)):
        attribute = attributes[i]
        if len(attribute[1]) == 0:
            for example in examples:
                attribute[1].add(example[i])
            attribute[1] = list(attribute[1])

def create_node(parent_index,relation,chosen_att,examples_list,attributes_list):
    # node has a form of list
    # node: [[parent_index, relation, attribute chosen to split, node_index],
    #                      [list of examples to count],[list of attributes to choose]]
    # list of examples and attributes above are list of indexes
    # attribute chosen to split is index in attributes list
    new_node = []
    new_node_info = [parent_index,relation,chosen_att,len(tree_nodes)]
    new_node.append(new_node_info)
    new_node.append(examples_list)
    new_node.append(attributes_list)

    tree_nodes.append(new_node)
    return new_node

def split_examples_from_node(node, attribute_index):
    # split current examples in one node based on attribute
    split_examples = {}
    values = attributes[attribute_index][1]

    examples_indexes_in_this_node = node[1]
    for value in values:
        split_examples[value] = []
    for i in range(len(examples_indexes_in_this_node)):
        example = examples[examples_indexes_in_this_node[i]]
        split_examples[example[attribute_index]].append(examples_indexes_in_this_node[i])
    return split_examples

def chooseAttribute(node):
    attributes_to_choose = node[2]
    min = 1000000000
    chosen_att = -1
    for att in attributes_to_choose:
        importance_value = importance(node,att)
        if importance_value < min:
            min = importance_value
            chosen_att = att
    node[0][2] = chosen_att
    return chosen_att

def importance(node, attribute):
    split_examples = split_examples_from_node(node,attribute)
    overall_entropy = 0
    total_num_examples = len(node[1])
    for value,examples_list in split_examples.items():
        prob = len(examples_list)*1.0/total_num_examples
        overall_entropy += prob * cal_entropy(examples_list)
    return overall_entropy

def cal_entropy(examples_list):
    output_values = attributes[-1][1]
    output_count  = [0]*len(output_values)
    for example_index in examples_list:
        example = examples[example_index]
        for i in range(len(output_values)):
            if example[-1]==output_values[i]:
                output_count[i]+=1
    entropy = 0
    for count in output_count:
        if count==0:
            continue
        prob = count*1.0/len(examples_list)
        entropy -= prob*math.log(prob,2)
    return entropy

def is_leaf_node(node):
    # node: [[parent_index, relation, attribute chosen to split, node_index],
    #                      [list of examples to count],[list of attributes to choose]]
    if not node[2]:
        return True
    all_examples_belong_to_the_same_output_class = True
    output_class = examples[node[1][0]][-1]
    for example_index in node[1]:
        if examples[example_index][-1] != output_class:
            all_examples_belong_to_the_same_output_class = False
    return all_examples_belong_to_the_same_output_class

def split(node):
    if is_leaf_node(node): # return if there are no attributes to choose -> leaf node
        return
    best_att = chooseAttribute(node)
    values_for_best_att = attributes[best_att][1]
    node_index                     = node[0][3]
    examples_to_count              = node[1]
    attributes_to_choose_for_child = node[2][:]
    attributes_to_choose_for_child.remove(best_att)

    # create a dictionary mapping each value in values_for_best_att to a list of suitable examples
    split_examples = split_examples_from_node(node,best_att)
    # create node child nodes
    for value in values_for_best_att:
        if not split_examples[value]:
            child_node = create_node(node_index, value, "", split_examples[value], [])
            split(child_node)
        else:
            child_node = create_node(node_index,value,"",split_examples[value],attributes_to_choose_for_child)
            split(child_node)

def build_tree():
    tree = {}
    for i in range(len(tree_nodes)):
        tree[i]=[]
    for node in tree_nodes:
        if (node[0][0]==-1): # root node
            continue
        tree[node[0][0]].append(node[0][3])
    return tree

def print_tree():
    pass

# ---------------------------------------------main program-----------------------------------------------------------#

# read in data
examples, attributes = readArffInput("restaurant.arff")
pre_process_string_data()
# for i in range(len(examples)):
#     print i
#     print examples[i]
# for i in range(len(attributes)):
#     print i
#     print attributes[i]

# build decision tree
root_node = create_node(-1, "", "", range(len(examples)), range(len(attributes)-1))
split(root_node)
for i in range(len(tree_nodes)):
    print i
    print tree_nodes[i]

# print decision tree
tree = build_tree()
print tree
print_tree()

