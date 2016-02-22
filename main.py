from tree_searches import Search
from tree_builder import TreeBuilder

def main():
    tree = TreeBuilder()
    tree.build_tree(tree.file, tree.root)
    print("Behavior tree loaded...")
    tree.root.print()
    print()

    behavior = input("Event: ('q' to exit): ")

    while behavior is not 'q':
        search = Search()

        # DEPTH FIRST
        response = search.depth_first_recursive(behavior, tree.root)

        # BREADTH FIRST
        #response = search.breadth_first(behavior, tree.root)

        print("Response = {}".format(response))
        behavior = input("Event: ('q' to exit): ")


if __name__ == "__main__":
    main()