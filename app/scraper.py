import requests
import datetime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


url = 'https://www.bbc.co.uk/news'
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.5735.110 Safari/537.36'
    )
}

# define the database model, create and connect
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String, unique=True)
    title = Column(String)
    url = Column(String)
    text = Column(String)
    retrieved_at = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('sqlite:///bbc_articles.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def fetch_headlines():
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            if '/news/articles/' in link['href'] and not link['href'].endswith('#comments'):
                article_id = link['href'].split('/')[-1]
                article_url = 'https://www.bbc.co.uk' + link['href']
                article_title = link.get_text().strip()
                
                if not session.query(Article).filter_by(article_id=article_id).first():
                    article_response = requests.get(article_url, headers=headers)
                    soup = BeautifulSoup(article_response.content, 'html.parser')
                    article_tag = soup.find('article')
                    if article_tag:
                        article_soup = BeautifulSoup(str(article_tag), 'html.parser')
                        text_blocks = article_soup.find_all('div', {'data-component': 'text-block'})
                        full_text = ""
                        for block in text_blocks:
                            block_text = block.get_text(separator=" ", strip=True)
                            full_text += block_text + " "

                    article = Article(article_id=article_id, title=article_title, url=article_url, text=full_text)
                    session.add(article)
        
        session.commit()
    else:
        return []

fetch_headlines()
