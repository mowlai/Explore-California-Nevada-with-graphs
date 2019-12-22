import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import utils as u
import itertools as it
import header as h
import pandas as pd
from func_3 import dijkstra
import folium
import webbrowser

def getPositions(nodes):
    '''
    Returns the dictionary of the position for each nodes; needs to visualizations task
    outputs:
        pos: dictionary of the positions
    '''
    pos=dict()
    for node in nodes:
        pos[node]=[coordinates["Longitude"][node-1], coordinates["Latitude"][node-1]]
    #print(pos)
    return pos

def visualize(nodes):

    pos=getPositions(nodes)
    print('pos\n', pos)
    
    m = folium.Map(location = (pos[nodes[0]][1]/1000000, 
                           pos[nodes[0]][0]/1000000), zoom_start = 13, tiles = 'openstreetmap')    
    locations=[]
    for node in nodes:
        locations.append((pos[node][1]/1000000, pos[node][0]/1000000))
    
    folium.PolyLine(locations).add_to(m)
    #display(m)
    m.save('plot_func_2.html')
    webbrowser.open("plot_func_2.html", new = 2)


def functionality_2():
    dataframes_names = ['coordinates', 'physical_dist', 'time_dist']


    globals()[dataframes_names[0]] = pd.read_csv(h.PATH_INFO, skiprows = 7, sep = " ", 
                                            delimiter = " ", names = ["Character", "ID_Node", "Longitude", "Latitude"],
                                            index_col = None, usecols = None, encoding = 'ISO-8859-1')

    eval(dataframes_names[0]).drop(columns = ["Character"], inplace = True)

    globals()[dataframes_names[1]] = pd.read_csv(h.PATH_DISTANCE, skiprows = 7, sep = " ", 
                                            delimiter = " ", names = ["Character", "Node_1", "Node_2", "Physical_distance"],
                                            index_col = None, usecols = None, encoding = 'ISO-8859-1')

    eval(dataframes_names[1]).drop(columns = ["Character"], inplace = True)

    globals()[dataframes_names[2]] = pd.read_csv(h.PATH_TIME, skiprows = 7, sep = " ", 
                                            delimiter = " ", names = ["Character", "Node_1", "Node_2", "Time_distance"],
                                            index_col = None, usecols = None, encoding = 'ISO-8859-1')
    eval(dataframes_names[2]).drop(columns = ["Character"], inplace = True)

    #print(globals())
    #physical_dist=globals()['physical_dist']
    #time_dist=globals()['time_dist']
    #coordinates=globals()['coordinates']
    complete = pd.merge(physical_dist, time_dist, on = ['Node_1', 'Node_2'])

    G = nx.from_pandas_edgelist(complete, 'Node_1', 'Node_2', ['Physical_distance', 'Time_distance'], create_using = nx.DiGraph())

    #imputs
    ok=False
    while not ok:
        inp=input('Give me a set of nodes (separated by space): ')
        nodes=list(map(int, inp.split()))
        distance=input('Give me a distance function:\ntime : the time distance;\nphysical : phisical distnce;\nnetwork : netword distance.\n')
        
        if distance not in ['time', 'physical', 'network']:
            print('Wrong inputs\nPlease reinsert\n')
        else:
            ok=True
    
    print(nodes, '\n', distance)
    


    
    paths={}#this save the paths betwenn the pair

    #the clique
    clique={node:dict() for node in nodes}

    for source in nodes: #iterate over the nodes to perform a clique
        for dest in nodes:
            if source!=dest: #if the pair of nodes are not the same node
                adj=clique[source]#obtain the enpty dictionary associated to che source
                print('dijkstraaaa')
                #djkComps=myDijkstra(g, source, dest)#calculate the distance
                djkComps=dijkstra(G, source, dest, distance)

                adj[dest]=djkComps[1]#add the neighbour with the weight
                paths[(source, dest)]=djkComps[0]#take the path
            else:
                adj=clique.get(source)
                adj[source]=0
                paths[(source, dest)]=[]
                
    # with ermutations
    inf=float('inf')
    minDist=inf
    minPerm=None
    perms=list(it.permutations(nodes))
    for perm in perms:
        w=0
        current=perm[0]
        for p in perm[1:]:# count the weight of the permutation
            w+=clique[current][p]
            current=p
        if w<minDist:
            minDist=w
            minPerm=perm
    if minPerm==None:# we can find a path among the nodes in input
        print('Not Possible')
        return
    current=minPerm[0]
    bigRoute=[]
    for el in minPerm[1:]:
        bigRoute.append((current, el))
        current=el

    print(bigRoute)

    '''
    finalNodes=[]
    completeRoute=[]
    for link in bigRoute:
        longPath=paths[link]#obtain the path that represent the the link between the two nodes
        edges=[]
        current=longPath[0]
        finalNodes.append(current)
        for node in longPath[1:]:
            edges.append((current, node))
            current=node
            finalNodes.append(current)

        completeRoute+=edges
    finalEdges=list(set(completeRoute))
    print('edges\n', finalEdges, '\nnodes\n', finalNodes)
    '''

    finalNodes=[]
    for link in bigRoute:
        longPath=paths[link]#obtain the path that represent the the link between the two nodes
        for node in longPath:
            finalNodes.append(node)

    #finalNodes=set(finalNodes)
    print('nodesSet\n', finalNodes)

    visualize(list(finalNodes))
    


