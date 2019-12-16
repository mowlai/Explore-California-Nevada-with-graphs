import networkx as nx
import header as h
import utils as u
import matplotlib.pyplot as plt
import pandas as pd
import sys

def myDijkstra(g, source, dest):
    '''
    Implementation of the Dijkstra algo for the shortest path in a graph
    inputs: 
        g: the graph in the form (dict): {n : { adjOfn : weight_n_to_adjOfn } }
        source: the source node
        dest: the destination node
    outputs:
        pred: the father's vector
        d: the distance list
        pathRevers: the dijkstra path
        d[dest]: the weight of the path
    '''
    nodi=[0]+list(g.keys())#obtain the nodes in the graph
    l=[source]#list of node we need to visit, start from the source
    s=[]#list of nodes visited
    d=[float('inf') for i in nodi]#the inizial (unknown) distanse set to infinity
    d[source]=0#distance of the sourse from itself
    pred=nodi.copy()#list of fathers
    

    while l!=[]:#till we haven't visited all nodes

        #loking for the el in l with minumun distance in d
        minDist=d[l[0]]
        i=l[0]
        for el in l[1:]:
            if d[el]<minDist:
                minDist=d[el]
                i=el
        #we have found the node with minimum distance 
        current=i#visiting...
        l.remove(i)#...
        s.append(current)#...
        adj=g[current]#adjacent
        for neighbour in adj:
            cumul=d[current]+g[current][neighbour]#calculate the cumulative distance
            if cumul<d[neighbour]:
                d[neighbour]=cumul#update the minimum distance for the neigbour from the current
                pred[neighbour]=current #update the father of the current
                if neighbour not in l:
                    l.append(neighbour)#we need to visit it

    # We had created the father's vector and the permanent distance vector
    if d[dest]==float('inf'):#if there isn't a path from the source to the destination
        print('Ther isn\'t a path from {} to {}'.format(source, dest))
        return pred, d, float('inf'), float('inf')
    else:
        #reation of the reverse path from the destination to the source based on the father's vector
        pathRevers=[dest]
        father=pred[dest]
        while father!=source:#since finde the source
            pathRevers.append(father)
            father=pred[father]
        pathRevers.append(source)#add the source
        pathRevers.reverse()#and reverse the list to obtain the path from the source to the destination

        return pred, d, pathRevers, d[dest]
        
def giveMyG(n):
    return nx.complete_graph(n)

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

def visualize(gf4, nv, wv):

    pos=getPositions()

    

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

def getPositions():
    '''
    Returns the dictionary of the position for each nodes; needs to visualizations task
    outputs:
        pos: dictionary of the positions
    '''
    pos=dict()
    with open(h.PATH_INFO, 'r') as info:
        for row in info:
            row=row[2:]#remove the inizial 'v'
            comp=list(map(int, row.split()))
            pos[comp[0]]=[comp[1], comp[2]]
    return pos

def printNodes():
    nodes=pd.read_csv(h.PATH_INFO, sep=' ', names=['a', 'node', 'lat', 'lon'], delimiter=None, index_col=None, usecols=None)
    nodes.plot(kind='scatter', x='lon', y='lat')

def functionality_4(nv, wv):
    '''
    Implementation of the functionality 4 
    inputs:
        nv: node visualization (boolean) if true, visulize the name of the node
        wv: weight visualization (boolean) if true, visualize the weight on the edge
    outputs:
        shortRoute: the 'shortest' route from the source to the list of node in input'
    '''

    #to delete 
    '''
    g={1:{6:1, 2:5, 7:1}, 2:{3:6, 5:1, 7:1}, 3:{4:7}, 4:{3:8, 5:9}, 5:{6:10, 3:1}, 6:{2:1}, 7:{8:1}, 8:{9:1}, 9:{10:1, 11:1, 13:1}, 10:{11:1}, 11:{12:1}, 12:{13:1}, 13:{}}

    gd=nx.DiGraph(g)
    nx.draw_planar(gd, with_labels=True)
    print('drawed')
    plt.title('iniziale')
    plt.show()
    '''

    #imputs
    ok=False
    while not ok:
        start=int(input('Give me the node H: '))
        inp=input('Give me a set of nodes (separated by space): ')
        p=list(map(int, inp.split()))
        distance=input('Give me a distance function:\nt : the time distance;\nd : phisical distnce;\nn : netword distance.\n')
        
        if distance not in ['t', 'd', 'n']:
            print('Wrong inputs\nPlease reinsert\n')
        else:
            ok=True
    
    print(start, '\n', p, '\n', distance)
    
    g=dict()
    print('graph created')
    u.add_nodes(g, list(range(1, h.NUM_VERTEX+1)))
    #u.add_nodes(g, list(range(1, 18)))
    #print('1', g)
    #g={1:{}, 2:{1:1}, 19:{4:1, 15:1, 13:1}, 3:{2:1, 6:1, 13:1, 4:1, 1:1}, 4:{14:1, 15:1}, 5:{4:1, 6:1}, 6:{3:1}, 7:{6:1, 13:1, 10:1}, 8:{7:1, 11:1}, 9:{5:1, 2:1, 7:1}, 10:{13:1}, 11:{14:1}, 12:{13:1, 4:1, 8:1}, 14:{9:1}, 13:{}, 15:{14:1, 13:1}, 16:{17:1}, 17:{18:1}, 18:{16:1}}
    #print('2', g)
    
    print('node added')
    if distance=='d':
        u.add_phisical_distance_edges(g)
    elif distance=='t':
        u.add_time_distance_edges(g)
    else:
        u.add_network_distance_edges(g)
    print('edges added')
    

    # i want create a clique with the all node given in input to save all distances between a pair of node
    
    paths={}#this save the paths betwenn the pair

    #the clique
    nodes=[start]+p # nodes of the clique 
    clique={}
    u.add_nodes(clique, list(set(nodes))) #add the nodes to the clique
    for source in nodes: #iterate over the nodes to perform a clique
        for dest in nodes:
            if source!=dest: #if the pair of nodes are not the same node
                adj=clique[source]#obtain the enpty dictionary associated to che source
                print('dijkstraaaa')
                djkComps=myDijkstra(g, source, dest)#calculate the distance
                adj[dest]=djkComps[3]#add the neighbour with the weight
                paths[(source, dest)]=djkComps[2]#take the path
            else:
                adj=clique[source]
                adj[source]=0
                paths[(source, dest)]=[]
    
    #this problem is np-hard; therin't a linear solution; we will adopt ad euristic solution called "the nearest neighbour"
    #at each step we chose the nearest as next point to visit

    bigRoute=myNearestNeighbour(clique, start, p[len(p)-1], nodes) #compute the route over the set in input
    print('big r', bigRoute)

    #check if it's possibile find a route over all nodes in input
    if None in bigRoute:
        print('Not possibile')
        return


    shortRoute=[start]
    st=start
    #print(paths)
    for node in bigRoute[1:]:#iteate over the big route to concatenate the path among two node in the gid route
        #print(paths[(st, node)])
        path=paths[(st, node)]
        shortRoute+=path[1:] if path!=float('inf') else [path]#concatenate taking only the elements from second to the end
        st=node
    print(shortRoute)
    if float('inf') in shortRoute:
        print('Not possibile')
        return
    print('ok s r', shortRoute)

    #create the graph of the short route
    gf4=dict()
    current=start
    for node in shortRoute[1:]:
        adj=gf4.get(current)
        if adj==None:
            gf4[current]={node: g[current][node]}
        else:
            adj[node]=g[current][node]
        current=node

    print('gf4: ', gf4)

    # call the visualizzation function 4
    
    visualize(gf4, nv, wv)  

if __name__=='__main__':
    node_visualize=True if sys.argv[1]=='t' else False
    weight_visualize=True if sys.argv[2]=='t' else False
    print(sys.argv)
    functionality_4(node_visualize, weight_visualize)