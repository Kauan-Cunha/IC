import sys
import os

# Obtém o diretório onde este arquivo (acougue.py) está localizado
current_dir = os.path.dirname(os.path.abspath(__file__))

# Adiciona o próprio diretório (Algoritmos) ao path para encontrar dfs_corte_burro, floria, etc.
sys.path.append(current_dir)

# Adiciona o diretório pai (Reescrita) ao path para encontrar Grafo.Grafo
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

import copy
import Grafo.Grafo as g
import dfs_corte_burro as dfs
import dfs_corte_intel as dfs_intel
import floria as flor
import critico
import desenhar as draw
import time


def acougue_teste(grafo: g.Grafo, media_esperada: float, tipo: str = 'burro') -> g.Grafo:
    """
    1. Calcula M(c) atual.
    2. Se M(c) <= T, para.
    3. Caso contrario, aplica tarjan modificado.
    4. Repete 1.
    """

    grafo_atual = copy.deepcopy(grafo)

    vetor_atual, media_atual, _, custo_atual = flor.floria(grafo_atual, is_max_or_min='max')
    

    iteracao = 0
    floria_tempo_medio = 0
    while True:
        # Trava de segurança
        if iteracao > 200:
            break

        if media_atual <= media_esperada:
            break


        grafo_ciclo = critico.grafoCritico(grafo_atual, media_atual, vetor_atual, is_max_or_min='max')

        if tipo == 'burro':
            grafo_atual = dfs.dfs_corte(grafo_atual, grafo_ciclo)
        else:
            grafo_atual = dfs_intel.dfs_corte(grafo_atual, grafo_ciclo)

        # draw.desenhar_grafo(grafo_atual, layout='circular')##------------------------------ se quiser ver o progresso desenhado
        # Calcula o novo M(c)
        time_inicio_floria = time.time()
        vetor_atual, media_atual, _, custo_atual = flor.floria(grafo_atual, is_max_or_min='max')
        time_fim_floria = time.time()

        floria_tempo_medio += (time_fim_floria - time_inicio_floria)

        iteracao += 1
    
    floria_tempo_medio /= iteracao
    return iteracao, floria_tempo_medio


def acougue(grafo: g.Grafo, media_esperada: float, tipo: str = 'burro') -> g.Grafo:
    """
    1. Calcula M(c) atual.
    2. Se M(c) <= T, para.
    3. Caso contrario, aplica tarjan modificado.
    4. Repete 1.
    """

    grafo_atual = copy.deepcopy(grafo)

    vetor_atual, media_atual, _, custo_atual = flor.floria(grafo_atual, is_max_or_min='max')

    iteracao = 0
    while True:
        # Trava de segurança
        if iteracao > 200:
            break

        if media_atual <= media_esperada:
            break


        grafo_ciclo = critico.grafoCritico(grafo_atual, media_atual, vetor_atual, is_max_or_min='max')

        if tipo == 'burro':
            grafo_atual = dfs.dfs_corte(grafo_atual, grafo_ciclo)
        else:
            grafo_atual = dfs_intel.dfs_corte(grafo_atual, grafo_ciclo)

        # draw.desenhar_grafo(grafo_atual, layout='circular')##------------------------------ se quiser ver o progresso desenhado
        # Calcula o novo M(c)
        vetor_atual, media_atual, _, custo_atual = flor.floria(grafo_atual, is_max_or_min='max')

        iteracao += 1
    
    return grafo_atual


def main():
    # --- Grafo "grafo" (O usado no teste) ---
    grafo = g.Grafo(3)
    
    # Índice 0: chegam 1 e 2
    grafo.adicionar_aresta(1, 0, 80)
    grafo.adicionar_aresta(2, 0, 60)
    
    # Índice 1: chega 0
    grafo.adicionar_aresta(0, 1, 2)
    
    # Índice 2: chega 0
    grafo.adicionar_aresta(0, 2, 2)

    
    draw. desenhar_grafo(grafo, layout='burro')
    result = acougue(grafo, 15, tipo='intel' )
    
    draw.desenhar_grafo(result, layout='circular')

    print(result)
if __name__ == "__main__":
    main()