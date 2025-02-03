import os
import pandas as pd
import matplotlib.pyplot as plt


class Display():
    #take in data, suburb, currency - create histogram of sales price frequency and save to file
    def prop_val_distribution(self, dataframe, suburb, target_currency):
        currency_dict = {
            "AUD": 1, "USD": 0.66, "INR": 54.25, "CNY": 4.72, "JPY": 93.87,
            "HKD": 5.12, "KRW": 860.92, "GBP": 0.51, "EUR": 0.60, "SGD": 0.88
        }
        if target_currency not in currency_dict:
            target_currency = "AUD"
            print("Currency not valid. Graph will be generated in AUD.")
        target_rate = currency_dict[target_currency]

        hist_title = "Property Value Distribution"
        if suburb == "all":
            filtered_dataframe = dataframe
        elif suburb not in dataframe['suburb'].unique():
            print(f"Suburb not found, Histogram generated based on all suburbs.")
            filtered_dataframe = dataframe
        else:
            filtered_dataframe = dataframe[dataframe['suburb'] == suburb]
            hist_title = f"Property Value Distribution in {suburb}"

        valid_dataframe = filtered_dataframe[pd.notna(filtered_dataframe['price'])].copy()
        valid_dataframe.loc[:, 'price'] = valid_dataframe['price'] * target_rate
        upper_limit = valid_dataframe['price'].quantile(0.95)
        lower_limit = valid_dataframe['price'].quantile(0.05)
        valid_dataframe['price'].plot(kind='hist', color='lightgrey', edgecolor='black', range=(lower_limit, upper_limit))

        plt.title(hist_title)
        plt.xlabel(f"Sale Price ({target_currency})")
        plt.ylabel("Frequency")
        if suburb == "all" or suburb not in dataframe['suburb'].unique():
            hist_filepath = os.path.join(self.get_graphs_directory(), f"hist_all_{target_currency.lower()}.png")
            print(f"\nHistogram saved in folder 'graphs' as 'hist_all_{target_currency.lower()}.png'.")
        else:
            hist_filepath = os.path.join(self.get_graphs_directory(),
                                         f"hist_{suburb.lower().replace(' ', '')}_{target_currency.lower()}.png")
            print(f"\nHistogram saved in folder 'graphs' as "
                  f"'hist_{suburb.lower().replace(' ', '')}_{target_currency.lower()}.png'.")
        plt.savefig(hist_filepath)

    #takes in data - create line graph of number of properties sold per year and save to file
    def sales_trend(self, dataframe):
        sales_dataframe = pd.DataFrame(columns=['year', 'properties_sold'])

        valid_dataframe = dataframe[pd.notna(dataframe['sold_date'])].copy()
        valid_dataframe['sold_year'] = valid_dataframe['sold_date'].str.split('/').str[2]

        sales_years = valid_dataframe['sold_year'].unique()
        for year in sales_years:
            sale_count = len(valid_dataframe[valid_dataframe['sold_year'] == year])
            sales_dataframe = sales_dataframe._append({'year': year, 'properties_sold': sale_count}, ignore_index=True)

        sales_dataframe = sales_dataframe.sort_values(by='year')
        sales_dataframe.plot(x='year', y='properties_sold', kind='line', marker='o', markersize=4,
                             color='black', title='Yearly Sales Trend', grid=False, legend=False)
        plt.xlabel('Year')
        plt.ylabel('Properties Sold')
        plt.gca().yaxis.grid(True, linestyle='-')
        line_filepath = os.path.join(self.get_graphs_directory(), "sales_trend.png")
        plt.savefig(line_filepath)
        print(f"\nLine Graph saved in folder 'graphs' as 'sales_trend.png'.")

    #get directory to store graphs in, create if doesn't exist
    def get_graphs_directory(self):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            graphs_dir = os.path.join(current_dir, "graphs")
            if not os.path.exists(graphs_dir):
                os.makedirs(graphs_dir)
            return graphs_dir
        