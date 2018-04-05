import csv
import graphviz as gv
import functools

graph = functools.partial(gv.Graph, format='pdf')
digraph = functools.partial(gv.Digraph, format='pdf')
nodes = []
edges = []
styles = {
    'graph': {
        'label': 'A Fancy Graph',
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'BT',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'hexagon',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    }
}

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph


def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph


G = eval ( open('./dict_name.txt', 'r').read() );

i=1
for stop, successors in G.iteritems() :
    if i > 500:
        break
    i = i + 1
    note = [] ##arrival stops which has been already dessined
    nodes.append((stop.decode('utf8'), {'label':stop}))
    for dist, successor in successors:
        if successor not in note:
            edges.append((stop, successor))
            note.append(successor)

result = add_edges(add_nodes(digraph(), nodes), edges)
#result = apply_styles(result, styles)
result.render('img/graphe_stops_2')
