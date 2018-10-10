from priorityQueue import PriorityQueue as PQ

def degreeDiscount(G, k, p=.01):
    S = [] # seed set
    dd = PQ() # degree discount
    t = dict() # number of adjacent vertices that are in S
    d = dict() # degree of each vertex

    # initialize degree discount
    for u in G.nodes():
        d[u] = sum([G[u][v]['weight'] for v in G[u]]) # each edge adds degree 1
        # d[u] = len(G[u]) # each neighbor adds degree 1
        dd.add_task(u, -d[u]) # add degree of each node
        t[u] = 0

    # add vertices to S greedily
    for i in range(k):
        u, priority = dd.pop_item() # extract node with maximal degree discount
        S.append(u)
        for v in G[u]:
            if v not in S:
                t[v] += G[u][v]['weight'] # increase number of selected neighbors
                priority = d[v] - 2*t[v] - (d[v] - t[v])*t[v]*p # discount of degree
                dd.add_task(v, -priority)
    return S

def runIC (G, S, p = .01):
    ''' Runs independent cascade model.
    Input: G -- networkx graph object
    S -- initial set of vertices
    p -- propagation probability
    Output: T -- resulted influenced set of vertices (including S)
    '''
    from copy import deepcopy
    from random import random
    T = deepcopy(S) # copy already selected nodes

    i = 0
    while i < len(T):
        for v in G[T[i]]: # for neighbors of a selected node
            if v not in T: # if it wasn't selected yet
                w = G[T[i]][v]['weight'] # count the number of edges between two nodes
                if random() <= 1 - (1-p)**w: # if at least one of edges propagate influence
                    print (T[i], 'influences', v)
                    T.append(v)
        i += 1

    return T

def generalGreedy(G, k, p=.01):
    ''' Finds initial seed set S using general greedy heuristic
    Input: G -- networkx Graph object
    k -- number of initial nodes needed
    p -- propagation probability
    Output: S -- initial set of k nodes to propagate
    '''
    import time
    start = time.time()
    R = 20 # number of times to run Random Cascade
    S = [] # set of selected nodes
    # add node to S if achieves maximum propagation for current chosen + this node
    for i in range(k):
        s = PQ() # priority queue
        for v in G.nodes():
            if v not in S:
                s.add_task(v, 0) # initialize spread value
                for j in range(R): # run R times Random Cascade
                    [priority, count, task] = s.entry_finder[v]
                    s.add_task(v, priority - float(len(runIC(G, S + [v], p)))/R) # add normalized spread value
        task, priority = s.pop_item()
        S.append(task)
        print i, k, time.time() - start
    return S