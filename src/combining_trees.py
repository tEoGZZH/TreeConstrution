import networkx as nx
import numpy as np

def bfs_double_checking(tree):
    # Initialize the tree
    print("Using bfs double checking")
    new_tree = nx.DiGraph()
    queue = []
    done = []
    # BFS the graph tp get the bfs tree
    queue.append("*root*")
    done.append("*root*")
    while queue:
        n = queue.pop(0)
        subnodes = tree.successors(n)
        for subnode in subnodes:
            if subnode not in done:
                queue.append(subnode)
                new_tree.add_node(subnode, sense=tree.nodes[subnode]["sense"])
                new_tree.add_edge(n, subnode)
                done.append(subnode)
    if not nx.is_tree(new_tree):
        print("Some problem caused double checking, not tree here")
    print(nx.number_of_nodes(new_tree), " Nodes has been checked")
    return new_tree


def add_embedding(embeddings, trees):
    new_tree = bfs_double_checking(nx.compose_all(trees))
    for node in new_tree.nodes():
        if node in embeddings:
            strlist_embd = [str(x) for x in np.array(embeddings[node])[:, 0].reshape(1, -1)[0]]
            new_tree.nodes[node]["sense_embedding"] = " ".join(strlist_embd)
            new_tree.nodes[node]["have_embedding"] = True
        else:
            new_tree.nodes[node]["have_embedding"] = False
    return new_tree


def delete_nodes_simple(tree):
    remove_nodes = [n for n in tree.nodes() if tree.nodes[n]["have_embedding"] == False and n != "*root*"]
    tree.remove_nodes_from(remove_nodes)
    new_nodes = [n for n in tree.nodes() if tree.in_degree(n) == 0 and n != "*root*"]
    new_edges = [("*root*", y) for y in new_nodes]
    tree.add_edges_from(new_edges)

    return tree


def bfs_check_sucs(tree, sucs):
    for n in sucs:
        if tree.nodes[n]["have_embedding"]:
            return True, n
    # Then check every successors'successor
    for n in sucs:
        bfs_check_sucs(tree, tree.successors(n))

    return False, None


def delete_nodes(tree):
    remove_nodes = [n for n in tree.nodes() if tree.nodes[n]["have_embedding"] == False and n != "*root*"]
    pre_dic = dict(nx.bfs_predecessors(tree, "*root*"))
    for n in remove_nodes:
        have_pre = False
        pre = pre_dic[n]
        while pre is not None:
            if tree.nodes[pre]["have_embedding"]:
                have_pre = True
                break
            else:
                if pre == "*root*":
                    pre = None
                else:
                    pre = pre_dic[pre]
        have_suc, suc = bfs_check_sucs(tree, tree.successors(n))
        if have_pre and have_suc:
            if not tree.has_edge(pre, suc):
                tree.add_edge(pre, suc)
        elif not have_pre and have_suc:
            if not tree.has_edge("*root*", suc):
                tree.add_edge("*root*", suc)

    tree.remove_nodes_from(remove_nodes)
    nodes_left = [n for n in tree.nodes() if tree.in_degree(n) == 0 and n != "*root*"]
    new_edges = [("*root*", y) for y in nodes_left]
    tree.add_edges_from(new_edges)

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


def combining_tree(trees, embedding_file):
    tree_with_embedding = add_embedding(embedding_file, trees)
    print("Original nodes from tree: ", len(tree_with_embedding.nodes()))
    tree_with_delete_node = delete_nodes(tree_with_embedding)
    tree_with_parent_location = parent_location(tree_with_delete_node)
    if not nx.is_tree(tree_with_parent_location):
        print("Some problem caused. not tree here after combining")
    print("Afterwards nodes from tree: ", len(tree_with_parent_location.nodes()))
    print("Finish combining the tree")
    print("Starting saving the file.......")

    return tree_with_parent_location

    # Save the file
    nx.write_gml(tree_with_parent_location, new_tree_file)
    save_sense_children_file(new_tree_file, children_file)
    save_sense_embedding(new_tree_file, sense_embedding_file)
    save_parent_location(new_tree_file, concate_code_file)
    print("All finished")
