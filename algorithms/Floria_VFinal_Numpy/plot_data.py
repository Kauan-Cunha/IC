import numpy as np
import matplotlib.pyplot as plt
import flor                 #meu algoritmo de floria 



#Parametros:
qtd_nodes = 150
qtd_media = 100



n_nodes = [x for x in range(1, qtd_nodes+1, 20)] #[1,2,4,8,16, ...]

x = [] 

y_run_time_karp = []#Num_Iterações
y_run_time_flor = [] #Running Time

for n in n_nodes:
    sum_time_karp=0
    sum_time_flor=0
    for _ in range(qtd_media):
        print(n)
        result = flor.main(n)
        sum_time_flor += result[0]
        sum_time_karp += result[1]
    x.append(n)
    y_run_time_karp.append(sum_time_karp/qtd_media)
    y_run_time_flor.append(sum_time_flor/qtd_media)


coeficientes = np.polyfit(x, y_run_time_flor, deg=2)
polinomio = np.poly1d(coeficientes)

coeficientes_karp = np.polyfit(x, y_run_time_karp, deg= 2)
polinomio_karp = np.poly1d(coeficientes_karp)

x_novo = np.linspace(1, qtd_nodes, qtd_nodes//20)
y_ajustado = polinomio(x_novo)
y_ajustado_karp = polinomio_karp(x_novo)

# plt.plot(x, y, marker="o", color = "r")
# plt.plot(x, y_run_time_karp, marker="x", color="g", label="Nº Iterações")
plt.title("Tempo de execução Karp versus Floría-Gritths")
plt.scatter(x, y_run_time_flor, marker ="o", color ="blue", label="Floría-Griffiths")
plt.scatter(x,y_run_time_karp, marker = "s", color = "red", label = "Karp")
plt.plot(x_novo, y_ajustado, color="g")
plt.plot(x_novo, y_ajustado_karp, color = "brown")
plt.ylabel("Média de tempo execução (s)")
plt.xlabel("Número de vértices")
plt.legend()
plt.plot()
plt.show()