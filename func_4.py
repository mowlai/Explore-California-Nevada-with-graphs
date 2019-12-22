import networkx as nx
import matplotlib.pyplot as plt
import header as h
import pandas as pd
import folium
import os
import webbrowser
from func_3 import dijkstra

def myNearestNeighbour(clique, s, e, nodes):
    '''
    Implementation of the algo nearest neighbour to implement the euristic solution
    inputs:
        clique: a clique graph
        s: source node
        e: destination node
    outputs:
        out: the path made by the algo N.N.
    '''
    #nodes=list(clique.keys())#nodes in the clique
    out=[s]#start costructing the output path
    nodes.pop(0)#remove the source...
    nodes.pop(-1)#and the destination
    current=s#the current node 
    while nodes!=[]:
        #find the nearest
        minDist=float('inf')
        minNode=None
        for node in nodes:
            dist=clique[current][node]
            if dist<minDist:
                minDist=dist
                minNode=node
            
        #add to out
        if minNode==None:#if there isn't a minimum path
            return [None]
        else:
            out.append(minNode)#append the minimum to the path
            current=minNode#change the current
            nodes.remove(minNode)#remove the node in the path
    if clique[current][e]==float('inf'):#if there isn't a path from the last to the dest
        out.append(None)#append none
    else:
        out.append(e)#adding the destination
    return out

def getEdgesLabels(g):
    '''
    return the lables of the edges
    '''
    labels=dict()
    for k, v in g.items():
        for adj, weight in v.items():
            labels[(k, adj)]=weight
    return labels

def visualize2(pos, start):
    
    m = folium.Map(location = (pos[start][1]/1000000, 
                           pos[start][0]/1000000), zoom_start = 13, tiles = 'openstreetmap')
    locations=[]
    for node in list(pos.keys()):
        folium.CircleMarker(location = (pos[node][1]/1000000, 
                                        pos[node][0]/1000000), radius = 3, line_color = '#3186cc', fill_color = '#FFFFFF', fill_opacity = 0.7, fill = True).add_to(m)
        
        locations.append((pos[node][1]/1000000, pos[node][0]/1000000))
    folium.PolyLine(locations).add_to(m)
    #display(m)
    m.save('Plot_func_4.html')
    webbrowser.open("Plot_func_4.html", new = 2)
    


def visualize(gf4, nv, wv):
    
    pos=getPositions(list(gf4.keys()))


    gg=nx.DiGraph(gf4)
    fig=plt.figure()

    if nv:
        nx.draw(gg, pos, with_labels=True, width=0.2, edge_color='#00FFFF', node_color='white', font_size=14, font_color='#1f78b4')
    else:
        nx.draw(gg, pos, width=0.2, edge_color='#00FFFF', node_color='white', font_size=14, font_color='#1f78b4')

    if wv:
        labels=getEdgesLabels(gf4)
        nx.draw_networkx_edge_labels(gg, pos,labels, label_pos=0.20, font_color='#002041', edge_color='#00FFFF')


    '''
    nx.draw(gg, pos, with_labels=True, edge_color='#00FFFF', node_color='white', font_size=14, font_color='#1f78b4')
    nx.draw_networkx_edge_labels(gg, pos, labels, label_pos=0.20, font_color='#002041', font_weight='normal')
    #nx.draw_networkx_edges(gg, pos, edgelist=[(1, 2)], arrowstyle='circle')
    '''

    fig.set_facecolor("#00000F")
    plt.show()

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
    

def printNodes():
    nodes=pd.read_csv(h.PATH_INFO, sep=' ', names=['a', 'node', 'lat', 'lon'], delimiter=None, index_col=None, usecols=None)
    nodes.plot(kind='scatter', x='lon', y='lat')



def functionality_4():

    files_names = os.listdir('./Files')
    
    dataframes_names = ['coordinates', 'physical_dist', 'time_dist']


    globals()[dataframes_names[0]] = pd.read_csv(os.getcwd() + '\\Files\\' + files_names[0], skiprows = 7, sep = " ", 
                                            delimiter = " ", names = ["Character", "ID_Node", "Longitude", "Latitude"],
                                            index_col = None, usecols = None, encoding = 'ISO-8859-1')

    eval(dataframes_names[0]).drop(columns = ["Character"], inplace = True)

    globals()[dataframes_names[1]] = pd.read_csv(os.getcwd() + '\\Files\\' + files_names[1], skiprows = 7, sep = " ", 
                                            delimiter = " ", names = ["Character", "Node_1", "Node_2", "Physical_distance"],
                                            index_col = None, usecols = None, encoding = 'ISO-8859-1')

    eval(dataframes_names[1]).drop(columns = ["Character"], inplace = True)

    globals()[dataframes_names[2]] = pd.read_csv(os.getcwd() + '\\Files\\' + files_names[2], skiprows = 7, sep = " ", 
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
        start=int(input('Give me the node H: '))
        inp=input('Give me a set of nodes (separated by space): ')
        p=list(map(int, inp.split()))
        distance=input('Give me a distance function:\ntime : the time distance;\nphysical : phisical distnce;\nnetwork : network distance.\n')
        
        if distance not in ['network', 'time', 'physical']:
            print('Wrong inputs\nPlease reinsert\n')
        else:
            ok=True

    print(start, '\n', p, '\n', distance)


    paths={}#this save the paths betwenn the pair

    #the clique
    nodes=[start]+p # nodes of the clique 
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

    # We are facing an NP-hard problem, that means there isn't a linear solution. In order to solve it we will adopt an euristic solution known as
    # "the nearest neighbour". This method, at each step, chooses the nearest node as next point to visit.

    bigRoute=myNearestNeighbour(clique, start, p[len(p)-1], nodes) #compute the route over the set in input

    print('big r', bigRoute)

    #check if it's possibile find a route over all nodes in input
    if None in bigRoute:
        print('Not possibile')
        return


    shortRoute=[start]
    st=start
    #print(paths)
    for node in bigRoute[1:]:# Iterate over the big route to concatenate the path among two nodes in the gid route
        #print(paths[(st, node)])
        path=paths[(st, node)]
        shortRoute+=path[1:] if path!=float('inf') else [path]#concatenate taking only the elements from second to the end
        st=node
    #print(shortRoute)
    if float('inf') in shortRoute:
        print('Not possibile')
        return
    print('ok s r', shortRoute, 'len', len(shortRoute))

    #create the graph of the short route
    gf4=dict()
    current=start
    for node in shortRoute[1:]:
        adj=gf4.get(current)
        if adj==None:
            gf4[current]={node: G[current][node]}
        else:
            if distance=='time':
                adj[node]=G[current][node]['Time_distance']
            elif distance=='physical':
                adj[node]=G[current][node]['Physical_distance']
            else:
                adj[node]=1
        current=node
    gf4[p[len(p)-1]]=dict()

    #print('gf4: ', gf4)

    # call the visualizzation function 4
    
    visualize(gf4, True, False) 
    pos=getPositions(shortRoute)
    #print('pos: ', pos)
    visualize2(pos, start) 


if __name__=='__main__':
    functionality_4()
