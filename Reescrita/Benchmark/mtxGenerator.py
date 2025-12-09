import random
import sys
import os

# Adiciona o diretório pai ao path para encontrar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Grafo.Grafo as g


#-----------------------------
# algoritmos de criação de grafos "aleatórios".
#-----------------------------

def gerar_grafo_completo(num_vertices: int, peso_min: int = 1000, peso_max: int = 1005) -> g.Grafo:
    """
    Gera um grafo direcionado completo (densidade 100%).
    Isso significa que para todo par (i, j), existe uma aresta i -> j.
    """
    grafo = g.Grafo(num_vertices)
    
    # Adicionar arestas i -> j para todo i, j
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j: 
                peso = random.randint(peso_min, peso_max)
                grafo.adicionar_aresta(i, j, peso)
    
    return grafo