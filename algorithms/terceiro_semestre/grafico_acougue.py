import random
import numpy as np
import matplotlib.pyplot as plt
import algoAcogue as acougue
import pprint # Módulo para formatar a lista de forma legível

def gerar_grafo_reverso_com_ciclo(num_vertices, num_extra_edges):
    """
    Gera um grafo aleatório com pelo menos um ciclo garantido.

    A representação é uma lista de adjacências REVERSA, onde
    grafo[i] contém uma lista de tuplas (pai, peso) para arestas pai -> i.
    """
    if num_vertices <= 0:
        return []

    grafo_reverso = [[] for _ in range(num_vertices)]
    
    # 1. Garante pelo menos um ciclo
    for i in range(num_vertices):
        origem = i
        destino = (i + 1) % num_vertices
        peso = random.randint(1, 100)
        grafo_reverso[destino].append((origem, peso))

    # 2. Adiciona arestas extras
    arestas_adicionadas = set()
    for i in range(num_vertices):
        arestas_adicionadas.add((i, (i + 1) % num_vertices))

    for _ in range(num_extra_edges):
        while True:
            origem = random.randint(0, num_vertices - 1)
            destino = random.randint(0, num_vertices - 1)
            if origem != destino and (origem, destino) not in arestas_adicionadas:
                break
        
        peso = random.randint(1, 100)
        grafo_reverso[destino].append((origem, peso))
        arestas_adicionadas.add((origem, destino))
        
    return grafo_reverso

def main():
    """
    Função principal para executar o teste de desempenho, gerar logs e plotar o gráfico.
    """
    tamanhos_dos_grafos = []
    iteracoes_de_convergencia = []
    log_entries = [] # Lista para armazenar as strings de log

    # --- Configurações do Teste ---
    MIN_VERTICES = 2
    MAX_VERTICES = 20
    PASSO = 1
    MEDIA_ALVO = 20.0

    print("Iniciando o teste de desempenho do algoritmo Açougue...")
    print(f"Testando grafos de {MIN_VERTICES} a {MAX_VERTICES} vértices.")

    for n_vertices in range(MIN_VERTICES, MAX_VERTICES + 1, PASSO):
        print(f"  - Gerando e testando grafo com {n_vertices} vértices...")
        
        n_arestas_extras = n_vertices 
        
        grafo_teste = gerar_grafo_reverso_com_ciclo(n_vertices, n_arestas_extras)
        
        # --- LÓGICA DE LOGGING ---
        # Formata a lista para ser bonita e legível
        pretty_list_str = pprint.pformat(grafo_teste, indent=4)
        # Cria a entrada de log no formato solicitado e a armazena
        log_entry = f"grafo_adj_{n_vertices} = {pretty_list_str}\n\n"
        log_entries.append(log_entry)
        
        # Chama a sua função de teste para obter o número de iterações
        iteracoes = acougue.acougue_teste(grafo_teste, MEDIA_ALVO)
        
        tamanhos_dos_grafos.append(n_vertices)
        iteracoes_de_convergencia.append(iteracoes)

    # --- ESCREVE O ARQUIVO DE LOG ---
    # Após o término de todos os testes, escreve o arquivo de uma só vez.
    try:
        with open("log.txt", "w") as log_file:
            # Escreve o cabeçalho com o número total de grafos logados
            log_file.write(f"Num_de_Logs: {len(log_entries)}\n\n")
            # Escreve todas as entradas de log armazenadas
            for entry in log_entries:
                log_file.write(entry)
        print("Arquivo 'log.txt' gerado com sucesso.")
    except IOError as e:
        print(f"Erro ao escrever o arquivo de log: {e}")


    print("Teste concluído. Gerando o gráfico...")

    # --- Plotando os resultados com Matplotlib ---
    x_data = np.array(tamanhos_dos_grafos)
    y_data = np.array(iteracoes_de_convergencia)

    try:
        coeficientes = np.polyfit(x_data, y_data, 2)
        polinomio_ajuste = np.poly1d(coeficientes)
        x_curva = np.linspace(x_data.min(), x_data.max(), 500)
        y_curva = polinomio_ajuste(x_curva)
    except np.linalg.LinAlgError:
        print("Não foi possível gerar a curva de ajuste.")
        x_curva, y_curva = [], []

    plt.figure(figsize=(10, 8))
    plt.scatter(x_data, y_data, color='blue', marker='o', label='Desempenho Real')
    if len(x_curva) > 0:
        plt.plot(x_curva, y_curva, '--', color='skyblue', label='Ajuste Polinomial (Tendência)')
    plt.title('Desempenho do Algoritmo Açougue', fontsize=16)
    plt.xlabel('Número de Vértices', fontsize=12)
    plt.ylabel('Número de Iterações para Convergência', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()