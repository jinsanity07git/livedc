import pandas as pd
from bs4 import BeautifulSoup
import os

# Function to clean and convert price strings to numeric values
def clean_price(price_str):
    # Remove dollar sign and commas
    price_str = price_str.replace('$', '').replace(',', '').strip()
    # Handle special case for negative values with space after minus sign
    if price_str.startswith('- '):
        price_str = price_str.replace('- ', '-')
    return pd.to_numeric(price_str)


def parse_quirkworks(rurl='./iventory.html'):
    furl = os.path.join(os.path.dirname(__file__),rurl)
    # Load the local HTML file
    with open(furl, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all vehicle items
    vehicle_items = soup.find_all('div', class_='vehicle-item')

    # List to hold the data
    data = []
    host = "https://www.quirkworkssubaru.com"
    # Loop through each vehicle item and extract the required information
    for item in vehicle_items:
        title = item.find('h6', class_='vehicle-item__title').text.strip()
        href = item.find('a', class_='js-vehicle-item-link')['href'].strip()
        full_title = f'<a href="{host + href}">{title}</a>'

        # Extract additional highlight items
        highlights = item.find_all('div', class_='vehicle-highlights__additional-item')
        highlight_data = {highlight.find('span', class_='vehicle-highlights__additional-label').text.strip(): highlight.find('span', class_='vehicle-highlights__additional-value').text.strip() for highlight in highlights}

        # Extract price information
        price_info = item.find('div', class_='mod-vehicle-price-theme1')
        msrp = price_info.find('div', class_='price __starting-price').find('div', class_='price_value').text.strip()
        savings = price_info.find('div', class_='price __price-rules').find('div', class_='price_value').text.strip()
        final_price = price_info.find('div', class_='price __final-price').find('div', class_='price_value').text.strip()
        
        # Combine all data into a single dictionary
        vehicle_data = {
            'Title': full_title,
            'Engine': highlight_data.get('Engine', ''),
            'Transmission': highlight_data.get('Transmission Description', ''),
            'Drivetrain': highlight_data.get('Drivetrain', ''),
            'Fuel Economy': highlight_data.get('Fuel Economy', ''),
            'MSRP': msrp,
            'Total Savings': savings,
            'Final Price': final_price
        }
        
        data.append(vehicle_data)

    # Create a DataFrame and save it to an Excel file
    df = pd.DataFrame(data)


    # Apply the clean_price function to the price columns
    df['MSRP'] = df['MSRP'].apply(clean_price)
    df['Total Savings'] = df['Total Savings'].apply(clean_price)
    df['Final Price'] = df['Final Price'].apply(clean_price)


    df["Saving %"] =  round(df['Total Savings']/df['MSRP'],3) *100

    df.sort_values(by="Saving %",inplace=True)

    return df


if __name__ == "__main__":
    parse_quirkworks()