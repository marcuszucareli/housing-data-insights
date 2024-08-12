# API for getting coordinates of the streets
import pandas as pd
import requests
import time

base_url = 'https://nominatim.openstreetmap.org/search?'


# Function to get coordinates from API
def get_coordinates(adresses):
    
    response_adresses = []
    
    for adress in adresses:
        
        # Create the url params
        params = {
            'street': adress['street'],
            'city': adress['city'],
            'country': 'Brasil',
            'limit': 1,
            'accept-language': 'pt-BR',
            'format': 'jsonv2',
            'email': 'papaulozucareli@gmail.com'
        }
        
        response = requests.get(url=base_url, params=params)
        
        # Get latitude, longitude of streets, also dealing errors
        if response.status_code == 200:
            
            street_data_list = response.json()
            
            if len(street_data_list) == 1:
                
                street_data = street_data_list[0]
                
                lat = street_data['lat']
                lon = street_data['lon']
                
            else:
                lat = None
                lon = None
        else:
            lat = 'error'
            lon = 'error'
        
        adress_with_coords = {
            'street': adress['street'],
            'lat': lat,
            'lon': lon
        }
        
        response_adresses.append(adress_with_coords)
        
        # API only allows 1 call per second
        time.sleep(1)
    
    return response_adresses


def coordinates_dataframe(dataframe):
    
    # Get street and city columns of the df
    df = dataframe[['street', 'city']]
    print(df)
    df.info()

    # Drop duplicates to consume less API resources
    print(len(df))
    print(df['street'].value_counts())
    df = df.drop_duplicates()
    print(len(df))

    # Convert df to dict
    list_of_adresses = df.to_dict('records')

    # Get coordinates via API
    adresses_with_coords = get_coordinates(list_of_adresses)
    for i in adresses_with_coords:
        print(i)

    # Join dataframes
    adresses_with_coords = pd.DataFrame(adresses_with_coords)
    adresses_with_coords.info()
    
    final_df = pd.merge(dataframe, adresses_with_coords, how='left', on='street')

    # Save df
    final_df.to_csv('apartments_data.csv')

df = pd.read_csv('apartments_data_scraped.csv')
