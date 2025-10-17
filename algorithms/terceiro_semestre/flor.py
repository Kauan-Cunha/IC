import numpy as np
import time
import grafoCriticoAlt as critic

def oleinik(f, c, m):
    """Calcula Lax-Oleinik para todo i. E retorna um vetor com o resultado (Tc) e outro com o índice j que faz o resultado (Argmin)"""
    Tc = []
    Argmin = []
    for i in range(len(f)):
        Tc.append(min(f-m+c[:,i]))
        Argmin.append(np.argmin(f-m+c[:,i]))

    return Tc, Argmin


def karp(custo):

    n = len(custo)

    # Calcula T(0), T^2(0), ... , T^n(0), T^{n+1}(0), onde T é o op. de Lax-Oleinik
    T = []
    T.append(np.zeros(n))
    for i in range(1,n+2):
        T.append(np.array(oleinik(T[i-1], custo, 0)[0]))

    min = np.max(custo) # cota superior para m(c) 
    for i in range(n):
        max = 0
        for k in range(1,n):
            maximize = (1/(n-k+1))*(T[n+1][i] - T[k][i]) # função a ser maximizada
            if max < maximize:
                max = maximize
        if min > max:
            min = max

    return min

def floria_rec(custo ,conjunto_v, f, m, iterada=1):
    """Função recursiva que calcula simutaneamente a Constate Cíclica Minimal e os Corretores de um grafo.
        Entrada:
        custo: matriz custo de grafo conexo. (em arestas inexistentes o valor deve ser math.inf);
        conjunto_v: vetor de tamanho #V(G) com todas as entradas [1]. (Marca se o vértice foi otimizado.);
        f: vetor/função arbitrária de tamanho #V(G);
    """

    Tc, sigma = oleinik(f, custo, m) #calcula o lax_oleinik para todo i e parcialmente sigma.

    for j in range(conjunto_v.size):
        if f[j] - Tc[j] > 1e-13:
            conjunto_v[j] = 1
            f[j] = Tc[j]
        else:                       #Calcula se os vértices foram otimizados e atualiza o conjunto_v.
            conjunto_v[j] = 0
            
    if np.count_nonzero(conjunto_v) == 0 or iterada == 200:  
        return f, m, iterada                                #Condição de parada: Caso conjunto V tenha apenas zeros ou atinja o limite de iteradas.

    ciclos = []
    for j in range(len(conjunto_v)):
        if conjunto_v[j] == 1:
            k = j
            custo_din = 0
            for passagem in range(1, iterada+1):                            #calcula dinamicamente a média dos possíveis ciclos.
                custo_din = (custo_din*(passagem-1) + custo[sigma[k]][k])/passagem

                if sigma[k] == j:
                    ciclos.append(custo_din)
                
                k = sigma[k]

    if len(ciclos) > 0:
        m = min(m, min(ciclos))                                 #atualiza a constante.

    return floria_rec(custo, conjunto_v, f, m, iterada + 1)

def floria(custo, max):
    """Creates all auxiliar estructure"""
    conjunto_v = np.ones(shape=len(custo[0]), dtype= np.int8)
    f = np.zeros(shape=len(custo))


    return floria_rec(custo, conjunto_v, f, max)


def main(custo, max):
    time_ini = time.time()
    result = floria(custo, max)
    time_fim = time.time()
    
    return time_fim - time_ini

if __name__ == '__main__':
    inf = float('inf')
    custo = [
        [inf, 2, inf],
        [2, inf ,1],
        [inf, 1, inf]
    ]

    vetor, valor, iterada = floria(np.array(custo), 100)
    print(f"---------Autovalor: {valor} \n Autovetor: {vetor}----------")
    print(critic.grafoCritico(custo, valor, vetor))