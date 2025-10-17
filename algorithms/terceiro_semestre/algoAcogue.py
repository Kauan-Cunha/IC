import flor_adj as flor
import desenhar_grafo as draw
import grafoCriticoAlt as critico
import tarjan_listaDOIS as tarjan
import copy


def acougue_teste(custo_reverso, media_esperada):
    """
    Versão da função 'acougue' modificada para retornar o número de iterações.
    """
    grafo_modificado_direto = converter_adj_reversa_para_direta(custo_reverso)
    iteracao = 0

    while True:
        grafo_modificado_reverso = converter_adj_direta_para_reversa(grafo_modificado_direto)
        
        # O segundo argumento de floria é ignorado se você fez as correções anteriores
        vetor, valor, _ = flor.floria(grafo_modificado_reverso, 200)

        # Condição de parada principal
        if valor <= media_esperada:
            break
        
        # Limite de segurança para evitar loops infinitos em casos extremos
        if iteracao >= 100: 
            # print("Aviso: Limite de 100 iterações atingido.")
            break
        
        # Encontre o subgrafo crítico
        custo_critico_reverso = critico.grafoCritico_adj(grafo_modificado_reverso, valor, vetor)
        
        # Trava de segurança para problemas de precisão numérica
        num_arestas_criticas = sum(len(arestas) for arestas in custo_critico_reverso)
        if num_arestas_criticas == 0:
            # print(f"Aviso: Nenhuma aresta crítica encontrada para a média {valor:.4f}. Interrompendo.")
            break

        # Prossiga com o corte
        iteracao += 1 # Incremente o contador apenas quando um corte for realizado
        custo_critico_direto = converter_adj_reversa_para_direta(custo_critico_reverso)
        grafo_modificado_direto = tarjan.tarjan_com_guia(grafo_modificado_direto, custo_critico_direto)

    return iteracao # Retorna o número de cortes realizados


def acougue(custo_reverso, media_esperada):

    #Copia do custo que modificaremos
    custo_modificado = copy.deepcopy(custo_reverso)

    # Usaremos o formato direto para Tarjan e reverso para Floria
    vetor_atual, media_atual, _ = flor.floria(custo_reverso, 100)

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
        vetor_atual, media_atual, _ = flor.floria(custo_modificado, 100)

        
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
    
    result = acougue(grafo, 30)
    
    draw.draw_weighted_graph_adj(result)


if __name__ == "__main__":
    main()