import random as ran
import math
import numpy as np

def print_matrix(matriz):
    """Prints a more readable matrix into terminal"""
    for i in matriz:
        for j in i:
            if j != np.nan : print(j, end=" ") 
            else : print("*", end=" ")        
        print()

def scan_matrix(n):
    """Given a size, it takes keyboard input to iniacilize a matrices and return it."""
    matriz = []
    for i in range(n):
        # Lê uma linha da matriz e converte em uma lista de números
        linha = input().split()
        new_line = []
        for elem in linha:
            if elem == "inf":
                new_line.append(math.inf)
            else:
                new_line.append(int(float(elem)))
        matriz.append(new_line)
    
    for i in range(n):
        matriz[i][i] = 0
    m = np.max(matriz)

    for i in range(n):
        matriz[i][i] = math.inf
    
    # Converte a lista de listas em um array 2D usando NumPy
    return np.array(matriz), m

def blocky(size, b_size, repeat = False):
    """It returns the connetion matrix of a "blocky graph" as described below
    
    A blocky graph contains a sub-graph in which all nodes are connected both ways(in this case nodes 0 to b_size-1) and
    the remaining are connected to it through only one way.

    size: number of nodes; b_size: sub_graph number of nodes; repeat: whether or not 2 remaning nodes can be connected to the same node.
    """

    matrix = np.zeros((size,size))
    matrix[0:b_size, 0:b_size] = np.ones((b_size, b_size))

    if repeat == False:
        entries = list(range(size-b_size))
        exits = list(range(size-b_size))
        ran.shuffle(entries)
        ran.shuffle(exits)
    else:
        entries = ran.choices(range(size-b_size), k = size - b_size)
        exits = ran.choices(range(size-b_size), k = size - b_size)
    
    #inserting entries and exits
    aux = 0
    for i, j in zip(entries, exits):
        matrix[i, aux+b_size] = 1
        matrix[aux+b_size, j] = 1
        aux+=1

    for i in range(size):
        matrix[i,i] = 0

    return matrix

def fully_connected_matrices(tam):
    """It returns the connection matrix of a fully connected graph. Ones represent connection, while zeros are the opposite"""

    matriz = np.empty([tam, tam])
    for i in range(tam):
        for j in range(tam):
            if i==j:
                matriz[i,j] = 0
            else:
                matriz[i,j] = 1

    return matriz

def randomised_weigh_matrix(c_matrix, max_value):
    """Given a connection matrix it returns a randomised weight matrix in range [0, max_value] and its greatest entrance"""
    new_matrix = np.copy(c_matrix)
    lenth = c_matrix[0].size
    maximum = 0
    for i in range(lenth):
        for j in range(lenth):
            if c_matrix[i,j] == 1:
                new_matrix[i,j] = ran.randint(0, max_value)
                maximum = maximum if maximum > new_matrix[i,j] else new_matrix[i,j] #checks if new entrance is the maximum
            else:
                new_matrix[i,j] = math.inf
    
    return new_matrix, maximum