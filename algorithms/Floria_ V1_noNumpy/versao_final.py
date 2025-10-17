import math
import numpy as np
from random import randint

#func_u é uma função vetor que associa a entrada ao número da posiçaõ da entrada.
#mtx_custo: é uma matriz que representa os pesos das arestas do nosso gráfico


def le_matriz(size: int, matriz: list):
    maior =  0 

    for _ in range(size):
        linha = list(map(int, input().split()))
        if max(linha) > maior : maior  = max([x for x in linha if x != 10000])
        matriz.append(linha)

    return maior

def imprimi_mtx(matriz):
    for i in matriz:
        for j in i:
            print(j, end=" ")           #Debug: printa matriz custo.
        print()


def imprimi_debug(vetor, func, m, iterada):
    print(f"""          ~~~Iterada {iterada}~~~
          
        Vetor_V: {vetor}
        Func_u: {func}
        M: {m}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """)

def eh_menor(menor, maior):
    return True if maior - menor > 1.0e-13 else False

def operador(mtx_custo: list, func_u: list, j: int, m: int):
    """
    Calcula o operador para uma func_u e entrada j. T(func_u(j))
    """

    min = math.inf
    aux = int()
    argmin = int()

    for i in range(len(mtx_custo)):
        if i != j:
            aux = func_u[i] + mtx_custo[i][j] - m
            if eh_menor(aux, min):
                min = aux
                argmin = i

    return min, argmin

    #operador_saida = [min, argmin]

def random_matrix(matrix: list, range_entries: int, size: int):
    """
    Cria matriz com entradas entre [1, range_entries] e tamanho size.
    Retorna a maior entrada da matriz
    """
    max = 0
    for i in range(size):
        line = []
        for j in range(size):
            if(i == j):
                line.append(math.inf)
            else:
                aux = randint(1, range_entries)
                line.append(aux)
                if(aux > max ) & (aux != math.inf):
                    max = aux
        matrix.append(line)

    return max

def tamanho(lista: list):
    soma = 0
    for i in lista:
        soma += i

    return soma


def main():
    size = 5
    limite_entrada = 5

    sigma = np.zeros(size, dtype=int)
    func_u = np.zeros(size, dtype=int)
    mtx_custo = np.array
    conjunto_v = [1] * size 
    qntd_v = size
    # m = random_matrix(mtx_custo, limite_entrada, size) #retorna custo da aresta mais "cara". E setta matriz_custo aleatória.
    m = le_matriz(5, mtx_custo)
    

    imprimi_mtx(mtx_custo)

    iterada = 1
    while qntd_v > 0:
        imprimi_debug(conjunto_v, func_u, m, iterada)

        for j in range(size): #calculando conjunto V
            operador_saida = operador(mtx_custo, func_u, j, m)
            if eh_menor(operador_saida[0], func_u[j]):
                if conjunto_v[j] == 0 : qntd_v += 1
                conjunto_v[j] = 1
                func_u[j] = operador_saida[0]   #func_u
                sigma[j] = operador_saida[1]

                for i in range(len(conjunto_v)): #calcula cota_superior para os vertices que não estõa no conjunto V.
                    if(i==j):
                        continue

                    if(mtx_custo[i][j]<20):
                        sigma[j] = i
                        break
            else:
                if conjunto_v[j] == 1 :  qntd_v -= 1
                conjunto_v[j] = 0
                sigma[j] = operador_saida[1]

        custo_min = math.inf #calculando m.

        for j in range(size):
            custo_medio = 0
            # achou_ciclo = False
            if conjunto_v[j] == 1:   #se j pertence ao conjunto v.
                aux = j
                passagem = 1
                for _ in range(iterada and size):
                    custo_medio = (custo_medio*(passagem-1) + mtx_custo[sigma[aux]][aux])/passagem #calcula a média dinâmicamente

                    if sigma[aux] == j:
                        if custo_medio < custo_min:
                            custo_min = custo_medio

                    aux = sigma[aux]
                    passagem += 1


        m = m if m<custo_min else custo_min
        iterada += 1

        
main()