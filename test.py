key = 1
keymap = {}
def encode_tree(tree):
    global key, keymap
    encoded = []
    for item in tree:
        if isinstance(item, str):
            encoded.append(key)
            keymap[key] = item
            key += 1
        elif isinstance(item, list):
            encoded.append(encode_tree(item))

    return encoded


graph = dict()
def build_graph(tree):
    global graph
    if isinstance(tree, list):
        current = tree[0]
    else:
        current = tree

    if current not in graph:
        graph[current] = []

    if isinstance(tree, list):
        children = tree[1:]
        for child in children:
            if isinstance(child, list):
                graph[current].append(child[0])
                build_graph(child)
            else:
                graph[current].append(child)
                build_graph(child)



expr = ['~', ['&', ['|', ['~', ['~', 'a']], 'b'], ['|', ['~', 'b'], 'a']]]
# encoded = encode_tree(expr)
# build_graph(encoded)

# for node, edges in graph.items():
#     print(node, end=' : ')
#     for edge in edges:
#         print(edge, end=' ')
#     print()


string = ''
def __printable(tree):
    global string
    lt_tree = None
    rt_tree = None

    if isinstance(tree, list) and len(tree) >= 1:
        current = tree[0]
        if len(tree) >= 2:
            lt_tree = tree[1]

        if len(tree) >= 3:
            rt_tree = tree[2]

    else:
        current = tree

    if current == '~':
        string += current
        if isinstance(lt_tree, list):
            string += '('
        __printable(lt_tree)
        if isinstance(lt_tree, list):
            string += ')'

    else:
        if lt_tree is not None:
            string += '('
            __printable(lt_tree)
            string += ' '

        string += current

        if rt_tree is not None:
            string += ' '
            __printable(rt_tree)
            string += ')'


__printable(expr)
print(string)
