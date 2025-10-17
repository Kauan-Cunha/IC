import numpy as np
import time
import desenhar_grafo as draw
import grafoCriticoAlt as critic
import tarjan_lista

def peso_aresta(c_adj, origem, destino):
    for pai, peso in c_adj[destino]:
        if pai == origem:
            return peso
    return float('-inf')  # ou outro valor padrão se não existir

def oleinik(f, c_adj, m):
    """
    Calcula a constante de lax-oleinik e o argmin(nó que minimiza). O retorno é Tc = [(ui, ji)] 
    sendo ui a nova função que minimiza e ji o no que minimiza.

    IMPORTANTE: 
    f := o resultado do operador anterior;
    c_adj := é uma lista de adj que representa o grafo, mas ele na verdade marca todos os nós que chegam em i.
    m := é a constante ciclica minimal
    """
    Tc = []     #terá tupla do tipo (u0, j0), u0 é o peso que minimiza e o j0 é o nó que minimiza (que chega em i)
    Argmax = []
    for i in range(len(c_adj)):
        j = int()
        u = float("-inf")
        for pai in c_adj[i]:
            #A tentativa aqui é checar se o pai zero maximiza o valor anterior, se sim, atualiza j e u
            if f[pai[0]] - m + pai[1] > u:
                u = f[pai[0]] - m + pai[1]
                j = pai[0]

        Tc.append(u) #adiciona a nova operador para cada i
        Argmax.append(j)

    return Tc, Argmax


def floria_rec(custo ,conjunto_v, f, m, iterada=1):
    """Função recursiva que calcula simutaneamente a Constate Cíclica Minimal e os Corretores de um grafo.
        Entrada:
        custo: matriz custo de grafo conexo. (em arestas inexistentes o valor deve ser math.inf);
        conjunto_v: vetor de tamanho #V(G) com todas as entradas [1]. (Marca se o vértice foi otimizado.);
        f: vetor/função arbitrária de tamanho #V(G);
    """

    Tc, sigma = oleinik(f, custo, m) #calcula o lax_oleinik para todo i e parcialmente sigma.


    for j in range(conjunto_v.size):
        if f[j] - Tc[j] < 1e-9:  #se f[j] é maior que u[0]
            conjunto_v[j] = 1   
            f[j] = Tc[j]
        else:                    #se for menor ou igual
            conjunto_v[j] = 0    #Calcula se os vértices foram otimizados e atualiza o conjunto_v.
    

    if np.count_nonzero(conjunto_v) == 0 or iterada == 200:  
        return f, m, iterada                                #Condição de parada: Caso conjunto V tenha apenas zeros ou atinja o limite de iteradas.

    ciclos = []
    for j in range(len(conjunto_v)):
        if conjunto_v[j] == 1:
            k = j
            custo_din = 0
            for passagem in range(1, iterada+1):                            #calcula dinamicamente a média dos possíveis ciclos.
                custo_din = (custo_din*(passagem-1) + peso_aresta(custo, sigma[k], k))/passagem

                if sigma[k] == j:
                    ciclos.append(custo_din)
                
                k = sigma[k]

    if len(ciclos) > 0:
        m = min(m, min(ciclos))                                 #atualiza a constante.

    return floria_rec(custo, conjunto_v, f, m, iterada + 1)

def floria(custo, max):
    """Creates all auxiliar estructure"""
    conjunto_v = np.ones(shape=len(custo), dtype= np.int8)
    f = np.zeros(shape=len(custo))

    return floria_rec(custo, conjunto_v, f, max)


if __name__ == '__main__':
 # Exemplo de lista de adjacências reversa (arestas que chegam em i)
    c_adj = [
        [(0, 274)],
        [(1, 267), (4, 41)],
        [(0, 28), (1, 35), (3, 44), (4, 242)],
        [(0, 7), (2, 277), (3, 29)],
        [(1, 27), (3, 212)]
    ]
    draw.draw_weighted_graph_adj(c_adj)
    vetor, valor, iterada = floria(c_adj, 300)
    print (vetor, valor, sep= '\n')

