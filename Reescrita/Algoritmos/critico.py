import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import Grafo.Grafo as g

def grafoCritico(grafo_original: g.Grafo, m: float, func: list, is_max_or_min: str = 'min') -> g.Grafo:
    """
    Gera um novo objeto Grafo contendo apenas as arestas críticas.
    Uma aresta (u -> v) é crítica se: func[v] == func[u] + peso - m
    """

    grafo_critico = g.Grafo(grafo_original.num_vertices)
    
    # Itera sobre todos os vértices (u) do grafo original
    for u in range(grafo_original.num_vertices):
        
        adjacencias = grafo_original.obter_chegada(u)
        
        iterador_arestas = adjacencias.items() if isinstance(adjacencias, dict) else adjacencias
        
        for v, peso in iterador_arestas:
            valor_calculado = func[u] + peso - m
            if np.isclose(func[v], valor_calculado):
                peso_final = peso
                grafo_critico.adicionar_aresta(v, u, peso_final)

    return grafo_critico