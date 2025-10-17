import math
import sys
from random import randint

#func_u é uma função vetor que associa a entrada ao número da posiçaõ da entrada.
#mtx_custo: é uma matriz que representa os pesos das arestas do nosso gráfico

def eh_menor(menor, maior):
    return True if maior - menor > 1.0e-13 else False

def imprimi_mtx(matriz):
    for i in matriz:
        for j in i:
            if j != math.inf : print(j, end=" ") 
            else : print("10000", end=" ")        #Debug: printa matriz custo.
        print()

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

def le_matriz(size):
    matriz = []
    for _ in range(size):
        linha = list(map(int, input().split()))
        matriz.append(linha)

    return matriz
        


def main():
    # size = int(input())
    # limite = int(input())
    size = int(sys.argv[1])
    limite = 20


    sigma = [0]*size  

    mtx_custo = list()
    vetor_v = [1] * size
    m = random_matrix(mtx_custo, limite, size)
    func_u = [0] * size



    min = int()
    
    iterada = 1


    print("################# ENTRADA #########################")
    print("Vetor_V: ", vetor_v)
    print("Func_u: ", func_u)                                           #debug: printa entrada.
    print("M:", m)      
    print("###################################################")
    

    iteracao = 1

    imprimi_mtx(mtx_custo)
    while tamanho(vetor_v) != 0:
        if iterada >20:
            sys.exit()

        for j in range(size): #calculando conjunto V
            operador_saida = operador(mtx_custo, func_u, j, m)
            if eh_menor(operador_saida[0], func_u[j]):
                vetor_v[j] = 1
                func_u[j] = operador_saida[0]   #func_u
                sigma[j] = operador_saida[1]
            else:
                vetor_v[j] = 0
                sigma[j] = operador_saida[1]




        for j in range(size): #calculando cota superior
            if vetor_v[j] == 0:
                for i in range(len(vetor_v)):
                    if(i==j):
                        continue

                    if(mtx_custo[i][j]<20):
                        sigma[j] = i
                        break

        custo_min = math.inf #calculando m.

        for j in range(size):
            custo_medio = 0
            # achou_ciclo = False
            if vetor_v[j] == 1:   #se j pertence ao conjunto v.
                aux = j
                passagem = 1
                for _ in range(iteracao and size):
                    custo_medio = (custo_medio*(passagem-1) + mtx_custo[sigma[aux]][aux])/passagem #calcula a média dinâmicamente

                    if sigma[aux] == j:
                        if custo_medio < custo_min:
                            custo_min = custo_medio

                    aux = sigma[aux]
                    passagem += 1


        m = m if m<custo_min else custo_min
        iteracao += 1
        
        print("##################", iterada, "########################")
        print(vetor_v)
        print(func_u)                                           #debug: printa cada iteração
        print(m)
        print("########################################\n")
        iterada += 1

main()
