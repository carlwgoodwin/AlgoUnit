import os
from interpret import Interpret
from display import Display


#define file path for data file
current_dir = os.path.dirname(os.path.abspath(__file__))
data_filepath = os.path.join(current_dir, "property_information.csv")

#main menu: interpret or display or exit
def main_menu():
    main_menu_options = ["1", "2", "3"]
    main_menu_text = (f"\nPlease select from the following options {main_menu_options}:\n"
                            "1) Data Interpreters\n2) Data Displayers\n3) Exit Program\n")
    main_menu_input = menu_input_check(main_menu_text, main_menu_options)
    return main_menu_input

#submenu interpret: suburb property summary or avg land size or identify specific price
def interpret_menu():
    interpret_menu_options = ["i", "ii", "iii"]
    interpret_menu_text = (f"\nPlease select from the following interpret options {interpret_menu_options}:\n"
                            "i) Suburb Property Summary\nii) Average Land Size\niii) Locate Price\n")
    interpret_menu_input = menu_input_check(interpret_menu_text, interpret_menu_options)
    return interpret_menu_input

#submenu display: histogram of dist, line graph of sales trends
def display_menu():
    display_menu_options = ["a", "b"]
    display_menu_text = (f"\nPlease select from the following display options {display_menu_options}:\n"
                                 "a) Property Value Histogram\nb) Sales Line Graph\n")
    display_menu_input = menu_input_check(display_menu_text, display_menu_options)
    return display_menu_input

#request suburb from user
def suburb_input():
    suburb_input = input("Please enter the suburb you would like to search in (eg. Clayton),"
                              "\nor enter 'all' to search all suburbs.\n")
    if suburb_input.lower() == "all":
        suburb_input = suburb_input.lower()
    else:
        suburb_input = suburb_input.title()
    return suburb_input

#check input for menus
def menu_input_check(menu_text, menu_options):
    while True:
        user_input = input(menu_text)
        if not user_input.isnumeric():
            user_input = user_input.lower()
        if user_input in menu_options:
            return user_input
        else:
            print(f"Invalid input please select from {menu_options}")

def main():
    #extract property info, store in new interpret class, welcome
    user_interpreter = Interpret()
    user_dataframe = user_interpreter.extract_property_info(data_filepath)
    print(user_dataframe['suburb'].unique())
    print("Welcome to the Investor Application.\nPlease note inputs are case-sensitive.\n\n")
    print(user_dataframe['price'].dtype)
    while True:
        #call main menu and get option
        main_menu_input = main_menu()

        #option 1: interpret submenu call get option
        if main_menu_input == "1":
            interpret_menu_input = interpret_menu()

            if interpret_menu_input == "i":
                #i: ask for suburb to search or all, call suburb summary
                print("Suburb summary selected.")
                user_suburb = suburb_input()
                user_interpreter.suburb_summary(user_dataframe, user_suburb)

            if interpret_menu_input == "ii":
                #ii: ask for suburb or all, call land size
                print("Average land size selected.")
                user_suburb = suburb_input()
                user_interpreter.avg_land_size(user_dataframe, user_suburb)

            if interpret_menu_input == "iii":
                #iii: ask for price to search, ask to suburb or all, call locate price
                print("Locate price selected.")
                user_target_price = input("Please enter a price to locate eg.(965000).\n").replace(",", "").replace(" ", "")
                user_suburb = suburb_input()
                print(user_interpreter.locate_price(float(user_target_price), user_dataframe, user_suburb))

        #option 2: submenu display call get option
        if main_menu_input == "2":
            user_displayer = Display()
            display_menu_input = display_menu()

            if display_menu_input == "a":
                #i: ask for suburb and currency, call histogram and save to file, let user know
                print("Histogram selected.\n")
                user_suburb = suburb_input()
                user_currency = input("Please enter a currency for the graph (eg. USD).\n").upper()
                user_displayer.prop_val_distribution(user_dataframe, user_suburb, user_currency)
                #if currency doesn't exist show in AUD and inform

            if display_menu_input == "b":
                #ii: call line graph, save to file let user know
                print("Line Graph selected.")
                user_displayer.sales_trend(user_dataframe)

        #option 3: break
        if main_menu_input == "3":
            break

if __name__ == "__main__":
    main()
