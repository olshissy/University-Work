# Part 1
from math import floor, ceil

# Constant for the number of housemates
NUM_PEOPLE = 5

class Edge:
    def __init__(self, neighbour, flow, capacity, reverse):
        """
        Function used to create an edge in the graph
        :param neighbour: the node the edge goes to as an index
        :param flow: the current flow through the edge as an integer
        :param capacity: the maximum flow that can go through the edge as an integer
        :param reverse: the index of the reverse edge for the current edge
        :Time complexity: O(1)
        :Aux space complexity: O(1)
        """
        self.neighbour = neighbour
        self.flow = flow
        self.capacity = capacity
        self.reverse = reverse

def collect_info(availability):
    """
    This function collects the information in an easier to use format for creating the graph
    This is done by creating lists for breakfast and dinner that use boolean values to show who is available for each day
    :param availability: a list of lists showing the availability of each housmate for each meal on each day
    :return breakfast: a list of lists containing boolean values showing who can make each breakfast each day
    :return: dinner: a list of lists containing boolean values showing who can make each dinner each day
    :Time complexity: O(n) where n is the number of days
    :Aux space complexity: O(n) where n is the number of days
    """
    # Initialise the variables for use later
    days = len(availability)
    breakfast = []
    dinner = []

    # Loop over all the days
    for i in range(days):
        day = availability[i] # Set the current day to the availability for that day

        # Initialise the current day breakfast and dinner lists
        breakfast_day = [False] * NUM_PEOPLE
        dinner_day = [False] * NUM_PEOPLE

        # Loop over all the house mates
        for j in range(NUM_PEOPLE):

            # If the list has a 1, that person can only make breakfast that day
            if day[j] == 1:
                breakfast_day[j] = True

            # If the list has a 2, that person can only make dinner that day
            elif day[j] == 2:
                dinner_day[j] = True

            # If the list has a 3, that person can make both breakfast and dinner that day
            elif day[j] == 3:
                breakfast_day[j] = True
                dinner_day[j] = True

        # Append both the current day meal lists to their larger lists
        breakfast.append(breakfast_day)
        dinner.append(dinner_day)

    return breakfast, dinner


def createGraph(availability):
    """
    This function creates the graph used to allocate the meals
    This is done by creating an adjacency list containing edge objects
    :param availability: a list of lists showing the availability of each housmate for each meal on each day
    :return: the graph as an adjacency list
    :Time complexity: O(n) where n is the number of days
    :Aux space complexity: O(n) where n is the number of days
    """
    # Initialise the variables for use later on
    NUM_DAYS = len(availability)
    breakfast, dinner = collect_info(availability)
    number_of_meals = NUM_DAYS * 2
    adjacencyList = [[] for i in range(number_of_meals + NUM_PEOPLE + 2 + (NUM_DAYS * NUM_PEOPLE))]
    first_meal_index = 6 + (NUM_PEOPLE * NUM_DAYS)
    final_meal_index = len(adjacencyList) - 2

    # Loop over all meals
    for i in range(first_meal_index, final_meal_index + 1):
        # Set the reverse ID to the index of the reverse edge in it's relevant list
        meal_reverse_id = len(adjacencyList[len(adjacencyList)-1])

        # Create an edge from the meal to the target vertex and it's reverse edge and add them to the adjacency list
        meal_forward_edge = Edge(len(adjacencyList) - 1, 0, 1, meal_reverse_id)
        adjacencyList[i].append(meal_forward_edge)
        meal_reverse_edge = Edge(i, 0, 0, len(adjacencyList[i]) - 1)
        adjacencyList[len(adjacencyList)-1].append(meal_reverse_edge)

    # Loop over all days
    for i in range(NUM_DAYS):
        # Initialise the current day breakfast and dinner from the lists found in collect_info
        current_day_breakfast = breakfast[i]
        current_day_dinner = dinner[i]

        # Loop over all the people
        for j in range(NUM_PEOPLE):
            # If the person can cook either dinner or breakfast on that day
            if current_day_breakfast[j] == True or current_day_dinner[j] == True:
                # Set the reverse ID to the index of the reverse edge in it's relevant list
                reverse_id = len(adjacencyList[(1 + NUM_PEOPLE + (NUM_DAYS * j) + i)])

                # Create an edge from the person to the selector and it's reverse edge and add them to the adjacency list
                forward_edge = Edge((1 + NUM_PEOPLE + (NUM_DAYS * j) + i), 0, 1, reverse_id)
                adjacencyList[j+1].append(forward_edge)
                reverse_edge = Edge(j+1, 0, 0, len(adjacencyList[j+1]) - 1)
                adjacencyList[(1 + NUM_PEOPLE + (NUM_DAYS * j) + i)].append(reverse_edge)

    # Loop over all days
    for i in range(NUM_DAYS):
        # Initialise the current day breakfast and dinner lists from the lists found in collect_info
        current_day_breakfast = breakfast[i]
        current_day_dinner = dinner[i]

        # Loop over all people
        for j in range(NUM_PEOPLE):
            # If the person can cook breakfast that day
            if current_day_breakfast[j] == True:
                # Set the reverse ID to the index of the reverse edge in it's relevant list
                reverse_id = len(adjacencyList[first_meal_index])

                # Create an edge from the selector to the meal and it's reverse edge and add them to the adjacency list
                forward_edge = Edge(first_meal_index, 0,1, reverse_id)
                adjacencyList[1 + NUM_PEOPLE + (NUM_DAYS * j) + i].append(forward_edge)
                reverse_edge = Edge(1 + NUM_PEOPLE + (NUM_DAYS * j) + i, 0, 0, len(adjacencyList[1 + NUM_PEOPLE + (NUM_DAYS * j) + i]) - 1)
                adjacencyList[first_meal_index].append(reverse_edge)

            if current_day_dinner[j] == True:
                # Set the reverse ID to the index of the reverse edge in it's relevant list
                reverse_id = len(adjacencyList[first_meal_index+NUM_DAYS])

                # Create and edge from the selector to the meal and it's reverse edge and add them to the adjacency list
                forward_edge = Edge(first_meal_index+NUM_DAYS, 0, 1, reverse_id)
                adjacencyList[1 + NUM_PEOPLE + (NUM_DAYS * j) + i].append(forward_edge)
                reverse_edge = Edge(1 + NUM_PEOPLE + (NUM_DAYS * j) + i, 0, 0, len(adjacencyList[1 + NUM_PEOPLE + (NUM_DAYS * j) + i])-1)
                adjacencyList[first_meal_index+NUM_DAYS].append(reverse_edge)

        first_meal_index += 1

    min_meals = floor(0.36 * len(availability)) # minimum meals initialised based on the specificaitons

    # Loop over all people
    for i in range(NUM_PEOPLE):
        # Set the reverse ID to the index of the reverse edge in it's relevant list
        person_reverse_id = len(adjacencyList[i+1])

        # Create an edge from the start vertex to the person and it's reverse edge and add them to the adjacency list
        # Initially set capacity as min_meals to saturate the people, so each person makes at least min_meals meals
        person_forward_edge = Edge(i + 1, 0, min_meals, person_reverse_id)
        adjacencyList[0].append(person_forward_edge)
        person_reverse_edge = Edge(0, 0, 0, len(adjacencyList[0]) - 1)
        adjacencyList[i+1].append(person_reverse_edge)

    return adjacencyList


def depthFirstSearch(u, t, bottleneck, visited, graph):
    """
    This function traverses through the graph and updates flow using ford fulkerson
    This was done using depth first search to traverse the graph and finding an augmenting path then updating the flow
    through that path
    :param u: current node index
    :param t: final node index
    :param bottleneck: minimum capacity of the edges encountered along the path
    :param visited: a list showing which vertices have been visited by DFS
    :param graph: an adjacency list representing the graph
    :return: the minimum capacity of the edges encountered along the path
    :Time complexity: O(n^2) where n is the number of days
    :Aux space complexity: O(n) where n is the number of days
    """
    # If the current node is the end node, return the bottleneck of the path
    if u == t:
        return bottleneck
    # Set the current node as visited
    visited[u] = True

    # Loop over all adjacent edges to u
    for i in range(len(graph[u])):
        # Initialise the forward edge and reverse edge
        forward_edge = graph[u][i]
        reverse_edge = graph[forward_edge.neighbour][forward_edge.reverse]
        residual = forward_edge.capacity - forward_edge.flow # residual = capacity - flow

        # If there is room for more flow and the edge has not been visited
        if residual > 0 and not visited[forward_edge.neighbour]:
            # Recursively call the function until it hits the base case
            augment = depthFirstSearch(forward_edge.neighbour, t, min(bottleneck, residual), visited, graph)

            # If the path has a bottleneck of more than 0, update the flow and the reverse flow and return the  bottlneck value
            if augment > 0:
                forward_edge.flow += augment
                reverse_edge.flow -= augment
                graph[u][i] = forward_edge
                graph[forward_edge.neighbour][forward_edge.reverse] = reverse_edge
                return augment
    # Return 0 if no augmenting path is found
    return 0


def ford_fulkerson(graph):
    """
    This function pushes flow through a network until no more flow can be pushed through it
    This is done by finding an augmenting path using DFS and updating the flow through the path as the minimum capacity
    of that path
    :param graph: an adjacency list representing a graph
    :return: total flow through the graph
    :Time complexity: O(n^2) where n is the number of days
    :Aux space complexity: O(n) where n is the number of days
    """
    u = 0 # Start at the start node
    t = len(graph) - 1 # End at the target node
    augment = 1000 # Allows the while loop to run at least once
    flow = 0 # Initial flow through the graph is 0

    while augment > 0:
        visited = [False] * len(graph) # Initially no vertices are visited
        # Call the depthFirstSeacrh function using the intialised variables
        augment = depthFirstSearch(u, t, float("inf"), visited, graph)
        flow += augment # Increment flow every iteration of the loop
    return flow

def collect_results(graph, number_of_days):
    """
    This function uses the results of ford fulkerson to create the final output
    This is done by looping through the selectors and seeing which meals they go to and which person they come from
    :param graph: an adjacency list representing a graph
    :param number_of_days: the number of days being looked at
    :return: the final output lists showing who will be cooking which meal
    :Time complexity: O(n) where n is the number of days
    :Aux space complexity: O(n) where n is the nunber of days
    """
    # Initialise varibales for use later
    first_selector = 6
    last_selector = 6 + (NUM_PEOPLE * number_of_days) - 1
    first_breakfast = 6 + (NUM_PEOPLE * number_of_days)
    first_dinner = first_breakfast + number_of_days

    # These lists are initally 5, so that if no person is added the meal is from a restuarant
    breakfast = [5] * number_of_days
    dinner = [5] * number_of_days
    goes_to_meal = False
    meal_index = -1

    # Loop over all selectors
    for i in range(first_selector, last_selector):
        # For each edge adjacent to the selector
        for edge in graph[i]:
            # If the flow is 1, then it goes to a meal, so set it to true and note the meal index
            if edge.flow == 1:
                goes_to_meal = True
                meal_index = edge.neighbour

        # Check if the meal is a dinner or a breakfast and note which day the meal belongs to
        if meal_index < first_dinner:
            meal = "breakfast"
            day_number = meal_index - first_breakfast
        else:
            meal = "dinner"
            day_number = meal_index - first_dinner

        # Calculate the person index using the information present
        person_index = round(((i-1-NUM_PEOPLE-(day_number-1))/number_of_days))

        # If the selector goes to a meal, check which type of meal it is and add the person at the relevant day to the
        # relevant meal list
        if goes_to_meal and meal == "breakfast":
            breakfast[day_number] = person_index
        elif goes_to_meal and meal == "dinner":
            dinner[day_number] = person_index
        goes_to_meal = False


    return breakfast, dinner



def allocate(availability):
    """
    This function uses all function above to allocate each person to their meals for the set number of days
    :param availability: a list of lists showing the availability of each housmate for each meal on each day
    :return: the final allocation for breakfasts and dinners foe the set number of days
    :Time complexity: O(n^2) where n is the number of days
    :Aux space complexity: O(n) where n is the number of days
    """
    # Create the graph and set the number of days
    graph = createGraph(availability)
    number_of_days = len(availability)

    # Call ford_fulkerson the first time to saturate each person to meet the min meals requirement
    ford_fulkerson(graph)

    # If a start to person edge is not saturated, there is no possible output so return None
    for edge in graph[0]:
        if edge.flow != edge.capacity:
            return None

    max_meals = ceil(0.44 * len(availability)) # Initialise max_meals per the requirements

    # Update the capacity of the person to start meals to max_meals
    for edge in graph[0]:
        edge.capacity = max_meals

    # Call ford fulkerson again to finalise the allocations
    ford_fulkerson(graph)

    max_takeout = floor(0.1 * len(availability)) # Initialise the max_takeout variable per the requirements

    # Calculate the number of meals allocated to the housemates
    flows = 0
    for edge in graph[0]:
        flows += edge.flow

    # If the number of meals allocated plus the maximum takeout meals is less than the number of required meals
    # the allocation is not possible so return None
    if (flows + max_takeout) < (len(availability) * 2):
        return None

    # Otherwise, use the function collect_results to create the required output
    breakfast,dinner = collect_results(graph,number_of_days)

    return breakfast, dinner


# Part 2
class Node:
    def __init__(self, label, string_number=-1):
        """
        Function used to create an instance of the Node class.
        This represents a node in the tree created later on
        :param label: The label of the node as a string
        :param string_number: the corresponding string the node belongs to. 0 for string 1, 1 for string 2 and 2 for both
        :Time complexity: = O(1)
        :Aux space complexity = O(1)
        """
        self.label = label
        self.children = [None]*29
        self.string_number = string_number

    def __repr__(self):
        return f"{self.label}"

class SuffixTree:
    def __init__(self, s, string1_len, string2_len):
        """
        This function is used to create a suffix tree class instance
        This was done by looping over the input string and creating relevant node instances and adding them to the correct
        children list of previous nodes
        :param s: the string that the suffix tree is being created for
        :param string1_len: The length of the first string in s
        :param string2_len: The length of the second string in s
        :Time complexity: O((N+M)^2) where N is the length of the first string and M is the length of the second string
        :Aux space complexity: O((N+M)^2) where N is the length of the first string and M is the length of the second string
        """

        # Root node and the whole string node are initalised in the tree
        self.root = Node(None)
        self.root.children[charToIndex(s[0])] = Node(s,0)

        # String lengths are saved for use later on
        self.string1_len = string1_len
        self.string2_len = string2_len

        # Loop over the string skipping the first character to add the rest of the suffixes, from longest to shortest
        for i in range(1, len(s)):

            # Begin at the root node and traverse down as far as it can go
            current = self.root
            j = i
            while j < len(s):
                if current.children[charToIndex(s[j])] != None:
                    child = current.children[charToIndex(s[j])]
                    label = child.label

                    # The edge is travered until the label is exhausted or until there is a mismatch
                    k = j + 1
                    while k-j < len(label) and s[k] == label[k-j]:
                        k += 1

                    # Check if the edge has been exhausted
                    if k-j == len(label):
                        current = child
                        j = k
                    else:
                        # Fell off in the middle of the edge
                        childExists, newChild = label[k-j], s[k]

                        # Checks which string the node label is a part of
                        if i < self.string1_len:
                            string_number = 0
                        else:
                            string_number = 1

                        # Create a middle node
                        mid = Node(label[:k-j], string_number)
                        mid.children[charToIndex(newChild)] = Node(s[k:], string_number)

                        # The original child now becomes the child of the middle node
                        mid.children[charToIndex(childExists)] = child
                        child.label = label[k-j:]

                        # Middle node now becomes the child of the original parent
                        current.children[charToIndex(s[j])] = mid
                else:
                    # No node exists so a new node is created as a leaf
                    # Checks to see if what string the node is a part of
                    if i < self.string1_len:
                        string_number = 0
                    else:
                        string_number = 1
                    current.children[charToIndex(s[j])] = Node(s[j:], string_number)

    def split_tree(self, node):
        """
        This function splits the tree's nodes into nodes that only contain one ending character
        This was done by traversing through the tree and cutting of the nodes with two ending characters at the first one
        :param node: The current node being checked
        :Time complexity: O(N+M) where N is the length of the first string and M is the length of the second string
        :Aux space complexity: O(1)
        """
        # Loop over all the children of the current node
        for node in node.children:
            # If a child is found
            if node is not None:
                # Loop over the child's label
                for i in range(len(node.label)):
                    # If the first string ending character is found, cut off the part of the string after it so the
                    # node only contains first string characters
                    if node.label[i] == "|":
                        node.label = node.label[:i+1]
                        break

                # Recursively call the fucntion for the current child
                self.split_tree(node)

    def check_is_in_string(self, node):
        """
        This function updates the string number attribute of the node to be 2 if it is contained in both strings
        This is done by traversing the tree and determining whether the node's children are in different strings to the
        node itself and updating the node to show it's in both if so
        :param node: The current node being checked
        :Time complexity: O(N+M) where N is the length of the first string and M is the length of the second string
        :Aux space complexity: O(1)
        """
        # Loop over all the children of the current node
        for child in node.children:
            # If a child is found
            if child is not None:
                # If the current node is from the first string and it's child is from the second string, the current node
                # would have to be from both strings
                if node.string_number == 0 and child.string_number == 1:
                    node.string_number = 2
                # Same as above, just the other way around
                elif node.string_number == 1 and child.string_number == 0:
                    node.string_number = 2

                # Repeat the code above on the current child
                self.check_is_in_string(child)

                # If the child is changed to be in both strings, the parent would be in both string as well
                if child.string_number == 2:
                    node.string_number = 2

    def search_tree(self, node, substr):
        """
        This function searches the tree to find the longest common substring between the two strings
        This is done by traversing through the tree and checking whether a substring appears in both strings, if it
        does it is checked to see if it is the current longest and if it is the LCS variable is updated
        :param node: The current node being checked
        :param substr: the current substring being looked at
        :Time complexity: O(N+M) where N is the length of the first substring and M is the length of the second substring
        :Aux space complexity: O(1)
        """
        # Initialise the longest substring as the current label
        longest_current_substr = node.label

        # Loop over all the children of the current node
        for child in node.children:
            # If a child is found
            if child is not None:
                # Create the current subtring by adding the substring and the current label
                sub = "".join([substr, child.label])

                # If the substring is in both strings, set it as the longest current found and call the function on the child
                if child.string_number == 2:
                    longest_current_substr = sub
                    self.search_tree(child, sub)

        # If the current found string is longer than the saved substring, reset the saved string to the current one
        if len(longest_current_substr) > len(self.LCS):
            self.LCS = longest_current_substr

    def longestCommonSubstring(self):
        """
        This function uses the search_tree function to find the longest common substring
        This is done by traversing through the children of the root node and calling the search_tree function if the
        child's label is in both strings
        :return: The longest common substring
        :Time complexity: O(N+M) where N is the length of the first substring and M is the length of the second substring
        :Aux space complexity: O(1)
        """
        # Initialise the current LCS as nothing
        self.LCS = ""

        # Loop over all the children of the root node
        for child in self.root.children:
            # If a child is found and it is in both strings, call the search_tree function on it
            if child is not None:
                if child.string_number == 2:
                    self.search_tree(child, child.label)

        # As spaces were replaced for functionality reasons, add them back and return the longest common substring
        return self.LCS.replace("{", " ")

def charToIndex(ch):
    """
    This function returns an index for adding a node to the children list using the ord function
    :param ch: The character being translated
    :return: the index value calculated
    :Time complexity: O(1)
    :Aux space complexity: O(1)
    """
    return ord(ch) - ord('a')

def compare_subs(submission1, submission2):
    """
    This function finds the longest common substring between two strings and the percentage of each string that the substring
    is.
    :param submission1: The first string to be checked
    :param submission2: The second string to be checked
    :return: A list containing the longest common substring, what percentage of the first string the substring is and
    what percentage of the second string the substring is
    :Time complexity: O((N+M)^2) where N is the length of the first string and M is the length of the second string
    :Aux space complexity: O((N+M)^2) where N is the length of the first string and M is the length of the second string
    """
    # Replace spaces from the string to avoid indexing errors later on, and define the lengths of each string
    submission1 = submission1.replace(' ', '{')
    string1_len = len(submission1)
    submission2 = submission2.replace(' ', '{')
    string2_len = len(submission2)

    # Join the two string together separated by their corresponding end characters
    combined = ''.join(submission1 + '|' + submission2 + '}')

    # Create a suffix tree for the combined string
    st = SuffixTree(combined, string1_len, string2_len)

    # Call the functions to set up for finding the longest common substring
    st.split_tree(st.root)
    st.check_is_in_string(st.root)

    # Find the LCS
    LCS = st.longestCommonSubstring()

    # Determine the percentage of each string this substring is
    percentage_1 = round((len(LCS) / len(submission1)) * 100)
    percentage_2 = round((len(LCS) / len(submission2)) * 100)
    return [LCS, percentage_1, percentage_2]



