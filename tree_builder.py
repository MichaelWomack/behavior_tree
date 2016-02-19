from tree_node import TreeNode
import re

class TreeBuilder():
    'class to parse xml file and build xml data into tree structure'

    def __init__(self):
        self.file = open('behavior_tree.xml', 'r').read()
        self.root = TreeNode()

    def build_tree(self, unparsed_xml, root):
        # gets <tag>, <tag "data"/>, or </tag>
        tag = re.search(r'(\<)(\/)?([A-Za-z]+)((.*)\/?)(\>)?', unparsed_xml)

        if (tag):
            tag = tag.group()
            new_node = TreeNode()

            # no children, get attrs then process rest of siblings
            if tag.endswith('/>'):
                self.get_node_attrs(tag, new_node, root)
                root.children.append(new_node)
                unparsed_siblings = re.search(r'(?<=%s)(<?.*)'%tag, unparsed_xml, re.DOTALL).group()

                if (unparsed_siblings != ""):
                    self.build_tree(unparsed_siblings, root)

            # has children, get attr and recursively get children
            elif tag.endswith('>'):
                close_tag = self.get_close_tag(tag)
                self.get_node_attrs(tag, new_node, root)

                num_close_tags = self.get_num_close_tags(tag, unparsed_xml)
                close_tag_start_index = [m.start() for m in re.finditer(close_tag, unparsed_xml)][num_close_tags - 1]
                close_tag_end_index = [m.end() for m in re.finditer(close_tag, unparsed_xml)][num_close_tags - 1]

                children = re.search(r'(?<={})(.+)'.format(tag), unparsed_xml[:close_tag_start_index], re.DOTALL).group()
                unparsed_siblings = unparsed_xml[close_tag_end_index:]

                if self.get_tag_name(tag) == 'root':
                    self.root = root
                    self.root.behavior = 'ROOT'
                    self.build_tree(children, root)
                else:
                    new_node.parent = root
                    root.children.append(new_node)
                    self.build_tree(children, new_node)

                if unparsed_siblings != "":
                    self.build_tree(unparsed_siblings, root)

    # gets node behavior and response attributes
    def get_node_attrs(self, tag, new_node, root):
        if ('behavior' in tag):
            behavior = re.search(r'(?<=behavior=")(.*?)(?=\")', tag).group()
            new_node.behavior = behavior
        if ('response' in tag):
            response = re.search(r'(?<=response=")(.*?)(?=\")', tag).group()
            new_node.response = response
        new_node.parent = root

    # returns close tag
    def get_close_tag(self, tag):
        close_tag = '</' + re.search('[A-Za-z]+', tag).group() + '>'
        return close_tag

    # returns true if node has children
    def is_parent(self, node):
        return node.endswith('>') and not node.endswith('/>') and not node.startswith('</')

    # returns true if tag is a closing tag
    def is_closing_tag(self, tag):
        tag_name = re.search('[A-Za-z]+', tag).group()
        return tag.startswith('</' + tag_name + '>')

    # returns the tag name
    def get_tag_name(self, tag):
        return re.search('[A-Za-z]+', tag).group()

    # returns the number of close tags for getting the correct one
    def get_num_close_tags(self, tag, file):
        tag_name = self.get_tag_name(tag)
        current_tag = tag
        num_closing_tags_needed = 1
        num_tags_to_catch = 1

        while not num_closing_tags_needed == 0:
            next_node_index = file.index(current_tag) + len(current_tag)
            current_tag = re.search(r'(\<)(\/)?((.*)\/?)(\>)?', file[next_node_index:]).group()

            if (self.is_parent(current_tag)) and self.get_tag_name(current_tag) == tag_name:
                num_closing_tags_needed += 1
                num_tags_to_catch += 1

            elif (self.is_closing_tag(current_tag)) and self.get_tag_name(current_tag) == tag_name:
                num_closing_tags_needed -= 1

            file = file[next_node_index:]
        return num_tags_to_catch


tree = TreeBuilder()
tree.build_tree(tree.file, tree.root)
print("\nBehavior Tree Loaded...\n")
tree.root.print()
