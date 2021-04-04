import json

DIRECTED = True

def build_gexf(data):
    L = ['<?xml version="1.0" encoding="UTF-8"?>\n',
        '<gexf xmlns:viz="http:///www.gexf.net/1.1draft/viz" version="1.1" xmlns="http://www.gexf.net/1.1draft">\n',
        '<meta lastmodifieddate="2010-03-03+23:44">\n',
        '<creator>Gephi 0.7</creator>\n',
        '</meta>\n',
        '<graph defaultedgetype="{}" idtype="string" type="static">\n'.format('directed' if DIRECTED else 'undirected')]
    # append to L based on data
    node_lines = []
    edge_lines = []
    source_id_map = {}
    node_lines_count = 0
    edge_lines_count = 0
    for (label, edge_dict) in data.items():
        if label not in source_id_map:
            node_lines.append(create_node_line(node_lines_count, label))
            source_id_map[label] = node_lines_count
            node_lines_count += 1

        for edge in edge_dict['edges']:
            if edge not in source_id_map:
                node_lines.append(create_node_line(node_lines_count, edge))
                source_id_map[edge] = node_lines_count
                node_lines_count += 1
            edge_lines.append(create_edge_line(edge_lines_count, source_id_map[label], source_id_map[edge]))    
            edge_lines_count += 1
            """

            add edges to edge_lines
            check gexf format if deprecated

            """
            

    node_lines.insert(0, f'<nodes count="{node_lines_count}">\n')
    node_lines.append('</nodes>\n')
    edge_lines.insert(0, f'<edges count="{edge_lines_count}">\n')
    edge_lines.append('</edges>\n')
    L += node_lines + edge_lines + ['</graph>\n', '</gexf>\n']
    return L

def create_node_line(count, label):
    return f'<node id="{count}.0" label="{label}"/>\n'

def create_edge_line(count, label_id, target):
    return f'<edge id="{count}" source="{label_id}.0" target="{target}.0"/>\n'

def main():    
    with open('data.json') as f:
        data = json.load(f)

    L = build_gexf(data)
    with open('graph.gexf', 'w') as fp:
        fp.writelines(L)

if __name__ == '__main__':
    main()