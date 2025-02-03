import math
import string
import random


class Car:
    def __init__(self, car_code=None, car_name=None, car_capacity=0, car_horsepower=0, car_weight=0, car_type=None):
        """
        Initializes a Car object with various attributes

        Args:
            car_code(str): The unique code of the car
            car_name(str): The name of the car
            car_capacity(int): The car's seating capacity
            car_horsepower(int): The car's horsepower
            car_weight(int): The weight of the car
            car_type(str): The type of the car (e.g., 'AWD', 'FWD', 'RWD')
        """
        self.car_code = car_code
        self.car_name = car_name
        self.car_capacity = car_capacity
        self.car_horsepower = car_horsepower
        self.car_weight = car_weight
        self.car_type = car_type

    def __str__(self):
        """
        Returns a string representation of the Car object

        Returns:
            str: A string containing car attributes
        """
        return f"{self.car_code}, {self.car_name}, {self.car_capacity}, {self.car_horsepower}, {self.car_weight}, {self.car_type}"

    def generate_car_code(self):
        """
        Generates a unique car code for the car

        Returns:
            str: A randomly generated car code
        """
        car_code = "'"
        for i in range(2):
            car_code += random.choice(string.ascii_uppercase)
        for i in range(6):
            car_code += random.choice(string.digits)
        self.car_code = car_code

    def generate_car_name(self):
        """
        Generates a random car name consisting of letters

        Returns:
            str: A randomly generated car name
        """
        car_name = ""
        length = random.randint(10, 20)
        for i in range(length):
            car_name += random.choice(string.ascii_letters)
        self.car_name = car_name

    def generate_car_type(self):
        """
        Generates a random car type (e.g., 'AWD', 'FWD', 'RWD')

        Returns:
            str: A randomly generated car type
        """
        car_types = ["AWD'", "FWD'", "RWD'"]
        self.car_type = random.choice(car_types)

    def probationary_license_prohibited_vehicle(self):
        """
        Checks if the car is prohibited for probationary license holders based on power-to-mass ratio

        Returns:
            bool: True if the car is prohibited, False if not
        """
        power_to_mass_ratio = math.ceil((self.car_horsepower / self.car_weight)*1000)
        if power_to_mass_ratio > 130:
            return True
        else:
            return False

    def found_matching_car(self, car_code):
        """
        Checks if a car matches the given car code

        Args:
            car_code(str): The car code to check against

        Returns:
            bool: True if the car matches the car code, False if not
        """
        return self.car_code == car_code

    def get_car_type(self):
        """
        Returns the car type

        Returns:
            str: The car type (e.g., 'AWD', 'FWD', 'RWD')
        """
        return f"{self.car_type}"
