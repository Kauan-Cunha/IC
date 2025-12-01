import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import copy
import Grafo.Grafo as g

def dfs_corte_rec(grafo: g.Grafo, u: int, visited: list, naPilha: list, grafo_guia: g.Grafo) -> None:
    """
    Função recursiva do algoritmo de Tarjan para lista de adjacências diretas.
    """
    naPilha[u] = True
    visited[u] = True

    arestas = list(grafo_guia.obter_chegada(u).items())
    for v, peso in arestas:

        if not visited[v]:
            dfs_corte_rec(grafo, v, visited, naPilha, grafo_guia)

        elif naPilha[v]:
            id_novo_no = grafo.num_vertices
            grafo.adicionar_vertice()
            
            peso_metade = peso / 2

            grafo.remover_aresta(u, v) # Remove v->u
            grafo.adicionar_aresta(v, id_novo_no, peso_metade)
            grafo.adicionar_aresta(id_novo_no, u, peso_metade)

    naPilha[u] = False

def dfs_corte(grafo: g.Grafo, grafo_critico: g.Grafo) -> g.Grafo:
    """
    Função principal de Tarjan que opera em um grafo de lista de adjacências diretas.
    """
    grafo_copia = copy.deepcopy(grafo)

    naPilha = [False] * grafo.num_vertices
    visited = [False] * grafo.num_vertices

    for i in range(grafo_critico.num_vertices):
        if not visited[i]:
            dfs_corte_rec(grafo_copia, i, visited, naPilha, grafo_critico)

    return grafo_copia

def main():
    # Criar grafo principal com 4 vértices
    grafo = g.Grafo(4)

    # Arestas do grafo original
    grafo.adicionar_aresta(3, 0, 1)   # 3 → 0
    grafo.adicionar_aresta(0, 1, 100) # 0 → 1
    grafo.adicionar_aresta(2, 1, 5)   # 2 → 1
    grafo.adicionar_aresta(1, 2, 50)  # 1 → 2
    grafo.adicionar_aresta(1, 3, 1)   # 1 → 3

    print("Adjacência do grafo original:")
    print(grafo.adjacencia)

    print("\nRodando Tarjan...")
    resultado = dfs_corte(grafo, grafo)  
    print("\nResultado de Tarjan:")
    print(resultado)

if __name__ == "__main__":
    main()