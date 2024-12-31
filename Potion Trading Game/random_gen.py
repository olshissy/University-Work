from typing import Generator


def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed


class RandomGen:

    def __init__(self, seed: int = 0) -> None:
        self.randomgen = lcg(pow(2, 32), 134775813, 1, seed)

    def randint(self, k: int) -> int:
        """
        Random number generator
        complexity: O(n) where n is the length of sum_bins
        """
        rand_list = []
        for i in range(5):
            # create a list of 5 random numbers passed through the generator function 'lcg'
            rand_nums = next(self.randomgen)
            rand_list.append(rand_nums)
            bins = []
            for num in rand_list:
                # each number generated above is converted into a 32 bit binary in which the 16 least significant bits are removed
                bins.append(int('{:032b}'.format(num)[:16]))
        # we sum each value in the bins list (#1's in each column), then convert to a string so that each digit can be iterated over
        sum_bins = str(sum(bins))
        bin_result = ""
        for digit in sum_bins:
            # if the digit in sum bins is either 0, 1 or 2 we append '0' to the final bin result
            if digit in ['0', '1', '2']:
                bin_result += "0"
            # else if the digit in sum is 3, 4 or 5 we append '1' to the final bin result
            else:
                bin_result += "1"
        # the binary number is then used in a formula to return the final result
        return int(bin_result, 2) % k + 1


if __name__ == "__main__":
    Random_gen = lcg(pow(2, 32), 134775813, 1, 0)

