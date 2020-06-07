
from graphviz import Digraph
dot = Digraph(comment='The Round Table')

generate_ast_from = ('aaaaa', [('DEC', ('s', 'string', ('STRING', ''))), ('FOR', (
('DEC', ('i', 'int', ('INT', 5))), ('REL', (('REF', 'i'), '<', ('INT', 10))),
('ASSIGN', ('i', ('BINOP', (('REF', 'i'), '+', ('INT', 1))))),
[('ASSIGN', ('s', ('BINOP', (('REF', 's'), '+', ('STRING', 'a')))))])), ('REF', 's')])

counter = 0
def node(element):
    global counter
    dot.node(str(counter),str(element))
    counter+=1
    return counter-1

def ast3(data):
    parent = None
    children = None

    if not isinstance(data[0], str):
        parent = 'block'
        children = data 
    else:
        parent = data[0]
        children = data[1:]
    
    parent_id = node(parent)
    
    for child in children:
        if isinstance(child, list) or isinstance(child, tuple):
            child_parent = ast3(child)
            dot.edge(str(parent_id), str(child_parent))
        else:            
            node_id = node(child)
            dot.edge(str(parent_id), str(node_id))
    return parent_id
    

# define expression for ast here: 
print(ast3(generate_ast_from))

print(dot.source)
dot.render('ast.gv', view=True)