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
        # Create a dummy node that is either 1 less than tree.right.symbol
        # if symbol is greater than or equal to 120 else 1 more than it
        if nodes_freq[0][0].symbol >= 120:
            return HuffmanNode(None, HuffmanNode(nodes_freq[0][0].symbol - 1),
                               nodes_freq[0][0])
        else:
            return HuffmanNode(None, HuffmanNode(nodes_freq[0][0].symbol + 1),
                               nodes_freq[0][0])
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
    >>> tree = huffman_tree({5: 10})
    >>> d = get_codes(tree)
    >>> tree = huffman_tree({60: 3, 61: 3, 62: 2, 63: 1, 64: 1})
    >>> d = get_codes(tree)
    >>> d == {62: '00', 63: '010', 64: '011', 60: '10', 61: '11'}
    True
    """
    # helper function: code_input
    def code_input(dict_, i):
        """Return a dictionary with all key values concatenated with
        string i

        @param dict(int, str) dict_: a dictionary to update
        @param str i: the code to input
        @rtype: dict(int, str)
        """
        for key in dict_:
            dict_[key] = i + dict_[key]
        return dict_

    code_dict = {}
    if tree.left.is_leaf() and tree.right.is_leaf():
        code_dict[tree.left.symbol] = "0"
        code_dict[tree.right.symbol] = "1"
        return code_dict
    elif tree.left.is_leaf():
        code_dict[tree.left.symbol] = "0"
        code_dict.update(code_input(get_codes(tree.right), "1"))
        return code_dict
    elif tree.right.is_leaf():
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
    def list_of_nodes(tree_):
        """Return a list of internal nodes of tree in postorder traversal.

        @param HuffmanNode tree_: a tree to traverse
        @rtype: list

        >>> t = HuffmanNode(None, HuffmanNode(6), HuffmanNode(7))
        >>> list_of_nodes(t) == [t]
        True
        >>> t = HuffmanNode(None, HuffmanNode(8), \
        HuffmanNode(None, HuffmanNode(5), HuffmanNode(6)))
        >>> list_of_nodes(t) == [HuffmanNode(None, HuffmanNode(5), \
        HuffmanNode(6)), HuffmanNode(None, HuffmanNode(8), \
        HuffmanNode(None, HuffmanNode(5), HuffmanNode(6)))]
        True
        """
        list_ = []
        if tree_.left.is_leaf() and tree_.right.is_leaf():
            list_.append(tree_)
            return list_
        elif tree_.left.is_leaf():
            list_.extend(list_of_nodes(tree_.right))
            list_.append(tree_)
            return list_
        elif tree_.right.is_leaf():
            list_.extend(list_of_nodes(tree_.left))
            list_.append(tree_)
            return list_
        else:
            list_.extend(list_of_nodes(tree_.left))
            list_.extend(list_of_nodes(tree_.right))
            list_.append(tree_)
            return list_

    internal_nodes = list_of_nodes(tree)
    for i in range(len(internal_nodes)):
        internal_nodes[i].number = i


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
    >>> freq = make_freq_dict(bytes([5]))
    >>> tree = huffman_tree(freq)
    >>> avg_length(tree, freq)
    1.0
    """
    dict_ = get_codes(tree)
    total = 0
    for key in dict_:
        if key in freq_dict:
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
    # helper function: code_cutter
    def code_cutter(str_):
        """ Return a list of bytes from a string of bits.

        @param str str_: a bitstring to cut
        @rtype: list

        >>> code_cutter("101110011")
        [185, 128]
        >>> code_cutter("101010")
        [168]
        """
        result = []
        index = 0
        while index + 8 < len(str_):
            result.append(bits_to_byte(str_[index:index+8]))
            index += 8
        if index < len(str_):
            result.append(bits_to_byte(str_[index:]))
        return result

    bit_string = ""
    for byte in text:
        bit_string += codes[byte]
    bit_list = code_cutter(bit_string)
    comp_byte = bytes(bit_list)
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
    if tree.left.is_leaf() and tree.right.is_leaf():
        return bytes([0, tree.left.symbol, 0, tree.right.symbol])
    elif tree.left.is_leaf():
        right_byte = tree_to_bytes(tree.right)
        full_byte = right_byte + bytes(
            [0, tree.left.symbol, 1, tree.right.number])
        return full_byte
    elif tree.right.is_leaf():
        left_byte = tree_to_bytes(tree.left)
        full_byte = left_byte + bytes(
            [1, tree.left.number, 0, tree.right.symbol])
        return full_byte
    else:
        left_byte = tree_to_bytes(tree.left)
        right_byte = tree_to_bytes(tree.right)
        full_byte = left_byte + right_byte + bytes([1, tree.left.number,
                                                    1, tree.right.number])
        return full_byte


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
    HuffmanNode(None, HuffmanNode(None, HuffmanNode(10, None, None), \
    HuffmanNode(12, None, None)), \
    HuffmanNode(None, HuffmanNode(5, None, None), HuffmanNode(7, None, None)))
    """
    # helper function: generate_huffman
    def generate_huffman(r_node):
        """ Return a HuffmanNode from a ReadNode.

        @param ReadNode r_node: a ReadNode to convert
        @rtype: HuffmanNode

        >>> huff = generate_huffman(ReadNode(0, 5, 0, 7))
        >>> huff == HuffmanNode(None, HuffmanNode(5), HuffmanNode(7))
        True
        >>> huff = generate_huffman(ReadNode(1, 1, 1, 0))
        >>> huff == HuffmanNode(None, HuffmanNode(), HuffmanNode())
        True
        >>> huff.left.number
        1
        >>> huff.right.number
        0
        """
        if r_node.l_type == 0 and r_node.r_type == 0:
            return HuffmanNode(None, HuffmanNode(r_node.l_data),
                               HuffmanNode(r_node.r_data))
        elif r_node.l_type == 0 and r_node.r_type == 1:
            huff_node = HuffmanNode(None, HuffmanNode(r_node.l_data),
                                    HuffmanNode())
            huff_node.right.number = r_node.r_data
            return huff_node
        elif r_node.l_type == 1 and r_node.r_type == 0:
            huff_node = HuffmanNode(None, HuffmanNode(),
                                    HuffmanNode(r_node.r_data))
            huff_node.left.number = r_node.l_data
            return huff_node
        else:
            huff_node = HuffmanNode(None, HuffmanNode(), HuffmanNode())
            huff_node.left.number = r_node.l_data
            huff_node.right.number = r_node.r_data
            return huff_node

    # helper function: combine_tree
    def combine_tree(trees_, index):
        """ Return a new tree based on the list of frame trees and take the
        HuffmanNode tree at index as the root tree.

        @param list[HuffmanNode] trees_: a list of Huffman nodes
        @param int index: the root index
        @rtype: HuffmanNode

        >>> t = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
        ReadNode(1, 1, 1, 0)]
        >>> huff_list = [generate_huffman(x) for x in t]
        >>> a = combine_tree(huff_list, 2)
        >>> a == HuffmanNode(None, HuffmanNode(None, HuffmanNode(10), \
        HuffmanNode(12)), HuffmanNode(None, HuffmanNode(5), HuffmanNode(7)))
        True
        >>> a.left.number
        1
        >>> a.right.number
        0
        >>> t = combine_tree(huff_list, 0)
        >>> t == HuffmanNode(None, HuffmanNode(5), HuffmanNode(7))
        True
        """

        root = trees_[index]
        if root.left.number is None and root.right.number is None:
            return root
        elif root.right.number is not None and root.left.number is None:
            right = combine_tree(trees_, root.right.number)
            number = root.right.number
            root.right = right
            root.right.number = number
            return root
        elif root.left.number is not None and root.right.number is None:
            left = combine_tree(trees_, root.left.number)
            number = root.left.number
            root.left = left
            root.left.number = number
            return root
        else:
            left = combine_tree(trees_, root.left.number)
            num_l = root.left.number
            right = combine_tree(trees_, root.right.number)
            num_r = root.right.number
            root.left = left
            root.right = right
            root.left.number = num_l
            root.right.number = num_r
            return root

    huffman_list = []
    for read_node in node_lst:
        huffman_list.append(generate_huffman(read_node))
    root_tree = combine_tree(huffman_list, root_index)
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
    # helper function: generate_huffman
    def generate_huffman(r_node):
        """ Return a HuffmanNode from a ReadNode.

        @param ReadNode r_node: a ReadNode to convert
        @rtype: HuffmanNode

        >>> huff = generate_huffman(ReadNode(0, 10, 0, 12))
        >>> huff == HuffmanNode(None, HuffmanNode(10), HuffmanNode(12))
        True
        >>> huff = generate_huffman(ReadNode(1, 0, 1, 0))
        >>> huff == HuffmanNode(None, HuffmanNode(), HuffmanNode())
        True
        """
        if r_node.l_type == 0 and r_node.r_type == 0:
            return HuffmanNode(None, HuffmanNode(r_node.l_data),
                               HuffmanNode(r_node.r_data))
        elif r_node.l_type == 0 and r_node.r_type == 1:
            return HuffmanNode(None, HuffmanNode(r_node.l_data), HuffmanNode())
        elif r_node.l_type == 1 and r_node.r_type == 0:
            return HuffmanNode(None, HuffmanNode(), HuffmanNode(r_node.r_data))
        else:
            return HuffmanNode(None, HuffmanNode(), HuffmanNode())

    # helper function: count_internal
    def count_internal(t):
        """
        Return number of internal nodes in t.

        @param HuffmanNode t: a Huffman node
        @rtype: int

        >>> t = HuffmanNode(None, HuffmanNode(1), HuffmanNode(2))
        >>> count_internal(t)
        1
        >>> t2 = HuffmanNode(None, t, HuffmanNode(6))
        >>> count_internal(t2)
        2
        """
        if t.is_leaf():
            return 0
        else:
            return 1 + sum([count_internal(t.left)]) + \
                   sum([count_internal(t.right)])

    # helper function: combine_tree
    def combine_tree(trees_):
        """ Return a new tree based on the list of frame trees and take the
        HuffmanNode tree at index as the root tree.

        @param list[HuffmanNode] trees_: a list of Huffman nodes
        @rtype: HuffmanNode

        >>> lst = [ReadNode(0, 5, 0, 7)]
        >>> lst_ = [generate_huffman(x) for x in lst]
        >>> combine_tree(lst_)
        HuffmanNode(None, HuffmanNode(5, None, None), \
        HuffmanNode(7, None, None))
        >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 2, 0, 3), \
        ReadNode(1, 0, 1, 0)]
        >>> lst_ = [generate_huffman(x) for x in lst]
        >>> t = combine_tree(lst_)
        >>> t == HuffmanNode(None, HuffmanNode(None, HuffmanNode(5), \
        HuffmanNode(7)), HuffmanNode(None, HuffmanNode(2), HuffmanNode(3)))
        True
        """
        root = trees_[- 1]
        if root.left.symbol is not None and root.right.symbol is not None:
            return root
        elif root.right.symbol is None and root.left.symbol is None:
            root.right = combine_tree(trees_[:-1])
            i = count_internal(root)
            root.left = combine_tree(trees_[:-i])
            return root
        elif root.right.symbol is None:
            root.right = combine_tree(trees_[:-1])
            return root
        elif root.left.symbol is None:
            root.left = combine_tree(trees_[:-1])
            return root

    huffman_list = []
    for node in node_lst:
        huffman_list.append(generate_huffman(node))
    root_tree = combine_tree(huffman_list[:root_index + 1])
    return root_tree


def generate_uncompressed(tree, text, size):
    """ Use Huffman tree to decompress size bytes from text.

    @param HuffmanNode tree: a HuffmanNode tree rooted at 'tree'
    @param bytes text: text to decompress
    @param int size: how many bytes to decompress from text.
    @rtype: bytes
    """
    # helper function: switch_dict
    def switch_dict(dict_):
        """ Return a dictionary where key and values are swapped.

        Precondiction: All the values are unique and are not mutable.

        @param dict dict_: a dictionary to swap
        @rtpe: dict

        >>> diction = {1 : '0', 2: '1'}
        >>> switch_dict(diction) == {'0': 1, '1': 2}
        True
        """
        swap_dict = {}
        for k, v in dict_.items():
            swap_dict[v] = k
        return swap_dict

    # helper function: get_bytes
    def get_bytes(text_, dict_, size_):
        """ Return a list, of length less than size_, of bytes from text_.

        @param bytes text_: text to decompress
        @param dict(str, int) dict_: a dictionary of codes to bytes
        @param int size_: how many bytes to decompress from text.
        @rtype: list
        """
        cur_bits = ""
        byte_list = []
        for byte in text_:
            cur_bits += byte_to_bits(byte)
            index = 1
            while index <= len(cur_bits) and len(byte_list) < size_:
                if cur_bits[0:index] in dict_:
                    byte_list.append(dict_[cur_bits[0:index]])
                    cur_bits = cur_bits[index:]
                    index = 1
                else:
                    index += 1
        return byte_list

    key = get_codes(tree)
    code_to_byte = switch_dict(key)
    return bytes(get_bytes(text, code_to_byte, size))


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
    # helper function: make_order
    def make_order(dict_):
        """ Return the keys of dict_ into a list in which the order depends
        on their value from largest to smallest.

        @param dict(int,int) dict_: a dictionary to order
        @rtype: list

        >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
        >>> make_order(freq)
        [97, 98, 99, 100, 101]
        """

        tupe_list = []
        for j, k in dict_.items():
            tupe_list.append((j, k))
        # Sort this list of tuple based on the index 1 value from
        # largest to smallest
        sorted_tuples = sorted(tupe_list, key=lambda value: value[1])
        ready = sorted_tuples[::-1]
        result = []
        for w, _ in ready:
            result.append(w)
        return result

    # helper function: levelorder_visit
    def levelorder_visit(tree_):
        """
        Return the list of leaves from HuffmanNode tree in levelorder traversal.

        @param HuffmanNode|None tree_: binary tree to visit
        @rtype: list

        >>> tree = HuffmanNode(None, HuffmanNode(5), \
        HuffmanNode(None, HuffmanNode(4), HuffmanNode(9)))
        >>> list_ = levelorder_visit(tree)
        >>> list_ == [HuffmanNode(5), HuffmanNode(4), HuffmanNode(9)]
        True
        """

        nodes = []
        result = []
        nodes.append(tree_)
        while len(nodes) != 0:
            next_node = nodes.pop(0)
            if next_node.symbol:
                result.append(next_node)
            if next_node.left:
                nodes.append(next_node.left)
            if next_node.right:
                nodes.append(next_node.right)
        return result

    order = make_order(freq_dict)
    modify = levelorder_visit(tree)
    for i in range(len(modify)):
        modify[i].symbol = order[i]

if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config="huffman_pyta.txt")
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
