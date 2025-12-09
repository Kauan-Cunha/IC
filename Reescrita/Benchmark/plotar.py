import sys
import os
import time
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import mtxGenerator as mtx

# Adiciona o diretório pai ao path para encontrar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Grafo.Grafo as g
from Algoritmos.acougue import acougue_teste



def rodar_benchmark():
    # CONFIGURAÇÕES DO BENCHMARK

    # Comece com valores baixos.
    tamanhos_vertices = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50] 
    
    amostras_por_tamanho = 3   # Média de 10 execuções para evitar dispersão
    media_esperada_alvo = 100    # Um valor baixo para forçar o algoritmo a trabalhar bastante
    
    tempos_burro = []
    tempos_intel = []

    print(f"Iniciando Benchmark...")
    print(f"Configuração: {amostras_por_tamanho} amostras por tamanho, Alvo de média = {media_esperada_alvo}")
    print("-" * 60)

    for n in tamanhos_vertices:
        print(f"Testando Grafos com N={n} vértices...")
        
        tempos_locais_burro = []
        tempos_locais_intel = []

        for i in range(amostras_por_tamanho):
            # Gera um grafo aleatório denso
            grafo_base = mtx.gerar_grafo_completo(n)
            

            # --- Teste Inteligente ---
            inicio = time.time()
            iteracao, _ = acougue_teste(grafo_base, media_esperada_alvo, tipo='intel')
            fim = time.time()
            tempos_locais_intel.append(fim - inicio)

            # --- Teste Burro ---
            inicio = time.time()
            iteracao_b, _ = acougue_teste(grafo_base, media_esperada_alvo, tipo='burro')
            fim = time.time()

            tempos_locais_burro.append(fim - inicio)
            print(f"b: {iteracao_b} | i: {iteracao}")

        # Calcula as médias
        media_b = np.mean(tempos_locais_burro)
        media_i = np.mean(tempos_locais_intel)
        
        tempos_burro.append(media_b)
        tempos_intel.append(media_i)
        
        print(f"\n  -> Média Burro: {media_b:.4f}s | Média Intel: {media_i:.4f}s")
        print("-" * 60)

    return tamanhos_vertices, tempos_burro, tempos_intel


def rodar_benchmark_floria():
    # CONFIGURAÇÕES DO BENCHMARK

    # Comece com valores baixos.
    tamanhos_vertices = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50] 
    
    amostras_por_tamanho = 3   # Média de 10 execuções para evitar dispersão
    media_esperada_alvo = 10    # Um valor baixo para forçar o algoritmo a trabalhar bastante
    
    tempos_burro = []
    tempos_intel = []

    print(f"Iniciando Benchmark...")
    print(f"Configuração: {amostras_por_tamanho} amostras por tamanho, Alvo de média = {media_esperada_alvo}")
    print("-" * 60)

    for n in tamanhos_vertices:
        print(f"Testando Grafos com N={n} vértices...")
        
        tempos_locais_burro = []
        tempos_locais_intel = []

        for i in range(amostras_por_tamanho):
            # Gera um grafo aleatório denso
            grafo_base = mtx.gerar_grafo_completo(n)
            


            _, floria_b = acougue_teste(grafo_base, media_esperada_alvo, tipo='burro')


            tempos_locais_burro.append(floria_b)


            _, floria_i = acougue_teste(grafo_base, media_esperada_alvo, tipo='intel')

            tempos_locais_intel.append(floria_i)
            

        # Calcula as médias
        media_b = np.mean(tempos_locais_burro)
        media_i = np.mean(tempos_locais_intel)
        
        tempos_burro.append(media_b)
        tempos_intel.append(media_i)
        
        print(f"\n  -> Média Burro: {media_b:.4f}s | Média Intel: {media_i:.4f}s")
        print("-" * 60)

    return tamanhos_vertices, tempos_burro, tempos_intel

def plotar_resultados(x, y_burro, y_intel):
    plt.figure(figsize=(10, 6))
    
    plt.plot(x, y_burro, marker='o', linestyle='-', color='red', label='Açougue (Burro)')
    plt.plot(x, y_intel, marker='s', linestyle='--', color='blue', label='Açougue (Inteligente)')
    
    plt.title('Benchmark: Corte de Ciclos em Grafos Densos (Comparando Floria)')
    plt.xlabel('Número de Vértices (N)')
    plt.ylabel('Tempo Médio de Execução (segundos)')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Adiciona os valores nos pontos
    for i, txt in enumerate(y_burro):
        plt.annotate(f"{txt:.2f}s", (x[i], y_burro[i]), textcoords="offset points", xytext=(0,10), ha='center', color='red')
        
    for i, txt in enumerate(y_intel):
        plt.annotate(f"{txt:.2f}s", (x[i], y_intel[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='blue')

    plt.tight_layout()
    plt.savefig('resultado_benchmark.png') # Salva em arquivo
    print("\nGráfico salvo como 'resultado_benchmark.png'")
    plt.show() # Mostra na tela

if __name__ == "__main__":
    x, y_burro, y_intel = rodar_benchmark()
    plotar_resultados(x, y_burro, y_intel)