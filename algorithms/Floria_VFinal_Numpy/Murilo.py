import random
import matplotlib.pyplot as plt
import time
import numpy as np
import math

n = 9               # número de arestas
density = 0.8       # densidade de arestas no grafo
max_cost = 100       # custo máximo de uma aresta
layout = 'circular' # layout do grafo


def rndm_graph(n, density, max_cost):

    """
    Gera uma matriz de custos aleatória que representa um grafo orientado.

    Se não existir uma aresta entre dois nós, o custo é definido como infinito.
    Se existir uma aresta, o custo é um número aleatório entre 0.1 e max_cost, com duas casas decimais.

    Args:
        n : O número de nós no grafo.
        density : A densidade de arestas no grafo.
        max_cost : O custo máximo de uma aresta.

    Returns:
      np.ndarray: A matriz de custos gerada.
    """

    matriz = []
    for i in range(n):
        linha = []
        for j in range(n):
            # Define a probabilidade de existir aresta
            if random.random() > density:
                custo = float('inf')  # não existe aresta
            else:
                # Gera um float positivo entre 0.1 e max_cost
                custo = round(random.uniform(0.1, max_cost), 2)
            linha.append(custo)
        matriz.append(linha)
    matriz = np.array(matriz)

    # Exibe a matriz
    # print("Matriz de custos gerada ('inf' representa ausência de aresta):\n")
    # print(matriz)

    return matriz

def mean_cost(path, c):

    """
    Fornece o custo médio sobre um caminho.

    Args:
        path : Lista de arestas (i,j) que compõem o caminho a ser analisado.
        c : Matriz de custos do grafo.

    Returns:
        float : Custo médio do caminho.
    """

    cost = 0
    for v in range(len(path)):
      (i,j) = path[v]
      cost += c[i][j]

    return cost/len(path)

def lax_oleinik(c,f):

    """
    Aplica o operador de Lax-Oleinik associado à função de custo c sobre a função f.

    O operador de Lax-Oleinik é definido sobre f : V(G) -> IR como:

      (Tf)(j) := min_i {f(i) + c(i,j)}

    onde c(i,j) é o custo associado à aresta (i,j) e f(i) é o valor da função f
    sobre o vértice i.

    Args:
        c : Matriz de custos do grafo, representando c(i,j).
        f : Vetor representando a função f.

    Returns:
        np.ndarray: Vetor representando Tf, o resultado da aplicação do
                    operador de Lax-Oleinik a f.
    """
    n = len(c)
    Tf = []
    for j in range(n):
      Tf.append(np.min(f+c[:,j]))

    return np.array(Tf)

def argmin(array):

    """
    Encontra o índice do elemento mínimo em um array.

    Esta função percorre o array fornecido e retorna o índice do elemento com o menor valor.
    Se houver vários elementos com o valor mínimo, o índice do primeiro elemento encontrado é retornado.

    Args:
        array : O array no qual procurar o elemento mínimo.

    Returns:
        int: O índice do elemento mínimo no array.
    """

    min_value = float('inf')
    min_index = None

    for i, value in enumerate(array):
        if value < min_value:
            min_value = value
            min_index = i

    return min_index

def Floria_Griffiths(c):

    """
    Inicia o algoritmo de Floría-Griffiths para encontrar a constante cíclica minimal e um corretor.

    Args:
        c : Matriz de custos do grafo.

    Returns:
        tuple : Uma tupla contendo o número de iterações (r), um corretor (u) e a constante cíclica minimal (m).
    """

    n = len(c)
    sigma_zero = []
    for j in range(n):
        for i in range(n):
            if c[i, j] != float('inf'):
                sigma_zero.append(i)
                break
    u_zero = np.zeros(n)
    m_zero = max_cost # cota superior para m(c)

    return iter_Floria_Griffiths(u_zero,m_zero,sigma_zero,c,0)


def iter_Floria_Griffiths(u,m,sigma,c,r,max_recursion_depth=200):

    """
    Executa uma iteração do algoritmo de Floría-Griffiths.

    Args:
        u : Corretor atual.
        m : Constante cíclica minimal atual.
        sigma : Função sigma atual.
        c : Matriz de custos do grafo.
        r : Número da iteração atual.
        max_recursion_depth : Profundidade máxima de recursão. Por padrão, 200.

    Returns:
        tuple : Uma tupla contendo o número de iterações (r), um corretor (u) e a constante cíclica minimal (m).
    """
    n = len(c)
    r += 1
    if r == 8:
        pass

    if r > max_recursion_depth:
        # print("Profundidade máxima de chamadas recursivas atingida. Retornando valores atuais.")
        return (r - 1, u, m)

    V = []
    Tu = lax_oleinik(c-m,u)
    for j in range(n):
        if u[j] - Tu[j] > 1.0e-13: # Verifica se u[j] > Tu[j] evitando erro de precisão finita
            V.append(j)

    # Condição de parada
    if len(V) == 0:
        return (r-1,u,m)

    u_new = []
    for j in range(n):
        u_new.append(min(u[j],Tu[j]))
    u_new = np.array(u_new)

    sigma_new = []
    for j in range(n):
      if j in V:
        sigma_new.append(argmin(u + c[:,j]))
      else:
        sigma_new.append(sigma[j])

    cycles = []
    for j in V:
      k = [j]
      s = None
      for i in range(1,r+1):
        k.append(sigma_new[k[i-1]])
        if k[i] == j:
          s = i
          break
      if s is not None:
        cycle = []
        for i in range(s,0,-1):
          cycle.append((k[i],k[i-1]))
        cycles.append(cycle)

    cycles_cost = np.array([mean_cost(cycle,c) for cycle in cycles])
    if (len(cycles_cost) == 0):
      m_new = m
    else:
      m_new = min(np.min(cycles_cost),m)

    # print(f"Iteração {r}:")
    # print(f"\tu = {u_new}")
    # print(f"\tm = {m_new}\n")

    return iter_Floria_Griffiths(u_new,m_new,sigma_new,c,r)

def renormalize(c, m, u):

    """
    Renormaliza a matriz de custos c usando a constante cíclica minimal m e um corretor u.

    A renormalização da matriz de custos é feita da seguinte forma:

        c_norm(i,j) := c(i,j) + u(i) - u(j) - m(c) >= 0

    Isso garante que o custo de ciclos minimais seja zero, isto é, m(c_norm) = 0.

    Args:
        c : A matriz de custos original.
        m : A constante cíclica minimal.
        u : Um corretor.

    Returns:
        np.ndarray: A matriz de custos renormalizada.
    """
    n = len(c)
    c_norm = c.copy()
    for i in range(n):
      for j in range(n):
        c_norm[i][j] += u[i] - u[j] - m
        if c_norm[i][j] < 1.0e-14:
          c_norm[i][j] = 0 # Ignora erros de precisão finita

    return c_norm

def karp(c):

    """
    Calcula a constante cíclica minimal de uma matriz de custos usando o algoritmo de Karp.

    O algoritmo de Karp é um método para calcular a constante cíclica minimal.
    Aqui, utilizamos o operador de Lax-Oleinik repetidamente para encontrar o valor mínimo.

    Args:
       c : A matriz de custos do grafo.

    Returns:
       float: A constante cíclica minimal da matriz de custos.
    """

    n = len(c)

    # Calcula T(0), T^2(0), ... , T^n(0), T^{n+1}(0), onde T é o op. de Lax-Oleinik
    T = [np.zeros(n)]
    for i in range(1,n+2):
        T.append(lax_oleinik(c,T[i-1]))

    min = max_cost # cota superior para m(c) 
    for i in range(n):
        max = 0
        for k in range(1,n):
            maximize = (1/(n-k+1))*(T[n+1][i] - T[k][i]) # função a ser maximizada
            if max < maximize:
                max = maximize
        if min > max:
            min = max

    return min


def le_matriz(n):
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

def matriz_ale(tam, lim):
    matriz = np.empty([tam, tam])
    maior = 0
    for i in range(tam):
        for j in range(tam):
            if i==j:
                matriz[i,j] = math.inf
            else:
                matriz[i,j] = random.randint(1, lim+1)
                maior = maior if maior > matriz[i,j] else matriz[i,j]

    return matriz, maior


def main(tam):
    correct = 0
    for i in range(100):
        custo =  np.array(matriz_ale(tam, 100)[0])
        s_time = time.time()
        result = Floria_Griffiths(custo)
        result = karp(custo)
        e_time = time.time()
        return e_time - s_time, result[0]
        # print()

if __name__ == "__main__":
   main()
