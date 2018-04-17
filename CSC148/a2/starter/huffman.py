"""
Code for compressing and decompressing using Huffman compression.
"""

from nodes import HuffmanNode, ReadNode


# ====================
# Helper functions for manipulating bytes


def get_bit(byte, bit_num):
    """ Return bit number bit_num from right in byte.

    @param int byte: a given byte
    @param int bit_num: a specific bit number within the byte
    @rtype: int

    >>> get_bit(0b00000101, 2)
    1
    >>> get_bit(0b00000101, 1)
    0
    """
    return (byte & (1 << bit_num)) >> bit_num


def byte_to_bits(byte):
    """ Return the representation of a byte as a string of bits.

    @param int byte: a given byte
    @rtype: str

    >>> byte_to_bits(14)
    '00001110'
    """
    return "".join([str(get_bit(byte, bit_num))
                    for bit_num in range(7, -1, -1)])


def bits_to_byte(bits):
    """ Return int represented by bits, padded on right.

    @param str bits: a string representation of some bits
    @rtype: int

    >>> bits_to_byte("00000101")
    5
    >>> bits_to_byte("101") == 0b10100000
    True
    """
    return sum([int(bits[pos]) << (7 - pos)
                for pos in range(len(bits))])


# ====================
# Functions for compression


def make_freq_dict(text):
    """ Return a dictionary that maps each byte in text to its frequency.

    @param bytes text: a bytes object
    @rtype: dict{int,int}

    >>> d = make_freq_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    """
    freq_dict = {}
    for i in text:
        if i not in freq_dict:
            freq_dict[i] = 1
        else:
            freq_dict[i] += 1
    return freq_dict


def huffman_tree(freq_dict):
    """ Return the root HuffmanNode of a Huffman tree corresponding
    to frequency dictionary freq_dict.

    @param dict(int,int) freq_dict: a frequency dictionary
    @rtype: HuffmanNode

    >>> freq = {2: 6, 3: 4}
    >>> t = huffman_tree(freq)
    >>> result1 = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> result2 = HuffmanNode(None, HuffmanNode(2), HuffmanNode(3))
    >>> t == result1 or t == result2
    True
    """
    nodes_freq = [(HuffmanNode(x), freq_dict[x]) for x in freq_dict]
    if len(nodes_freq) == 1:
        return HuffmanNode(None, HuffmanNode("dummy node"), nodes_freq[0][0])
    else:
        while len(nodes_freq) > 1:
            tup_1 = min(nodes_freq, key=lambda t: t[1])
            nodes_freq.remove(tup_1)
            tup_2 = min(nodes_freq, key=lambda t: t[1])
            nodes_freq.remove(tup_2)
            nodes_freq.append((HuffmanNode(None, tup_1[0], tup_2[0]),
                               tup_1[1] + tup_2[1]))
        return nodes_freq[0][0]


def get_codes(tree):
    """ Return a dict mapping symbols from tree rooted at HuffmanNode to codes.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: dict(int,str)

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    >>> tree = HuffmanNode(None, HuffmanNode(None, HuffmanNode(1), HuffmanNode(2)), HuffmanNode(None, HuffmanNode(3), HuffmanNode(4)))
    >>> d = get_codes(tree)
    >>> d == {1 : "00", 2: "01", 3:"10", 4:"11"}
    True
    """
    # helper function: code_input
    def code_input(dict_, i):
        """Return a dictionary with all key values concatenated with string i

        @param dict(int, str) dict_: a dictionary to update
        @param str i: the code to input
        @rtype: dict(int, str)
        """
        for key in dict_:
            dict_[key] = i + dict_[key]
        return dict_

    code_dict = {}
    if tree is not None and tree.left.is_leaf() and tree.right.is_leaf():
        if tree.left.symbol != "dummy node":
            code_dict[tree.left.symbol] = "0"
        code_dict[tree.right.symbol] = "1"
        return code_dict
    elif tree is not None and tree.left.is_leaf():
        code_dict[tree.left.symbol] = "0"
        code_dict.update(code_input(get_codes(tree.right), "1"))
        return code_dict
    elif tree is not None and tree.right.is_leaf():
        code_dict[tree.right.symbol] = "1"
        code_dict.update(code_input(get_codes(tree.left), "0"))
        return code_dict
    else:
        code_dict.update(code_input(get_codes(tree.left), "0"))
        code_dict.update(code_input(get_codes(tree.right), "1"))
        return code_dict


def number_nodes(tree):
    """ Number internal nodes in tree according to postorder traversal;
    start numbering at 0.

    @param HuffmanNode tree:  a Huffman tree rooted at node 'tree'
    @rtype: NoneType

    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(None, HuffmanNode(9), HuffmanNode(10))
    >>> tree = HuffmanNode(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    def list_of_nodes(tree):
        """Return a list of internal nodes in postorder traversal

        @param HuffmanNode tree: a tree to traverse
        @rtype: list

        >>> t = HuffmanNode(None, HuffmanNode(6), HuffmanNode(7))
        >>> list_of_nodes(t) == [t]
        True
        >>> t = HuffmanNode(None, HuffmanNode(8), HuffmanNode(None, HuffmanNode(5), HuffmanNode(6)))
        >>> list_of_nodes(t) == [HuffmanNode(None, HuffmanNode(5), HuffmanNode(6)), HuffmanNode(None, HuffmanNode(8), HuffmanNode(None, HuffmanNode(5), HuffmanNode(6)))]
        True
        """
        list_ = []
        if tree.left.is_leaf() and tree.right.is_leaf():
            list_.append(tree)
            return list_
        elif tree.left.is_leaf():
            list_.extend(list_of_nodes(tree.right))
            list_.append(tree)
            return list_
        elif tree.right.is_leaf():
            list_.extend(list_of_nodes(tree.left))
            list_.append(tree)
            return list_
        else:
            list_.extend(list_of_nodes(tree.left))
            list_.extend(list_of_nodes(tree.right))
            list_.append(tree)
            return list_

    internal_nodes = list_of_nodes(tree)
    for i in range(len(internal_nodes)):
        node = internal_nodes[i]
        node.number = i


def avg_length(tree, freq_dict):
    """ Return the number of bits per symbol required to compress text
    made of the symbols and frequencies in freq_dict, using the Huffman tree.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @param dict(int,int) freq_dict: frequency dictionary
    @rtype: float

    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(9)
    >>> tree = HuffmanNode(None, left, right)
    >>> avg_length(tree, freq)
    1.9
    """

    dict_ = get_codes(tree)
    total = 0
    for key in dict_:
        total += len(dict_[key]) * freq_dict[key]
    return total / sum([freq_dict[x] for x in freq_dict])


def generate_compressed(text, codes):
    """ Return compressed form of text, using mapping in codes for each symbol.

    @param bytes text: a bytes object
    @param dict(int,str) codes: mappings from symbols to codes
    @rtype: bytes

    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0])
    >>> result = generate_compressed(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> result = generate_compressed(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    """

    def cut(bits):
        """Return a list of strings which represent bytes.

        @param str bits: A string representation of bits
        @rtype: list

        >>> cut("00000000")
        ['00000000']
        >>> cut("101110011")
        ['10111001', '1']
        """

        if len(bits) <= 8:
            return [bits]
        else:
            list_ = [bits[:8]]
            list_.extend(cut(bits[8:]))
        return list_

    string = ""
    comp_byte = bytes([])
    for by in text:
        string += codes[by]
    list_ = cut(string)
    for i in list_:
        comp_byte += bytes([bits_to_byte(i)])
    return comp_byte


def tree_to_bytes(tree):
    """ Return a bytes representation of the tree rooted at tree.

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: bytes

    The representation should be based on the postorder traversal of tree
    internal nodes, starting from 0.
    Precondition: tree has its nodes numbered.

    >>> tree = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanNode(None, HuffmanNode(3), HuffmanNode(2))
    >>> right = HuffmanNode(5)
    >>> tree = HuffmanNode(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    """

    if tree.left.symbol == "dummy node":
        return bytes([0, tree.right.symbol])
    else:
        if tree.left.is_leaf() and tree.right.is_leaf():
            return bytes([0, tree.left.symbol, 0, tree.right.symbol])
        elif tree.left.is_leaf():
            right = tree_to_bytes(tree.right)
            full = right + bytes([0, tree.left.symbol, 1, tree.right.number])
            return full
        elif tree.right.is_leaf():
            left = tree_to_bytes(tree.left)
            full = left + bytes([1, tree.left.number, 0, tree.right.symbol])
            return full
        else:
            left = tree_to_bytes(tree.left)
            right = tree_to_bytes(tree.right)
            full = left + right + bytes([1, tree.left.number, 1, tree.right.number])
            return full


def num_nodes_to_bytes(tree):
    """ Return number of nodes required to represent tree (the root of a
    numbered Huffman tree).

    @param HuffmanNode tree: a Huffman tree rooted at node 'tree'
    @rtype: bytes
    """
    return bytes([tree.number + 1])


def size_to_bytes(size):
    """ Return the size as a bytes object.

    @param int size: a 32-bit integer that we want to convert to bytes
    @rtype: bytes

    >>> list(size_to_bytes(300))
    [44, 1, 0, 0]
    """
    # little-endian representation of 32-bit (4-byte)
    # int size
    return size.to_bytes(4, "little")


def compress(in_file, out_file):
    """ Compress contents of in_file and store results in out_file.

    @param str in_file: input file whose contents we want to compress
    @param str out_file: output file, where we store our compressed result
    @rtype: NoneType
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = make_freq_dict(text)
    tree = huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (num_nodes_to_bytes(tree) + tree_to_bytes(tree) +
              size_to_bytes(len(text)))
    result += generate_compressed(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)


# ====================
# Functions for decompression


def generate_tree_general(node_lst, root_index):
    """ Return the root of the Huffman tree corresponding
    to node_lst[root_index].

    The function assumes nothing about the order of the nodes in the list.

    @param list[ReadNode] node_lst: a list of ReadNode objects
    @param int root_index: index in the node list
    @rtype: HuffmanNode

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanNode(None, HuffmanNode(None, HuffmanNode(10, None, None), HuffmanNode(12, None, None)), HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None)))
    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), ReadNode(1, 1, 1, 3), ReadNode(0, 6, 1, 0)]
    >>> t = generate_tree_general(lst, 2)
    >>> t == HuffmanNode(None, HuffmanNode(None, HuffmanNode(10), HuffmanNode(12)), HuffmanNode(None, HuffmanNode(6), HuffmanNode(None, HuffmanNode(5), HuffmanNode(7))))
    True
    """

    def generate_huffman(note):
        """ Return a new tree based on the given ReadNode node.

        @param ReadNode note: a given ReadNode
        @rtype: HuffmanNode

        >>> t = generate_huffman(ReadNode(0, 5, 0, 7))
        >>> t
        HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None))
        >>> t = generate_huffman(ReadNode(1, 1, 1, 0))
        >>> t
        HuffmanNode(None, HuffmanNode(None, None, None), HuffmanNode(None, None, None))
        >>> t.left.number
        1
        >>> t.right.number
        0
        """

        if note.l_type == 0 and note.r_type == 0:
            return HuffmanNode(None, HuffmanNode(note.l_data),
                               HuffmanNode(note.r_data))
        elif note.l_type == 0 and note.r_type == 1:
            k = HuffmanNode(None, HuffmanNode(note.l_data), HuffmanNode())
            k.right.number = note.r_data
            return k
        elif note.l_type == 1 and note.r_type == 0:
            k = HuffmanNode(None, HuffmanNode(), HuffmanNode(note.r_data))
            k.left.number = note.l_data
            return k
        else:
            k = HuffmanNode(None, HuffmanNode(), HuffmanNode())
            k.left.number, k.right.number = note.l_data, note.r_data
            return k

    def combine_trees(trees_, index):
        """ Return a new tree based on the list of frame trees and take the
        HuffmanNode tree at int index as the root tree.

        @param list[HuffmanNode] trees_:
        @param int index:
        @rtype: HuffmanNode

        >>> t = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), ReadNode(1, 1, 1, 0)]
        >>> huff_list = [generate_huffman(x) for x in t]
        >>> a = combine_trees(huff_list, 2)
        >>> a == HuffmanNode(None, HuffmanNode(None, HuffmanNode(10, None, None), HuffmanNode(12, None, None)), HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None)))
        True
        >>> a.left.number
        1
        >>> a.right.number
        0
        >>> combine_trees(huff_list, 0)
        HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None))
        """

        root = trees_[index]
        if root.left.number is None and root.right.number is None:
            return root
        elif root.left.number is None and root.right.number is not None:
            right = combine_trees(trees_, root.right.number)
            number = root.right.number
            root.right = right
            root.right.number = number
            return root
        elif root.left.number is not None and root.right.number is None:
            left = combine_trees(trees_, root.left.number)
            number = root.left.number
            root.left = left
            root.left.number = number
            return root
        else:
            left = combine_trees(trees_, root.left.number)
            num_l = root.left.number
            right = combine_trees(trees_, root.right.number)
            num_r = root.right.number
            root.left = left
            root.right = right
            root.left.number = num_l
            root.right.number = num_r
            return root

    trees = []
    for node in node_lst:
        trees.append(generate_huffman(node))
    root_tree = combine_trees(trees, root_index)

    return root_tree


def generate_tree_postorder(node_lst, root_index):
    """ Return the root of the Huffman tree corresponding
    to node_lst[root_index].

    The function assumes that the list represents a tree in postorder.

    @param list[ReadNode] node_lst: a list of ReadNode objects
    @param int root_index: index in the node list
    @rtype: HuffmanNode

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanNode(None, HuffmanNode(None, HuffmanNode(5, None, None), \
    HuffmanNode(7, None, None)), \
    HuffmanNode(None, HuffmanNode(10, None, None), HuffmanNode(12, None, None)))
    """


def generate_uncompressed(tree, text, size):
    """ Use Huffman tree to decompress size bytes from text.

    @param HuffmanNode tree: a HuffmanNode tree rooted at 'tree'
    @param bytes text: text to decompress
    @param int size: how many bytes to decompress from text.
    @rtype: bytes
    """

    def find_key(value, diction):
        """ Return the key which stores the value.

        Precondiction: All the values that are stored in the diction are unique
        values, and str value must be in the diction's values.

        @param str value:
        @param dict diction:
        @rtpe: str | int

        >>> diction = {1 : '0', 2: '1'}
        >>> find_key('0', diction)
        1
        """

        tuples = diction.items()
        for j, k in tuples:
            if value == k:
                return j

    process_bits = []
    for byte in text:
        process_bits.append(byte_to_bits(int(byte)))
    final_bits = ""
    for bit in process_bits:
        final_bits += bit
    codes_dict = get_codes(tree)
    got = 0
    re = bytes([])
    index = 0
    while got < size:
        t = ""
        while t not in codes_dict.values():
            t += final_bits[index]
            index += 1
        key = find_key(t, codes_dict)
        re += bytes([key])
        got += 1
    return re


def bytes_to_nodes(buf):
    """ Return a list of ReadNodes corresponding to the bytes in buf.

    @param bytes buf: a bytes object
    @rtype: list[ReadNode]

    >>> bytes_to_nodes(bytes([0, 1, 0, 2]))
    [ReadNode(0, 1, 0, 2)]
    """
    lst = []
    for i in range(0, len(buf), 4):
        l_type = buf[i]
        l_data = buf[i+1]
        r_type = buf[i+2]
        r_data = buf[i+3]
        lst.append(ReadNode(l_type, l_data, r_type, r_data))
    return lst


def bytes_to_size(buf):
    """ Return the size corresponding to the
    given 4-byte little-endian representation.

    @param bytes buf: a bytes object
    @rtype: int

    >>> bytes_to_size(bytes([44, 1, 0, 0]))
    300
    """
    return int.from_bytes(buf, "little")


def uncompress(in_file, out_file):
    """ Uncompress contents of in_file and store results in out_file.

    @param str in_file: input file to uncompress
    @param str out_file: output file that will hold the uncompressed results
    @rtype: NoneType
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_general(node_lst, num_nodes - 1)
        size = bytes_to_size(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(generate_uncompressed(tree, text, size))


# ====================
# Other functions

def improve_tree(tree, freq_dict):
    """ Improve the tree as much as possible, without changing its shape,
    by swapping nodes. The improvements are with respect to freq_dict.

    @param HuffmanNode tree: Huffman tree rooted at 'tree'
    @param dict(int,int) freq_dict: frequency dictionary
    @rtype: NoneType

    >>> left = HuffmanNode(None, HuffmanNode(99), HuffmanNode(100))
    >>> right = HuffmanNode(None, HuffmanNode(101), \
    HuffmanNode(None, HuffmanNode(97), HuffmanNode(98)))
    >>> tree = HuffmanNode(None, left, right)
    >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
    >>> improve_tree(tree, freq)
    >>> avg_length(tree, freq)
    2.31
    """
    # todo

if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="huffman_pyta.txt")
    # TODO: Uncomment these when you have implemented all the functions
    # import doctest
    # doctest.testmod()

    import time

    mode = input("Press c to compress or u to uncompress: ")
    if mode == "c":
        fname = input("File to compress: ")
        start = time.time()
        compress(fname, fname + ".huf")
        print("compressed {} in {} seconds."
              .format(fname, time.time() - start))
    elif mode == "u":
        fname = input("File to uncompress: ")
        start = time.time()
        uncompress(fname, fname + ".orig")
        print("uncompressed {} in {} seconds."
              .format(fname, time.time() - start))
