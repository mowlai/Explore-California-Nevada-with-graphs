import header as h
def add_nodes(g, nodes):
    for el in nodes:
        g[el]=dict() #add a list of node prom 1 to the max number of nodes
    #g.add_nodes_from(list(range(1, h.NUM_VERTEX+1)))#add a list of node prom 1 to the max number of nodes

def add_phisical_distance_edges(g):
    with open(h.PATH_DISTANCE, 'r') as distances:
        for row in distances:
            row=row[2:]#remove the inizial 'a'
            comp=list(map(int, row.split()))
            adj=g.get(comp[0])
            if adj==None:
                g[comp[0]]={comp[1]:comp[2]}
            else:
                g[comp[0]][comp[1]]=comp[2]
            #g.add_edge(comp[0], comp[1], weight=comp[2])

def add_time_distance_edges(g):
    with open(h.PATH_TIME, 'r') as times:
        for row in times:
            row=row[2:]#remove the inizial 'a'
            comp=list(map(int, row.split()))
            adj=g.get(comp[0])
            if adj==None:
                g[comp[0]]={comp[1]:comp[2]}
            else:
                g[comp[0]][comp[1]]=comp[2]
            #g.add_edge(component[0], component[1], weight=component[2])

def add_network_distance_edges(g):
    with open(h.PATH_TIME, 'r') as times:
        for row in times:
            row=row[2:]#remove the inizial 'a'
            comp=list(map(int, row.split()))
            adj=g.get(comp[0])
            if adj==None:
                g[comp[0]]={comp[1]:1}
            else:
                g[comp[0]][comp[1]]=1
            #g.add_edge(component[0], component[1], weight=1)