import pandas as pd

# Creates a dataframe with country, city and population
def cities_df():
    capital = pd.read_csv("csv/capital.csv")
    population = pd.read_csv("csv/population.csv")
    merged_df = pd.merge(capital, population, on='country')
    merged_df['Population\r\n(2023)'] = merged_df['Population\r\n(2023)'].str.replace(',', '').astype(int)
    merged_df = merged_df.rename(columns={'Population\r\n(2023)': 'population'})
    merged_df = merged_df[['country', 'capital', 'population']]
    return merged_df[merged_df['population'] > 1000000]

# Returns a dictionary with country as key and city as value
def get_countries_capital_population():
    filtered_df = cities_df()
    
    country_city_dict = {}
    for index, row in filtered_df.iterrows():
        country_city_dict[row['country']] = row['capital']

    return country_city_dict
    
# Returns a list of cities sorted alphabetically
def cities_alphabetical():
    countries = ['Russia', 'Japan', 'United Arab Emirates',
                'United States', 'Mexico', 'Canada', 
                'Italy', 'France', 'United Kingdom',
                'Brazil', 'Argentina', 'Peru',
                'Kenya', 'Egypt', 'Morocco',                
                'Australia', 'New Zealand', 'Philippines']
    dicty = get_countries_capital_population()
    returned = [dicty[i] for i in countries]
    returned = sorted(returned)
    return returned

def main():
    pass

if __name__ == "__main__":
    main()