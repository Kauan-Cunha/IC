import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import Grafo.Grafo as g
import numpy as np

def oleinik(f, grafo, m):
    """
    Calcula a constante de lax-oleinik e o argmax(nó que maximiza).
    """
    Tc = []
    Argmin = []
    MinCost = []
    for i in range(grafo.num_vertices):
        # Se ninguém chega em i, mantemos o valor de f[i] e definimos inf como o custo mínimo.
        if not grafo.obter_chegada(i):
            Tc.append(f[i])      
            Argmin.append(i)     
            MinCost.append(float('inf'))
            continue             

        # Se tiver Pai(s) calcula o mínimo entre eles e armazena o argmin e o custo da aresta mínima.
        j = -1 
        u = float("inf")
        custo_aresta_min = float("inf")
        for pai, valor in grafo.obter_chegada(i).items():
            valor_candidato = f[pai] - m + valor
            if valor_candidato < u:
                u = valor_candidato
                j = pai
                custo_aresta_min = valor

        Tc.append(u)
        Argmin.append(j)
        MinCost.append(custo_aresta_min)

    return Tc, Argmin, MinCost

def floria_rec(grafo ,conjunto_v, f, m, iterada=1):
    """Função recursiva que calcula simutaneamente a Constate Cíclica Minimal e os Corretores de um grafo.
        Entrada:
        custo: matriz custo de grafo conexo. (em arestas inexistentes o valor deve ser math.inf);
        conjunto_v: vetor de tamanho #V(G) com todas as entradas [1]. (Marca se o vértice foi otimizado.);
        f: vetor/função arbitrária de tamanho #V(G);
    """

    #Esse custo_sigma guarda os valores dos pais para serem usados em media_dinâmica
    Tc, sigma, custos_sigma = oleinik(f, grafo, m) #calcula o lax_oleinik para todo i e parcialmente sigma.

    for j in range(conjunto_v.size):
        if f[j] - Tc[j] > 1e-13:  #se f[j] é maior que u[0]
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
            for passagem in range(1, iterada+1):
                # Substitui a chamada peso_aresta por um acesso O(1)
                custo_din = (custo_din*(passagem-1) + custos_sigma[k])/passagem

                if sigma[k] == j:
                    ciclos.append(custo_din)
                
                k = sigma[k]

    if len(ciclos) > 0:
        m = min(m, min(ciclos))                                 #atualiza a constante.

    return floria_rec(grafo, conjunto_v, f, m, iterada + 1)

def floria(grafo: g.Grafo, is_max_or_min = 'min') -> list:
    # 1. Configura o modo (isso agora troca os pesos internamente na classe)
    tipo = 1 if is_max_or_min == 'max' else 0
    grafo.definir_max_ou_min(tipo) 

    # 2. Executa o algoritmo (ele nem sabe que os pesos mudaram)
    conjunto_v = np.ones(grafo.num_vertices, dtype= np.int8)
    f = np.zeros(grafo.num_vertices)
    vetor, valor, iterada = floria_rec(grafo, conjunto_v, f, grafo.obter_max())

    # 3. Restaura para o padrão (opcional, mas boa prática)
    grafo.definir_max_ou_min(0)
    
    if is_max_or_min == 'max':
        valor = -valor
        
    return vetor, valor, iterada, grafo

def main():
    grafo = g.Grafo(4)

def main():
    grafo = g.Grafo(4)

    # Adicionar arestas (Corrigido para bater com flor_adj_dual.py)
    grafo.adicionar_aresta(3, 0, 1)     
    grafo.adicionar_aresta(0, 1, 100)
    grafo.adicionar_aresta(2, 1, 1)
    grafo.adicionar_aresta(1, 2, 50)
    grafo.adicionar_aresta(1, 3, 1)

    # Rodar Flória usando 'min' para comparar com o original
    vetor, valor, iterada, grafo = floria(grafo, is_max_or_min='min')

    print("vetor:", vetor)
    print("valor:", valor)
    print("iterada:", iterada)


if __name__ == "__main__":
    main()