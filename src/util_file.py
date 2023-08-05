import networkx as nx
import json


def read_embedding(embedding_file):
    print("Start Reading the sense embeddings......")
    with open(embedding_file, "r+") as fr:
        embedding = json.load(fr)
    print("Total ", len(embedding), "sense embeddings are loaded")
    print("Finish reading")
    return embedding


def read_roots(roots_file):
    with open(roots_file, "r+") as fr:
        line = fr.readline()
        roots = line.strip().split()
    return roots


def save_sense_children_file(tree_file, sense_file):
    T = nx.read_gml(tree_file)
    with open(sense_file, "w") as f:
        nodes = T.nodes()
        for node in nodes:
            children = T.successors(node)
            line = node + " " + " ".join(children) + "\n"
            f.write(line)
        f.close()


def save_sense_embedding(tree_file, sense_embedding_file):
    T = nx.read_gml(tree_file)
    with open(sense_embedding_file, "w") as f:
        for node in T.nodes():
            if T.nodes[node]["have_embedding"] == True:
                line = node + " " + T.nodes[node]["sense_embedding"] + "\n"
                f.write(line)
        f.close()


def save_parent_location(tree_file, concate_code_file):
    T = nx.read_gml(tree_file)
    with open(concate_code_file, "w") as f:
        for node in T.nodes():
            if T.nodes[node]["have_embedding"] == True:
                line = node + " " + " ".join(map(lambda x: str(x), T.nodes[node]["parent_location"])) + "\n"
                f.write(line)
        f.close()
