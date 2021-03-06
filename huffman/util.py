import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    # Set pointer to beginning of stream
    try:
        tree_stream.seek(0)
        tree = pickle.load(tree_stream)
        return tree
    
    # Exception if the Huffmann Tree description is invalid
    except EOFError:
        print("Invalid Huffman Tree")
        return NONE


def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    # Set node to tree root node
    node = tree
    
    # In C, used to check if right and left child nodes were NULL
    # But we can just use the isinstance function to check that
    # Use Paul's preorder function example as guideline here
    
    # Read the Huffmann tree till a leaf node is reached
    while isinstance(node, huffman.TreeLeaf) == False: 
        try:
            current_bit = bitreader.readbit()
        
        # Exception if EOF arrives in file before reaching EOF leaf in HUFFMANN
        # Manually ensure that None is returned
        except EOFError:
            return None
             
        if current_bit == 1:
            node = node.getRight()
        else:
            node = node.getLeft()
    return node.getValue()


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    tree_root = read_tree(compressed)
    # Cannot decompress if there is no valid tree
    if tree_root == None:
        return
        
    # Pointer is shifted to the start of the binary file in compressed
    my_bit_reader = bitio.BitReader(compressed)
    my_bit_writer = bitio.BitWriter(uncompressed)
    
    
    value = decode_byte(tree_root, my_bit_reader)
    
    # For EOFError, our tree leaf stores None
    # Will keep on doing this till we get to the None TreeLeaf i.e. end of file
    while value != None:
        # Each value is written using a 8 bit binary number
        my_bit_writer.writebits(value, 8)
        value = decode_byte(tree_root, my_bit_reader)
    
    # Always flush after using writebits
    my_bit_writer.flush()
    return


def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    pickle.dump(tree, tree_stream)
    return

def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    my_bit_writer = bitio.BitWriter(compressed)
    write_tree(tree, compressed)
    my_bit_reader = bitio.BitReader(uncompressed)
    
    table = huffman.make_encoding_table(tree)
    
    end_of_file = False
    while end_of_file != True:
        try:
            byte = my_bit_reader.readbits(8)
            for item in table[byte]:
                my_bit_writer.writebit(item)
        
        except EOFError:
            end_of_file = True
            for item in table[None]:
                my_bit_writer.writebit(item)
    
    my_bit_writer.flush()
    return
