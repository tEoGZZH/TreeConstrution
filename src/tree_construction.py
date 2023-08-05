import networkx as nx
from get_tree_from_wordnet import get_tree_from_wordnet as getTree
from combining_trees import combining_tree as comTree
import util_file

if __name__ == '__main__':
    # Extract trees from wordnet
    root_file = "..\\Dataset\\All\\roots.txt"
    roots = util_file.read_roots(root_file)
    trees = getTree(roots)

    # Combining all the trees and add attribute
    sense_embedding_file = "..\\Dataset\\gloss_dic_20230619.txt"
    sense_embeddings = util_file.read_embedding(sense_embedding_file)
    tree = comTree(trees, sense_embeddings)
    print("With ", len(tree.nodes()), "nodes in tree and ", len(sense_embeddings), "sense embeddings",
          "{:.4%} are covered".format(len(tree.nodes())/len(sense_embeddings)))

    # Save the file
    new_tree_file = "..\\Dataset\\All\\tree_with_everything.gml"
    children_file = "..\\Dataset\\All\\sense_children.txt"
    new_sense_embedding_file = "..\\Dataset\\All\\sense_embedding.txt"
    concate_code_file = "..\\Dataset\\All\\catcode.txt"

    nx.write_gml(tree, new_tree_file)
    util_file.save_sense_children_file(new_tree_file, children_file)
    util_file.save_sense_embedding(new_tree_file, new_sense_embedding_file)
    util_file.save_parent_location(new_tree_file, concate_code_file)
    print("All finished")