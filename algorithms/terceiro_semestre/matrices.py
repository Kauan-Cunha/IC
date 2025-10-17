import random as ran
import math
import numpy as np
import random as ran
import numpy as np

def matriz_custo_para_lista_adj(matriz_custo):
  """
  Converte uma matriz de custo para uma lista de adjacência REVERSA ponderada.
  Para cada nó, a lista contém as arestas que CHEGAM nele.

  Args:
    matriz_custo: Uma lista de listas representando a matriz de custo.
                  Valores > 0 são os pesos das arestas.
                  O valor 0 é tratado como a ausência de uma aresta.

  Returns:
    Uma lista de listas representando a lista de adjacência reversa.
    Cada elemento da lista interna é uma tupla (pai, peso).
  """
  num_vertices = len(matriz_custo)
  lista_adj = [[] for _ in range(num_vertices)]

  for i in range(num_vertices): # i é a origem (pai)
    for j in range(num_vertices): # j é o destino
      # Verifica se o valor é maior que 0 para considerar a existência da aresta
      if matriz_custo[i][j] > 0:
        peso = matriz_custo[i][j]
        # Adiciona na lista do nó de DESTINO (j) a tupla (ORIGEM, peso)
        lista_adj[j].append((i, peso))

  return lista_adj

def random_sparse_connected_matrix(size):
    """
    Gera uma matriz de adjacências para um grafo direcionado aleatório
    que é garantidamente fortemente conexo.
    """
    if size <= 0:
        return np.zeros((0, 0), dtype=int)

    matrix = np.zeros((size, size), dtype=int)
    
    # 1. Criar um ciclo Hamiltoniano para garantir a conectividade forte
    nodes = list(range(size))
    ran.shuffle(nodes)
    for i in range(size):
        start_node = nodes[i]
        end_node = nodes[(i + 1) % size] # O % size faz o ciclo fechar
        matrix[start_node, end_node] = 1
    
    edges_added = size

    # 2. Adicionar arestas aleatórias restantes
    max_edges = size * (size - 1)
    limit_edges = int(0.7 * max_edges)
    
    if limit_edges < size:
        num_edges = size
    else:
        num_edges = ran.randint(size, limit_edges)

    while edges_added < num_edges:
        i = ran.randint(0, size - 1)
        j = ran.randint(0, size - 1)
        
        if i != j and matrix[i, j] == 0:
            matrix[i, j] = 1
            edges_added += 1
            
    return matrix

def random_sparse_matrix(size):
    """
    Gera uma matriz de adjacências para um grafo direcionado aleatório.
    O número de arestas é gerado aleatoriamente, garantindo um grafo esparso.

    Args:
        size (int): O número de vértices no grafo.

    Returns:
        Um array NumPy representando a matriz de adjacências (com 0s e 1s).
    """
    # O número máximo de arestas em um grafo direcionado sem laços é n * (n - 1).
    # Para garantir que o grafo seja esparso, vamos limitar o número de arestas
    # a um valor aleatório entre 1 e 50% do número máximo de arestas possível.
    max_edges = size * (size - 1)
    # Defines an upper limit for the number of edges to avoid too dense a graph
    # (here, 30% of the total possible edges, but you can adjust this value)
    limit_edges = int(0.7 * max_edges)

    if limit_edges < 1:
        num_edges = 1
    else:
        num_edges = ran.randint(1, limit_edges)

    matrix = np.zeros((size, size), dtype=int)
    edges_added = 0
    while edges_added < num_edges:
        i = ran.randint(0, size - 1)
        j = ran.randint(0, size - 1)
        
        # Ensures no loops and that the edge doesn't already exist.
        if i != j and matrix[i, j] == 0:
            matrix[i, j] = 1
            edges_added += 1

    return matrix

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
    """
    Dada uma matriz de conexão (com 0s e 1s), retorna uma matriz de pesos
    aleatórios no intervalo [1, max_value].
    """
    # FIX: Cria uma cópia da matriz com o tipo 'float' para evitar erros.
    # No entanto, a lógica a seguir nem precisaria, pois não usaremos 'inf'.
    new_matrix = c_matrix.astype(float)
    lenth = c_matrix.shape[0]  # Forma mais robusta de obter o tamanho
    maximum = 0

    for i in range(lenth):
        for j in range(lenth):
            # A matriz c_matrix original tem 1 onde existe uma aresta.
            if c_matrix[i, j] == 1:
                # Atribui um peso aleatório à aresta.
                weight = ran.randint(1, max_value)
                new_matrix[i, j] = weight
                if weight > maximum:
                    maximum = weight
            else:
                # FIX: Onde não há aresta, o valor deve ser 0.
                # A função matriz_custo_para_lista_adj já interpreta 0 como ausência de aresta.
                # Isso evita o uso de math.inf e previne o erro.
                new_matrix[i, j] = 0

    return new_matrix, maximum