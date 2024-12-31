from math import isqrt


def largest_prime(k: int) -> int:
    """
    Finds the largest prime number less than k
    complexity: O(k), where k is the max value of the range that the function has to find the largest prime number
    """
    first_prime = 2
    bool_arr = [True] * k  # creates a boolean array up to k values with all values set to True
    # Have a for loop that runs from 2 to the square root of k
    for i in range(first_prime, isqrt(k)):
        # If the number is true, it will then run a for loop, else it moves to the next value of i
        if bool_arr[i]:
            # Run a for loop that will assign the muliples of i to false until we reach k, to show that it is not a prime number, the last number in list
            for j in range(i * i, k, i):
                # Create a variable j for placeholder to assign the number as false in the list
                bool_arr[j] = False

    # Have a for loop that will run until it reaches the last prime number
    for n in range(k):
        if bool_arr[n]:
            max_prime = n
    # Get the last index of the list, for largest prime number

    # Return the max prime number to be used
    return (max_prime)






