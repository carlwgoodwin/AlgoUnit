# Assignment 2 FIT9136: Car Retailer Recommendation and Ordering System
# Student Name: Carl Goodwin
# Student ID: 34362452
# Date Created: Sep 6 2023
# Last Modified: Sep 24 2023
# Description: This program implements a car retailer system. It allows users to find the nearest car retailer,
# get car purchase advice, place car orders, and interact with car retailers and their stock.

from car_retailer import CarRetailer
from car import Car

import os
import random

# define file paths for stock and order files
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
relative_stock_dir = os.path.join("data", "stock.txt")
relative_order_dir = os.path.join("data", "order.txt")
stock_filepath = os.path.join(parent_dir, relative_stock_dir)
order_filepath = os.path.join(parent_dir, relative_order_dir)


def main_menu():
	"""get user input for main menu"""
	user_input = input("\nPlease enter an option (a, b, c, d):\na) Look for the nearest car retailer\n"
					   "b) Get car purchase advice\nc) Place a car order\nd) Exit\n")
	return user_input

def nearest_retailer_menu():
	"""get user input for nearest retailer"""
	user_input = input("\nPlease enter your postcode to find the nearest retailer or type 'exit' to return to main menu.\n\n")
	return user_input

def purchase_advice_menu(retailer_list):
	"""get user input for selecting a retailer for purchase advice"""
	user_input = input(f"\nPlease select a retailer to continue (1, 2, 3) or type 'exit' to return to main menu.\n"
					   f"1) {retailer_list[0].retailer_id} at {retailer_list[0].carretailer_address}\n2) {retailer_list[1].retailer_id} "
					   f"at {retailer_list[1].carretailer_address}\n3) {retailer_list[2].retailer_id} at {retailer_list[2].carretailer_address}\n")
	return user_input

def purchase_advice_submenu():
	"""get user input for purchase advice submenu"""
	user_input = input("\nPlease select from the following options for advice (i, ii, iii, iv) or type 'exit' to return to main menu.\n"
					   "i) Recommend a car\nii) Get all cars in stock\niii) Get cars in stock by car types\n"
					   "iv) Get probationary licence permitted cars in stock\n")
	return user_input

def generate_test_data():
	"""generate test data of 3 retailers and 4 cars per retailer"""
	# generate retailers
	test_retailers = []
	for i in range(3):
		test_retailer = CarRetailer()
		test_retailer.generate_retailer_id(test_retailers)
		test_retailer.generate_retailer_name()
		test_retailer.generate_retailer_address()
		test_retailer.generate_business_hours()
		test_retailers.append(test_retailer)

	# update stock file with generated data
	update_path = stock_filepath.replace(".txt", "_update.txt")
	try:
		with open(update_path, "w") as update_file:
			for retailer in test_retailers:
				update_file.write(str(retailer) + "\n")
			os.replace(update_path, stock_filepath)
	except FileNotFoundError:
		print("File not found.")

	# generate cars for each retailer, update stock file using add_to_stock function
	for retailer in test_retailers:
		for i in range(4):
			test_car = Car()
			test_car.generate_car_code()
			test_car.generate_car_name()
			test_car.car_capacity = random.randint(5, 20)
			test_car.car_horsepower = random.randint(140, 280)
			test_car.car_weight = random.randint(1500, 2800)
			test_car.generate_car_type()
			retailer.add_to_stock(test_car, stock_filepath)

	return test_retailers


def main():
	"""main function to run program"""
	retailers = generate_test_data()
	# handle input from main menu
	while True:
		main_menu_input = main_menu()

		# find nearest retailer based on input postcode
		if main_menu_input == "a":
			while True:
				nearest_retailer_input = nearest_retailer_menu()
				if nearest_retailer_input == 'exit':
					break
				# calculate nearest retailer based on postcode and display ID and address
				if len(nearest_retailer_input) == 4 and nearest_retailer_input.isdigit():
					retailer_distances = {}
					for retailer in retailers:
						postcode_distance = retailer.get_postcode_distance(int(nearest_retailer_input))
						retailer_distances[retailer] = postcode_distance
					nearest_retailer = min(retailer_distances, key=retailer_distances.get)
					print(f"\nYour nearest retailer is {nearest_retailer.retailer_id} located at {nearest_retailer.carretailer_address}.\n")
					break
				else:
					print("Please enter a valid 4-digit numeric postcode.")

		# provide car purchase advice
		elif main_menu_input == "b":
			exit_advice = False
			user_retailer = None
			while True:
				purchase_advice_input = purchase_advice_menu(retailers)
				if purchase_advice_input == 'exit':
					exit_advice = True
					break
				# display retailers and get user input for choice
				if purchase_advice_input.isdigit() and 1 <= int(purchase_advice_input) <= 3:
					user_retailer = retailers[int(purchase_advice_input)-1]
					break
				else:
					print("\nPlease enter a valid menu option (1, 2, 3)\n")
			# display submenu and get user input for choice
			if not exit_advice and user_retailer:
				while True:
					purchase_advice_subinput = purchase_advice_submenu()
					if purchase_advice_subinput == 'exit':
						break
					# recommend a car from selected retailer
					elif purchase_advice_subinput == "i":
						recommended_car = random.choice(user_retailer.carretailer_stock)
						print(f"\nYour recommended car is {recommended_car} from the retailer {user_retailer.retailer_id}.\n")
						break
					# display all cars in stock from selected retailer
					elif purchase_advice_subinput == "ii":
						user_retailer_carstock = user_retailer.get_all_stock(stock_filepath)
						print(f"\nThe retailer (ID: {user_retailer.retailer_id}, Name: {user_retailer.retailer_name}) "
							  f"has the current cars in stock:\n")
						for car in user_retailer_carstock:
							print(f"Code: {car.car_code}, Name: {car.car_name}, Capacity: {car.car_capacity}, "
								  f"Horsepower: {car.car_horsepower}, Weight: {car.car_weight}, Car Type: {car.car_type}")
						break
					# get cars in stock filtered by car type from selected retailer based on user input
					elif purchase_advice_subinput == "iii":
						car_types_list = []
						while True:
							car_type_input = input("Please enter the car types you would like to see stock of (AWD, RWD, FWD) "
												   "or type 'exit' to return to main menu.\n"
												   "Note: for more than one type please separate them by a blank space (AWD FWD).\n")
							if car_type_input == 'exit':
								exit_advice = True
								break
							car_types_list = car_type_input.split()
							if not car_types_list:
								print("\nPlease provide a car type.\n")
								continue
							valid_input = True
							for car_type in car_types_list:
								if car_type not in ["AWD", "RWD", "FWD"]:
									valid_input = False
							if valid_input:
								break
							else:
								print("\nPlease enter valid car types (AWD, RWD, FWD).\n")
						if not exit_advice:
							for i in range(len(car_types_list)):
								car_types_list[i] = car_types_list[i] + "'"
							user_retailer_carstock_bytype = user_retailer.get_stock_by_car_type(car_types_list)
							print(f"\nThe retailer (ID: {user_retailer.retailer_id}, Name: {user_retailer.retailer_name}) "
								  f"has the current cars in stock with requested type(s):\n")
							for car in user_retailer_carstock_bytype:
								print(f"Code: {car.car_code}, Name: {car.car_name}, Capacity: {car.car_capacity}, "
									  f"Horsepower: {car.car_horsepower}, Weight: {car.car_weight}, Car Type: {car.car_type}")
						break
					# get probationary permitted cars in stock from selected retailer
					elif purchase_advice_subinput == "iv":
						user_retailer_carstock_probationary = user_retailer.get_stock_by_licence_type("P")
						print(f"\nThe retailer (ID: {user_retailer.retailer_id}, Name: {user_retailer.retailer_name}) "
							  f"has the current stock of probationary permitted cars:\n")
						for car in user_retailer_carstock_probationary:
							print(f"Code: {car.car_code}, Name: {car.car_name}, Capacity: {car.car_capacity}, "
								  f"Horsepower: {car.car_horsepower}, Weight: {car.car_weight}, Car Type: {car.car_type}")
						break
					else:
						print("\nPlease enter a valid menu option (i, ii, iii, iv)\n")

		# place an order for a car from a certain retailer
		elif main_menu_input == "c":
			exit_order = False
			user_order_retailer = None
			user_order_car = None
			# get user input of retailer id and car code for order
			while True:
				user_input_order = input("\nPlease enter the retailer id and car code of the car you'd like to order separated by a space "
										 "(eg. 58386466 AE064405).\n")
				if user_input_order == 'exit':
					exit_order = True
					break
				user_input_list = user_input_order.split()
				if len(user_input_list) != 2:
					print("\nPlease enter a retailer ID and car code separated by a space.\n"
						  "Note: enter 'exit' to return to the main menu.\n")
					continue
				user_input_retailerid = user_input_list[0]
				user_input_carcode = "'" + user_input_list[1]
				for retailer in retailers:
					if str(retailer.retailer_id) == user_input_retailerid:
						user_order_retailer = retailer
				if user_order_retailer is None:
					print("\nPlease enter a valid retailer ID.\n"
						  "Note: enter 'exit' to return to the main menu.\n")
					continue
				order_car_list = user_order_retailer.get_all_stock(stock_filepath)
				for car in order_car_list:
					if car.car_code == user_input_carcode:
						user_order_car = car
				if user_order_car is None:
					print("\nPlease enter a valid car code.\n"
						  "Note: enter 'exit' to return to the main menu.\n")
					continue
				break
			# generate order object based on user input and write to order file
			if not exit_order:
				user_order = user_order_retailer.create_order(user_order_car.car_code)
				update_path = order_filepath.replace(".txt", "_update.txt")
				try:
					with open(update_path, "w") as update_file:
						update_file.write(str(user_order))
						os.replace(update_path, order_filepath)
						print(f"Car {user_order_car.car_code} has successfully been ordered from Retailer {user_order_retailer.retailer_id}!")
				except (FileNotFoundError, IOError) as error:
					print(f"Could not access the file: {error}")

		# exit the program
		elif main_menu_input == "d":
			print("\nExiting the program.\n")
			break

		else:
			print("Please enter a valid menu option.")

if __name__ == "__main__":
	main()
