# BBC News Article Scraper

This Python script scrapes articles from the BBC News website and stores them in a local SQLite database. It collects article headlines, URLs, and full texts, saving them for future use.
Features

    Fetches headlines from the BBC News homepage.
    Extracts full text of articles.
    Saves article information (ID, title, URL, and text) to a local SQLite database.
    Avoids duplicate entries by checking if an article already exists in the database.

## Requirements

To run this script, you need the following Python libraries:

    requests - For making HTTP requests.
    beautifulsoup4 - For parsing HTML and extracting article content.
    sqlalchemy - For database interactions.

## Setup
1. Clone the Repository

Clone or download this repository to your local machine:

```
git clone <repository-url>
cd <repository-directory>
```
2. Set Up a Virtual Environment

Create a virtual environment to isolate your project dependencies. Run the following command to create a virtual environment named venv:

```
python -m venv venv
```
Activate the virtual environment:

On Windows:
```
venv\Scripts\activate
```
On macOS/Linux:

```
source venv/bin/activate
```
3. Install Requirements

Ensure your virtual environment is activated, then install the required libraries using requirements.txt:

```
pip install -r requirements.txt
```

4. Run the Script

Execute the script to start scraping:

```
python scraper.py
```
The script will fetch headlines from the BBC News homepage, retrieve the full text of each article, and store the details in bbc_articles.db, a SQLite database file created in the same directory.

## Database Schema

The script creates a SQLite database with the following table:
articles

    id (INTEGER, Primary Key, Autoincrement)
    article_id (TEXT, Unique)
    title (TEXT)
    url (TEXT)
    text (TEXT)
    retrieved_at (DATETIME, default to current UTC time)

## Code Explanation

Fetching Headlines

    The fetch_headlines() function requests the BBC News homepage and parses it to extract article links. It filters links that contain '/news/articles/' and avoids comment sections.

Storing Articles

    For each article link, the script:
        Checks if the article already exists in the database.
        Fetches the article page.
        Extracts the article text.
        Saves the article information to the SQLite database.

Database Setup

    SQLAlchemy is used to define the database model and create the SQLite database file (bbc_articles.db) if it doesn't already exist.

## Notes

The script currently handles a basic structure of the BBC News website. If the website structure changes, the script may require adjustments.

Ensure you comply with the BBC's terms of service and robots.txt file when scraping their website.