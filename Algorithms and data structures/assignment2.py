# Part 1 

import heapq

class RoadGraph():
    def __init__(self, roads, cafes) -> None:
        """
        Function used to create an instance of the RoadGraph class.
        This function uses other function calls to limit the amount of code in the init method
        :param roads: a list of tuples which shows the nodes the road goes between and the time it takes
        :param cafes: a list of tuples which shows which nodes the cafes are at and their wait times
        :return: None
        :Time complexity: O(|V| + |E|) where V is the set of locations in roads and E is the set of roads
        :Aux space complexity: O(|V| + |E|) where V is the set of locations in roads
        """
        self.roads = roads
        self.cafes = cafes
        self.v = self.find_biggest_node()
        self.adjList = self.adjacency_list()
    
    def routing(self, start, end):
        """
        This function finds the shortest path with the smallest time between two nodes with the condition that a cafe
        must be passed through
        This was done using Dijkstra's algorithm and the two graphs created in the adjaceny_list function
        :param start: The node the user wants to start at as it's integer value
        :param end: The node the user wants to get to as it's integer value
        :return: The shortest path to get from start to end that passes through a cafe as a list of nodes
        :Time complexity: O(|E|log|V|) where E is the set of roads and V is the set of locations in roads
        :Aux space complexity: O(|V| + |E|) where E is the set of roads and V is the set of locations in roads
        """

        # Intialise all variables needed to undergo Dijkstra's algorithm
        dists = [float("inf")] * 2*self.v
        pred = [-1] * 2*self.v
        dists[start] = 0
        Q = [(dists[start], start)]

        # While the priority queue is empty, pop off the smallest item in it
        while len(Q) > 0:
            dist, u = heapq.heappop(Q)

            # If the edge weight is smaller than the stored distance
            if dist <= dists[u]:
                # Loop over the adjacent vertices and calculate the distance between them
                for vertex in self.adjList[u]:
                    distance = dist + vertex[1]

                    # If this distance is smaller than what is stored change the stored distance to it and update the
                    # predecessor of it and push it to the queue
                    if distance < dists[vertex[0]]:
                        dists[vertex[0]] = distance
                        pred[vertex[0]] = u
                        heapq.heappush(Q, (distance, vertex[0]))

        # Initialise the variables for creating the path
        path = []
        index = end + self.v

        while index != start:
            # If the predecessor is still -1, there is no path possible between start and end
            if pred[index] == -1:
                return None

            # If the predecessor is not the same as the current vertex
            if pred[index] != index - self.v:
                # If the index is larger than the number of nodes append the index - the number of nodes
                if index >= self.v:
                    path.append(index - self.v)

                # Otherwise just append the index
                else:
                    path.append(index)
            index = pred[index] # Reassign the index so the loop can end at some point
        path.append(start) #Append the start node to the list at the very end

        # Return the reversed list created to get the path from start to end
        return path[::-1]


    def find_biggest_node(self):
        """
        This function searches through the nodes and finds the node with the highest integer value
        This was done by searching the roads list and re-setting the biggest node when a higher node was found
        :param: None
        :return: The biggest node value + 1 in order to get the length the list will need to be due to the zero indexing
        :Time complexity: O(|E|) where E is the set of roads
        :Aux space complexity: O(1)
        """
        biggest_node = 0 #Initialise the biggest node to the smallest possible value

        # Loop over all roads and check both the start and end nodes to determine if they are larger
        for road in self.roads:
            if road[0] > biggest_node:
                biggest_node = road[0]
            elif road[1] > biggest_node:
                biggest_node = road[1]
        return biggest_node + 1

    def adjacency_list(self):
        """
        This function creates an adjacency list where the nodes adjacent to node i are at adjList[i]
        This was done using two graphs where the first graph shows the edge weights between nodes and the second
        being connected via cafes and their wait times
        :param: None
        :return: the adjacency list of the graph
        :Time complexity: O(|V| + |E|) where V is the set of locations in roads and E is the set of roads
        :Aux space complexity: O(|V|) where V is the set of locations in roads
        """
        adjList = [[] for i in range(self.v*2)] # Create a list of length twice v for the two graphs

        # Loop over all the roads and adjacent vertices to the correct places
        for road in self.roads:
            adjList[road[0]].append((road[1], road[2]))
            adjList[road[0] + self.v].append((road[1] + self.v, road[2]))

        # Loop over all cafes and add them and their wait times to the corresponding position in the second graph
        for cafe in self.cafes:
            adjList[cafe[0]].append((cafe[0]+self.v, cafe[1]))

        return adjList



# Part 2

def find_biggest_node(scores):
    """
    This function searches through the nodes and finds the node with the highest integer value
    This was done by searching the downhill scores list and re-setting the biggest node when a higher node was found
    :param: None
    :return: The biggest node value + 1 in order to get the length the list will need to be due to the zero indexing
    :Time complexity: O(|D|) where D is the set of downhill segments
    :Aux space complexity: O(1)
    """
    biggest_node = 0 # Initialise the biggest node to the smallest possible value

    # Loop over all roads and check both the start and end nodes to determine if they are larger
    for score in scores:
        if score[0] > biggest_node:
            biggest_node = score[0]
        elif score[1] > biggest_node:
            biggest_node = score[1]
    return biggest_node + 1

def adjacency_list(scores, v):
    """
    This function will create an adjacency list for the graph being created
    This is done by looping through the downhill scores and appending the end edge to the list of the start edge
    :param scores: A list of tuples showing the start node, the end node and the score of that path
    :param v: The maximum number of nodes in the graph
    :return: The adjacecny list for the graph
    :Time complexity: O(|D|) where D is the set of downhill segments
    :Aux space complexity: O(|P|) where P is the number of intersection points
    """
    adjList = [[] for i in range(v)] # Create an arra of length P where P is the number of intersections

    # Loop over all the downhill segments and add any nodes adjacent to the first node in the corresponding
    # position in the adjacency list
    for i in range(len(scores)):
        adjList[scores[i][0]].append((scores[i][1], scores[i][2]))
    return adjList

def criticalPath(u, adjList, longest, pred):
    """
    This function finds the longest path through a graph
    This was done using the critical path algorithm and altering it to add a predecessor list to find the path
    :param u: The start vertex as an integer
    :param adjList: The adjacency list of the graph as created previously
    :param longest: A list of the longest distances to vertex i
    :param pred: A list of predecessors to vertex i
    :return: The updated value at longest u
    :return: The updated predecessors list
    :Time complexity: O(|D|) where D is the set of downhill segments
    :Aux space complexity: O(1)
    """
    # If no score has been calculated for the current node, set it to 0
    if longest[u] == float("inf"):
        longest[u] = 0

        # Loop over all the adjacent vertices and recursively call the function for each vertex
        for vertex in adjList[u]:
            value = vertex[1] + criticalPath(vertex[0], adjList, longest, pred)[0]

            # If the newly calculated score is larger than the current score change the predecessor to the current
            # node and replace the longest value with the newly calculated one
            if value > longest[u]:
                pred[vertex[0]] = u
                longest[u] = value

    return longest[u], pred

def optimalRoute(downhillScores, start, finish):
    """
    This function determines the longest path between the start and finish points based on the highest scores
    This was done by calling the critical path method and using the predecessors list to return a path
    :param downhillScores: A list of tuples showing the start node, the end node and the score for that segment
    :param start: The starting point as an integer
    :param finish: The end point as an integer
    :return: The path that will return the highest score from start to finish
    :Time complexity: O(|D|) where D is the set of downhill segments
    :Aux space complexity: O(|P|) where P is the number of intersection points
    """
    # Set up all the values in order to find the longest path
    v = find_biggest_node(downhillScores)
    adjList = adjacency_list(downhillScores, v)
    longest = [float("inf")] * v
    pred = [-1] * v

    # Call the critical path function on the start node
    new_pred = criticalPath(start, adjList, longest, pred)[1]

    # Set up the list ot find the path
    path = [finish]
    index = finish

    # While the predecessor is not the start node append it to the path and re-set the index to continue the loop
    while new_pred[index] != start:
        if new_pred[index] == -1:
            return None
        path.append(new_pred[index])
        index = new_pred[index]

    # Append the start node to the back of the list
    path.append(start)

    # Return the path list in reverse order to get the path from start to finish
    return path[::-1]
