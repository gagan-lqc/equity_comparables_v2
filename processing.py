# processing.py
import logging
from scraping import scrape_website_content

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_url(url, id, name, description, ticker, exchange, hq):
    try:
        logging.info(f"Scraping URL: {url}")
        output = scrape_website_content(url, id, name, description, ticker, exchange, hq)
        logging.info(output.get('title', 'Title not found'))
        return output
    except Exception as e:
        logging.error(f"Error occurred while scraping {url}: {str(e)}")
        return {}