import math
from random import randint

#func_u é uma função vetor que associa a entrada ao número da posiçaõ da entrada.
#mtx_custo: é uma matriz que representa os pesos das arestas do nosso gráfico
    
def operador_oleinik(custo, funcao_u, m):
    """
    Calcula Operador de Oleinik dado a relação de custo, uma funcao U e a constante ciclica minimal m.
    Estabelece o conjunto V com base no critério de lax_oleinik[i] < u[i]
    Estabelece a nova função U, com base no critério min{u(i), operador_oleinik(i)}
    """
    # define o minimo como o maior valor possível inicialmente
    lax_oleinik = [math.inf] * len(custo)
    conjunto_V = [0] * len(custo)
    aux = 0

    # percorre cada vértice e calcula o operador Lax Oleinik
    for i in range(len(custo)):
        for j in range(len(custo)):
            if(i==j):
                continue
            aux = funcao_u[i] + custo[i][j] - m
            # o operador i sempre assume o valor minimo
            lax_oleinik[i] = min(aux, lax_oleinik[i])

        # determina lax_oleinik
        if(lax_oleinik[i]<funcao_u[i]):
            conjunto_V[i] = 1

        # determina a nova função arbitrária u
        funcao_u[i] = min(funcao_u[i], lax_oleinik[i])

    return lax_oleinik, conjunto_V, funcao_u

def matriz_aleatoria(n, limite):
    """
    Cria uma matriz aleatória n x n, que pode representa o custo ou a matriz de adjascência
    Assume valores entre 1 e um limite e retorna o maior valor da matriz
    A posição [i][i] = 0, tanto para o custo, quanto para os caminhos entre os vértices
    """
    matriz = []
    maximo = 0
    for i in range(n):
        linha = []
        for j in range(n):
            if(i==j):
                linha.append(0)
            
            # Gera números aleatórios de 1 até o limite
            else:
                linha.append(randint(1, limite))  
        
        matriz.append(linha)    
        # Encontrar o valor máximo na matriz
        maximo = max(max(linha) for linha in matriz)
    
    return matriz, maximo

def tamanho(lista: list):
    soma = 0
    for i in lista:
        soma += i

    return soma


def main():
    #Pega a entrada.
    tamanho = int(input())
    limite = int(input())

    vetor_argmin = [0]* tamanho
    vetor_v = [1] * tamanho
    mtx_custo, m = matriz_aleatoria(tamanho, limite)
    funcao_u = [1] * tamanho


    

    for i in mtx_custo:
        for j in i:
            print(j, end=" ")           #Debug: printa matriz custo.
        print()


    min = int()
    iterada = 1


    print("################# ENTRADA #########################")
    print("Vetor_V: ", vetor_v)
    print("Func_u: ", funcao_u)                                           #debug: printa entrada.
    print("M:", m)      
    print("###################################################")
    
    while tamanho(vetor_v) != 0:
        
        operador, vetor_v, funcao_u = operador_oleinik(mtx_custo, funcao_u, m)

        for j in range(tamanho): #calculando cota superior
            if vetor_v[j] == 0:
                for i in range(vetor_v):
                    if(i==j):
                        continue

                    if(mtx_custo[i][j]<math.inf):
                        vetor_argmin[j] = i
                        break

        
        for j in range(tamanho): #calculando mr
            if vetor_v[j] == 1:
                for i in range(j+1, tamanho):
                    min = math.inf
                    if j == vetor_argmin[i]:
                        custo_ciclo = 0
                        aux = j
                        for _ in range(i - j):
                            custo_ciclo += mtx_custo[aux][vetor_argmin[aux]]
                            aux = vetor_argmin[aux]
                        
                        min = custo_ciclo if custo_ciclo<min else min


        m = m if m<min else min
        
        print("##################", iterada, "########################")
        print(vetor_v)
        print(funcao_u)                                           #debug: printa cada iteração
        print(m)
        print("########################################")
        iterada += 1
    
    print(m)  

main()
