from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt


def bfs_from_wordnet(root):
    # Initialize the tree
    T = nx.DiGraph()
    queue = []
    done = []
    # Add root to the tree
    T.add_node("*root*")
    T.add_node(root, sense=wn.synset(root).definition())
    T.add_edge("*root*", root)
    queue.append(root)
    done.append(root)
    # BFS the graph tp get the bfs tree
    while queue:
        n = queue.pop(0)
        subnodes = wn.synset(n).hyponyms()
        for subnode in subnodes:
            subnode_name = subnode.name()
            if subnode_name not in done:
                queue.append(subnode_name)
                T.add_node(subnode_name, sense=subnode.definition())
                T.add_edge(n, subnode_name)
                done.append(subnode_name)
    if not nx.is_tree(T):
        print("Some problem caused when extract from wordnet not tree here for ", root)
    print(nx.number_of_nodes(T), " Nodes from ", root, "has been extracted")
    return T


def draw_graph(G):
    nx.draw_planar(G, with_labels=True, font_weight='bold')
    plt.savefig('fig.png', bbox_inches='tight')


def get_tree_from_wordnet(roots):
    trees = []
    for root in roots:
        print("Start extracting", root)
        T = bfs_from_wordnet(root)
        trees.append(T)
    return trees
