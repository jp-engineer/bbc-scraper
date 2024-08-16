import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
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

engine = create_engine('sqlite:///bbc_articles.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def fetch_headlines():
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = soup.find_all('a', href=True)
        
        articles = []
        for link in all_links:
            if '/news/articles/' in link['href'] and not link['href'].endswith('#comments'):
                article_id = link['href'].split('/')[-1]
                article_url = 'https://www.bbc.co.uk' + link['href']
                article_title = link.get_text().strip()
                
                # Check if article already exists in the database
                if not session.query(Article).filter_by(article_id=article_id).first():
                    article = Article(article_id=article_id, title=article_title, url=article_url)
                    session.add(article)
                    articles.append({"id": article_id, "url": article_url, "title": article_title})
        
        session.commit()
        return articles 
    else:
        return []

fetch_headlines()
