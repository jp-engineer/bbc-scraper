import requests
from bs4 import BeautifulSoup

# Define the URL for BBC News
url = 'https://www.bbc.com'

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
    response = requests.get(url + '/news', headers=headers)
    
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
            
            # Extract and collect the text and href of each headline
            for headline in headlines:
                headline_text = headline.get_text().strip()
                # Remove the 'Live.' prefix if present
                if headline_text.startswith("Live.\xa0"):
                    headline_text = headline_text.replace("Live.\xa0", "").strip()

                # Ensure the headline has sufficient length
                if len(headline_text) > 20:
                    # Get the hyperlink
                    headline_link = url + headline['href']
                    # Create a tuple of headline text and link
                    headlines_found.append((headline_text, headline_link))

            return headlines_found
        else:
            print("The specified news section could not be found.")
            return []
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

# Call the function to fetch and return the headlines
headlines = fetch_bbc_headlines()
print(headlines)
