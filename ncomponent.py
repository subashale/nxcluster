import networkx as nx
import numpy as np
import random

class NComponent:
    """ Create parameterized cluster based on random graphs

    Keyword arguments:
    ------------------
    @cluster : number of clusters or list of nodes in clusters
    @node : require nodes to create clusters, only if @cluster is int
    @degree : edges between each nodes in the clusters
    @n_bridge: connector nodes to other clusters

    Functions:
    ---------
    create -- generate graph based on arguments
                if @cluster is int then it takes total number of cluster
                then @node is require to create nodes in each clusters
                this will creates uniformed clusters

                if @cluster is list it takes nodes and number of cluster it self
                here we can manage cluster sizes

    remove_edge -- removing connecting nodes to each clusters
    draw_graph -- to draw graph using nx.draw method

    """
    def __init__(self, cluster=2, node=20, degree=4, n_bridge=2):
        self.cluster = cluster
        self.node = node
        self.degree = degree
        self.n_bridge = n_bridge

    def create(self):
        # create graph for each cluster and store in dict
        self.graph_holder = {}

        # if int then select node else use list
        if type(self.cluster) is int:
            for i in range(self.cluster):
                self.graph_holder[i] = nx.barabasi_albert_graph(n=self.node, m=self.degree)
        elif type(self.cluster) is list:
            for i, cluster in enumerate(self.cluster):
                self.graph_holder[i] = nx.barabasi_albert_graph(n=cluster, m=self.degree)
        else:
            print("Please provide int or list to create cluster, list must contain discrete value")

        # update second cluster nodes value to starting from numNodes-1
        # to create separate cluster in one graph and joint some edges later
        all_node_oder_rename = []
        for key, graph in self.graph_holder.items():
            for i in graph.edges:
                if key == 0:
                    rename_edge = np.matrix(i)
                    all_node_oder_rename.append(tuple(rename_edge.tolist()[0]))
                else:
                    rename_edge = np.matrix(i) + (len(graph.nodes) * key)
                    #                     print(len(graph.nodes)*key)
                    all_node_oder_rename.append(tuple(rename_edge.tolist()[0]))
        #         print(all_node_oder_rename)

        # Random nodes mapping
        # getting random nodes from each clusters
        self.bride_edges_node = []
        for n, graph in self.graph_holder.items():
            if n != 0:
                initial = n * len(graph.nodes)
                end = len(graph.nodes) * (n + 1)
            else:
                initial = 0
                end = len(graph.nodes)
            #         print(initial, end-1)
            random_node = random.sample(range(initial, end - 1), self.n_bridge)
            self.bride_edges_node.append(random_node)
        #         print(self.bride_edges_node)

        # two cluster selection and creating edges
        self.bridge_edges_form = []
        for i in range(len(self.bride_edges_node) - 1):
            check = i + 1
            if i == 0:
                two_cluster = self.bride_edges_node[:check + 1]
                self.bridge_edges_form += [(a_node, b_node) for a_node, b_node in zip(*[node for node in two_cluster])]
            else:
                two_cluster = self.bride_edges_node[check - 1:][:2]
                self.bridge_edges_form += [(a_node, b_node) for a_node, b_node in zip(*[node for node in two_cluster])]
        #         print(self.bridge_edges_form)

        # combining all edges n_cluster's graphs
        all_node_oder_rename += self.bridge_edges_form

        #     print(all_node_oder_rename[-5:])
        # create new graph with processed edge list
        self.graph = nx.Graph()
        self.graph.add_edges_from(all_node_oder_rename)

    #         return self.graph

    # n_remove = reduce edge from each brige nodes equally
    # separate = create disjoint graph
    def remove_edge(self, n_remove=0):

        if n_remove > len(self.bride_edges_node[0]):
            print("doesn't exists edges: ", n_remove)
            return
        edges_list = [list(i) for i in self.graph.edges]
        linker_edge_list = [list(i) for i in self.bridge_edges_form]
        #     print(edges_list)
        #     print(linker_edge_list)

        # remove all edges from linker_edge
        for i in linker_edge_list:
            edges_list.remove(i)

        # remove nodes from each cluster
        self.previous_bridge_edges_node = self.bride_edges_node
        self.bride_edges_node = []
        for i, nodes in enumerate(self.previous_bridge_edges_node):
            self.bride_edges_node.append([x for x in nodes if x not in nodes[:n_remove]])

        # two cluster selection and creating edges
        self.bridge_edges_form = []
        for i in range(len(self.bride_edges_node) - 1):
            check = i + 1
            if i == 0:
                two_cluster = self.bride_edges_node[:check + 1]
                self.bridge_edges_form += [(a_node, b_node) for a_node, b_node in zip(*[node for node in two_cluster])]
            else:
                two_cluster = self.bride_edges_node[check - 1:][:2]
                self.bridge_edges_form += [(a_node, b_node) for a_node, b_node in zip(*[node for node in two_cluster])]

        #         print(self.bride_edges_node)

        # add other edges
        edges_list += self.bridge_edges_form

        # edge tuples and graph
        edge = [tuple(i) for i in edges_list]
        #         print(edge)
        self.graph = nx.Graph()
        self.graph.add_edges_from(edge)

    #         return self.graph
    def draw_graph(self):
        return nx.draw(self.graph)
