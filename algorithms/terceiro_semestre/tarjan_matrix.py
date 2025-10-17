import time

def tarjan_rec(adj:list, raiz: int, disc:list, low:list, visited:list, pilha: list, naPilha:list, current_disc: int) -> None:
    pilha.append(raiz)
    naPilha[raiz] = True
    visited[raiz] = True
    disc[raiz] = current_disc[0]
    low[raiz] = disc[raiz]
    current_disc[0] += 1

    for i in range(len(adj)):
        if adj[raiz][i] == 1:
            if naPilha[i] == True:        #caso I: aresta de retorno, aresta não está na pilha
                low[raiz] = min(low[raiz], disc[i])
        
            elif visited[i] == False:       #caso II: aresta descendente, aresta não está na pilha
                tarjan_rec(adj, i, disc, low, visited, pilha, naPilha, current_disc)
                low[raiz] = min(low[raiz], low[i])
    
    #Se ao retornar o low e o disc forem iguais significa que a raiz é "cabeça" da SSC
    if low[raiz] == disc[raiz]:
        while pilha[-1] != raiz:
            retirado = pilha.pop()
            low[retirado] = low[raiz]
            naPilha[retirado] = False
            

        naPilha[pilha.pop()] = False

def tarjan(adj):
    pilha = []
    naPilha = [False] * len(adj)
    current_disc = [0]
    visited = [False] * len(adj)
    disc = [-1] * len(adj)
    low = [-1] * len(adj)

    for i in range(len(adj)):
        if visited[i] == False:
            tarjan_rec(adj, i, disc, low, visited, pilha, naPilha, current_disc)

    return low


# Exemplo de como usar:
# grafo_adj = [
#     [ 0, 1, 0, 0, 0 ],
#     [ 1, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 1, 0 ],
#     [ 0, 0, 0, 0, 1 ],
#     [ 0, 0, 1, 0, 0 ]  
# ]

# componentes = tarjan(grafo_adj)
# print(componentes)

def main(listaAdj):
    # grafo_lista_result = listaAdj.copy()
    time_ini = time.time()
    tarjan(listaAdj)
    time_fim = time.time()
    
    return time_fim - time_ini