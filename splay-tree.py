import re
import sys
from queue import Queue


class splay_tree(object):

    def __init__(self):
        self.root = None

    def root_key(self):
        return self.root.key

    def root_data(self):
        return self.root.data

    def add(self, key, data):
        if self.root == None:
            self.root = node(key, data, None, None, None)
            return 1
        current_node = node(self.root.key, self.root.data, self.root.left, self.root.right, None) 
        while True:
            if key > current_node.key and current_node.right != None:
                current_node = current_node.right
            if key < current_node.key and current_node.left != None:
                current_node = current_node.left
            if key > current_node.key and current_node.right == None:
                new_node = node(key, data, None, None, current_node)
                current_node.right = new_node
                '''
                print("print", new_node.key)
                self.my_print()
                '''
                self.root = self.splay(new_node)
                return 1
            if key < current_node.key and current_node.left == None:
                new_node = node(key, data, None, None, current_node)
                current_node.left = new_node
                '''
                print("print", new_node.key)
                self.my_print()
                '''
                self.root = self.splay(new_node)
                return 1
            if key == current_node.key:
                return 0

    
    def set_value(self, key, value):
        if self.root == None:
            return 0
        current_node = self.root
        while current_node.key != key:
            if key > current_node.key:
                current_node = current_node.right
            if current_node == None:
                break
            if key < current_node.key:
                current_node = current_node.left
            if current_node == None:
                break
        if current_node == None:
            return 0
        current_node.data = value
        self.root = self.splay(current_node)
        return 1

    def delete(self, key):
        searching_node = []
        if self.search_without_splay(self.root, key, searching_node) == 0 or self.root == None:
            return 0
        self.root = self.splay(searching_node[0])
        if self.root.right == None and self.root.left == None:
            self.root = None
            return 1
        if self.root.right == None:
            self.root = self.root.left
            self.root.parent = None
            return 1
        new_root = self.root.left
        if new_root == None:
            self.root = self.root.right
            self.root.parent = None
            return 1
        
        while new_root.right != None:
            new_root = new_root.right
        if new_root == self.root.left:
            new_root.right = self.root.right
            if new_root.right != None:
                new_root.right.parent = new_root
            new_root.parent = None
            self.root = new_root
            return 1

        self.root.left.parent = None
        self.root.left = self.splay(new_root)
        self.root.left.right = self.root.right
        self.root.right.parent = self.root.left
        self.root = self.root.left

        return 1

    def search(self, searching_node, key):
        while True:
            if searching_node == None:
                return None
            if key == searching_node.key:
                return self.splay(searching_node)
            if key < searching_node.key and searching_node.left != None:
                searching_node = searching_node.left
                continue
            if key > searching_node.key and searching_node.right != None:
                searching_node = searching_node.right
                continue
            return self.splay(searching_node)

    def my_search(self, key):
        if self.root == None:
            return 0
        self.root = self.search(self.root, key)
        if self.root.key == key:
            return 1
        else:
            return 0

    def search_without_splay(self, current_node, key, searching_node):
        if self.root == None:
            return 0
        if current_node.key == key:
            searching_node.append(current_node)
            return 1
        if current_node.key < key and current_node.right != None:
            return self.search_without_splay(current_node.right, key, searching_node)
        if current_node.key > key and current_node.left != None:
            return self.search_without_splay(current_node.left, key, searching_node)
        return 0

    def my_min(self, min_elem_list):
        if self.root == None:
            return 0
        min_elem = self.root
        while min_elem.left != None:
            min_elem = min_elem.left
        self.root = self.splay(min_elem)
        min_elem_list.append(self.root.key)
        min_elem_list.append(self.root.data)
        return 1
        

    def my_max(self, max_elem_list):
        if self.root == None:
            return 0
        max_elem = self.root
        while max_elem.right != None:
            max_elem = max_elem.right
        self.root = self.splay(max_elem)
        max_elem_list.append(self.root.key)
        max_elem_list.append(self.root.data)
        return 1

    def my_print(self):
        if self.root == None:
            print("_")
            return
        nodes = []
        print("[", self.root.key," ", self.root.data,"]", sep = '') #выводим корень
        indicate = 0
        if self.root.left != None or self.root.right != None:
            indicate = 1
        nodes.append(self.root.left)
        nodes.append(self.root.right)
        level = 1
        while indicate == 1:
            indicate = 0
            for i in range(2**level):
                current_node = nodes[0]
                if i == 0 and current_node == None:
                    print("_", end = '')
                elif i == 0 and current_node != None:
                    print("[", current_node.key," ", current_node.data," ",current_node.parent.key,"]", sep = '', end = '') 
                elif current_node == None:
                    print(" _", end = '')
                else:
                    print(" [", current_node.key," ", current_node.data," ",current_node.parent.key,"]", sep = '', end = '')
                if current_node != None:
                    if current_node.left != None or current_node.right != None:
                        indicate = 1
                    nodes.append(current_node.left)
                    nodes.append(current_node.right)
                if current_node == None:
                    nodes.append(None)
                    nodes.append(None)
                nodes.pop(0)
            print()
            level += 1
        return
    def my_print_2(self, print_list): #переписать

        if self.root == None:
            print_list.append('_\n')
            return print_list
        nodes = []
        print_list.append('[')
        print_list.append(self.root.key)
        print_list.append(' ')
        print_list.append(self.root.data)
        print_list.append(']\n')
        indicate = 0
        if self.root.left != None or self.root.right != None:
            indicate = 1
        nodes.append(self.root.left)
        nodes.append(self.root.right)
        level = 1
        while indicate == 1:
            indicate = 0
            for i in range(2**level):
                current_node = nodes[0]
                if i == 0 and current_node == None:
                    print_list.append('_')
                elif i == 0 and current_node != None:
                    
                    print_list.append('[')
                    print_list.append(current_node.key)
                    print_list.append(' ')
                    print_list.append(current_node.data)
                    print_list.append(' ')
                    print_list.append(current_node.parent.key)
                    print_list.append(']')
                    
                    #print_list.append('['+'{}'.format(current_node.key) +' '+'{}'.format(current_node.data)+' '+'{}'.format(current_node.parent.key)+']')
                    #print_list.append('[{} {} {}]'.format(current_node.key,current_node.data,current_node.parent.key))
                elif current_node == None:
                    print_list.append(' _')
                else:
                    
                    print_list.append(' [')
                    print_list.append(current_node.key)
                    print_list.append(' ')
                    print_list.append(current_node.data)
                    print_list.append(' ')
                    print_list.append(current_node.parent.key)
                    print_list.append(']')
                    
                    #print_list.append('[ {} {} {}]'.format(current_node.key,current_node.data,current_node.parent.key))
                    #print_list.append(' ['+'{}'.format(current_node.key)+' '+'{}'.format(current_node.data)+' '+'{}'.format(current_node.parent.key)+']')
                if current_node != None:
                    if current_node.left != None or current_node.right != None:
                        indicate = 1
                    nodes.append(current_node.left)
                    nodes.append(current_node.right)
                if current_node == None:
                    nodes.append(None)
                    nodes.append(None)
                nodes.pop(0)
            print_list.append('\n')
            level += 1
        return print_list
    
    def max_height(self, node, h, index, dict_of_indexes: dict):
        if node:
            new_h = h + 1
            left_index = 2 * index + 1
            right_index = 2 * index + 2
            dict_of_indexes[index] = node

            return max(self.max_height(node.left, new_h, left_index, dict_of_indexes),
            self.max_height(node.right, new_h, right_index, dict_of_indexes))
        else:
            return h

    def node_to_string(self, n):
        if n == self.root:
            return '[{} {}]'.format(n.key, n.data)#'[' + str(n.key) + ' ' + str(n.data) + ']'
        else:
            return '[{} {} {}]'.format(n.key, n.data, n.parent.key)#'[' + str(n.key) + ' ' + str(n.data) + ' ' + str(n.parent.key) + ']'

    def new_print(self):

        dict_of_indexes = {}
        height = self.max_height(self.root, 0, 0, dict_of_indexes)
        need_to_print = (1 << height) - 1
        #print(height)
        if need_to_print == 0:
            return '_'

        list_of_nodes = [' _'] * need_to_print

        for index, node in dict_of_indexes.items():
            if ((index + 1) & index) == 0:
                list_of_nodes[index] = ('\n' if index != 0 else '') + self.node_to_string(node)
            else:
                list_of_nodes[index] = ' '+ self.node_to_string(node)
        for i in range(1, height):
            index = 2 ** i
            list_of_nodes[index - 1] = '\n' + list_of_nodes[index - 1][1:]

        string = ''.join(list_of_nodes)
        return string.strip()       


    def splay(self,splaying_node):
        while True:
            if splaying_node.parent == None:
                return splaying_node
            parent = splaying_node.parent
            grandparent = parent.parent
            if grandparent == None:                                                 # поворот типа zig
                self.rotate(parent, splaying_node) 
                return splaying_node    
            else:
                if (grandparent.left == parent) == (parent.left == splaying_node):   # поворот типа zigzig
                    self.rotate(grandparent, parent)
                    self.rotate(parent, splaying_node)
                else:                                                               # поворот типа zigzag
                    self.rotate(parent, splaying_node)
                    self.rotate(grandparent, splaying_node)

    def rotate(self,parent, child):
        grandparent = parent.parent
        if grandparent != None:
            if grandparent.left == parent:
                grandparent.left = child
            else:
                grandparent.right = child

        if parent.left == child:
            parent.left, child.right = child.right, parent
        else:
            parent.right, child.left = child.left, parent

        child.keep_parent(child)
        parent.keep_parent(parent)
        child.parent = grandparent

class node:
    def __init__(self, key = None, data = None, left = None, right = None, parent = None):
        self.left = left
        self.right = right
        self.parent = parent
        self.key = key
        self.data = data

    def set_parent(self, child, parent):
        if child != None:
            child.parent = parent

    def keep_parent(self, parent):
        self.set_parent(parent.left, parent)
        self.set_parent(parent.right, parent)


tree = splay_tree()
for str in sys.stdin.readlines():
    if str == '' or str == '\n':
        continue
    if str:
        command = re.match("^add -?\d+ \S+$",str)
        if command:
            args = command.group(0).split(' ')
            if not tree.add(int(args[1]), args[2]):
                print("error")
            continue

        command = re.match("^set -?\d+ \S+$",str)
        if command:
            
            args = command.group(0).split(' ')
            if not tree.set_value(int(args[1]),args[2]):
                print("error")
            continue

        command = re.match("^delete -?\d+$",str)
        if command:
            args = command.group(0).split(' ')
            if tree.delete(int(args[1])) == 0:
                print("error")
            continue

        command = re.match("^search -?\d+$",str)
        if command:
            args = command.group(0).split(' ')
            if tree.my_search(int(args[1])) == 0:
                print(0)
            else:
                print(1,tree.root_data())
            continue

        command = re.match("^min$",str)
        if command:
            min_node = []
            if not tree.my_min(min_node):
                print("error")
            else:
                print(min_node[0], min_node[1])
            continue

        command = re.match("^max$",str)
        if command:
            max_node = []
            if not tree.my_max(max_node):
                print("error")
            else:
                print(max_node[0], max_node[1])
            continue

        command = re.match("^print$",str)
        if command:
            '''
            print_list = []
            print_list = tree.to_string()
            for x in print_list:
                print(x, end = '')
            '''
            #print_for_splay_tree(tree) #взял внешнюю функцию так как с внутренней функций программа не проходила по времени
            print(tree.new_print())
            continue

        print("error")
        