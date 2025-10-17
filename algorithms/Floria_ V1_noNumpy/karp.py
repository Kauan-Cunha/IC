''' Class to represent an edge of the directed weighted graph'''
class edge:
    def __init__(self, u, wt):
        self.From = u
        self.wt = wt
       
num_of_vertices = 5
''' To store the edges '''
edges = [[] for i in range(num_of_vertices)]

'''Helper Function to add an edge in the graph '''
def AddEdge(v1, v2, wt):
   
    ''' Since the graph is directed, we have to add only the forward edge'''
    edges[v2].append(edge(v1, wt))

''' Function for Karp's Minimum average weight cycle algorithm '''
def KarpsAlgo(d):
   
    ''' An array to store average values'''
    avg = [-1 for i in range(num_of_vertices)]
 
    ''' Calculate the average of cycles using the d table '''
    for i in range(num_of_vertices):
        if d[num_of_vertices][i] != -1:
         
            '''calculating average using Karps Algorithm '''
            for j in range(num_of_vertices):
                if (d[j][i] != -1):
                    avg[i] = max(avg[i],(d[num_of_vertices][i]-d[j][i])/(num_of_vertices-j))
       
       
    ''' Finding the minimum average value '''
    ans = 100000000000;
    for i in range(num_of_vertices):
        if (avg[i] > -1 and avg[i] < ans):
            ans = avg[i]
           
    return ans


'''Driver Function'''
def main():
   
    ''' Adding Edges to the graph'''
    
    AddEdge(0, 1, 32)
    AddEdge(0, 2, 41)
    AddEdge(0, 3, 59)
    AddEdge(0, 4, 3)

    AddEdge(1, 0, 59)
    AddEdge(1, 2, 86)
    AddEdge(1, 3, 4)
    AddEdge(1, 4, 79)

    AddEdge(2, 0, 66)
    AddEdge(2, 1, 77)
    AddEdge(2, 3, 42)
    AddEdge(2, 4, 58)

    AddEdge(3, 0, 59)
    AddEdge(3, 1, 58)
    AddEdge(3, 2, 80)
    AddEdge(3, 4, 30)

    AddEdge(4, 0, 80)
    AddEdge(4, 1, 62)
    AddEdge(4, 2, 80)
    AddEdge(4, 3, 16)

        

    d = [[None] * num_of_vertices for i in range(num_of_vertices + 1)]
    for i in range(num_of_vertices + 1):
        for j in range(num_of_vertices):
            d[i][j] = -1
 
    d[0][0] = 0
 
    ''' calculating the shortest path and updating the table d '''
    for i in range(1, num_of_vertices+1):
        for j in range(num_of_vertices):
            for k in range(len(edges[j])):
               
                if d[i-1][edges[j][k].From] != -1:
                    cwt = d[i-1][edges[j][k].From] + edges[j][k].wt;
                   
                    if d[i][j] == -1:
                        d[i][j] = cwt
                    else:
                       d[i][j] = min(d[i][j], cwt)
     
   
    ''' Calling the KarpsAlgo function with d table and printing the results'''
    ans = KarpsAlgo(d)
    print(ans)
   
'''Executing Main'''
main()