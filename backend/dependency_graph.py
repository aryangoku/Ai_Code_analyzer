import os
import networkx as nx

def build_graph(repo_path):

    graph = nx.DiGraph()

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".py"):

                graph.add_node(file)

    return list(graph.nodes)