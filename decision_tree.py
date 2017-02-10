def readInput(filepath):
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

def pre_process_string_data(examples,attributes):
    for i in range(len(attributes)):
        attribute = attributes[i]
        if len(attribute[1]) == 0:
            for example in examples:
                attribute[1].add(example[i])
            attribute[1] = list(attribute[1])

# main program

# read in data
examples,attributes = readInput("C:/Users/Doan Duy Duc/Desktop/restaurant.arff")
pre_process_string_data(examples,attributes)
for e in examples:
    print e
for a in attributes:
    print a

# build decision tree