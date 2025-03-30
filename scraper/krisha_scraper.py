import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_apartments_primary(rent=False, num_pages=10, delay=1):

    """
    Scrapes primary data about the apartment from Krisha.kz
    
    Args:
        rent (bool): Indicates which url to use. False for Sale apartment listng and True for Rent listing
        num_pages (int): Number of pages to scrape. Usually it is 1000 pages max to scrape.
        delay (int): How many seconds should be between requests. By default it's 1 second
    Returns:
        pd.DataFrame: DataFrame contains raw primary data about apartment
    """

    # Setting base url
    base_url = ""
    if rent:
        base_url = "https://krisha.kz/arenda/kvartiry/astana/"
    else:
        base_url = "https://krisha.kz/prodazha/kvartiry/astana/"
 
    apartments = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        listings = soup.find_all("div", class_="a-card")

        for listing in listings:
            try:
                title = listing.find("a", class_="a-card__title").get_text(strip=True)
                price = listing.find("div", class_="a-card__price").get_text(strip=True)
                location = listing.find("div", class_="a-card__subtitle").get_text(strip=True)
                link = "https://krisha.kz" + listing.find("a", class_="a-card__title")['href']
                
                apartments.append([title, price, location, link])
            except AttributeError:
                continue
        
        # Respectful scraping delay
        time.sleep(delay)

    # Convert data to a DataFrame
    df = pd.DataFrame(apartments, columns=["Title", "Price", "Location", "Link"])
    
    return df