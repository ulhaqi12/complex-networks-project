import csv
import pandas as pd
import networkx as nx
import logging


logging.basicConfig(level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def create_network():
    """
    This function reads data from data folder and construct a network.

    """
    with open('data/actors.csv', 'r') as nodecsv:
        nodereader = csv.reader(nodecsv)
        nodes = [n for n in nodereader][1:]

    node_names = [n[0] for n in nodes]

    with open('data/actor_edges.csv', 'r') as edgecsv:
        edgereader = csv.reader(edgecsv)
        edges = [tuple(e) for e in edgereader][1:]

    G = nx.Graph()

    G.add_nodes_from(node_names)
    G.add_edges_from(edges)

    role_dict = {}
    number_of_movies_dict = {}
    birth_dict = {}
    awards_dict = {}
    nominee_dict = {}

    for node in nodes:  # Loop through the list, one row at a time
        role_dict[node[0]] = node[1]
        number_of_movies_dict[node[0]] = node[2]
        birth_dict[node[0]] = node[3]
        awards_dict[node[0]] = node[4]
        nominee_dict[node[0]] = node[5]

    nx.set_node_attributes(G, role_dict, 'role')
    nx.set_node_attributes(G, number_of_movies_dict, 'number_of_movies')
    nx.set_node_attributes(G, birth_dict, 'date_of_birth')
    nx.set_node_attributes(G, awards_dict, 'awards_won')
    nx.set_node_attributes(G, nominee_dict, 'awards_nominee')

    return G


def calculate_average_degree(G):
    """
    calculates the average degree of a nerwork
    """

    return sum(dict(G.degree()).values()) / len(G)


def calculate_basic_properties(G):
    """
    Function to calculate basic properties of network
    """

    return {
        'number_of_nodes': G.number_of_nodes(),
        'number_of_edges': G.number_of_edges(),
        'is_connected': nx.is_connected(G),
        'number_of_componentes': nx.number_connected_components(G),
        'average_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
        'triadic_closure': nx.transitivity(G),
        'density': nx.density(G),
        'diameter': nx.diameter(G)
    }


def calculate_centralities(graph):
    """
    function will calculate all the centrality measures.
    """

    centrality_measures = dict()
    centrality_measures['Degree Centrality'] = nx.degree_centrality(graph)
    logging.info("Degree Centrality calculated.")

    centrality_measures['Closeness Centrality'] = nx.closeness_centrality(graph)
    logging.info("Closeness Centrality calculated.")

    centrality_measures['Betweenness Centrality'] = nx.betweenness_centrality(graph)
    logging.info("Betweenness Centrality calculated.")

    centrality_measures['Eigenvector Centrality'] = nx.eigenvector_centrality(graph)
    logging.info("Eigenvector Centrality calculated.")

    centrality_measures['Katz Centrality'] = nx.katz_centrality(graph)
    logging.info("Katz Centrality calculated.")

    centrality_measures['PageRank Centrality'] = nx.pagerank(graph)
    logging.info("PageRank Centrality calculated.")

    # Create a DataFrame
    df = pd.DataFrame.from_dict(centrality_measures, orient='index').transpose()

    return df


if __name__ == "__main__":
    logging.info("Started creating network.")
    graph = create_network()
    logging.info("Network is created.")
    # basic_properties = calculate_basic_properties(graph)
    # print(basic_properties)

    print(calculate_centralities(graph))


