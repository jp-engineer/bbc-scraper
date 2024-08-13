import requests
from bs4 import BeautifulSoup

# Define the URL for BBC News
url = 'https://www.bbc.com/news'

# Define the Chrome User-Agent
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.5735.110 Safari/537.36'
    )
}

def fetch_bbc_headlines():
    # Send an HTTP GET request to the BBC News website
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Locate the div with the ID "nations-news-uk"
        news_section = soup.find('div', id='nations-news-uk')
        
        if news_section:
            # Find all anchor tags within this div
            headlines = news_section.find_all('a')
            headlines_found = []
            
            # Extract and print the text of each headline
            for i, headline in enumerate(headlines, 1):
                headline_text = f"{headline.get_text().strip()}"
                if len(headline_text) > 20:
                    headlines_found.append(headline_text)

            print(headlines_found)
        else:
            print("The specified news section could not be found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Call the function to fetch and print the headlines
fetch_bbc_headlines()
