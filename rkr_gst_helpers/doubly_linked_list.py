
class Node(object):

    def __init__(self, maximal_match_length, data=None, next_node=None, prev_node=None):
        self.maximal_match_length = maximal_match_length
        self.next_node = next_node
        self.prev_node = prev_node
        self.tiles = []  # I think tiles is equivalent to data

        if not data:
            self.data = []
        elif type(data) != list:
            self.data = [data]
        elif type(data) == list:
            self.data = data

    def get_next(self):
        return self.next_node

    def set_next(self, next_node):
        self.next_node = next_node

    def get_prev(self):
        return self.prev_node

    def set_prev(self, prev_node):
        self.prev_node = prev_node

    def get_data(self):
        return self.data

    def set_data(self, data):
        if type(data) != list:
            self.data.append(data)
        elif type(data) == list:
            self.data = self.data + data

    def get_tiles(self):
        return self.tiles

    def set_tiles(self, tiles):
        if type(tiles) == str:
            self.data.append(tiles)
        elif type(tiles) == list:
            self.tiles = self.data + tiles

class LinkedList(object):
    """ A Doubly Linked list used in the Running Karp-Rabin Greedy String Tiling algorithm. 
    
    The doubly linked list maintains nodes (class Node) that contain lists of string data. Each list of string data 
    contains strings with the same maximal match length. A node in the doubly linked list can be initialized with 
    either a string or a list of strings. The __init() handles the creation of the list. There are several methods, 
    which include some maintenance functions.
    
    Importantly, the root node is set to the last position data was added or updated to, and each node has a distinct
    maximal_match_length.
    
    Attributes:
        maximal_match_length (int): During the tiling the maximal match length is used to create tiling lengths.
        data (string): May be a string or list of strings. The data for each node is a list of strings. Adding or
            updating data handles a string or a list of strings. When a node is initialized it is initialized to a
            list of strings.
            
    Methods:
        get_size(): Gets the number of nodes in the doubly linked list.
        remove(maximal_match_length): Removes the node with the given maximal_match_length.
        find(maximal_match_length): Finds the node with the given maximal_match_length.
        add(maximal_match_length, data): Adds data to the given maximal_match_length. If the maximal_match_length
            does not exist a new node is created and the data initialized.
        set_root(maximal_match_length): Sets the root node to the specified maximal_match_length.
        move_to(maximal_match_length): Moves to the node specified by the maximal_match_length, or to the nearest 
            node given the maximal_match_length..
        move_up(): From the root node will move up the linked list to the top node: get_prev().
        move_down(): From the root node will move down the list to the last node: get_next().
        load_initial_data(maximal_match_length, data): Used to load initial data for testing.

    Example: 
            mylist = LinkedList()
            print ''
            print 'Load initial data.'
            print ''       
            mylist.load_initial_data(2, '2')
            mylist.load_initial_data(4, '4')
            mylist.load_initial_data(6, '6')
            mylist.load_initial_data(8, '8')
            mylist.load_initial_data(10, '10')
            maximal_match_length = 10
            print 'Set root node: ', mylist.set_root(maximal_match_length)
            print 'Move down    : '
            mylist.move_down()
            maximal_match_length = 2
            print 'Set root node: ', mylist.set_root(maximal_match_length)
            maximal_match_length = 7
            print 'Add data (11): ', mylist.add(maximal_match_length, '7')
            maximal_match_length = 2
            print 'Set root node: ', mylist.set_root(maximal_match_length)
            print 'Move up      : '
            mylist.move_up()
    """

    def __init__(self, root=None):
        self.root = root
        self.size = 0
        self.curr_mml = None
        self.maximal_match_lengths = []

    def get_size(self):
        return self.size

    def remove(self, maximal_match_length):
        this_node = self.root
        while this_node:

            if this_node.maximal_match_length == maximal_match_length:
                next = this_node.get_next()
                prev = this_node.get_prev()

                if next:
                    next.set_prev(prev)
                if prev:
                    prev.set_next(next)
                else:
                    self.root = this_node
                self.size -= 1
                self.curr_mml = this_node.maximal_match_length

                return True  # Data removed.
            else:
                this_node = this_node.get_next()
        return False  # Data not found.

    def find(self, maximal_match_length):
        # Do not set self.curr_mml using find()
        this_node = self.root
        while this_node:
            if this_node.maximal_match_length == maximal_match_length:
                return this_node
            else:
                if this_node.maximal_match_length > maximal_match_length:
                    this_node = this_node.get_next()
                else:
                    this_node = this_node.get_prev()
        return None

    def add(self, maximal_match_length, data):
        this_node = self.root

        # If nodes do not exist.
        if not this_node:
            new_node = Node(maximal_match_length, data)
            self.size += 1
            self.root = new_node
            self.curr_mml = maximal_match_length
            self.maximal_match_lengths.append(maximal_match_length)
            new_node.set_prev(None)
            new_node.set_next(None)
            return new_node.maximal_match_length

        while this_node:
            # The equivalence updates the data, while the inequalities create new data on a new node.
            if maximal_match_length == this_node.maximal_match_length:
                this_node.set_data(data)
                self.root = this_node
                self.curr_mml = this_node.maximal_match_length
                return this_node.maximal_match_length
            elif maximal_match_length < this_node.maximal_match_length:
                curr_node = this_node
                next_node = this_node.get_next()
                this_node = next_node
                # If last node then this_node is None: maximal_match_length exceeds bounds.
                if next_node:
                    if maximal_match_length > next_node.maximal_match_length:
                        new_node = Node(maximal_match_length, data, curr_node)
                        self.size += 1
                        self.root = new_node
                        self.curr_mml = maximal_match_length
                        self.maximal_match_lengths.append(maximal_match_length)
                        new_node.set_next(next_node)
                        new_node.set_prev(curr_node)
                        curr_node.set_next(new_node)
                        next_node.set_prev(new_node)
                        return new_node.maximal_match_length
                    else:
                        this_node = next_node
                else:
                    new_node = Node(maximal_match_length, data, curr_node)
                    self.size += 1
                    self.root = new_node
                    self.curr_mml = maximal_match_length
                    self.maximal_match_lengths.append(maximal_match_length)
                    new_node.set_next(None)
                    new_node.set_prev(curr_node)
                    curr_node.set_next(new_node)
                    return new_node.maximal_match_length
            elif maximal_match_length > this_node.maximal_match_length:
                curr_node = this_node
                prev_node = this_node.get_prev()
                this_node = prev_node
                # If first node then this_node is None: maximal_match_length exceeds bounds.
                if prev_node:
                    if maximal_match_length < prev_node.maximal_match_length:
                        new_node = Node(maximal_match_length, data, curr_node)
                        self.size += 1
                        self.root = new_node
                        self.curr_mml = maximal_match_length
                        self.maximal_match_lengths.append(maximal_match_length)
                        new_node.set_prev(prev_node)
                        new_node.set_next(curr_node)
                        curr_node.set_prev(new_node)
                        prev_node.set_next(new_node)
                        return new_node.maximal_match_length
                    else:
                        this_node = prev_node
                else:
                    new_node = Node(maximal_match_length, data, curr_node)
                    self.size += 1
                    self.root = new_node
                    self.curr_mml = maximal_match_length
                    self.maximal_match_lengths.append(maximal_match_length)
                    new_node.set_prev(None)
                    new_node.set_next(curr_node)
                    curr_node.set_prev(new_node)
                    return new_node.maximal_match_length
        return

    def set_root(self, maximal_match_length):
        this_node = self.root
        while this_node:
            if this_node.maximal_match_length == maximal_match_length:
                self.root = this_node
                self.curr_mml = this_node.maximal_match_length
                return this_node.maximal_match_length
            else:
                this_node = this_node.get_next()
        return

    def move_to(self, maximal_match_length):
        # Do not set self.curr_mml using move_to()
        this_node = self.root
        while this_node:
            if maximal_match_length == this_node.maximal_match_length:
                return this_node.data
            elif maximal_match_length < this_node.maximal_match_length:
                curr_node = this_node
                next_node = this_node.get_next()
                this_node = next_node
                # If last node then this_node is None: maximal_match_length exceeds bounds.
                if next_node:
                    if maximal_match_length >= next_node.maximal_match_length:
                        return next_node.maximal_match_length
                else:
                    return curr_node.maximal_match_length
            elif maximal_match_length > this_node.maximal_match_length:
                curr_node = this_node
                prev_node = this_node.get_prev()
                this_node = prev_node
                # If first node then this_node is None: maximal_match_length exceeds bounds.
                if prev_node:
                    if maximal_match_length <= prev_node.maximal_match_length:
                        return prev_node.maximal_match_length
                else:
                    return curr_node.maximal_match_length
        return

    def move_down(self):
        # Do not set self.curr_mml using move_down()
        curr_node = None
        this_node = self.root
        while this_node:
            print '         MML : ', this_node.maximal_match_length
            curr_node = this_node
            this_node = this_node.get_next()
        return curr_node

    def move_up(self):
        # Do not set self.curr_mml using move_up()
        curr_node = None
        this_node = self.root
        while this_node:
            print '         MML : ', this_node.maximal_match_length
            curr_node = this_node
            this_node = this_node.get_prev()
        return curr_node

    def load_initial_data(self, maximal_match_length, data):
        new_node = Node(maximal_match_length, data, self.root)
        if self.root:
            self.root.set_prev(new_node)
        self.root = new_node
        self.curr_mml = new_node.maximal_match_length
        self.size += 1
