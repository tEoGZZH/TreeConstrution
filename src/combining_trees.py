import networkx as nx
import numpy as np


def add_embedding(embeddings, trees):
    # Compose tree
    print("Composing trees......")
    new_tree = nx.compose_all(trees)
    print("Composing finished")
    # Add embedding for the nodes
    for node in new_tree.nodes():
        if node in embeddings:
            strlist_embd = [str(x) for x in np.array(embeddings[node])]
            new_tree.nodes[node]["sense_embedding"] = " ".join(strlist_embd)
            new_tree.nodes[node]["have_embedding"] = True
        else:
            new_tree.nodes[node]["have_embedding"] = False
    return new_tree


def delete_nodes(tree, embeddings):
    # Nodes that do not have embeddings, need to be removed
    remove_nodes = [n for n in tree.nodes() if
                    tree.nodes[n]["have_embedding"] is False and n not in ["*root*", "a", "s", "r", "v"]]

    # Check number
    all_nodes = tree.nodes()
    have_embedding = [n for n in tree.nodes() if tree.nodes[n]["have_embedding"] is True]
    print("All nodes here: ", len(all_nodes), "remove here: ", len(remove_nodes), "have embedding here: ",
          len(have_embedding))

    # Remove the nodes
    for n in remove_nodes:
        pre = list(tree.predecessors(n))[0]
        sucs = list(tree.successors(n))
        tree.add_edges_from([(pre, suc) for suc in sucs])
        tree.remove_node(n)

    print("After remove nodes, is connected?", nx.is_weakly_connected(tree))
    print("After remove nodes, is tree?", nx.is_tree(tree))
    # Add embedding for top level words
    for node in ["a", "s", "r", "v"]:
        sucs = list(tree.successors(node))
        ems = []
        for suc in sucs:
            ems.append(embeddings[suc])
        em = np.mean(ems, axis=0).tolist()
        strlist_embd = [str(x) for x in em]
        tree.nodes[node]["sense_embedding"] = " ".join(strlist_embd)

    return tree


def parent_location(tree):
    # Add layer
    max_layer = 0
    for node in tree.nodes():
        layer = nx.shortest_path_length(G=tree, source="*root*", target=node) + 1
        if layer > max_layer:
            max_layer = layer
        tree.nodes[node]["layer"] = layer

    print("Max Layer: ", max_layer)
    # Giving a sorting
    tree.nodes["*root*"]["layer_location"] = "0"
    for layer in range(1, max_layer):
        nodes = [x for x in tree.nodes() if tree.nodes[x]["layer"] == layer]
        for i in range(len(nodes)):
            tree.nodes[nodes[i]]["layer_location"] = i + 1
    # Get parent location
    for node in tree.nodes:
        location = []
        path = nx.shortest_path(source="*root*", target=node, G=tree)
        path.pop()
        for n in path:
            location.append(tree.nodes[n]["layer_location"])
        for i in range(max_layer - len(location)):
            location.append(0)
        tree.nodes[node]["parent_location"] = location
    return tree


def combining_tree(trees, embeddings):
    print("Start to combine tree")
    tree_with_embedding = add_embedding(embeddings, trees)
    print("Original nodes from tree: ", len(tree_with_embedding.nodes()))
    tree_with_delete_node = delete_nodes(tree_with_embedding, embeddings)
    tree_with_parent_location = parent_location(tree_with_delete_node)
    if not nx.is_tree(tree_with_parent_location):
        print("Some problem caused. not tree here after combining")
    print("Afterwards nodes from tree: ", len(tree_with_parent_location.nodes()))

    return tree_with_parent_location
