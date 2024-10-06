import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# EDGAR API
def fetch_sec_filings(company_cik, filing_type='10-K', start_date=None, end_date=None):
    base_url = "https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {'User-Agent': 'YourCompanyName yourname@example.com'}
    
    response = requests.get(base_url.format(cik=company_cik.zfill(10)), headers=headers)
    data = response.json()
    
    filings = []
    for filing in data['filings']['recent']:
        if filing['form'] == filing_type:
            filing_date = datetime.strptime(filing['filingDate'], '%Y-%m-%d')
            if (not start_date or filing_date >= start_date) and (not end_date or filing_date <= end_date):
                filings.append({
                    'company_cik': company_cik,
                    'filing_type': filing_type,
                    'filing_date': filing['filingDate'],
                    'accession_number': filing['accessionNumber']
                })
    
    return filings

# NewsAPI
def fetch_news_articles(company_name, api_key, days_back=30):
    base_url = "https://newsapi.org/v2/everything"
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    params = {
        'q': company_name,
        'from': start_date,
        'sortBy': 'publishedAt',
        'apiKey': api_key,
        'language': 'en'
    }
    
    response = requests.get(base_url, params=params)
    articles = response.json()['articles']
    
    return [{
        'company_name': company_name,
        'title': article['title'],
        'description': article['description'],
        'content': article['content'],
        'published_at': article['publishedAt'],
        'source': article['source']['name']
    } for article in articles]

# Web Scraping
def scrape_company_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Example: Extract all paragraph text
    paragraphs = soup.find_all('p')
    text_content = ' '.join([p.get_text() for p in paragraphs])
    
    return {
        'url': url,
        'content': text_content,
        'scraped_at': datetime.now().isoformat()
    }

# Data ingestion
def ingest_data(company_cik, company_name, company_website):
    with ThreadPoolExecutor(max_workers=3) as executor:
        sec_future = executor.submit(fetch_sec_filings, company_cik)
        news_future = executor.submit(fetch_news_articles, company_name, os.getenv("NEWS_API_KEY"))
        web_future = executor.submit(scrape_company_website, company_website)
        
        sec_filings = sec_future.result()
        news_articles = news_future.result()
        website_data = web_future.result()
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Insert SEC filings
        cur.executemany("""
            INSERT INTO sec_filings (company_cik, filing_type, filing_date, accession_number)
            VALUES (%(company_cik)s, %(filing_type)s, %(filing_date)s, %(accession_number)s)
            ON CONFLICT (company_cik, accession_number) DO UPDATE
            SET filing_date = EXCLUDED.filing_date
        """, sec_filings)
        
        # Insert news articles
        cur.executemany("""
            INSERT INTO news_articles (company_name, title, description, content, published_at, source)
            VALUES (%(company_name)s, %(title)s, %(description)s, %(content)s, %(published_at)s, %(source)s)
            ON CONFLICT (company_name, title, published_at) DO NOTHING
        """, news_articles)
        
        # Insert website data
        cur.execute("""
            INSERT INTO website_data (url, content, scraped_at)
            VALUES (%(url)s, %(content)s, %(scraped_at)s)
            ON CONFLICT (url) DO UPDATE
            SET content = EXCLUDED.content, scraped_at = EXCLUDED.scraped_at
        """, website_data)
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error ingesting data: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    ingest_data("0000320193", "Apple Inc.", "https://www.apple.com/environment/")