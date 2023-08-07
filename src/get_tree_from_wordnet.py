from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G):
    nx.draw_planar(G, with_labels=True, font_weight='bold')
    plt.savefig('fig.png', bbox_inches='tight')


def get_path_tree(nodes):
    trees = []
    for node in nodes:
        tree = nx.DiGraph()
        # Add root to the tree
        tree.add_node("*root*")
        path = max(wn.synset(node).hypernym_paths(), key=len)
        # Add top level word a, s, r, v for some words
        top_level_words = ["a", "s", "r", "v"]
        is_noun = True
        for top in top_level_words:
            if "."+top+"." in node:
                tree.add_node(top)
                tree.add_edge("*root*", top)
                top_level_word = top
                is_noun = False
                break

        # Add other nodes to the tree
        for i in range(len(path)):
            # First node, entity.n.01 for nouns, "a", "s", "r", "v" for others
            # Add node to the tree
            tree.add_node(path[i].name(), sense=path[i].definition())
            if i == 0:
                if is_noun:
                    # entity.n.01, add edge to the root
                    tree.add_edge("*root*", path[i].name())
                else:
                    # others, add edge to the top level words
                    tree.add_edge(top_level_word, path[i].name())
            else:
                # Add edges to its predecessor
                tree.add_edge(path[i-1].name(), path[i].name())
        trees.append(tree)
    return trees


def get_tree_from_wordnet(nodes):
    # The trees is the highest hypernym path from the nodes
    trees = get_path_tree(nodes)
    print("Finish get tree")
    return trees
