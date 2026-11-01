"""
PageRank and other scores
=========================

Rank the vertices of a small web graph.
"""

# %%
# Four pages link to each other; page ``0`` is linked to by all the others.

import jgrapht as jg

g = jg.Graph(directed=True)
for v in range(4):
    g.add_vertex(v)
for u, v in [(1, 0), (2, 0), (3, 0), (0, 1), (2, 1)]:
    g.add_edge(u, v)

# %%
# PageRank gives a dictionary from vertex to score; the scores sum to one.

pr = jg.pagerank(g)
for v, score in sorted(pr.items(), key=lambda item: -item[1]):
    print(v, round(score, 3))

# %%
# Other scores work the same way.

print(jg.closeness_centrality(g))
print(jg.betweenness_centrality(g))
