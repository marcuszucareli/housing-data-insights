# Scraping data from ZAP, a famous house marketing website in brazil
import undetected_chromedriver as uc
import pandas as pd
from bs4 import BeautifulSoup

options = uc.ChromeOptions()

driver = uc.Chrome(options=options)

# Apartmens data list
apartments_data = []

def get_apartments(page):
    # Get page html
    driver.get(f'https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-jose-dos-campos/?pagina={page}')

    # Parse HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Get cards of each apartment
    apartments = soup.find_all('div', attrs={'data-position': True})
    
    if len(apartments) == 0:
        return

    # Extract information of the cards
    for apartment in apartments:
        
        # Neighborhood, city
        location = apartment.find('h2')
        
        if location:
            try:
                location = location.get_text()
                neighborhood, city = location.split(',')
            except:
                neighborhood = None
                city = None
        
        # Street
        street = apartment.find('p', attrs={'data-cy': "rp-cardProperty-street-txt"})
        if street:
            street = street.text
        
        # Description
        description = apartment.find('p', attrs={'class': 'ListingCard_card__description__slBTG'})
        if description:
            description = description.text
        
        # Area
        area = apartment.find('p', attrs={'itemprop':'floorSize'})
        if area:
            area = area.text
            area = area.replace(' m²', '')
        
        # Rooms
        rooms = apartment.find('p', attrs={'itemprop':'numberOfRooms'})
        if rooms:
            rooms = rooms.text
        
        # Parking spaces
        parking = apartment.find('p', attrs={'itemprop':'numberOfParkingSpaces'})
        if parking:
            parking = parking.text
        
        # Bathrooms
        bathrooms = apartment.find('p', attrs={'itemprop':'numberOfBathroomsTotal'})
        if bathrooms:
            bathrooms = bathrooms.text
        
        # Price
        price_div = apartment.find('div', attrs={'data-cy':'rp-cardProperty-price-txt'})
        price = price_div.find('p', attrs={'class':'l-text l-u-color-neutral-28 l-text--variant-heading-small l-text--weight-bold undefined'})
        if price:
            price = price.text
            price = price.replace('R$ ', '')
            price = price.replace('.', '')
            print(price)
        
        # URL
        url = apartment.find('a', attrs={'itemprop':'url'})
        if url:
            url = url.get('href')
        
        # Dictionary of data
        apartment_data = {
            'neighborhood': neighborhood,
            'city': city,
            'street': street,
            'description': description,
            'area': area,
            'rooms': rooms,
            'parking': parking,
            'bathrooms': bathrooms,
            'price': price,
            'url': url
        }
        
        apartments_data.append(apartment_data)


i = 1
while i != 101:
    get_apartments(i),
    i = i + 1

# Close chrome driver
driver.quit()

# Generate dataframe
df = pd.DataFrame(apartments_data)
    
df.to_csv(f'apartments_data_scraped.csv')
