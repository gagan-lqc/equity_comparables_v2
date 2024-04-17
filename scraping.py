# scraping.py
import re
import requests
from bs4 import BeautifulSoup

def clean_text(text):
    # Remove special characters and symbols except for alphanumeric characters and spaces
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    # Remove extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def scrape_website_content(url, id, name, description, ticker, exchange, hq):
    result = {}
    result['id'] = id
    result['name'] = name
    result['description'] = description
    result['url'] = url
    result['ticker'] = ticker
    result['exchange'] = exchange
    result['hq'] = hq

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            title_tag = soup.find('title')
            if title_tag:
                result['title'] = clean_text(title_tag.text.strip())
            else:
                result['title'] = "Title tag not found on the webpage."

            meta_description_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_description_tag:
                result['description'] = clean_text(meta_description_tag.get('content').strip())
            else:
                result['description'] = "Meta description tag not found on the webpage."

            body_tag = soup.find('body')
            if body_tag:
                result['body'] = clean_text(body_tag.text.strip())
            else:
                result['body'] = "Body tag not found on the webpage."

        else:
            
            result['error'] = "Failed to retrieve content. Status code: " + str(response.status_code)

    except requests.Timeout:
        result['error'] = "Timeout error: Request timed out while trying to access the webpage."

    except requests.RequestException as e:
        result['error'] = "Request error: " + str(e)

    return result