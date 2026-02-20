def csv_to_list(filename):
    with open(filename, 'r') as file:
        data_list = []
        for line in file:
           line = line.strip().replace('"', '').split(",")
           data_list.append(line)
    return data_list

def generate_tree(filename) -> dict:
    operators = ['+', '-', '*', '/', '(', ')']
    root_node = {}
    input_list = csv_to_list(filename)
    for i, input in enumerate(input_list):
        stack = []
        for node in input:
            if node not in operators:
                stack.append(node)
            else:
                if len(stack)<2:
                    raise ValueError('Invalid expression:not enough operands')
                stack.pop()
                stack.pop()
                stack.append([node])
        root_node[str(i)] = stack[0]
        if len(stack)!=1:
            raise ValueError('Invalid expression: missing operands')
    
    return root_node








def main():
    print("Solution for Problem 1: Constructing Expression Tree")
    filename = 'data\p1_construct_tree.csv'
    root = generate_tree(filename)
    for key, value in root.items():
        print(f'Root node for expression : {int(key)+1}: {value}')

    return 0


















if __name__ == "__main__":
    main()