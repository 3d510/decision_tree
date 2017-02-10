examples   = []
attributes = [] # notice last element of attributes is the output to classify
tree_nodes = []
tree_node_index_counter = 0

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

def chooseAttribute(node):
    attributes_to_choose = node[2]
    max = -1000000000
    chosen_att = -1
    for att in attributes_to_choose:
        importance_value = importance(node,att)
        if importance_value > max:
            max = importance_value
            chosen_att = att
    node[0][2] = chosen_att
    return chosen_att

def importance(node, attribute):
    return 0

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
    split_examples = {}
    for value in values_for_best_att:
        split_examples[value] = []
    for i in range(len(examples_to_count)):
        example = examples[examples_to_count[i]]
        split_examples[example[best_att]].append(examples_to_count[i])

    # create node child nodes
    for value in values_for_best_att:
        if not split_examples[value]:
            continue # if there are no examples with this value for best attribute, skip
        child_node = create_node(node_index,value,"",split_examples[value],attributes_to_choose_for_child)
        split(child_node)


# ---------------------------------------------main program-----------------------------------------------------------#

# read in data
examples, attributes = readArffInput("restaurant.arff")
pre_process_string_data()
# for e in examples:
#     print e
# for a in attributes:
#     print a

# build decision tree
root_node = create_node(-1, "", "", range(len(examples)), range(len(attributes)))
split(root_node)
# for node in tree_nodes:
#     print node

# print decision tree



