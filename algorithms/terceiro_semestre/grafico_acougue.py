# teste_convergencia.py
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import algoAcogue as acougue

# --- PARÂMETROS DO EXPERIMENTO ---

# Diretório onde os grafos de teste estão localizados
DIRETORIO_GRAFOS = "grafos_de_teste"

# Define os tamanhos dos grafos a serem testados (deve corresponder ao que foi gerado)
TAMANHOS_TESTE = range(5, 101, 5)

# Quantos grafos testar para cada tamanho (deve corresponder ao que foi gerado)
GRAFOS_POR_TAMANHO = 10

# Média de ciclo desejada para o critério de parada do algoritmo
MEDIA_ESPERADA_FINAL = 0.0

# --- FUNÇÃO DE LEITURA DE GRAFO ---

def ler_grafo_de_arquivo(caminho_arquivo: str) -> list:
    """
    Lê um grafo de um arquivo de texto e o retorna no formato de lista de adjacência reversa.
    O formato do arquivo esperado é: 'filho pai peso' por linha.
    """
    arestas = []
    num_nos = 0
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            if not linha.strip(): continue # Pula linhas vazias
            filho, pai, peso = map(int, linha.strip().split())
            arestas.append((filho, pai, peso))
            num_nos = max(num_nos, filho, pai)

    adj_reversa = [[] for _ in range(num_nos + 1)]
    for filho, pai, peso in arestas:
        adj_reversa[filho].append((pai, peso))
        
    return adj_reversa

# --- FUNÇÃO PRINCIPAL DE EXECUÇÃO ---

def executar_experimento():
    """
    Executa o ciclo de testes a partir dos grafos pré-gerados,
    coleta os dados e gera o gráfico de resultados.
    """
    if not os.path.exists(DIRETORIO_GRAFOS):
        print(f"Erro: O diretório '{DIRETORIO_GRAFOS}' não foi encontrado.")
        print("Por favor, execute o script 'gerar_grafos_com_ciclo.py' primeiro.")
        return

    resultados = {n: [] for n in TAMANHOS_TESTE}
    
    print("\nIniciando o experimento de convergência...")
    tempo_total_inicio = time.time()

    for n in TAMANHOS_TESTE:
        print(f"\nTestando grafos de tamanho n={n}...")
        for i in range(GRAFOS_POR_TAMANHO):
            nome_arquivo = os.path.join(DIRETORIO_GRAFOS, f"grafo_n{n}_id{i}.txt")
            
            custo_reverso = ler_grafo_de_arquivo(nome_arquivo)
            
            iteracoes = acougue.acougue_teste(custo_reverso, MEDIA_ESPERADA_FINAL)
            
            resultados[n].append(iteracoes)
            print(f"  Grafo {i+1}/{GRAFOS_POR_TAMANHO}: {iteracoes} iterações.")
            
    tempo_total_fim = time.time()
    print(f"\nExperimento concluído em {tempo_total_fim - tempo_total_inicio:.2f} segundos.")

    # --- ANÁLISE E PLOTAGEM DOS RESULTADOS ---
    print("Analisando resultados e gerando gráfico...")
    
    tamanhos_plot = sorted(resultados.keys())
    medias_iteracoes = [np.mean(resultados[n]) for n in tamanhos_plot]
    desvios_padrao = [np.std(resultados[n]) for n in tamanhos_plot]
    
    plt.figure(figsize=(12, 7))
    plt.errorbar(tamanhos_plot, medias_iteracoes, yerr=desvios_padrao,
                 fmt='-o', capsize=5, label='Média de Iterações com Desvio Padrão')
    
    plt.title('Convergência do Algoritmo "Açougue" (Ciclo Máximo Garantido)')
    plt.xlabel('Tamanho do Grafo (Número de Vértices)')
    plt.ylabel('Número Médio de Iterações')
    plt.xticks(TAMANHOS_TESTE)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    
    nome_grafico = 'convergencia_acougue_ciclo_garantido.png'
    plt.savefig(nome_grafico)
    print(f"Gráfico salvo como '{nome_grafico}'.")
    
    plt.show()

if __name__ == '__main__':
    executar_experimento()