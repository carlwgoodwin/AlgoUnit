import pandas as pd


class Interpret():
    #convert csv to pandas dataframe
    def extract_property_info(self, file_path):
        try:
            dataframe = pd.read_csv(file_path)
            return dataframe
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as error:
            print(f"Error: {error}")
            return None

    #take in dataframe and suburb - display mean, standard deviation, median, min, max
    #of bedrooms, bathrooms and parking spaces
    def suburb_summary(self, dataframe, suburb):
        filtered_dataframe = self.suburb_input_filter(dataframe, suburb)
        if filtered_dataframe.empty:
            return

        bedroom_summary = filtered_dataframe['bedrooms'].agg(['mean', 'std', 'median', 'min', 'max'])
        bathroom_summary = filtered_dataframe['bathrooms'].agg(['mean', 'std', 'median', 'min', 'max'])
        parking_summary = filtered_dataframe['parking_spaces'].agg(['mean', 'std', 'median', 'min', 'max'])

        print(f"SUBURB SUMMARY ({suburb.upper()})\nBedrooms:\n")
        print(bedroom_summary)
        print("\nBathrooms:\n")
        print(bathroom_summary)
        print("\nParking Spaces:\n")
        print(parking_summary)
    #take in data and suburb - convert hectares to m^2, display average land size
    def avg_land_size(self, dataframe, suburb):
        filtered_dataframe = self.suburb_input_filter(dataframe, suburb)
        if filtered_dataframe.empty:
            return
        valid_dataframe = filtered_dataframe[pd.notna(filtered_dataframe['land_size_unit'])]
        valid_dataframe.loc[valid_dataframe['land_size_unit'] == 'ha', 'land_size'] *= 10000
        valid_dataframe.loc[valid_dataframe['land_size_unit'] == 'ha', 'land_size_unit'] = "m^2"

        avg_land_size = valid_dataframe['land_size'].mean()
        rounded_avg = round(avg_land_size, 2)
        if suburb == 'all':
            print(f"\nThe average land size in all suburbs is {rounded_avg} m^2.\n")
        else:
            print(f"\nThe average land size in {suburb} is {rounded_avg} m^2.\n")
        #column_view = valid_dataframe['land_size_unit'].unique()

    #take in data, price and suburb - return and display true or false whether price is found
    def locate_price(self, target_price, data, target_suburb):
        filtered_data = self.suburb_input_filter(data, target_suburb)
        if filtered_data.empty:
            return
        valid_data = filtered_data[pd.notna(filtered_data['price'])]
        sorted_data = valid_data.sort_values(by='price', ascending=False)

        low_price, high_price = 0, len(sorted_data)-1
        found_price = False
        while low_price <= high_price:
            mid_value = (low_price + high_price) // 2
            mid_price = sorted_data.iloc[mid_value]['price']

            if mid_price == target_price:
                found_price = True
                break
            elif mid_price < target_price:
                high_price = mid_value - 1
            else:
                low_price = mid_value + 1
        return found_price

    #filter dataframe based on suburb input
    def suburb_input_filter(self, dataframe, suburb):
        if suburb != "all" and suburb not in dataframe['suburb'].unique():
            print(f"The suburb {suburb} was not found. Please check format (eg. Clayton)")
        if suburb != "all":
            filtered_dataframe = dataframe[dataframe['suburb'] == suburb]
        else:
            filtered_dataframe = dataframe
        return filtered_dataframe
