import os
import random
import time

from retailer import Retailer
from car import Car
from order import Order

# define paths for stock path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
relative_dir = os.path.join("data", "stock.txt")
stock_filepath = os.path.join(parent_dir, relative_dir)


class CarRetailer(Retailer):
	"""
	Initializes a CarRetailer object with the provided or default values

	Args:
	    retailer_id(int): The unique retailer identifier
	    retailer_name(str): The name of the retailer
	    carretailer_address(str): The address of the car retailer
	    carretailer_business_hours(tuple): The opening and closing hours of the retailer
	    carretailer_stock(list): List of cars in the retailer's stock
	    """
	def __init__(self, retailer_id=None, retailer_name=None, carretailer_address=None, carretailer_business_hours=None,
				 carretailer_stock=None):
		super().__init__(retailer_id, retailer_name)
		self.carretailer_address = carretailer_address
		self.carretailer_business_hours = carretailer_business_hours
		if carretailer_stock is not None:
			self.carretailer_stock = carretailer_stock
		else:
			self.carretailer_stock = []

	def __str__(self):
		"""
		Returns a string representation of the CarRetailer object

        Returns:
		    str: A string containing retailer details
		"""
		return f"{self.retailer_id}, {self.retailer_name}, {self.carretailer_address}, {self.carretailer_business_hours}, " \
			   f"{self.carretailer_stock}"

	def generate_retailer_address(self):
		"""
        Generates a random address for the retailer from a predefined list of addresses.
		"""
		test_address_list = ["Wellington Rd Clayton, VIC3168", "Clayton Rd Mount Waverley, VIC3170",
							 "Doncaster Rd Doncaster, VIC3108", "Plummer St Port Melbourne, VIC3207",
							 "Lever St Oakleigh, VIC3166", "Arden St North Melbourne, VIC3051",
							 "South Rd Moorabbin, VIC3189", "Sydney Rd Coburg, VIC3058"]
		self.carretailer_address = random.choice(test_address_list)

	def generate_business_hours(self):
		"""
		Generates random business hours for the retailer
		"""
		opening_hours = []
		closing_hours = []
		for hours in range(14, 21):
			opening_hours.append(hours * 0.5)
		for hours in range(32, 41):
			closing_hours.append(hours * 0.5)
		opening_hour = random.choice(opening_hours)
		closing_hour = random.choice(closing_hours)
		self.carretailer_business_hours = (opening_hour, closing_hour)

	def load_current_stock(self, path):
		"""
        Loads the current stock of cars for the retailer from a file

        Args:
            path(str): The file path to the stock file
		"""
		try:
			with open(path, "r") as file:
				stock_file = file.read()
				stock_file_lines = stock_file.split('\n')
				current_retailer_items = []
				for line in stock_file_lines:
					items = line.replace("(", "" ).replace(")", "").replace("[", "").replace("]", "")
					items = items.split(", ")
					if items[0] == str(self.retailer_id):
						current_retailer_items = items
				for item in current_retailer_items:
					if item[0] == "'":
						self.carretailer_stock.append(item)
				if len(current_retailer_items) == 0:
					print("retailer_id not found in file.")
		except (FileNotFoundError, IOError) as error:
			print(f"Could not access the file: {error}")

	def is_operating(self, cur_hour):
		"""
		Checks if the retailer is currently operating based on the current time

        Args:
            cur_hour(float): The current time in hours

        Returns:
            bool: True if the retailer is operating, False if not
        """
		if self.carretailer_business_hours[0] <= cur_hour <= self.carretailer_business_hours[1]:
			return True
		else:
			return False

	def get_all_stock(self, path):
		"""
		Retrieves all cars in the retailer's stock from a stock file

		Args:
		    path(str): The file path to the stock file

		Returns:
		    list: A list of Car objects in the retailer's stock
		"""
		try:
			with open(path, "r") as file:
				stock_file = file.read()
				stock_file_lines = stock_file.split('\n')
				for line in stock_file_lines:
					items = line.replace("(", "" ).replace(")", "").replace("[", "").replace("]", "")
					items = items.split(", ")
					if items[0] == str(self.retailer_id):
						current_retailer_items = items
				cars_stock = []
				for i in range(len(current_retailer_items)):
					if current_retailer_items[i][0] == "'":
						current_car_info = current_retailer_items[i:i + 6]
						current_car = Car(current_car_info[0], current_car_info[1], int(current_car_info[2]),
										  int(current_car_info[3]), int(current_car_info[4]), current_car_info[5])
						cars_stock.append(current_car)
				return cars_stock
		except (FileNotFoundError, IOError) as error:
			print(f"Could not access the file: {error}")

	def get_postcode_distance(self, postcode):
		"""
		Calculates the distance between the retailer's postcode and a given postcode

		Args:
		    postcode(int): The target postcode

		Returns:
		    int: The absolute difference between the postcodes
		"""
		retailer_postcode = self.carretailer_address.split(", ")[-1][3:]
		return abs(int(retailer_postcode) - postcode)

	def remove_from_stock(self, car_code):
		"""
		Removes a car with the specified car code from the retailer's stock

		Args:
		    car_code(str): The car code to be removed

		Returns:
		    bool: True if the car is successfully removed, False if not
		"""
		updated_stock = []
		for car in self.carretailer_stock:
			if car != car_code:
				updated_stock.append(car)
		self.carretailer_stock = updated_stock
		update_path = stock_filepath.replace(".txt", "_update.txt")
		try:
			with open(stock_filepath, "r") as current_file:
				with open(update_path, "w") as update_file:
					stock_file = current_file.read()
					stock_file_lines = stock_file.split('\n')
					current_retailer_items = []
					for line in stock_file_lines:
						items = line.replace("(", "" ).replace(")", "").replace("[", "").replace("]", "")
						items = items.split(", ")
						if items[0] == str(self.retailer_id):
							current_retailer_items = items
							update_file.write(current_retailer_items[0] + ", " + current_retailer_items[1] + ", "
											  + current_retailer_items[2] + ", " + current_retailer_items[3] + ", ("
											  + current_retailer_items[4] + ", " + current_retailer_items[5] + "), [")
							found_carcode = True
							for i in range(len(current_retailer_items)):
								if current_retailer_items[i][0] == "'":
									if current_retailer_items[i] != car_code:
										if found_carcode:
											update_file.write(current_retailer_items[i] + ", " + current_retailer_items[i+1] + ", "
															  + current_retailer_items[i+2] + ", " + current_retailer_items[i+3] + ", "
															  + current_retailer_items[i+4] + ", " + current_retailer_items[i+5])
											found_carcode = False
										else:
											update_file.write(", " + current_retailer_items[i] + ", " + current_retailer_items[i+1] + ", "
															  + current_retailer_items[i+2] + ", " + current_retailer_items[i+3] + ", "
															  + current_retailer_items[i+4] + ", " + current_retailer_items[i+5])
							update_file.write("]\n")
						elif items[0] != str(self.retailer_id):
							update_file.write(line + "\n")
					if len(current_retailer_items) == 0 or car_code not in current_retailer_items:
						return False
					else:
						os.replace(update_path, stock_filepath)
						return True
		except (FileNotFoundError, IOError) as error:
			print(f"Could not access the file: {error}")

	def add_to_stock(self, car, path):
		"""
		Adds a car to the retailer's stock and updates the stock file

		Args:
		    car(Car): The Car object to be added to the stock
		    path(str): The file path to the stock file

		Returns:
		    bool: True if the car is successfully added, False if not
		"""
		update_path = path.replace(".txt", "_update.txt")
		try:
			with open(path, "r") as current_file:
				with open(update_path, "w") as update_file:
					stock_file = current_file.read()
					stock_file_lines = stock_file.split('\n')
					line_add = None
					for line in stock_file_lines:
						items = line.replace("(", "").replace(")", "").replace("[", "").replace("]", "")
						items = items.split(", ")
						if items[0] == str(self.retailer_id) and car.car_code not in items:
							line_add = line.replace("]", "")
							if len(self.carretailer_stock) == 0:
								update_file.write(line_add + car.car_code + ", " + car.car_name + ", " + str(car.car_capacity) + ", "
												  + str(car.car_horsepower) + ", " + str(car.car_weight) + ", " + car.car_type + "]\n")
							else:
								update_file.write(line_add + ", " + car.car_code + ", " + car.car_name + ", " + str(car.car_capacity) + ", "
												  + str(car.car_horsepower) + ", " + str(car.car_weight) + ", " + car.car_type + "]\n")
							self.carretailer_stock.append(car.car_code)
						elif items[0] != str(self.retailer_id):
							update_file.write(line + "\n")
					if line_add == None:
						return False
					else:
						os.replace(update_path, stock_filepath)
						return True
		except (FileNotFoundError, IOError) as error:
			print(f"Could not access the file: {error}")

	def get_stock_by_car_type(self, car_types):
		"""
		Retrieves cars in the retailer's stock based on car types

		Args:
		    car_types(list): List of car types to filter the stock

		Returns:
		    list: A list of Car objects matching the specified car types
		"""
		total_stock = self.get_all_stock(stock_filepath)
		stock_cartype = []
		for car in total_stock:
			if car.car_type in car_types:
				stock_cartype.append(car)
		return stock_cartype

	def get_stock_by_licence_type(self, licence_type):
		"""
		Retrieves cars in the retailer's stock based on licence type restrictions

		Args:
		    licence_type(str): The type of driver's licence ('P', 'L', 'Full')

		Returns:
		    list: A list of Car objects permitted by the specified licence type
		"""
		total_stock = self.get_all_stock(stock_filepath)
		stock_notforbidden = []
		if licence_type == "P":
			for car in total_stock:
				if not car.probationary_license_prohibited_vehicle():
					stock_notforbidden.append(car)
			return stock_notforbidden
		elif licence_type == "L" or licence_type == "Full":
			return total_stock
		else:
			print("Please enter a valid licence type ('P', 'L', 'Full')")

	def car_recommendation(self):
		"""
		Generates a random car recommendation from the retailer's stock

		Returns:
		    Car: A randomly recommended Car object
		"""
		total_stock = self.get_all_stock(stock_filepath)
		car_recommend = random.choice(total_stock)
		return car_recommend

	def create_order(self, car_code):
		"""
		Creates a new order for a specified car and retailer

		Args:
		    car_code(str): The car code of the car to be ordered

		Returns:
		    Order: An Order object representing the created order, or None if the retailer is not operating
		"""
		current_time = time.localtime()
		current_hour = current_time.tm_hour
		current_minute = current_time.tm_min
		minute_fraction = current_minute / 60.0
		current_time_float = current_hour + minute_fraction
		current_time_rounded = round(current_time_float, 1)
		target_car = None
		if self.is_operating(current_time_rounded):
			current_stock = self.get_all_stock(stock_filepath)
			for car in current_stock:
				if car_code == car.car_code:
					target_car = car
			created_order = Order(order_car=target_car, order_retailer=self)
			created_order.generate_order_creation_time()
			created_order.generate_order_id(car_code)
			self.remove_from_stock(car_code)
			return created_order
		else:
			print(f"Retailer is not currently operating, please place your order between {self.carretailer_business_hours[0]} "
				  f"and {self.carretailer_business_hours[1]}.")
