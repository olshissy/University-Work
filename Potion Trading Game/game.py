from __future__ import annotations
# ^ In case you aren't on Python 3.10

from random_gen import RandomGen
from hash_table import LinearProbePotionTable
from potion import Potion
from avl import AVLTree


class Game:
    """
    There were two ADTs used in our Game class which were the AVL Tree and Hash Table.
    The hash table was to store the potion_data with easy access.
    The AVL tree was for storing potions, using buy prices as key, in the inventory, ...
    since the vendors’ potion selection uses kth_largest.
    """

    def __init__(self, seed=0) -> None:
        self.rand = RandomGen(seed=seed)
        self.inventory = AVLTree()
        self.profits = AVLTree()

    def set_total_potion_data(self, potion_data: list) -> None:
        """
        Processes the potion data by adding it to a hash table

        complexity: O(n) where n is the number of potions in potion_data
        """
        # creating a hash table(potionData) with the size of the provided data's length
        self.potionData = LinearProbePotionTable(len(potion_data), True)
        for potion in potion_data:  # provided data (potion[0]=name, potion[1]=type, potion[2] = buyprice)
            # creating a new potion with the provided data
            new_potion = Potion.create_empty(potion[1], potion[0], potion[2])  # create_empty(type,name,buyprice)
            # inserting the new potion into the hash table potionData
            self.potionData.insert(potion[0], new_potion)  # insert(key,data)

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Adds the required quantity of each potion to the inventory (AVL tree)

        complexity: O(Clog(N)) where C is the length of potion_name_amount_pairs and N is the number of potions provided in set_total_potion_data

        The complexity of the for loop is C as it loops through the length of potion_name_amount_pairs. Inside this loop it uses the insert method of the
        AVL tree which is O(depth) or O(log(N)) where N is the number of potions in self.potion_data created in set_total_potion_data. Therefore overall complexity
        for this function is O(Clog(N))
        """
        for pair in potion_name_amount_pairs:  # pair[0]=name/key, pair[1]=quantity
            # setting the quantities of each potion in potion data
            self.potionData[pair[0]].quantity = pair[1]
            # setting the potion's data in inventory with the potion's buy price as the key
            self.inventory[self.potionData[pair[0]].buy_price] = self.potionData[pair[0]]

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """
        Randomly chooses the potion each vendor will have in their inventory

        complexity: O(Clog(N)) where C is equal to num_vendors and N is the number of potions provided in set_total_potion_data

        The complexity for the for loop is C as it loops through all the vendors. Inside the loop, the kth_largest function is used which follows
        the complexity of O(log(N)) where is this scenario N is the number of options in set_total_potion_data. Therefore, the overall complexity for this
        function is O(Clog(N))
        """
        # creating an empty list for the return results
        result = []
        # creating an empty list for the potions that will be returned to the inventory
        return_items = []

        # picking potions for each vendor from the inventory
        for i in range(num_vendors, 0, -1):
            # generating a random number
            p = self.rand.randint(i)
            # finding the pth most expensive potion in the inventory
            pthMostExpensive = self.inventory.kth_largest(p)
            # appending the potion's name and quantity as a tuple into results, what the function has to return
            result.append((pthMostExpensive.item.name, pthMostExpensive.item.quantity))
            # appending the potion name and quantity into return items
            return_items.append((pthMostExpensive.key, pthMostExpensive.item))
            # delete the pth most expensive potion in the inventory
            del self.inventory[pthMostExpensive.key]

        # returning the potions from the vendor back into the inventory
        for item in return_items:
            # item[0] = key, item[1] = the item
            # inserting the item back into the inventory with the item key
            self.inventory[item[0]] = item[1]
        # return the item that was appended from line 44
        return result

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        """
        Solve game adds all potions to an avl tree with the profits as the key.
        It then loops through all money values for each turn and finds the highest amount of each potion it can buy checking the one with the highest profit first.
        It then appends this value to the results list.

        complexity: O(Nlog(N) + MN) where N is the length of potion_valuations and M is the length of starting_money

        The complexity of the first for loop is N as it loops through all potions in potion_valuations. Inside this loop, the insert function is used from the AVL tree.
        This function follows the complexity of O(log(N)) where here N is the length of potion_valuations. The complexity of the first loop is then O(Nlog(N)).
        The second loop has complexity of M as it loops through all values in starting_money. Inside the loop, the while loop has worst case complexity N as it
        will continue to run till the money is gone which will worst case be until all potion quantity is exhausted. Therefore the complexity of this section is O(MN).
        The overall complexity for this function is therefore O(Nlog(N) + MN)
        """
        results = []
        # Loops through the potions and adds them to the profit AVL tree
        for potion in potion_valuations:
            buy_price = self.potionData[potion[0]].buy_price
            profit = potion[1] - buy_price
            key = profit + 1 / buy_price  # Prioritise items with lower buy price and avoids duplicate keys as buy prices are different
            self.profits[key] = potion[0]

        # Each value in starting_money indicates a new turn
        for money in starting_money:
            final_money = 0
            kth = 1
            while money > 0:
                highest_profit = self.profits.kth_largest(
                    kth)  # Initially the largest profit then decends down the tree
                profit = highest_profit.key
                potion = self.potionData[highest_profit.item]
                highest_quantity = money / potion.buy_price  # The highest quantity of the current potion the player can buy with their current money

                # If they are able to purchase all the potion
                if highest_quantity >= potion.quantity:
                    selling_price = (
                                                profit - 1 / potion.buy_price) + potion.buy_price  # Price they sell the potion for (subtracting the added item for creating keys)
                    final_money += selling_price * potion.quantity  # Add the price sold for the amount of potion sold
                    money -= potion.buy_price * potion.quantity  # Remove the buy price of the quantity bought
                else:
                    selling_price = (profit - 1 / potion.buy_price) + potion.buy_price

                    # Uses the highest possible quantity able to be purchased of the potion
                    final_money += selling_price * highest_quantity  # Add the price sold for the amount of potion sold
                    money -= potion.buy_price * highest_quantity  # Remove the buy price of the quantity bought
                kth += 1  # Increment to get the next largest potion if there is money left
            results.append(final_money)
        return results



