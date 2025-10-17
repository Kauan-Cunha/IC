import numpy as np
import flor
import matplotlib.pyplot as plt
from time import time
from datetime import date
import csv
import terceiro_semestre.matrices as matrices

def line_count(fname):
    with open(fname) as f:
        i = 0
        for line in f:
            i += 1
    return i


def plot_time(func, qtd_nodes = 150, qtd_media = 10, skip = 10):
    """
    It plots the execution mean time graph of a given function
    """

    x = [i for i in range(0, qtd_nodes+1, skip)]
    y = []

    #Creating y exit
    for i in x:
        sum_y = 0
        adjacencia = matrices.fully_connected_matrices(20)
        custo, max = matrices.randomised_weigh_matrix(adjacencia, 100)
        for _ in range(qtd_media):
            ini_time = time()
            result = func(custo, max)[1]
            end_time = time()
            sum_y += end_time - ini_time
        y.append(sum_y/qtd_media)

    #write in CSV file
    label = input("Insert a label to plot: ")
    with open("plot_data.csv", 'a', newline="") as f:
        csv_writer  = csv.writer(f)
        csv_writer.writerow([date.today(), label, x, y])
    
    n_linhas = line_count("plot_data.csv")
    print(f"Added plot to line {n_linhas}the data set.")

    return n_linhas


def assemple_graph(id: int, labeling, colour = "r", mark= "o", fit_graph = False):
    """
    It assembles all the plots you want.
    The process is: plot, assemble, show.
    """

    with open("plot_data.csv", "r") as f:
        csvreader = csv.reader(f)
        for i, line in enumerate(csvreader):
            if i == id:
                print(line)
                x = eval(line[2])
                y = eval(line[3])
                plt.scatter(x, y, marker= mark, color = colour, label = labeling)
                break


def show_graph():
    plt.show()

def main():
    data_line = plot_time(flor.floria, 2000, 100, 20)
    print(data_line)
    assemple_graph(data_line-1, "Testando")
    show_graph()


if __name__ == "__main__":
    main()