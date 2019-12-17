import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import utils as u
import itertools as it
import header as h

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

def f2():

    #imputs
    ok=False
    while not ok:
        inp=input('Give me a set of nodes (separated by space): ')
        nodes=list(map(int, inp.split()))
        distance=input('Give me a distance function:\nt : the time distance;\nd : phisical distnce;\nn : netword distance.\n')
        
        if distance not in ['t', 'd', 'n']:
            print('Wrong inputs\nPlease reinsert\n')
        else:
            ok=True
    
    print(nodes, '\n', distance)
    
    g=dict()
    print('graph created')


    
    #g={1:{}, 2:{1:1}, 19:{4:1, 15:1, 13:1}, 3:{2:1, 6:1, 13:1, 4:1, 1:1}, 4:{14:1, 15:1}, 5:{4:1, 6:1}, 6:{3:1}, 7:{6:1, 13:1, 10:1}, 8:{7:1, 11:1}, 9:{5:1, 2:1, 7:1}, 10:{13:1}, 11:{14:1}, 12:{13:1, 4:1, 8:1}, 14:{9:1}, 13:{}, 15:{14:1, 13:1}, 16:{17:1}, 17:{18:1}, 18:{16:1}}
    
    
    print('node added')
    
    if distance=='d':
        u.add_phisical_distance_edges(g)
    elif distance=='t':
        u.add_time_distance_edges(g)
    else:
        u.add_network_distance_edges(g)
    print('edges added')

     #to visulize the graph
     '''
    gg=nx.DiGraph(g)
    nx.draw(gg, with_labels=True)
    plt.show()
    '''
    
    inf=float('inf')
    paths={}#this save the paths betwenn the pair

    #the clique
    clique={}
    u.add_nodes(clique, nodes) #add the nodes to the clique
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

    # with ermutations
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

    completeRoute=[]
    for n in bigRoute:
        completeRoute+=paths[n]

    print(completeRoute)


f2()

