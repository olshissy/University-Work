class Potion:

    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """
        This method creates a potion with quantity of 0
        complexity - O(1)
        """
        return cls(potion_type, name, buy_price, 0)  # Creates a new potion with quantity 0

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        Universal hash function

        Complexity = O(n) where n is the number of characters in potion_name
        pre-condition = Potion name is of type string and table size is >= 0
        """
        assert type(potion_name) == str, "Potion name should be a string"
        assert tablesize >= 0, "Table size should be positive or zero"

        # use universal hash method
        value = 0
        a = 31415
        b = 27183
        for char in potion_name:
            value = (ord(char) + a * value) % tablesize
            a = a * b % (tablesize - 1)
        return value

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        A hash function that may cause clustering and collisions

        Complexity = O(n) where n is the number of characters in potion_name
        pre-condition = Potion name is of type string and table size is >= 0
        """
        assert type(potion_name) == str, "Potion name should be a string"
        assert tablesize >= 0, "Table size should be positive or zero"

        value = 0

        # Selected values that aren't prime and are multiples of each other
        # May cause clustering and many collisions
        a = 1024
        b = 2048
        for char in potion_name:
            value = (ord(char) + a * value) % tablesize
        return value

