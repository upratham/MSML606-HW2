def csv_to_list(filename):
    with open(filename, 'r') as file:
        data_list = []
        for line in file:
           line = line.strip().replace('"', '').split(",")
           data_list.append(line)
    return data_list

def construct_tree(filename) -> dict:
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
                right = stack.pop()
                left = stack.pop()
                stack.append({"value": node, "left": left, "right": right})
        root_node[str(i)] = stack[0]
        if len(stack)!=1:
            raise ValueError('Invalid expression: missing operands')
    
    return root_node


def _split_csv_with_quotes(line):

    fields = []
    cur = []
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            in_quotes = not in_quotes
        elif ch == ',' and not in_quotes:
            fields.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    fields.append("".join(cur).strip())

    # Remove surrounding quotes if any
    cleaned = []
    for f in fields:
        f = f.strip()
        if len(f) >= 2 and f[0] == '"' and f[-1] == '"':
            f = f[1:-1]
        cleaned.append(f)
    return cleaned

def read_rows(filename):
    """
    Reads p2_traversals.csv and returns a list of rows:
      each row is (postfix_list, expected_prefix_list, expected_infix_list, expected_postfix_list)
    """
    rows = []
    with open(filename, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            cols = _split_csv_with_quotes(line)
            # In case of any stray parsing issues, skip bad lines
            if len(cols) < 4:
                continue

            postfix = cols[0].split(",") if cols[0] else []
            exp_prefix = cols[1].split(",") if cols[1] else []
            exp_infix = cols[2].split(",") if cols[2] else []
            exp_postfix = cols[3].split(",") if cols[3] else []
            rows.append((postfix, exp_prefix, exp_infix, exp_postfix))
    return rows


def construct_tree_2(tokens):
    """
    Builds a proper binary expression tree from postfix token list.
    Node format: {"value": token, "left": <node>, "right": <node>}
    Leaf nodes have left/right = None.
    """
    ops = {"+", "-", "*", "/"}
    stack = []
    for t in tokens:
        if t not in ops:
            stack.append({"value": t, "left": None, "right": None})
        else:
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression: not enough operands")
            right = stack.pop()
            left = stack.pop()
            stack.append({"value": t, "left": left, "right": right})
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression: missing operators/operands")
    return stack[0]

def prefix_expression(root):
    if root is None:
        return []
    out = [str(root["value"])]
    out += prefix_expression(root["left"])
    out += prefix_expression(root["right"])
    return out

def postfix_expression(root):
    if root is None:
        return []
    out = []
    out += postfix_expression(root["left"])
    out += postfix_expression(root["right"])
    out.append(str(root["value"]))
    return out

def infix_expression(root):
    """
    In-order traversal with parentheses as separate list items.
    Parenthesizes every internal node (matches the provided expected format).
    """
    if root is None:
        return []
    l = root["left"]
    r = root["right"]
    v = str(root["value"])

    # leaf
    if l is None and r is None:
        return [v]

    # internal
    return ["("] + infix_expression(l) + [v] + infix_expression(r) + [")"]


def main():
    print("Solution for Problem 1: Constructing Expression Tree")
    filename = 'data\p1_construct_tree.csv'
    root = construct_tree(filename)
    for key, value in root.items():
        print(f'Root node for expression : {int(key)+1}: {value}')

    print("Solution for Problem 2: Constructing Expression Tree")
    
    filename_2 = "data/p2_traversals.csv"
    rows = read_rows(filename_2)
    results = []
    all_ok = True
    for idx, (postfix_in, exp_pre, exp_in, exp_post) in enumerate(rows):
        tree = construct_tree_2(postfix_in)

        got_pre = prefix_expression(tree)
        got_in = infix_expression(tree)
        got_post = postfix_expression(tree)

        ok = (got_pre == exp_pre) and (got_in == exp_in) and (got_post == exp_post)
        if not ok:
            all_ok = False

        results.append({
            "row": idx + 1,
            "input_postfix": postfix_in,
            "prefix": got_pre,
            "infix": got_in,
            "postfix": got_post,
            "matches_expected": ok
        })


    print("Total rows:", len(results))
    print("All match expected:", all_ok)

    for r in results:
        print(f"Row {r['row']}: matches expected? {r['matches_expected']}")
        print(f"  Input Postfix: {r['input_postfix']}")
        print(f"  Got Prefix: {r['prefix']}")
        print(f"  Got Infix: {r['infix']}")
        print(f"  Got Postfix: {r['postfix']}")
    



   












    return 0




if __name__ == "__main__":
    main()