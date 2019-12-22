import sys
import time
import func_1 as f1
import func_3 as f3
import func_2 as f2
import func_4 as f4

def func_1():


    f1.func_1()
    

def func_2():
    f2.functionality_2()
    
    
def func_3():

    coordinates_dict, G = f3.get_coords_and_graph()

    t = time.time()
    s_o_r = f3.shortest_ordered_route(G, int(input('Please choose a source node: ')), set(map(int, input('Now please choose a list of spaced nodes: ').split())), input('And, now, input a type of distance: '))
    print('Computing the shortest ordered route...')
    print('Elapsed time:')
    print(round(time.time() - t, 2))

    f3.visualize_func_3(coordinates_dict, s_o_r)

def func_4():
    
    f4.functionality_4()

if __name__== '__main__':

    ok=False
    while not ok:

        func = input('Choose the functionality(1, 2, 3 or 4)\nor e to exit the program: ')

        if func == '1':
            func_1()
        elif func == '2':
            func_2()
        elif func == '3':
            func_3()
        elif func == '4':
            func_4()
        elif func == 'e':
            ok=True
        else:
            print('I\'m sorry... your choice is wrong\nPlease retry or type \'e\'')
    
