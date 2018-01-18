
# coding: utf-8

# In[ ]:


class Node(object):
    """"""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    
    @property
    def dleft(self):
        if self.left is None: 
            return None
        return self.left.data
        
    @dleft.setter
    def dleft(self, value):
        self.left = None(data)
    
    @property
    def dright(self):
        if self.right is None:
            return None
        return self.right.data
    
    @dright.setter
    def dright(self, value):
        self.right = Node(value)

class Tree(object):
    """"""
    def __init__(self, root_data):
        self.root = Node(root_data)
        self.nodes = 1
       
    @property
    def root_node(self):
        return self.root
    
    def add(self, value):
        cur_node = self.root
        while cur_node:
            if value > cur_node.data:
                if cur_node.right == None:
                    cur_node.right = Node(value)
                    break
                else:
                    cur_node = cur_node.right
            else:
                if cur_node.left == None:
                    cur_node.left = Node(value)
                    break
                else:
                    cur_node = cur_node.left
                    
        self.nodes += 1
        return

def print_inorder_reg(node):
    if node is None:
        return

    print_inorder_reg(node.left)
    #print ("Data: {}".format(node.data))
    print_inorder_reg(node.right)

def print_inorder_gen(node):
    if node is None:
        return
    for n in print_inorder_gen(node.left):
        yield n

    yield node.data
    for n in print_inorder_gen(node.right):
        yield n
    
def build_tree(slist):
    """
    Build tree from a sorted list slist.
    """
    siz = len(slist)
    
    if siz == 0:
        return None
    if siz == 1:
        return Tree(slist[0])
    
    ix = int(siz/2)
    t = Tree(slist[ix])
    
    def build_tree_impl(l):
        sz = len(l)
        if sz == 0:
            return
        ix = int(sz/2)
        t.add(l[ix])
        
        fhalf = l[:ix]
        shalf = l[ix+1 :]
        
        build_tree_impl(fhalf)
        build_tree_impl(shalf)
        pass
    
    build_tree_impl(slist[:ix])
    build_tree_impl(slist[ix+1:])
    return t

if __name__ == "__main__":
    """
    t = Tree(5)
    t.add(1)
    t.add(6)
    t.add(2)
    t.add(7)
    print_inorder(t.root_node)
    """
    l = []
    for i in range(0, 99999):
        l.append(i)
    
    t = build_tree(l)

    print_inorder_reg(t.root_node)

    """
    #Generator based
    for i in print_inorder_gen(t.root_node):
        pass
    """
    
    pass

