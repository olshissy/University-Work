from bitarray import bitarray
import sys


def lz77_compression(string):
    """
    The LZ77 string compression algorithm 

    :param string: the string to be compressed
    :return: A list of compressed tuples of the form (length, offset, next char)
    """
   
    search_window = 0 #Search window starts at the start of the string 
    compressed = []

    #Loop until the search window reaches the end of the string 
    while search_window < len(string):

        match_length = 0
        match_offset = 0

        #Loop over the current search window 
        for j in range(search_window): 
            k = 0

            #Continue the search outside of the search window to find the longest match
            while search_window + k < len(string) and string[j + k] == string[search_window + k]:
                k += 1

                #If this exceeds the current match length 
                if k > match_length:

                    #Update the match length and match offset values 
                    match_length = k
                    match_offset = search_window - j

        #Find the next character in the string
        next_char = string[search_window + match_length] if search_window + match_length < len(string) else ''
        
        #Append the tuple to the compressed list 
        compressed.append((match_offset, match_length, next_char))

        #Increment the search window end based on the found match length 
        search_window += match_length + 1

    return compressed



class Node:
    """
    A class representing a huffman tree node 
    """
    
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None



def build_huffman_tree(frequencies):
    """
    Builds the huffman tree for a sequence of characters

    :param frequencies: a dictionary of characters and their frequencies
    :return: the root node of the huffman tree 
    """
   
    frequency_items = list(frequencies.items())

    #Create a list of nodes for each character
    nodes = [Node(char, freq) for char, freq in frequency_items]

    #Combine the nodes until only one tree remains
    while len(nodes) > 1:
        #Sort based on frequency
        nodes.sort(key=lambda x: x.freq)

        #Pick the two least frequent nodes 
        left = nodes.pop(0)
        right = nodes.pop(0)

        #New node created with two nodes as children 
        merged_node = Node(None, left.freq + right.freq)
        merged_node.left = left
        merged_node.right = right

        #Add the new node to the list of nodes
        nodes.append(merged_node)

    #The final node is the root of the tree 
    return nodes[0]



def generate_huffman_codes(root, current_code, codes):
    """
    Generates the huffman codes for characters from a huffman tree

    :param root: the root node of the huffman tree
    :param current_code: the current code for the character
    :param codes: a dictionary of the codes of each character in the tree 
    """
    
    #If the tree is invalid stop the function
    if root is None:
        return 
    
    #If the character exists, add that character's code to the codes list 
    if root.char is not None:
        codes[root.char] = current_code

    #Traverse the left of the tree and add a 0 to the code
    generate_huffman_codes(root.left, current_code + '0', codes)

    #Traverse the right of the tree and add a 1 to the code 
    generate_huffman_codes(root.right, current_code + '1', codes)



def calculate_frequencies(string):
    """
    Calculates the frequencies of each character and total characters in a string

    :param string: the string being checked
    :return frequency: the frequencies of each character in the string
    :return total_chars: the total number of characters in the string 
    """
    
    frequency = {}
    total_chars = 0

    #Loop over the string
    for char in string:
        #Increment total chars 
        total_chars += 1
        
        #If the character already exists in dict, increment freq
        if char in frequency:
            frequency[char] += 1
        
        #Otherwise, add the character to dict with freq of 1
        else:
            frequency[char] = 1
    
    return frequency, total_chars



def elias_integer_encode(number):
    """
    Provides the elias encoding for non-negative integers

    :param number: the number to be encoded
    :return: the elias encoding of the non-negative integer
    """

    #For the non-negative integer elias encoding
    number += 1
    
    binary_num = bin(number)[2:] #Remove '0b' prefix
    code = binary_num

    #Loop until the final length encoding is reached 
    while number > 1:
        #New number is the length of the previous minus 1
        number = len(binary_num) - 1

        #Obtain the binary of this length and replace the MSB with 0
        binary_num = bin(number)[2:]
        binary_num = '0' + binary_num[1:]
        
        #Add to the current code 
        code = binary_num + code

    return code



def to_8bit_binary(num):
    """
    Gets the 8-bit binary code for a number 

    :return: the 8-bit binary for a number
    """
    
    return format(num & 0xFF, '08b')



def generate_file_data(input_file):
    """
    Generates the bitstream to be output to the binary file 

    :param input_file: the file containing the required data 
    """

    with open(input_file, 'r') as input:
        file_content = input.read()

    # Obtain the LZ77 compressed data (you should implement this function)
    lz77_compressed = lz77_compression(file_content)

    # Calculate the frequencies for Huffman encoding (you should implement this function)
    frequencies, file_size = calculate_frequencies(file_content)

    # Build the Huffman tree and generate the codes (you should implement this function)
    root = build_huffman_tree(frequencies)
    huffman_codes = {}
    generate_huffman_codes(root, '', huffman_codes)
    codes = list(huffman_codes.items())
    codes = sorted(codes, key=lambda x: ord(x[0]))

    # Prepare the header as a bitarray
    header = bitarray()

    # Encode the file size using Elias encoding
    file_size_encoded = elias_integer_encode(file_size)
    header.extend(file_size_encoded)

    # Encode the filename length and filename
    filename_length = len(input_file)
    filename_length_encoded = elias_integer_encode(filename_length)
    header.extend(filename_length_encoded)
    for char in input_file:
        ascii_code = to_8bit_binary(ord(char))
        header.extend(ascii_code)

    # Encode Huffman table
    unique_chars = len(frequencies)
    unique_chars_encoded = elias_integer_encode(unique_chars)
    header.extend(unique_chars_encoded)
    for char, code in codes:
        #Encode the ascii value for each character
        ascii_code = to_8bit_binary(ord(char))
        header.extend(ascii_code)

        #Encode the length of the Huffman code for each character 
        len_code_encoded = elias_integer_encode(len(code))
        header.extend(len_code_encoded)

        #Encode the Huffman code of each character 
        header.extend(code)

    # Prepare the LZ77 data as a bitarray
    lz77_data = bitarray()
    for offset, length, next_char in lz77_compressed:
        lz77_data.extend(elias_integer_encode(offset))
        lz77_data.extend(elias_integer_encode(length))
        lz77_data.extend(huffman_codes[next_char])

    # Combine header and lz77 data into a single bitstream
    final_bitstream = header + lz77_data

    # Padding to make it a multiple of 8 bits
    padding = (8 - len(final_bitstream) % 8) % 8
    if padding > 0:
        final_bitstream.extend('0' * padding)

    # Generate the output filename
    output_filename = input_file + '.bin'

    #Write bitstream to a file 
    with open(output_filename, 'wb') as output_file:
        final_bitstream.tofile(output_file)



# if __name__ == "__main__":
#     input_file = sys.argv[1]

#     generate_file_data(input_file)
