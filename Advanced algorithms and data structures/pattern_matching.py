import sys

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
        This version of the comparison function will also add to the z-value if the 
        character in the pattern is the wild card character '!'

        :param start: index where matching starts
        :param end: index where matching ends
        :return: None
        """
        while end < n and (txt[end-start] == txt[end] or txt[end-start] == '!' or txt[end] == '!'):
            end += 1
        z_array[k] = end - start
        end -= 1

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


def pattern_match(txt, pat):
    concat_string = pat + '$' + txt

    matches = [] 

    #If the pattern is empty, there are no matches
    if pat == '':
        return matches

    z_values = z_algorithm(concat_string)

    #Loop over all the Z values
    for i in range(len(z_values)):
        #If the current z value is the same as the pattern length there is a match
        if z_values[i] == len(pat):
            #Check if the calculated value is a valid index and appends to matches 
            if (i - (len(pat) + 1)) >= 0:
                matches.append(i - (len(pat) + 1))

    return matches


if __name__ == '__main__':
    _, filename1, filename2 = sys.argv
    txt = read_file(filename1)
    pat = read_file(filename2)
    matches = pattern_match(txt, pat)
    output_file(matches, "output_q2.txt")