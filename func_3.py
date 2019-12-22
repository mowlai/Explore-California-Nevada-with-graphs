import os
import time 
import folium
import webbrowser
import collections
import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm
from folium.map import *
from folium import plugins
from folium.plugins import FloatImage
from folium.plugins import MeasureControl
from fibonacci_heap import Fibonacci_heap

# Custom function to create a coordinates dictionary and a graph
def get_coords_and_graph():
    
    files_names = os.listdir('./Files')

    dataframes_names = ['coordinates', 'physical_dist', 'time_dist']

    for k in tqdm(range(3)):
        if os.getcwd() + '\\Files\\' + files_names[k] == os.getcwd() + '\\Files\\' + files_names[0]:
            globals()[dataframes_names[k]] = pd.read_csv(os.getcwd() + '\\Files\\' + files_names[0], skiprows = 7, sep = " ", 
                                              delimiter = " ", names = ["Character", "ID_Node", "Longitude", "Latitude"],
                                              index_col = None, usecols = None, encoding = 'ISO-8859-1')
            eval(dataframes_names[k]).drop(columns = ["Character"], inplace = True)
            eval(dataframes_names[k])['Longitude'] = coordinates['Longitude']/1000000
            eval(dataframes_names[k])['Latitude'] = coordinates['Latitude']/1000000
        elif os.getcwd() + '\\Files\\' + files_names[k] == os.getcwd() + '\\Files\\' + files_names[1]:
            globals()[dataframes_names[k]] = pd.read_csv(os.getcwd() + '\\Files\\' + files_names[1], skiprows = 7, sep = " ", 
                                              delimiter = " ", names = ["Character", "Node_1", "Node_2", "Physical_distance"],
                                              index_col = None, usecols = None, encoding = 'ISO-8859-1')
            eval(dataframes_names[k]).drop(columns = ["Character"], inplace = True)
        elif os.getcwd() + '\\Files\\' + files_names[k] == os.getcwd() + '\\Files\\' + files_names[2]:
            globals()[dataframes_names[k]] = pd.read_csv(os.getcwd() + '\\Files\\' + files_names[2], skiprows = 7, sep = " ", 
                                              delimiter = " ", names = ["Character", "Node_1", "Node_2", "Time_distance"],
                                              index_col = None, usecols = None, encoding = 'ISO-8859-1')
            eval(dataframes_names[k]).drop(columns = ["Character"], inplace = True)

    t = time.time()
    print('Creating the coordinates dictionary...')
    coordinates_dict = coordinates.set_index('ID_Node').T.to_dict('list')
    print('Elapsed time:')
    print(round(time.time() - t, 2))

    complete = pd.merge(physical_dist, time_dist, on = ['Node_1', 'Node_2'])

    t2 = time.time()
    print('Creating the graph...')
    G = nx.from_pandas_edgelist(complete, 'Node_1', 'Node_2', ['Physical_distance', 'Time_distance'], create_using = nx.DiGraph())
    print('Elapsed time:')
    print(round(time.time() - t2, 2))
    
    return coordinates_dict, G

# Custom function to run a BFS over the graph and checking it a node is connected or not
def b_f_s(graph, root): 
    visited, queue = set(), collections.deque([root])
    while queue: 
        vertex = queue.popleft()
        for neighbour in graph[vertex]: 
            if neighbour not in visited: 
                visited.add(neighbour) 
                queue.append(neighbour)
    return visited

# Custom function created to get the distance attribute from each edge.
def get_weight(graph, node_a, node_b, measure):
    if measure == 'network':
        return 1
    elif measure == 'time':
        return graph.get_edge_data(node_a, node_b)['Time_distance']
    elif measure == 'physical':
        return graph.get_edge_data(node_a, node_b)['Physical_distance']

# Custom function to implement the Dijkstra algorithm
def dijkstra(graph, source, destination, measure = 'network'):
    # The first if condition is deployed to avoid the case of an erroneous distance measure typing.
    if measure in ['network', 'time', 'physical']:
        # Here we decided to prevent the algorithm from starting by checking whether a node is not connected
        # via BFS.
        if destination in b_f_s(graph, source):
            # The variable 'shortest paths' is basically a dictionary where the keys are nodes and the values are a tuple
            # containing the couple (previous node, weight). We initialize it with the source vertex and set its weight to 0.
            shortest_paths = {source: (None, 0)}
            #The variable 'current_node' does basically store the node we are on, we initialize it with the source
            # vertex in the beginning
            current_node = source
            # The variable 'visited' is a set keeping trace of the visited nodes.
            visited = set()
            # The variable 'heap' is a Fibonacci heap we use to store our nodes and order them by
            # their current weight. To create it we resorted to an existing library which we modified
            # to better meet our requirements.
            heap = Fibonacci_heap()

            while current_node != destination:
                if current_node not in visited:
                    # Here we add our current node to the set of visited ones
                    visited.add(current_node)
                # The variable 'destinations' is essentially an adjacency list, it extracts all the edges
                # departing from the current node
                destinations = [elem[1] for elem in graph.edges(current_node)]
                # The variable 'current_node_weight' stores the weight attribute on the edge connected
                current_node_weight = shortest_paths[current_node][1]

                # During the following loop we visit all the nodes connected to the current one
                for next_node in destinations:
                    # Here we compute the weight of current edge as the sum:
                    # weight of the edge + weight of edges previously visited 
                    weight = get_weight(graph, current_node, next_node, measure) + current_node_weight
                    # Here we add nodes to the heap
                    if next_node not in visited and next_node not in heap.nodes:
                        heap.enqueue(next_node, weight)

                    # Here we add a new node to the shortest path, or update
                    # it if the current path is shorter than previous path
                    if next_node not in shortest_paths:
                        shortest_paths[next_node] = (current_node, weight)
                    else:
                        current_shortest_weight = shortest_paths[next_node][1]
                        if current_shortest_weight > weight:
                            shortest_paths[next_node] = (current_node, weight)

                # If our heap is empty, we cannot continue
                # nor reach the destination
                if not heap.__bool__():
                    return "Not Possible"
                
                # Here we update current_node with the next one,
                # namely the destination with lowest weight
                current_node = heap.dequeue_min().m_elem

            # Creating a path and reversing it
            path = []
            while current_node is not None:
                path.append(current_node)
                # Extract the previous node from shortest_paths
                next_node = shortest_paths[current_node][0]
                # Update current_node
                current_node = next_node
            # Reverse path
            path = path[::-1]
            return (path, shortest_paths[path[-1]][1])
        else:
            print('The graph is not connected.')
    else:
        print('Invalid measure, please try again.')
        
# Custom function to apply the Dijkstra algorithm in order to obtain a shortest ordered route
def shortest_ordered_route(graph, source, destinations, measure = 'network'):
    # Creating a list to store the source node and the destinations in order to pass it 
    # to folium and differentiate the sizes
    lst = []
    lst.append(source)
    lst.extend(destinations)
    # Storing the source vertex in a variable with the same name
    source  = source
    # List variable to store the path 
    total_steps = []
    # List variable to store the chosen distance measure
    total_weight = 0
    # Iterating over the elements in the list of different destinations to reach
    for destination in destinations:
        # An in condition to avoid printing two times the same node
        if not total_steps:
            # Storing the path and the sum of weights
            steps, weight = dijkstra(graph, source, destination, measure)
            # Updating the variables 
            total_steps +=steps
            total_weight += weight
            source = destination
        # Same steps as above, with just one more: we pop the first elements in the list
        # of steps, which is the same one in the last postion of the other list
        else:
            steps, weight = dijkstra(graph, source, destination, measure)
            steps.pop(0)
            total_steps += steps
            total_weight += weight
            source = destination
    # Printing the output, conditioned to the selected measure
    print("Path:")
    print(*total_steps)
    if measure == 'network':
        print("Network distance:")
        print(total_weight)
    elif measure == 'time':
        print("Time distance:")
        print(total_weight)
    elif measure == 'physical':
        print("Physical distance:")
        print(total_weight)
    return total_steps, total_weight, lst


#t3 = time.time()
#s_o_r = shortest_ordered_route(G, int(input('Please choose a source node: ')), set(map(int, input('Now please choose a list of spaced nodes: ').split())), input('And, now, input a type of distance: '))
#print('Computing the shortest ordered route...')
#print('Elapsed time:')
#print(round(time.time() - t3, 2))

def visualize_func_3(coordinates_dict, s_o_r):
    m = folium.Map(location = tuple(coordinates_dict[s_o_r[0][0]][::-1]), zoom_start = 10, tiles = 'openstreetmap')

    folium.PolyLine([tuple(coordinates_dict[node][::-1]) for node in s_o_r[0]], color = 'violet', weight = 2.5, opacity = 1).add_to(m)

    for node in s_o_r[0]:
        if node in s_o_r[2]:
            folium.CircleMarker(location = tuple(coordinates_dict[node][::-1]), radius = 10, line_color = 'purple', fill_color = 'black', fill_opacity = 0.8, fill = True).add_to(m)
        else:
            folium.CircleMarker(location = tuple(coordinates_dict[node][::-1]), radius = 5, line_color = '#3186cc', fill_color = '#FFFFFF', fill_opacity = 0.8, fill = True).add_to(m)
        
    m.save(outfile = "Func_3.html")

    webbrowser.open("Func_3.html", new = 2)

