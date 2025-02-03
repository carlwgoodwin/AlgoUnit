import random
import string


class Retailer:
    def __init__(self, retailer_id=None, retailer_name=None):
        """
        Initializes a Retailer object with an ID and name

        Args:
            retailer_id(int): The unique ID of the retailer
            retailer_name(str): The name of the retailer
        """
        self.retailer_id = retailer_id
        self.retailer_name = retailer_name

    def __str__(self):
        """
        Returns a string representation of the Retailer object

        Returns:
            str: A string containing retailer ID and name
        """
        return f"{self.retailer_id}, {self.retailer_name}"

    def generate_retailer_id(self, list_retailer):
        """
        Generates a unique retailer ID not present in the given list of retailers

        Args:
            list_retailer(list): A list of existing Retailer objects

        Returns:
            int: A unique retailer ID
        """
        existing_id_list = []
        for retailer in list_retailer:
            existing_id_list.append(retailer.retailer_id)
        while True:
            retailer_id = random.randint((10**7), (10**8-1))
            if retailer_id not in existing_id_list:
                self.retailer_id = retailer_id
                break

    def generate_retailer_name(self):
        """
        Generates a random retailer name consisting of 10 letters

        Returns:
            str: A randomly generated retailer name
        """
        random_string = ''
        for letter in range(10):
            random_letter = random.choice(string.ascii_letters)
            random_string += random_letter
        self.retailer_name = random_string
