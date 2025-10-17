import lax_oleinik as lax
from sys import argv
import math

def main():
    size = int(input())
    matriz_custo = list()
    m = lax.random_matrix(matriz_custo, 10, size)
    sigma = [0] * size

    u = [0] * size #vetor/funcao arbitraria u0
    V_use = size
    V = [1] * size #marca se foi otimizado ou não.

    while V_use>0:      #Calcula o operador de u(j) e troca V(j)
        for j in range(size):
            min_and_arg = lax.operador_oleinik(matriz_custo, u, m, j, sigma)
            if (min_and_arg[2]):
                if(V[j] == 0):
                    V[j] = 1
                    V_use += 1
            else:
                if(V[j] == 1):
                    V[j] = 0
                    V_use -= 1
                sigma[j] = (j+1)%size

    for ent in u:
        print(ent)

    print("####################################################")

    for a in matriz_custo:
        for b in a:
            print(b, end=" ")
        print()


if __name__ == "__main__":
    main()


    #Falta calcular o cota superior m0, m1, m2, m(c).  