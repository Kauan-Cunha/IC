# gerar_grafos_com_ciclo.py
import os
import random

# --- PARÂMETROS DA GERAÇÃO ---

# Diretório para salvar os grafos de teste
DIRETORIO_GRAFOS = "grafos_de_teste"

# Define os tamanhos dos grafos a serem testados
TAMANHOS_TESTE = range(5, 101, 5)  # [5, 10, 15, ..., 100]

# Quantos grafos gerar para cada tamanho
GRAFOS_POR_TAMANHO = 10

# Pesos para o ciclo principal (garantido)
PESO_ALTO_MIN = 200
PESO_ALTO_MAX = 300

# Pesos para as arestas aleatórias "distraidoras"
PESO_BAIXO_MAX = 50

# Densidade das arestas distraidoras (0.2 = 20% de chance de existir uma aresta extra)
DENSIDADE_ARESTAS_EXTRA = 0.2

def gerar_grafos_garantindo_ciclo():
    """
    Gera e salva grafos de teste, garantindo que cada um tenha um ciclo
    Hamiltoniano com pesos altos, projetado para ser o ciclo de média máxima.
    """
    if not os.path.exists(DIRETORIO_GRAFOS):
        os.makedirs(DIRETORIO_GRAFOS)
        print(f"Diretório '{DIRETORIO_GRAFOS}' criado.")

    print("Iniciando a geração de grafos com ciclo de média máxima garantido...")
    for n in TAMANHOS_TESTE:
        for i in range(GRAFOS_POR_TAMANHO):
            # O formato é uma lista de adjacência REVERSA
            # adj_reversa[filho] = [(pai, peso), ...]
            adj_reversa = [[] for _ in range(n)]
            arestas_existentes = set()

            # 1. Criar o ciclo Hamiltoniano com pesos altos
            # O ciclo será: 0 -> 1 -> 2 -> ... -> (n-1) -> 0
            for pai in range(n):
                filho = (pai + 1) % n
                peso = random.randint(PESO_ALTO_MIN, PESO_ALTO_MAX)
                adj_reversa[filho].append((pai, peso))
                arestas_existentes.add((pai, filho))

            # 2. Adicionar arestas "distraidoras" com pesos baixos
            for pai in range(n):
                for filho in range(n):
                    # Não sobrescrever uma aresta do ciclo principal
                    if (pai, filho) in arestas_existentes:
                        continue
                    
                    # Adicionar aresta extra com base na densidade
                    if random.random() < DENSIDADE_ARESTAS_EXTRA:
                        peso = random.randint(1, PESO_BAIXO_MAX)
                        adj_reversa[filho].append((pai, peso))
            
            # 3. Salvar o grafo em arquivo
            nome_arquivo = os.path.join(DIRETORIO_GRAFOS, f"grafo_n{n}_id{i}.txt")
            with open(nome_arquivo, 'w') as f:
                for filho, arestas in enumerate(adj_reversa):
                    for pai, peso in arestas:
                        f.write(f"{filho} {pai} {peso}\n")
        print(f"  Grafos de tamanho n={n} gerados.")
        
    print("Geração de grafos concluída.")

if __name__ == '__main__':
    gerar_grafos_garantindo_ciclo()