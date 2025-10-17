import operacaoTropicalMtx as ot
import numpy as np
import flor
import time

def grafoCritico_adj(c_adj, m, u):
    """
    Retorna a lista de adjacências do grafo crítico:
    Só mantém as arestas cujo peso renormalizado é zero (ou próximo de zero).
    O peso armazenado é o peso original da aresta.
    """
    n = len(c_adj)
    c_crit_reverso = []
    for i in range(n):
        entradas = []
        for pai, peso in c_adj[i]:
            # Fórmula correta para MAX-PLUS
            w_norm = u[pai] + peso - m - u[i]
            if abs(w_norm) < 1.0e-13:
                # Adiciona no formato REVERSO (como a entrada)
                entradas.append((pai, peso))
        c_crit_reverso.append(entradas)
    return c_crit_reverso

def grafoCritico(c, m, u):

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
        c_norm[i][j] += u[j] - u[i] - m
        if c_norm[i][j] < 1.0e-14 and c_norm[i][j] != float('-inf'):
          c_norm[i][j] = 0 # Ignora erros de precisão finita

    return c_norm

def graficoCriticoAlt(matrixCusto):
    """
    Função que calcula o grafo crítico de um grafo a partir da matriz de custo.
    """
    S = matrixCusto.T

    tau = flor.karp(matrixCusto)
    SEstrela = ot.estrelaKleene(S, tau)

    grafoCritico = np.zeros((len(SEstrela), len(SEstrela)), dtype=np.float64)
    
    for i in range(len(SEstrela)):
        for j in range(len(SEstrela)):
            for k in range(len(SEstrela)):
                if S[i][j] + SEstrela[j][k] != SEstrela[i][k]:
                    break
                if SEstrela[k][j] != SEstrela[k][i] + S[i][j]:
                    break
            
            grafoCritico[j][i] = 1

    return grafoCritico

def grafoCriticoEstrela(matrixCusto):
    S = matrixCusto.T
    tau = flor.karp(matrixCusto)
    print("Tau: ", tau)
    SEstrela = ot.estrelaKleene(S, tau)

    #Teste das colunas
    autovetor = None
    for coluna in SEstrela.T:
        soma = tau + coluna.tolist()
        multiplicacao = ot.mult_matriz_vetor(S, coluna)

        if np.allclose(multiplicacao, soma):
            autovetor = coluna
            break

        
    #Achar grafoCritico
    grafoFinal = np.empty((len(SEstrela), len(SEstrela)), dtype=np.float64)

    for i in range(len(S)):
        for j in range(len(S)):
            grafoFinal[i][j] = S[j][i] + autovetor[i] - autovetor[j] - tau 
    
    return grafoFinal-tau   

def grafoCriticoCombConvexa(matriz):
    """Entraremos o grafo crítico partindo da prop. 5.30:
        
        O vetor resultado de combinação convexa das colunas da estrela de Kleene é separante.
        
    """
    tau = flor.karp(matriz)
    print(f"TAU DA COMB CONVEXA: {tau}")
    S = matriz.T
    SEstrela = ot.estrelaKleene(S,tau)

    #Calculando vetor separante!
    a_r = 1/len(matriz)
    vetor_separante = [0]*len(matriz)
    for coluna in SEstrela.T:
        vetor_separante = vetor_separante + (coluna * a_r)
    
    #Calculando Ŝ:

    s_normalizada = np.zeros((len(matriz), len(matriz)))
    
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            s_normalizada[i][j] = S[i][j] + vetor_separante[j] - vetor_separante[i]
    
    return s_normalizada

def grafoCriticoProp(matriz):
    subGrafoCrit = np.zeros((len(matriz), len(matriz)))
    tau = flor.karp(matriz)
    
    # Não transponha a matriz. S(i, j) deve ser o peso do arco (i, j).
    S = matriz 
    
    SEstrela = ot.estrelaKleene(S, tau)

    # Verificando a Condição ii para cada aresta (i, j)
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            aux = True
            for j_0 in range(len(matriz)):
                # A condição matemática para a aresta (i, j)
                if S[i][j] + SEstrela[j][j_0] != SEstrela[i][j_0]:
                    aux = False
                    break  # Otimização: se falhou uma vez, não precisa continuar
            
            if aux:
                # Se a condição valeu para todo j_0, a aresta (i, j) é crítica.
                subGrafoCrit[i][j] = 1
                
    return subGrafoCrit


def grafoCriticoFloria(custo: list[list]) -> list[list]:
    """
    Usando floria encontramos o autovetor e valor
    """

def main():
    A = ot.ler_matriz()
    ot.imprimir_matriz(ot.estrelaKleene(A))
