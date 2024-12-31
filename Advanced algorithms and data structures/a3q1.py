#Oliver Hiscoke 32461356

import random
import sys

def modularExponentiation(a,b,n):
    """
    Computes the modular exponentiation of a raised to the power of b modulo n using repeated squaring

    :param a: The base number
    :param b: The exponent
    :param n: The modulus
    :return: The result of the modular exponentiation 
    """

    #Determine the binary representation of the exponent
    binaryRep = bin(b)[2:]

    #Base case
    current = a % n

    if binaryRep[-1] == 1:
        result = current
    else:
        result = 1

    #Iterate through remaining bits in the binary representation in reverse
    for bit in reversed(binaryRep):
       
        #Compute the next term in the sequence
        current = (current * current) % n 
        
        if bit == '1':
            
            #Update the result
            result = (result * current) % n
    
    return result



def millerRabinRandomisedPrimality(n, k=5):
    """
    Determines whether a number is prime using Miller-Rabin randomised primality test

    :param n: The number to be tested for primality 
    :param k: The number of rounds of testing to perform 
    :return: 1 if the number is probably prime or 0 if the number is not prime 
    """
    
    # Special cases
    if n == 2 or n == 3:
        return 1
    
    # Only want to test odd integers
    if n % 2 == 0:
        return 0
    
    # Factor n-1 as (2^s) * t, where t is odd
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2
    
    # Run k random tests
    for _ in range(k):
        # Select a random witness
        a = random.randint(2, n - 2)
        
        # Compute a^t mod n
        x = modularExponentiation(a,t,n)
        
        # Check if n satisfies Fermat’s little theorem for this witness
        if x == 1 or x == n - 1:
            continue
        
        # Run the sequence test
        for _ in range(s - 1):
            x = modularExponentiation(x, 2, n)
            if x == n - 1:
                break
        
        else:
            return 0
    
    # n has passed all tests, so it's probably prime
    return 1



def euclids(a, b):
    """
    Computes the greatest common divisor of two integers

    :param a: The first integer
    :param b: The second integer
    :return: The greatest common divisor of the two integers 
    """

    #Base case
    if b == 0:
        return a
    
    return euclids(b, a%b)



def generateKeys(d):
    """
    Generates the public and private keys of the RSA encyrption

    :param d: Parameter for controlling the start of the search for primes 
    """

    primes = []
    x = d

    # Find two distinct primes of the form 2^x - 1
    while len(primes) < 2:
        candidate = (2 ** x) - 1
        if millerRabinRandomisedPrimality(candidate):
            primes.append(candidate)
        x += 1  # Increment x to find the next prime

    #Obtain the prime number values 
    p, q = primes[0], primes[1]

    #Calculate the modulus value
    n = p*q

    #Calculate the lambda value 
    lambda_value = (p - 1) * (q - 1) // euclids(p - 1, q - 1)

    #Randomly generate the exponent untul e and lambda are relatively prime
    while True:
        e = random.randint(3, lambda_value - 1)

        if euclids(e, lambda_value) == 1:
            break
    
    #Write the modulus and exponent to the public key file
    with open("output_q1_public.txt", 'w') as public_file:
        public_file.write('# modulus (n)\n')
        public_file.write(f"{n}\n")
        public_file.write("# exponent (e)\n")
        public_file.write(f"{e}\n")

    #Write the primes to the private key file 
    with open("output_q1_private.txt", 'w') as private_file:
        private_file.write("# p\n")
        private_file.write(f"{p}\n")
        private_file.write("# q\n")
        private_file.write(f"{q}\n")



if __name__ == "__main__":

    try:
        d = int(sys.argv[1])
        if d <= 2:
            raise ValueError("Input integer d must be greater than 2")
    except ValueError as e:
        print(e)
        sys.exit(1)

    generateKeys(d)