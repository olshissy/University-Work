def scoreSort(results):
    """
    Sorts an array based on the scores of the games
    :param results: An array of arrays representing games between two teams and their scores
    :return: The array sorted based on the scores of the games
    :time complexity: O(N) where N is the length of the input array
    :aux time complexity: O(N) where N is the length of the input array
    """
    # Set the variables to begin count sort
    maxScore = 100 # highest possible attainable score
    countLen = maxScore + 1 # length of the count array based on the highest score
    count = [0] * countLen # initial count array

    output = [0] * len(results) # the output array for the final sorting

    # Loop over all elements in the input and increment the respective index in count array
    for element in results:
        count[element[2]] += 1

    # Saving the position of the items to keep counting sort stable
    for i in range(1,countLen):
        count[i] += count[i-1]

    # Inserting the sorted items into the ouput list
    for i in range(len(results)):
        output[count[results[i][2]]-1] = results[i]
        count[results[i][2]] -= 1

    # Reversing the list so it is sorted by ascending scores
    sortedList = []
    for i in range(len(output)-1,-1,-1):
        sortedList.append(output[i])

    return sortedList

def lexiSort(team, roster):
    """
    Sorts an indivdual string in lexicographical order
    :param team: the string to be sorted representing a team
    :param roster: Denotes the number of characters in the character set
    :return: The team string sorted into lexicographical order
    :time complexity: O(M) where M is the length of the team string
    :aux space complexity: O(M) where M is the length of the team string
    """
    # Initialise variables for counting sort
    ordA = ord("A") # Base value
    count = [0] * roster

    # Loop over the letters in the string and increment the respective count array index
    for letter in team:
        ordLetter = ord(letter)
        index = ordLetter - ordA # B = 1, C = 2, etc.
        count[index] += 1

    # Create the output array with the string values in lexicographical order
    output = []
    for i in range(roster):
        output.append(chr(i + ordA) * count[i])

    return ''.join(output) # Join the final sorted list back to a string before returning

def findScore(results, score):
    """
    Finds games in the results array with the same score as the input
    If none are found, it will find the games with the next highest score
    :param results: an array of arrays representing a game between teams and their scores
    :param score: the score that is being searched for
    :return: a list of the games with the same score or the next highest score
    :time complexity: O(N) where N is the number of games in the input list
    :aux space complexity: O(N) where N is the number of games in the input list
    """
    # Initialise variables
    searchedMatches = []
    val = False

    if score > 50:
        # Loop over the input array and check if the selected score exists, if so append the game to the new array
        # and set the truth value to True
        for i in range(len(results)):
            if score == results[i][2]:
                searchedMatches.append(results[i])
                val = True

        # If no games with this score are found
        if val == False:
            nextScore = 0 # Initialise the next score as 0

            # Loop over the results array from the back
            for i in range(len(results)-1,0,-1):
                # If the score is equal to the created nextScore variable, add it to searchedMatches
                if nextScore == results[i][2]:
                    searchedMatches.append(results[i])
                # If the score is greater than the input score, append the game to searchedMatches and edit the nextScore
                # variable to find other matches
                elif score < results[i][2] and nextScore == 0:
                    searchedMatches.append(results[i])
                    nextScore = results[i][2]
                # Break the loop if no other matches are found
                elif len(searchedMatches) >= 1:
                    break
    # If the score is below or equal to 50
    else:
        # Flip all the games to show the lower score
        for i in range(len(results)-1, 0, -1):
            flippedScore = 100 - results[i][2]

            #If the inputted score is equal to the flipped score, add the game to searchedMatches
            if score == flippedScore:
                searchedMatches.append([results[i][1], results[i][0], flippedScore])
                val = True

        # If no games are found
        if val == False:
            nextScore = 0

            # Loop over the list and repeat the same process as above to find the games with the next highest scores
            for i in range(len(results)):
                flippedScore = 100 - results[i][2]
                if nextScore == flippedScore:
                    searchedMatches.append([results[i][1], results[i][0], flippedScore])
                elif score < flippedScore and nextScore == 0:
                    searchedMatches.append([results[i][1], results[i][0], flippedScore])
                    nextScore = flippedScore
                elif len(searchedMatches) >= 1:
                    break
    return searchedMatches

def removeDuplicateGames(results, length):
    """
    Removes any games in the input that are not unique
    :param results: an array of arrays representing a game between teams and their scores
    :param length: the max length of the output array
    :return: the input list with duplicate games removed
    :time complexity: O(NM) where N is the number of games in the input list and M is the length of the team names
    :aux space complexity: O(N) where N is the number of games in the input list
    """
    if length == 0:
        return []

    # Creating a temporary array for storing results
    tempArray = list(range(length))

    # Loop over the array and check to see if the current item is the same as the previous item
    # If it isn't add this item to the temporary array
    j = 0
    for i in range(0, length - 1):
        if results[i] != results[i-1]:
            tempArray[j] = results[i]
            j += 1

    # Adding the last element in results to the temporary array
    tempArray[j] = results[length-1]
    j += 1

    #Creating a new array without the excess spaces in tempArray that is the same as the input without any duplicate games
    dupsRemoved = [0]*j
    for i in range(0,j):
        dupsRemoved[i] = tempArray[i]

    return dupsRemoved

def countSortLetters(array, col, base, team):
    """
    Count sort algorithm that is used by radix sort to sort the games lexicographically based on teams
    :param array: a list of games with the teams and the score
    :param col: the column of the string currently being sorted
    :param base: the maximum number of elements in the count array
    :param team: the current team the array is being sorted by
    :return: lexicographically sorted array based on the inputted team
    :time complexity: O(N) where N is the length of the input array
    :aux space complexity: O(N) where N is the length of the input array
    """
    # Intialise variables for counting sort
    output = [0] * len(array)
    count = [0] * (base)
    ordA = ord('A')

    # Loop over the items in the input array and increment the respective count array index
    for item in array:
        letter = ord(item[team][col]) - ordA
        count[letter] += 1

    # Save the positions of the elements in the array to keep counting sort stable
    for i in range(len(count)-1):
      count[i + 1] += count[i]

    # Create an output of the sorted values in the array
    for item in reversed(array):
        letter = ord(item[team][col]) - ordA
        output[count[letter] - 1] = item
        count[letter] -= 1

    return output

def radixSortLetters(array):
    """
    Algorithm that calls the counting sort letters function to sort the games lexographically based on the teams
    :param array: The list of games that includes the teams and the score
    :return: The final lexogrpahically sorted list
    :time complexity: O(NM) where N is the length of the input array and M is the length of the team names
    :aux space complexity: O(NM) where N is the length of the input array
    """
    maxCol = len(array[0][0]) # Length of a team string

    # Loops over each team in the game
    for team in range(1, -1, -1):
      # Loops over each letter in the team string and sorts the array based on it using counting sort
      for col in range(maxCol-1, -1, -1):
        array = countSortLetters(array, col, 26, team)
    return array

def analyze(results, roster, score):
    """
    Finds the top 10 matches from the input and all the games with the same or next highest score to the input score
    :param results: a list of games that includes the teams and the score of each game
    :param roster: the number of characters in the character set for the team names
    :param score: the score being searched for
    :return: a list of two lists including the top 10 matches and the matches with the same or next highest score to the input
    :time complexity: O(NM) where N is the length of the input array and M is the length of the team names
    :aux space complexity: O(N) where N is the length of the input array
    """
    # Creates an array where all scores in the games are above 50
    for i in range(0, len(results)):
        # If they are below 50, flip the teams and find the new score
        if results[i][2] <= 50:
            results[i] = [results[i][1], results[i][0], 100 - results[i][2]]

    # Sort each team string lexicographically
    for element in results:
        element[0] = lexiSort(element[0], roster)
        element[1] = lexiSort(element[1], roster)

    lexoSortedResults = radixSortLetters(results) # Sorts the array lexicographically based on the team strings
    sortedResults = scoreSort(lexoSortedResults) # Then sorts the array in ascending order based on the game scores
    finalSortedResults = removeDuplicateGames(sortedResults, len(sortedResults)) # Removes duplicate games from the array

    # Creates top 10 matches list
    top10matches = []
    i = 0
    # Loop will continue to add matches to the list until the length is 10 or the results list is exhausted
    while i < len(finalSortedResults):
        if i == 10:
            break
        top10matches.append(finalSortedResults[i])
        i += 1

    # If the top 10 list is less than 10 matches, add the inverses of the matches present
    if len(top10matches) != 10:
        index = len(finalSortedResults) - 1

        # Loop backwards over the results list
        while index >= 0:
            # Loop will break when top10 becomes 10 matches of results are exhausted
            if len(top10matches) == 10:
                break
            # Flip the results of the lowest match, to get the next highest score
            newMatch = [finalSortedResults[index][1], finalSortedResults[index][0], 100-finalSortedResults[index][2]]
            top10matches.append(newMatch)
            index -= 1
        # Sort the new list and remove any potential duplicates
        top10matches = removeDuplicateGames(top10matches, len(top10matches))
        top10matches = radixSortLetters(top10matches)
        top10matches = scoreSort(top10matches)

    searchedMatches = findScore(finalSortedResults,score) # Use the findScore function to create searchedMatches

    #If the list is not empty, resort it lexicographically based on the team strings
    if searchedMatches != []:
        searchedMatches = radixSortLetters(searchedMatches)

    return [top10matches, searchedMatches]















