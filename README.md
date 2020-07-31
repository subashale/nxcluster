# nxcluster
Parameterized clusters design (components) with removing feature of connector nodes' edges.

components takes either integer with number of nodes to create uniformed clusters (having same number of nodes in each cluster) or
takes list to create diverse cluster sizes

### run
<u>1. Uniform clusters<u>
init_G = nc(cluster=3, node=15, degree=3, n_bridge=2)
init_G.create()
init_G.draw_graph()

<u>2. Diverse clusters</u>
init_G = nc(cluster=[10, 15, 20], degree=3, n_bridge=2)
init_G.create()
init_G.draw_graph()

<u>3. Remove edges </u>
init_G.remove_edge(n_remove=1)
init_G.draw_graph()
