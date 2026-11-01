"""
Matching workers to jobs
========================

Assign workers to jobs at minimum cost with a weighted bipartite matching.
"""

# %%
# The workers are ``w0..w2`` and the jobs ``j0..j2``. Each edge weight is the cost of the pairing; the
# algorithm needs every worker-job pair to have a cost (a complete bipartite graph).

import jgrapht as jg

g = jg.Graph(weighted=True)
workers, jobs = ["w0", "w1", "w2"], ["j0", "j1", "j2"]
for v in workers + jobs:
    g.add_vertex(v)

costs = {("w0", "j0"): 4.0, ("w0", "j1"): 2.0, ("w0", "j2"): 7.0,
         ("w1", "j0"): 3.0, ("w1", "j1"): 8.0, ("w1", "j2"): 5.0,
         ("w2", "j0"): 9.0, ("w2", "j1"): 1.0, ("w2", "j2"): 6.0}
for (w, j), c in costs.items():
    g.add_edge(w, j, weight=c)

# %%
# A minimum weight perfect matching pairs every worker with a job.

m = jg.bipartite_minimum_weight_perfect_matching(g, workers, jobs)
print(m.weight)
print(sorted((g.edge_source(e), g.edge_target(e)) for e in m.edges))

# %%
# Without costs, the largest set of pairings is a maximum cardinality matching.

print(len(jg.maximum_matching(g).edges))  # at most three, one per worker
