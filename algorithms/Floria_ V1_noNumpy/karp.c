#include<bits/stdc++.h>
#include<vector>
using namespace std;
 
const int num_of_vertices = 5;
 
/* Struct variable to represent edge */
typedef struct{
    int from, wt;
}edge;
 
/* a vector of type edge to store the edges of the given graph*/
vector <edge> edges[num_of_vertices];
 
/*Helper Function to add an edge in the graph */
void AddEdge(int v1 ,int v2 ,int wt)
{
    /* Since the graph is directed, we have to add only the forward edge*/
    edges[v2].push_back({v1, wt});
}

/* Function for Karp's Minimum average weight cycle algorithm */
double KarpsAlgo(int d[num_of_vertices+1][num_of_vertices])
{
    /* An array to store average values */
    vector<double> avg(num_of_vertices, -1);
 
    /* Calculate the average of cycles using the d table */
    for (int i=0; i<num_of_vertices; i++)
    {
        if (d[num_of_vertices][i] != -1)
        {  
            /*calculating average using Karps Algorithm */
            for (int j=0; j<num_of_vertices; j++)
                if (d[j][i] != -1)
                    avg[i] = max(avg[i],
                ((double)d[num_of_vertices][i]-d[j][i])/(num_of_vertices-j));
        }
    }
 
    /* Finding the minimum average value */
    double ans = 100000000000;
    for (int i=0; i<num_of_vertices; i++){
        if (avg[i] > -1 && avg[i] < ans)
            ans = avg[i];
    }
    return ans;
}
 
/* Driver Function */
int main()
{
    /* Adding Edges to the graph */
    AddEdge(0, 1, 2);
    AddEdge(1, 2, 5);
    AddEdge(3, 1, 1);
    AddEdge(2, 3, 1);
    AddEdge(2, 0, 7);
    AddEdge(4, 0, 4);
    AddEdge(4, 2, 3);
   
    /* initializing the d table to store the shortest path distance */
    int d[num_of_vertices+1][num_of_vertices];
   
    /* set all values of d as -1 */
    for (int i=0; i<=num_of_vertices; i++)
        for (int j=0; j<num_of_vertices; j++)
            d[i][j] = -1;
 
    d[0][0] = 0;
 
    /* calculating the shortest path and updating the table d */
    for (int i=1; i<=num_of_vertices; i++)
    {
        for (int j=0; j<num_of_vertices; j++)
        {
            for (int tmp=0; tmp<edges[j].size(); tmp++)
            {
                if (d[i-1][edges[j][tmp].from] != -1)
                {
                    int curr_wt = d[i-1][edges[j][tmp].from] +
                                  edges[j][tmp].wt;
                    if (d[i][j] == -1)
                        d[i][j] = curr_wt;
                    else
                       d[i][j] = min(d[i][j], curr_wt);
                }
            }
        }
    }
   
    /* Calling the KarpsAlgo function with d table and printing the results*/
    double ans = KarpsAlgo(d);
    cout <<ans;
   
    return 0;
}