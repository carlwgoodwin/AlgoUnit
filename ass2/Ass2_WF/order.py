import string
import random
import time


class Order:
    def __init__(self, order_id=None, order_car=None, order_retailer=None, order_creation_time=None):
        """
        Initialise order object with provided or default values.

        Args:
            order_id(str): unique order identifier
            order_car(Car): car object to be ordered
            order_retailer(CarRetailer): retailer object where car is ordered from
            order_creation_time(int): UNIX timestamp when order is created
        """
        self.order_id = order_id
        self.order_car = order_car
        self.order_retailer = order_retailer
        self.order_creation_time = order_creation_time

    def __str__(self):
        """
        Return string representation of order object.

        Returns:
            str: String containing order details
        """
        return f"{self.order_id}, {self.order_car.car_code}, {self.order_retailer.retailer_id}, {self.order_creation_time}"

    def generate_order_id(self, car_code):
        """
        Generate unique order ID based on provided car code and current time

        Args:
            car_code(str): The car code of the car to be ordered

        Returns:
            str: Generated order ID
        """
        # generate random string of 6 letters
        str_1 = "~!@#$%^&*"
        random_string = ''
        for letter in range(6):
            random_letter = random.choice(string.ascii_lowercase)
            random_string += random_letter
        # capitalise 2nd, 4th and 6th letters
        upper_string = (random_string[0] + random_string[1].upper() + random_string[2] + random_string[3].upper()
                        + random_string[4] + random_string[5].upper())
        # convert to ASCII values and modify
        ascii_list = []
        for letter in upper_string:
            ascii_list.append(ord(letter))
        ascii_modified_list = []
        for code in ascii_list:
            code_modified = code * code
            code_modified = code_modified % len(str_1)
            ascii_modified_list.append(code_modified)
        # map modified ASCII values to special chars
        specialchar_list = []
        for i in ascii_modified_list:
            specialchar_list.append(str_1[i])
        # create string of special chars
        specialchar_string = upper_string
        for i in range(len(upper_string)):
            specialchar_string += specialchar_list[i] * i
        # concatenate components to form the order ID
        order_id = specialchar_string + car_code + str(self.order_creation_time)
        self.order_id = order_id
        return order_id

    def generate_order_creation_time(self):
        """
        Generates UNIX timestamp of when order is created

        Returns:
            int: current timestamp of when order is created
        """
        self.order_creation_time = int(time.time())
