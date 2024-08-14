import requests
from bs4 import BeautifulSoup

url = 'https://www.bbc.co.uk/news'
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.5735.110 Safari/537.36'
    )
}

def fetch_bbc_headlines():
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = soup.find_all('a', href=True)
        
        article_links = ['https://www.bbc.co.uk' + link['href'] for link in all_links if '/news/articles/' in link['href'] and not link['href'].endswith('#comments')]
        
        return article_links
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

article_links = fetch_bbc_headlines()
print(article_links)
