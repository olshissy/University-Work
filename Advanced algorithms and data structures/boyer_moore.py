from copy import copy 
import sys

NO_OF_CHARS = 90

def get_char_index(char: str) -> int:
    """
    Function to get the index of a string character - ASCII [37, 126] (printable characters)
    
    Time complexity: O(1)

    :param char: character that's index needs to be found
    :return: index of the character
    """
    return ord(char) - 37



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



def z_algorithm(txt: str) -> list[int]:
    """
    Gusfield's Z algorithm implementation used to find Z values at each index of a string
    Time complexity: O(n) where n is the length of the input string

    :param txt: String used to find the Z values
    :return: Array containing the Z values of the input string 
    """

    #Variable declaration
    n = len(txt)
    z_array = [0] * n
    left = 0
    right = 0

    def comparison(start, end):
        """
        Function used to compare a string to a substring until there is no longer a match

        :param start: index where matching starts
        :param end: index where matching ends
        :return: None
        """
        while end < n and txt[end-start] == txt[end]:
            end += 1
        z_array[k] = end - start
        end -= 1

    #Find Z values from Z1 as Z0 is not useful information
    for k in range(1,n):
        
        #Case 1 
        if k > right: 
            left, right = k, k
            comparison(left, right)

        #Case 2 
        else:
            index = k - left

            #Case 2a
            if z_array[index] < right - k: 
                z_array[k] = z_array[index]
            
            #Case 2b
            else: 
                left = k
                comparison(left, right)
    
    return z_array



def extended_bad_character(pattern: str) -> list[list[int]]:
    """
    Function that implements the extended bad character used to find the rightmost occurrence of the bad character in the pattern to the left of the mismatch
    
    Time complexity: O(|A| * m) where |A| is the size of the alphabet and m is the length of the pattern 

    :param pattern: the pattern that is being processed
    :return: the Rk(x) matrix
    """
    bad_char_table = [[-1] * NO_OF_CHARS] 

    for i in range(1, len(pattern)):
        #Copies the previous row to maintain the values that will not be changed here
        previous_row = copy(bad_char_table[i-1]) 

        #Updates the table to reflect the last occurrence of the character up to the previous index
        previous_row[get_char_index(pattern[i-1])] = i - 1 
        
        #Appends this to the table
        bad_char_table.append(previous_row)

    return bad_char_table



def stricter_good_suffix(pattern: str):
    """
    This function is the a stricter good suffix rule, where instead of storing
    the rightmost occurence of a good suffix, we store all good suffixes in a 2D array.
    Each list entry corresponds to a potential mismatch position, with index being the preceding
    character of the good suffix. The array is initialised as -1 for all characters, except the final 
    entry which is intialised to 0 and stores the rightmost occurrence of each position. This special
    value is used when the stricter good suffix rule doesn't apply  e.g. when there are no 
    good suffixes in the pattern with a preceding character that matches the bad character.

    Time complexity: O(|A| * m) where |A| is the length of the alphabet and m is the length of the pattern

    :param pattern: the pattern that is being processed
    :return: the good suffix table 

    """
    m = len(pattern)

    z_suffix = z_algorithm(pattern[::-1])[::-1]

    good_suffix = [[-1] * (NO_OF_CHARS + 1) for _ in range(m+1)]

    #Set the last value of each inner array to 0 as a special value for when there are no 
    #good suffixes with the bad character as the preceding character
    for i in range(m + 1):
        good_suffix[i][-1] = 0

    for p in range(m):
        #Calculate the length as usual and save the preceding character
        j = m - z_suffix[p]
        preceding = pattern[p - z_suffix[p]]

        #Update the value at the index of the preceding char in the relevant array
        good_suffix[j][get_char_index(preceding)] = p
        
        #Set the rightmost occurrence of the good suffix for the special case mentioned earlier
        good_suffix[j][-1] = p

    return good_suffix



def matched_prefix(pattern: str) -> list[int]:
    """
    Function that implements the matched prefix rule 
    Time complexity: O(m) where m is the length of the pattern

    :param pattern: the pattern to be processes
    :return: an array of matched prefix values
    """
    m = len(pattern)
    mp_table = [0] * (m + 1)
    mp_table[0] = m
    z_values = z_algorithm(pattern)

    j = 0 #Keeps track of the max length of substrings that match the prefix

    for i in range(m - 1, 0, -1):
        j = max(j, z_values[i]) 
        mp_table[i] = j
    
    return mp_table



def boyer_moore(txt: str, pattern: str) -> list[int]:
    """
    Function that implements the Boyer-Moore Algorithm with the new good suffix rule
    Time complexity: O(n + m)

    :param txt: string being looked at for matches
    :param pattern: string to be matched against the main string 
    :return: indicies of where matches are present 
    """
    n = len(txt)
    m = len(pattern)

    #Preprocess the pattern using above functions
    bad_char_table = extended_bad_character(pattern)
    good_suffix_table = stricter_good_suffix(pattern)
    matched_prefix_table = matched_prefix(pattern)

    matches = []

    if pat == '':
        return matches

    current_shift = 0
    start = 0
    stop = 0

    #Loop while the shift value is within the bounds of the text and pattern
    while current_shift <= n - m:
        j = m - 1 #Start at the end of the pattern

        #While there are still characters left in pattern and there is match
        while j >= 0 and pattern[j] == txt[current_shift + j]:
            #Galil's optimisation to avoid redundant rechecks
            if j == stop:
                j = start
            j -= 1

        #If the pattern is exhausted (there is a match)
        if j < 0:
            matches.append(current_shift)

            #Update shift value using matched prefix 
            current_shift += m - matched_prefix_table[1] if current_shift + m < n else 1

        else:
            mismatch_char = txt[current_shift + j]

            bad_char_shift = j - bad_char_table[j][get_char_index(mismatch_char)]
            p = good_suffix_table[j+1][get_char_index(mismatch_char)]
            
            #No good suffix was found with the bad char as the preceding char
            if p == -1:
                p = good_suffix_table[j][-1] #Set the value to rightmost good suffix

            #If a good suffix is present 
            if p > 0:
                good_suffix_shift = m - p - 1
                
                #This can be used to skip over already checked sections
                start = p - m + j
                stop = p - 1
            
            #No good suffix is present, we shift using matched prefix 
            else:
                start = 0
                stop = matched_prefix_table[j + 1] - 1
                good_suffix_shift = m - matched_prefix_table[j + 1] - 1

            current_shift += max(1, bad_char_shift, good_suffix_shift)
    
    return matches
                

if __name__ == "__main__":
    _, filename1, filename2 = sys.argv
    txt = read_file(filename1)
    pat = read_file(filename2)
    matches = boyer_moore(txt, pat)
    output_file(matches, "output_q1.txt")