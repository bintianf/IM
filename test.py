import networkx as nx
import random
import matplotlib.pyplot as plt
G = nx.Graph()
with open('random.txt') as f:
    n, m = f.readline().split()
    for line in f:
        u, v = map(int, line.split())
        # try:
        #     G[u][v]['weight'] += 1
        # except:
        G.add_edge(u,v, weight=1)
print (nx.info(G))

from ICmodel import degreeDiscount
import time
#calculate initial set
seed_size = 10
S = degreeDiscount(G, 10)
print ('Initial set of', seed_size, 'nodes chosen')
print (S)
start = time.time()

from ICmodel import generalGreedy
# calculate average activated set size
iterations = 200 # number of iterations
avg = 0
for i in range(iterations):
		T = generalGreedy(G, S)
		avg += float(len(T))/iterations
		# print i, 'iteration of IC'
print ('Avg. Targeted', int(round(avg)), 'nodes out of', len(G))
print (time.time() - start)
# plot the graph
# sp = nx.spring_layout(G)
# plt.axis('off')
# nx.draw_networkx(G, pos=sp, with_labels = False, node_size = 35)
# plt.show()