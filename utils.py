import header as h
def add_nodes(g):
    g.add_nodes_from(list(range(1, h.NUM_VERTEX+1)))#add a list of node prom 1 to the max number of nodes

def add_phisical_distance_edges(g):
    with open(h.PATH_DISTANCE, 'r') as distances:
        for row in distances:
            row=row[2:]#remove the inizial 'a'
            component=row.split()
            g.add_edge(component[0], component[1], weight=component[2])

def add_time_distance_edges(g):
    with open(h.PATH_TIME, 'r') as times:
        for row in times:
            row=row[2:]#remove the inizial 'a'
            component=row.split()
            g.add_edge(component[0], component[1], weight=component[2])

def add_network_distance_edges(g):
    with open(h.PATH_TIME, 'r') as times:
        for row in times:
            row=row[2:]#remove the inizial 'a'
            component=row.split()
            g.add_edge(component[0], component[1], weight=1)