import math
import numpy as np
import matrices as matrices
import grafoCriticoAlt as gc

def mult_matriz(A, B):
    """"Multiplicação de matrizes A e B com multiplicação tropical"""
    C = np.zeros((len(A), len(B[0])), dtype=np.float64)
    
    for i in range(len(A[0])):
        for j in range(len(A[0])):
            min = math.inf
            for k in range(len(A[0])):
                result = A[i][k] + B[k][j]
                if min > result:
                    min = result
            C[i][j] = min
    return C

def identidadeTropical(n):
    """Cria uma matriz identidade tropical (i,j) = 0 se i == j, inf caso contrário"""
    I = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            if i != j:
                I[i][j] = math.inf
    return I

def mult_N_matriz(A, n):
    """Multiplicação de matriz A por ela mesma n vezes"""
    if n == 0:
        return identidadeTropical(len(A))
    C = np.copy(A)
    for i in range(n-1):
        C = mult_matriz(C, A)
    return C

def mult_matriz_vetor(A, v):
    """Multiplicação de matriz A por vetor v com multiplicação tropical"""
    C = []
    for i in range(len(A)):
        min_val = math.inf
        for j in range(len(A[0])):
            result = A[i][j] + v[j]
            if min_val > result:
                min_val = result
        C.append(min_val)
    return C

def imprimir_matriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if j == len(matriz[0]) - 1:
                print(matriz[i][j])
            else:
                print(matriz[i][j], end=" ")
    print()

def ler_matriz():
    """Lê uma matriz do usuário, aceitando 'inf' como infinito"""
    matriz = []
    n = int(input())
    for i in range(n):
        linha_str = input().split()
        linha = []
        for val in linha_str:
            if val == "inf":
                linha.append(math.inf)
            else:
                linha.append(float(val))
        matriz.append(linha)
    return np.array(matriz)

def estrelaKleene(matriz, tau):
    """Calcula a estrela de Kleene de uma matriz"""
    n = matriz.shape[0]
    matriz_resultante = np.empty((n, n), dtype=np.float64)

    lista_matrizes = []
    for i in range(n):
        lista_matrizes.append(mult_N_matriz(matriz-tau, i))
    
    for i in range(n):
        for j in range(n):
            min = math.inf
            for k in range(n):
                result = lista_matrizes[k][i][j]
                if min > result:
                    min = result
            matriz_resultante[i][j] = min

    return matriz_resultante

def main():
    mtx = matrices.fully_connected_matrices(3)
    mtx_custo = matrices.randomised_weigh_matrix(mtx, 10)
    imprimir_matriz(mtx_custo[0])

    s_normalizado = gc.grafoCriticoCombConvexa(mtx_custo[0])
    mtxC_normalizado = s_normalizado.T
    imprimir_matriz(mtxC_normalizado)
    mtxC_normalizadoDOIS = gc.grafoCriticoProp(mtx_custo[0])

    
    imprimir_matriz(mtxC_normalizadoDOIS)


if __name__ == "__main__":
    main()