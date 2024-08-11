# Scraping data from ZAP, a famous house marketing website in brazil
import undetected_chromedriver as uc
import pandas as pd
from bs4 import BeautifulSoup

options = uc.ChromeOptions()
# options.headless = True
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--disable-extensions")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
# options.add_argument("--enable-features=WebRTC-H264WithOpenH264FFmpeg")

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
        
        # Dictionary of data
        apartment_data = {
            'neighborhood': neighborhood,
            'city': city,
            'street': street,
            'description': description,
            'area': area,
            'rooms': rooms,
            'parking': parking,
            'bathrooms': bathrooms
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
