
class TreeNode:
    'class to create tree nodes'

    def __init__(self, behavior=None, response=None, parent=None):
        self.behavior = behavior
        self.response = response
        self.parent = parent
        self.children = []

    def print(self, iteration=0):
        print('\t' * iteration + self.__str__())

        new_itr = iteration + 1
        for child in self.children:
             child.print(new_itr)

    def __str__(self):
        if (self.response == '' or self.response is None):
            return "Behavior: {}".format(self.behavior)
        elif (self.behavior == '' or self.behavior is None):
            return "Response: {}".format(self.response)
        else:
            return "Behavior: {} Response: {}".format(self.behavior, self.response)



