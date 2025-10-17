from graphviz import Digraph

# Matriz de custo (exemplo)
def visualize(matrix):
    # Criar grafo usando Graphviz
    dot = Digraph()

    for i in range(len(matrix)):
        dot.node(str(i))  # Adiciona os nós

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:  # Apenas para custos não-zero
                dot.edge(str(i), str(j), label=str(matrix[i][j]))

    dot.render("graph", format="png", cleanup=True)  # Salva e renderiza como PNG
    dot.view()  # Abre a imagem renderizada
