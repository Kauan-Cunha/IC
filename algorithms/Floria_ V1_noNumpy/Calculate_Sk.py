from sys import argv
from math import inf

min = 0
def calc_sk():
    size = int(argv[1])


    c =  [
        [inf, 1.5, 4, 1.5, 4],
        [2.5, inf, 3, 6, 3],
        [1.5, 2, inf, 5, 5],
        [7, 7, 3, inf, 3],
        [4, 2, 2, 1, inf]
    ]

    rec_calc_sk(c, 1, size, 0)
    print(min)


def rec_calc_sk(ini, c, count, k, current_sum):
    #we can mesure the layer through the k. Layer will be 
    global min
    if count == k:
        print(current_sum)
        if current_sum < min:
            min = current_sum
            return
    else:
        for i in enumerate(c[count]):
            if(i != )
            rec_calc_sk(c, c[count][i]+1, k, current_sum+i)

if __name__ == '__main__':
    calc_sk()
