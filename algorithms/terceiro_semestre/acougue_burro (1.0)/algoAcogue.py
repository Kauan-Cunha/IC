import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import flor_adj_dual as flor
import desenhar_grafo as draw
import grafoCriticoAlt as critico
import tarjan_listaDOIS as tarjan
import copy

def acougue_teste(custo_reverso, media_esperada):

    #Copia do custo que modificaremos
    custo_modificado = copy.deepcopy(custo_reverso)

    # Usaremos o formato direto para Tarjan e reverso para Floria
    vetor_atual, media_atual, _, custo_invertido = flor.floria(custo_reverso, 0, is_max_or_min= 'max')

    #Começo a iterar    
    iteracao = 0
    while True:
        if iteracao > 200:
            break
        
        if media_atual <= media_esperada:
            break

        #Pego meu ciclo maximizante
        grafo_critico = critico.grafoCritico_adj(custo_modificado, media_atual, vetor_atual)

        #Corta o ciclo maximizante
        _, custo_modificado,_ = tarjan.tarjan_subgrafo_lista(custo_modificado, grafo_critico)

        #Pega o novo valor do vetor e constante ciclica maximal.
        vetor_atual, media_atual, _, custo_invertido = flor.floria(custo_modificado, 0)

        
        print(media_atual)
        iteracao += 1
    
    return iteracao



def acougue(custo_reverso, media_esperada):
    """
    custo_lista: A linha representada em grafo de precedencia do que você quer melhorar.
    T: Tempo arbitrario máximo de espera em um ciclo/rota/linha.

    1.Calcula M(c) atual.
    2.Se M(c)<=T, para.
    3.Caso contrario, aplica tarjan modificado.
    4.Repete 1.

    """

    #Copia do custo que modificaremos
    custo_modificado = copy.deepcopy(custo_reverso)

    # Usaremos o formato direto para Tarjan e reverso para Floria
    vetor_atual, media_atual, _, custo_invertido = flor.floria(custo_reverso, 0, is_max_or_min= 'max')

    #Começo a iterar    
    iteracao = 0
    while True:
        if iteracao > 200:
            break
        
        if media_atual >= -media_esperada:
            break

        #Pego meu ciclo maximizante
        grafo_critico = critico.grafoCritico_adj(custo_invertido, media_atual, vetor_atual, is_max_or_min = 'max')

        draw.draw_weighted_graph_adj(grafo_critico)
        #Corta o ciclo maximizante
        _, custo_invertido,_ = tarjan.tarjan_subgrafo_lista(custo_invertido, grafo_critico)
        draw.draw_weighted_graph_adj(custo_invertido)
        #Pega o novo valor do vetor e constante ciclica maximal.
        vetor_atual, media_atual, _, custo_invertido = flor.floria(custo_invertido, 0, is_max_or_min= 'min')

        
        print(media_atual)
        iteracao += 1
    
    return custo_invertido

        

def main():
    grafo = [
        [[1,1], [4, 1000], [3, 1]],
        [[1,2], [0,100]],
        [[0,100]],
        [[2,200]],
        [],
        [[2,9]]
    ]
    
    draw.draw_weighted_graph_adj(grafo)
    
    result = acougue(grafo, 20)
    
    draw.draw_weighted_graph_adj(result)


if __name__ == "__main__":
    main()