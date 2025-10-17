import flor_adj as flor
import desenhar_grafo as draw
import grafoCriticoAlt as critico
import tarjan_listaDOIS as tarjan
import copy


def acougue_teste(custo_reverso, media_esperada):

    #Copia do custo que modificaremos
    custo_modificado = copy.deepcopy(custo_reverso)

    # Usaremos o formato direto para Tarjan e reverso para Floria
    vetor_atual, media_atual, _ = flor.floria(custo_reverso, 0)

    #Começo a iterar    
    iteracao = 0
    while True:
        if iteracao > 200:
            break
        
        if media_atual <= media_esperada:
            break

        #Pego meu ciclo maximizante
        grafo_critico = critico.grafoCritico_adj(custo_modificado, media_atual, vetor_atual)

        draw.draw_weighted_graph_adj(grafo_critico)
        #Corta o ciclo maximizante
        _, custo_modificado,_ = tarjan.tarjan_subgrafo_lista(custo_modificado, grafo_critico)
        draw.draw_weighted_graph_adj(custo_modificado)
        #Pega o novo valor do vetor e constante ciclica maximal.
        vetor_atual, media_atual, _ = flor.floria(custo_modificado, 0)

        
        print(media_atual)
        iteracao += 1
    
    return iteracao



def acougue(custo_reverso, media_esperada):

    #Copia do custo que modificaremos
    custo_modificado = copy.deepcopy(custo_reverso)

    # Usaremos o formato direto para Tarjan e reverso para Floria
    vetor_atual, media_atual, _ = flor.floria(custo_reverso, 0)

    #Começo a iterar    
    iteracao = 0
    while True:
        if iteracao > 200:
            break
        
        if media_atual <= media_esperada:
            break

        #Pego meu ciclo maximizante
        grafo_critico = critico.grafoCritico_adj(custo_modificado, media_atual, vetor_atual)

        draw.draw_weighted_graph_adj(grafo_critico)
        #Corta o ciclo maximizante
        _, custo_modificado,_ = tarjan.tarjan_subgrafo_lista(custo_modificado, grafo_critico)
        draw.draw_weighted_graph_adj(custo_modificado)
        #Pega o novo valor do vetor e constante ciclica maximal.
        vetor_atual, media_atual, _ = flor.floria(custo_modificado, 0)

        
        print(media_atual)
        iteracao += 1
    
    return custo_modificado

        

def main():
    grafo = [
        [(3, 1)],  # Vértice 0 aponta para 1 e peso 20
        [(0, 100), (2, 1)],   # Vértice 1 aponta para 0 e peso 5
        [(1, 50)],  # Vértice 2 aponta para 3 e peso 10
        [(1, 1)],   # Vértice 3 aponta para 4 e peso 1
    ]
    
    draw.draw_weighted_graph_adj(grafo)
    
    result = acougue(grafo, 20)
    
    draw.draw_weighted_graph_adj(result)


if __name__ == "__main__":
    main()