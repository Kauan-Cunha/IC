import networkx as nx
import matplotlib.pyplot as plt
import flor_adj_dual as f
import grafoCriticoAlt as g
from typing import overload
import desenhar_grafo as d

#ESSE ARQUIVO E ESPECÍFICO PARA ARMAZENAR A DEFINIÇÃO DA ESTRUTURA DE DAODS SOB A QUAL CHAMAMOS DE GRAFO
#LEMBRE-SE. POR CONVENIENCIA AS ADJACENCIAS REPRESENTAM OS NÓS QUE CHEGAM A TERMINADA ENTRADA DO VETOR.


class Grafo:
    def __init__(self, lista_adjacencia = []):
        """
        lista_adjacencia := lista de adjacencia.
        maior := valor que armazena o maior ou menor entrada do grafo.
        """
        self.lista_adjacencia = lista_adjacencia
        if len(lista_adjacencia) > 0:
            pesos = (peso for linha in lista_adjacencia for (_, peso) in linha)
            self.maior = max(pesos)

            pesos_min = (peso for linha in lista_adjacencia for (_, peso) in linha)
            self.menor = min(pesos_min)
            
            self.cardinalidade = len(lista_adjacencia)
        else:
            self.maior = None
            self.menor = None
        

    def autovetor_autovalor(self, tipo = 'maximal'):
        """
            A ideia aqui é simplemeste aplicar floria e retornar o autovalor e autovetor
        """

        vetor, valor, _, _ = f.floria(self.lista_adjacencia, -self.menor, tipo)

        return vetor, valor
    
    def grafo_critico(self, tipo = 'maximal') -> Grafo: # type: ignore
        """
            Aplica floria e retorna o grafo_critico
        """

        if tipo == 'maximal':
            vetor, valor, _, custo_invertido = f.floria(self.lista_adjacencia, -self.menor, tipo)
            adj = g.grafoCritico_adj(custo_invertido, valor, vetor, is_max_or_min= 'max')
            return Grafo(adj)
        
        elif tipo == 'minimal':
            vetor, valor, _, _ = f.floria(self.lista_adjacencia, self.maior, tipo)
            adj = g.grafoCritico_adj(self.lista_adjacencia, valor, vetor, is_max_or_min='min')
            return Grafo(adj)

    @overload
    def adicionar(self, i: int, j:int, peso:int):
        if self.cardinalidade <= j:                                 #adicionamos arestas se precisar.
            for i in range(self.cardinalidade - j + 1):
                self.lista_adjacencia.append([])        
        else:
            self.lista_adjacencia[j].append((i, peso)) 

    @overload
    def adicionar(self, j:int, chegadas:list):
        if self.cardinalidade <= j:                                 #adicionamos arestas se precisar.
            for i in range(self.cardinalidade - j + 1):
                self.lista_adjacencia.append([])   
        else:
            for i in chegadas:
                self.lista_adjacencia[j].append(i)        

    def desenhar(self):
        d.draw_weighted_graph_adj(self.lista_adjacencia)