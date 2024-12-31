import sys

global_end = -1

def read_file(file_path: str) -> str:
    """
    Function used to read files and extract the contents of them 

    :param file_path: file path 
    :return: file contents
    """
    f = open(file_path, 'r')
    line = f.readline()
    f.close()
    return line



def output_file(outputs: list, output_file: str) -> None:
    """
    Function used to write output to a file 

    :param outputs: output results as a list 
    :param output_file: output file path 
    :return: None
    """
    f = open(output_file, "w")
    for item in outputs:
        f.write(f"{item}\n")
    f.close()



class Node:
    def __init__(self, start, end=None, is_leaf = False):
        """
        Constructor method for a node in the suffix tree

        :param start: Start index of the edge label for the node 
        :param end: End index of the edge label for the node 
        :is_leaf: Boolean indicating whether the node is a leaf
        """
        self.children = {}
        self.start = start
        self.end = end 
        self.suffix_link = None
        self.is_leaf = is_leaf



    def edge_length(self, position):
        """
        Calculate the length of the edge label from this node to its child

        :param position: Current position in the input text
        :return: Length of the edge label 
        """
        if self.end is None:
            return position + 1 - self.start
        return self.end - self.start
    


    def __getattribute__(self, name) :
        """
        Override to return the global end value for leaf nodes when accessing the end attribute 
        """
        if name == "end" and self.is_leaf:
            return global_end
        return super(Node, self).__getattribute__(name)


class SuffixTree:
    def __init__(self, text):
        """
        Constructor for the suffix tree which is built using Ukkonen's algorithm

        :param text: The input string for which the suffix tree is being built
        """
        self.text = text
        self.root = Node(None, None)
        self.root.suffix_link = self.root
        
        #Variables for tree generation
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remainder = 0
        self.position = -1
        self.last_new_node = None
        
        self.build_tree()



    def build_tree(self):
        """
        Build the suffix tree by extending it one character at a time 
        """
        for i in range(len(self.text)):
            self.extend_suffix_tree(i)



    def extend_suffix_tree(self, pos):
        """
        Extend the suffix tree by adding a new character at position 'pos'

        :param pos: Current position of the input string 
        """
        global global_end
        global_end += 1
        self.position = pos
        self.remainder += 1
        self.last_new_node = None

        #While there are still suffixes to add 
        while self.remainder > 0:
            #If no edge is set, set the active edge to the current character
            if self.active_length == 0:
                self.active_edge = pos

            #If there is no edge that currently starts with the current character
            if self.text[self.active_edge] not in self.active_node.children:
                # Rule 2 - new leaf node 
                self.active_node.children[self.text[self.active_edge]] = Node(pos, None, is_leaf=True)

                #If a new internal node was created previously, set the active node as its suffix link
                if self.last_new_node is not None:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None #Reset for next iteration
            
            #If the character exists on an edge 
            else:
                #Retrieves the child node corresponding to the matching edge 
                next_node = self.active_node.children[self.text[self.active_edge]]
                
                #Checks if need to move down the edge, if true continue without further processing (skip count)
                if self.skip_count(next_node):
                    continue
                
                #Rule 3 - No further action is required 
                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    
                    #If there was a previously created node, set the suffix link
                    if self.last_new_node is not None and self.active_node != self.root:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None

                    self.active_length += 1
                    break #Showstopper rule 
                
                #Position where the edge should be split
                split_end = next_node.start + self.active_length
                
                #New internal node representing the split
                split_node = Node(next_node.start, split_end)
                
                #Set the current active node's child to point to this new split node
                self.active_node.children[self.text[self.active_edge]] = split_node
                
                #Create a new leaf node representing the remainder of the string 
                split_node.children[self.text[pos]] = Node(pos, None, is_leaf=True)
                
                #Update the start of the original edge to the split point 
                next_node.start = split_end
                
                #Link the split node to the original node 
                split_node.children[self.text[split_end]] = next_node

                #If there was a previously created node, set its suffix link to the new split node
                if self.last_new_node is not None:
                    self.last_new_node.suffix_link = split_node

                #Set the last new node to the newly created node for suffix link setting in the next iteration
                self.last_new_node = split_node

            self.remainder -= 1 #Suffix has been successfully addded to the tree

            #If the active node is the root, decrement active length and adjust the active edge 
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remainder + 1
            
            #Follow the suffix link if there is one available
            elif self.active_node.suffix_link is not None:
                self.active_node = self.active_node.suffix_link
            
            #If no suffix link is available, reset the active node to the root
            else:
                self.active_node = self.root



    def skip_count(self, next_node):
        """
        Perform the skip count optimisation for Ukkonen's algorithm 

        :param next_node: the next node in the tree
        :return: Boolean indicating if the skip count succeeded 
        """
        #If the active length exceeds or matches the edge length, move to the next node
        if self.active_length >= next_node.edge_length(self.position):
            
            #Moves the active edge forward by the length of edge, skipping over characters
            self.active_edge += next_node.edge_length(self.position)
            
            #Decreases active length by length of the edge, reducing number of characters to be processed
            self.active_length -= next_node.edge_length(self.position)

            #Sets active node to next node, completing the skip over 
            self.active_node = next_node
            return True
        return False
    


    def dfs_suffix_array(self, current_node, label_length, suffix_array):
        """
        Perform a depth first search to generate a suffix array

        :param current_node: Current node in the suffix tree
        :param label_length: Current length of the string label
        :param suffix_array: The suffix array being constructed 
        """
        #If a leaf is reached, store the start of the current suffix in the suffix array
        if current_node.is_leaf:
            suffix_array.append(self.position - label_length)
            return
        
        #Traverse all children of the node in lexicographical order
        for child in sorted(current_node.children.keys()):
            child_node = current_node.children[child]
            edge_len = child_node.edge_length(self.position) #length of the edge label for the current child
            self.dfs_suffix_array(child_node, label_length + edge_len, suffix_array)



    def build_suffix_array(self):
        """
        Build the suffix array by traversing the suffix tree

        :return: The constructed suffix array 
        """
        suffix_array = []

        #Start the tree traversal from the root
        self.dfs_suffix_array(self.root, 0, suffix_array)

        return suffix_array


def get_bwt(string):
    """
    Generate the BWT for the input string

    :param string: Input string 
    :return: The constructed BWT and suffix array of the string 
    """
    n = len(string)

    #Generate the suffix array using Ukkonen's algorithm 
    suffix_tree = SuffixTree(string)
    suffix_array = suffix_tree.build_suffix_array()
    
    
    bwt = [''] * n

    #Iterate through the suffix array
    for i in range(n):
        #Find the character before the start of the current suffix
        j = suffix_array[i] - 1
        
        #If j is negative, wrap around to the last character
        if j < 0:
            j = n - 1
        
        #Add character to the BWT
        bwt[i] = string[j]

    #Return the joined array and the generated suffix array
    return ''.join(bwt), suffix_array



def get_ranks(array):
    """
    Generate a dictionary containing the first occurrence of characters in the array

    :param array: Array of characters
    :return: Dictionary with the first occurrence rank of each character
    """
    #Define a dictionary to store the first occurrence of each character
    ranks = {}
    
    for i, char in enumerate(array):
        #If the character does not already exist in the dict, add it with its first occurrence
        if char not in ranks:
            ranks[char] = i

    return ranks



def get_no_occurrences(ranks, string):
    """
    Calculate the running count of occurrences for each character in the string

    :param ranks: Dictionary of first occurrence ranks for each character
    :param string: BWT string 
    :return: List of dictionaries representing the occurrence count up to each position
    """
    no_occurences = [] #List to store the running count 
    count = {char: 0 for char in ranks.keys()} #Initialise the count of each character to 0
    
    #Iterate through the BWT
    for char in string:
        #Increment the count of the current character
        count[char] += 1 

        #Append a copy of the current count dictionary to the list 
        no_occurences.append(count.copy()) 

    return no_occurences



def bwt_pattern_matching(string, pat):
    """
    Function to do pattern matching using BWTs with the wildcard character '!' that can act as any character

    :param string: the input string to search for the pattern 
    :param pat: the pattern to search for 
    :return: A list of starting indices of all matches in the text
    """

    #Get the BWT and suffix array of the string
    bwt, suffix_array = get_bwt(string)

    #Find the first column of the suffix array by sorting the BWT
    first_column = sorted(bwt)

    #Get the ranks and number of occurrences of each character in the string 
    ranks = get_ranks(first_column)
    no_occurrences = get_no_occurrences(ranks, bwt)

    #Start matching the pattern from the last character to the first character
    return check_match(bwt, suffix_array, ranks, no_occurrences, pat, len(pat) - 1, 0, len(string) - 1)



def check_match(bwt, suffix_array, ranks, no_occurrences, pat, pat_idx, sp, ep):
    """
    Recursively check for matches of the pattern in the BWT

    :param bwt: the BWT of the input string
    :param suffix_array: the suffix array of the input string
    :param ranks: the ranks of the characters in the first column of the BWT
    :param no_occurrences: a 2D array containing the number of occurrences of each character up to an index 
    :param pat: the pattern to search for 
    :param pat_idx: the index of the current character in the pattern
    :param sp: the start position in the BWT for the current search
    :param ep: the end position in the BWT for the current search
    """

    #Base case: If all characters in the pattern have been exhausted 
    if pat_idx < 0:
        #Return the suffix array indices corresponding to the current range 
        return [suffix_array[i] for i in range(sp, ep + 1)]

    current_char = pat[pat_idx]

    if current_char == '!':
        matches = []

        #Iterate through all characters in ranks 
        for char in ranks:
            #Calculate the sp and ep values for this character
            new_sp = ranks[char] + (no_occurrences[sp - 1][char] if sp > 0 else 0)
            new_ep = ranks[char] + (no_occurrences[ep][char] - 1)

            #If the new range is valid, continue recursive search 
            if new_sp <= new_ep:
                matches.extend(check_match(bwt, suffix_array, ranks, no_occurrences, pat, pat_idx - 1, new_sp, new_ep))
       
        return sorted(matches)
    
    else:

        #If the character is not in ranks, the pattern does not match 
        if current_char not in ranks:
            return []

        #Calculate sp and ep values of the current character 
        sp = ranks[current_char] + (no_occurrences[sp - 1][current_char] if sp > 0 else 0)
        ep = ranks[current_char] + (no_occurrences[ep][current_char] - 1)

        #If the new range is invalid, no match
        if sp > ep:
            return []
        
        #Recursively search the next character in pattern 
        return check_match(bwt, suffix_array, ranks, no_occurrences, pat, pat_idx - 1, sp, ep)


if __name__ == "__main__":
    _, filename1, filename2 = sys.argv
    txt = read_file(filename1)
    pat = read_file(filename2)
    matches = bwt_pattern_matching(txt, pat)
    output_file(matches, "output_a2q1.txt")

