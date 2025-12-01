import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import copy
import Grafo.Grafo as g

def busca_binaria(pilha_maximos: list, altura: int) -> tuple:
    """
    Encontra o primeiro elemento na pilha cujo peso é MAIOR ou IGUAL à altura fornecida.
    Assume que pilha_maximos está ordenada pelo peso de forma crescente.
    """
    esquerda, direita = 0, len(pilha_maximos) - 1
    resultado = None

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        aresta, peso, altura_atual = pilha_maximos[meio]

        if altura_atual >= altura:
            resultado = (aresta, peso) 
            direita = meio - 1
        else:
            esquerda = meio + 1

    if resultado is None:
        return None
    
    return resultado[0][0], resultado[0][1], resultado[1]

def dfs_corte_rec(grafo_alvo: g.Grafo, u: int, visited: list, naPilha: list, pilha_maximos: list, grafo_guia: g.Grafo, altura: int = 0) -> None:
    """
    Função recursiva.
    grafo_alvo: O grafo completo que será MODIFICADO.
    grafo_guia: O grafo de arestas críticas usado para NAVEGAR.
    """
    naPilha[u] = altura
    visited[u] = True

    # Navega usando as arestas do GRAFO GUIA (Crítico)
    # Convertemos para lista para evitar erros se o dicionário mudar durante a execução
    arestas_criticas = list(grafo_guia.obter_chegada(u).items()) if grafo_guia.obter_chegada(u) else []

    for v, peso in arestas_criticas:
        itens_removidos = []

        # Mantém a pilha de máximos consistente com o caminho atual no guia
        while len(pilha_maximos) > 0 and peso >= pilha_maximos[-1][1]:         
            itens_removidos.append(pilha_maximos.pop())

        pilha_maximos.append(((u,v), peso, altura + 1)) 

        if not visited[v]:
            dfs_corte_rec(grafo_alvo, v, visited, naPilha, pilha_maximos, grafo_guia, altura + 1)
            
            # Limpa pilha no retorno da recursão
            if len(pilha_maximos) > 0 and pilha_maximos[-1][0] == (u,v):
                pilha_maximos.pop()

        elif naPilha[v] != -1:
            # Ciclo detectado! Realiza o corte inteligente no grafo_alvo
            
            # Encontra a melhor aresta para cortar usando busca binária na pilha
            res_busca = busca_binaria(pilha_maximos, naPilha[v])
            
            if res_busca:
                x, y, peso_max = res_busca
                
                # Garante que a aresta existe no grafo ALVO antes de cortar
                if grafo_alvo.obter_peso(y, x) is not None:
                    id_novo_no = grafo_alvo.num_vertices
                    grafo_alvo.adicionar_vertice()
                    
                    peso_metade = peso_max / 2
                    
                    # Aplica o corte no alvo
                    grafo_alvo.remover_aresta(x, y)
                    grafo_alvo.adicionar_aresta(y, id_novo_no, peso_metade)
                    grafo_alvo.adicionar_aresta(id_novo_no, x, peso_metade)

        # Backtracking da pilha de máximos
        if pilha_maximos and pilha_maximos[-1][0] == (u,v):
                pilha_maximos.pop()
            
        while itens_removidos:
            pilha_maximos.append(itens_removidos.pop())

    naPilha[u] = -1

def dfs_corte(grafo_completo: g.Grafo, grafo_critico: g.Grafo) -> g.Grafo:
    """
    Recebe o grafo completo (alvo) e o crítico (guia).
    Retorna uma cópia do completo com os cortes aplicados.
    """
    pilha_maximos = []
    grafo_modificado = copy.deepcopy(grafo_completo)
    
    naPilha = [-1] * grafo_modificado.num_vertices
    visited = [False] * grafo_modificado.num_vertices

    # Itera sobre vértices que existem no grafo crítico
    for i in range(min(grafo_critico.num_vertices, grafo_modificado.num_vertices)):
        # Só inicia a busca se houver conexões críticas
        if not visited[i] and grafo_critico.obter_chegada(i):
            dfs_corte_rec(grafo_modificado, i, visited, naPilha, pilha_maximos, grafo_critico)

    return grafo_modificado
def main():
    # Criar grafo principal com 4 vértices
    grafo = g.Grafo(4)

    # Arestas do grafo original
    grafo.adicionar_aresta(3, 0, 1)   # 3 → 0
    grafo.adicionar_aresta(0, 1, 100) # 0 → 1
    grafo.adicionar_aresta(2, 1, 1)   # 2 → 1
    grafo.adicionar_aresta(1, 2, 50)  # 1 → 2
    grafo.adicionar_aresta(1, 3, 1)   # 1 → 3

    print("Adjacência do grafo original:")
    print(grafo.adjacencia)

    print("\nRodando Tarjan...")
    resultado = dfs_corte(grafo)  
    print("\nResultado de Tarjan:")
    print(resultado)

if __name__ == "__main__":
    main()