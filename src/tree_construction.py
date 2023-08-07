import networkx as nx
from get_tree_from_wordnet import get_tree_from_wordnet as getTree
from combining_trees import combining_tree as comTree
import util_file

if __name__ == '__main__':
    # Read embedding file:
    sense_embedding_file = "..\\Dataset\\gloss_embedding.txt"
    sense_embeddings = util_file.read_embedding(sense_embedding_file)

    # Extract trees from wordnet
    trees = getTree(sense_embeddings.keys())
    # Combine the trees
    tree = comTree(trees, sense_embeddings)
    print("Finish combining the tree")
    print("With ", len(tree.nodes())-5, "nodes in tree, except for 5 root nodes", len(sense_embeddings), "sense embeddings",
          "{:.4%} are covered".format((len(tree.nodes())-5)/len(sense_embeddings)))

    # Save the file
    new_tree_file = "..\\Dataset\\output\\tree_with_everything.gml"
    children_file = "..\\Dataset\\output\\sense_children.txt"
    new_sense_embedding_file = "..\\Dataset\\output\\sense_embedding.txt"
    concate_code_file = "..\\Dataset\\output\\catcode.txt"

    nx.write_gml(tree, new_tree_file)
    util_file.save_sense_children_file(tree, children_file)
    util_file.save_parent_location(tree, concate_code_file)
    util_file.save_sense_embedding(tree, new_sense_embedding_file)
    print("All finished")