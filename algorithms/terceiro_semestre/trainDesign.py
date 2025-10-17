from florMax import floria
from tarjan_lista import tarjan_lista as tarjan
from matrices import matriz_custo_para_lista_adj as mtxToAdj
from desenhar_grafo import desenhar 
from grafoCriticoAlt import grafoCritico

def design_train(custo_lista: list, T: int):
    """
    custo_lista: A linha representada em grafo de precedencia do que você quer melhorar.
    T: Tempo arbitrario máximo de espera em um ciclo/rota/linha.

    1.Calcula M(c) atual.
    2.Se M(c)<=T, para.
    3.Caso contrario, aplica tarjan modificado.
    4.Repete 1.

    """
    
    matriz_adj = mtxToAdj(custo_lista)
    m, u = floria(matriz_adj)
    c_normalizada = grafoCritico(matriz_adj, m, u)
    desenhar(c_normalizada)
    while m <= T:
        nova_malha = tarjan(c_normalizada)
        m, u = floria(c_normalizada)