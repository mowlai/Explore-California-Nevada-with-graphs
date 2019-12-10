import networkx as ntx
import header as h
import utils as u
import matplotlib.pyplot as plt


def f4():
    #to delete 
    distance='d'

    #imputs
    '''
    h=int(input('Give me the node H: '))
    inp=input('Give me a set of nodes (separated by space: )')
    p=set(map(int, inp.split()))
    distance=input('Give me a distance function:\nt : the time distance;\nd : phisical distnce;\nn : netword distance.\n')
    #aggiungere controllo sull'input
    print(h, '\n', p, '\n', distance)
    '''

    g=ntx.Graph()
    print('graph created')
    u.add_nodes(g)
    print('node added')
    if distance=='t':
        u.add_phisical_distance_edges(g)
    elif distance=='d':
        u.add_time_distance_edges(g)
    else:
        u.add_network_distance_edges(g)
    print('edges added')

    

    #ntx.draw(g)
    #print('drawed')
    #plt.show()



if __name__=='__main__':
    print('main')
    f4()