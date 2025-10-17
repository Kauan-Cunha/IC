import matrices 
import numpy as np
import matplotlib.pyplot as plt
import tarjan_lista
import tarjan_matrix
import time
from matrices import matriz_custo_para_lista_adj

qtd_nodes = 500
qtd_media = 20

# Define a lista de número de nós para testar, com passos mais regulares
n_nodes = [x for x in range(2, qtd_nodes + 1, 3)]

x = [] 
y_run_time_lista = []
y_run_time_matriz = []

for n in n_nodes:
    sum_time_lista = 0
    sum_time_matrix = 0

    for _ in range(qtd_media):
        # Gerando uma matriz de adjacência para o grafo esparso
        adj = matrices.random_sparse_matrix(n)
        
        # Converte a matriz de adjacência (0s e 1s) para lista de adjacência
        # A função matriz_custo_para_lista_adj está com a lógica invertida para matriz de 0s e 1s
        # Vamos usar uma lógica mais simples para a conversão
        
        # Converte a matriz adjacência (0 e 1s) para a lista de adjacência
        lista_adj = matriz_custo_para_lista_adj(adj)

        # Medindo o tempo para o algoritmo de Tarjan com lista de adjacências
        start_time = time.time()
        tarjan_lista.main(lista_adj)
        end_time = time.time()
        sum_time_lista += (end_time - start_time)

        # Medindo o tempo para o algoritmo de Tarjan com matriz
        start_time = time.time()
        tarjan_matrix.main(adj)
        end_time = time.time()
        sum_time_matrix += (end_time - start_time)

    x.append(n)
    y_run_time_matriz.append(sum_time_matrix / qtd_media)
    y_run_time_lista.append(sum_time_lista / qtd_media)

# Ajuste do polinômio de segundo grau para os dados
coeficientes_lista = np.polyfit(x, y_run_time_lista, deg=2)
polinomio_lista = np.poly1d(coeficientes_lista)

coeficientes_matriz = np.polyfit(x, y_run_time_matriz, deg=2)
polinomio_matriz = np.poly1d(coeficientes_matriz)

x_novo = np.linspace(min(x), max(x), 100)
y_ajustado_lista = polinomio_lista(x_novo)
y_ajustado_matriz = polinomio_matriz(x_novo)

# ---
# Plotagem dos resultados

plt.figure(figsize=(10, 6))
plt.title("Tempo de Execução: Tarjan em Lista vs. Matricial")
plt.xlabel("Número de Vértices")
plt.ylabel("Tempo de Execução Médio (s)")

# Pontos de dados
plt.scatter(x, y_run_time_matriz, marker="o", color="blue", label="Tarjan Matricial")
plt.scatter(x, y_run_time_lista, marker="s", color="red", label="Tarjan em Lista")

# Linhas de ajuste polinomial
plt.plot(x_novo, y_ajustado_matriz, color="lightblue", linestyle="--", label="Ajuste Matricial")
plt.plot(x_novo, y_ajustado_lista, color="lightcoral", linestyle="--", label="Ajuste em Lista")

plt.legend()
plt.grid(True)
plt.show()