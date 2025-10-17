import math
from random import randint  

def operador_oleinik(mtx_custo: list[list], vetor_u: list, m: int, j: int, sigma: list):
    """
    Calcula Operador de Oleinik dado a mtx_custo e um vetor/func U e m0.
    """
    min = vetor_u[j] #inf é o maior inteiro em python
    argmin = 0
    aux = 0
    auxdois

    for i in range(len(mtx_custo)):
        aux = vetor_u[i] + mtx_custo[i][j] - m
        if (aux < min) & (i != j):
            auxdois = 1
            min = aux
            argmin = i


    vetor_u[j] = min
    sigma[j] = argmin

    return min, argmin, aux

######################################################################



#######################################################################