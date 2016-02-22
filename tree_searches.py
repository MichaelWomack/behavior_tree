from collections import deque
import random

class Search():
    'methods to implement depth-first and breadth-first searches'

    def __init__(self):
        self.discovered = []
        self.response = "No Response Found"

    # Once the behavior key has been found, it will choose a
    # random child from that node to continue the search, and so on
    def depth_first_recursive(self, behavior_key, root, found=False):
        self.discovered.append(root)

        if root.behavior == behavior_key or found:
            if len(root.children) != 0:
                next_node = random.choice(root.children)
                self.response = self.depth_first_recursive(behavior_key, next_node, found=True)
            else:
                self.response = root.response
        else:
            for child in root.children:
                if child not in self.discovered:
                    self.response = self.depth_first_recursive(behavior_key, child, found=found)
        return self.response

    # Once the behavior key has been found, it only cares about the children
    # of the behavior key and all other nodes are dropped from queue. If that hasn't
    # happened, the search proceeds as usual checking each node
    def breadth_first(self, behavior_key, root):
        nodes = deque([])
        nodes.append(root)
        behavior_found = False

        while len(nodes) != 0:
            current_node = nodes.popleft()

            if current_node.behavior == behavior_key:
                behavior_found = True
                nodes = deque(current_node.children)

            if behavior_found:
                if len(current_node.children) > 0:
                    random_child = random.choice(current_node.children)
                    nodes = deque([random_child])
                else:
                    self.response = current_node.response
            else:
                for child in current_node.children:
                    nodes.append(child)
        return self.response

