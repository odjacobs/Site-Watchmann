import json
import requests
import time
import sqlite3
from bs4 import BeautifulSoup
from discord import SyncWebhook

# Load settings
with open('config.json', 'r') as f:
    config = json.load(f)

interval = config['interval']

# Initialize webhook
webhook_url = config['webhook']
webhook = SyncWebhook.from_url(webhook_url)

# Connect to SQLite database
conn = sqlite3.connect("links.sqlite3")
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS links
             (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT)''')


def updateLinks(url):
    new_links = []
    try:
        # Make HTTP request to URL
        response = requests.get(url)

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract links from webpage that contain "/products"
        links = set([link.get("href") for link in soup.find_all("a") if "/products" in link.get("href")])

        # Compare links with existing links in database
        for link in links:
            c.execute("SELECT * FROM links WHERE link = ?", (link,))
            result = c.fetchone()
            if result is None:
                # New link found, insert into database
                c.execute("INSERT INTO links (link) VALUES (?)", (link,))
                conn.commit()
                print(f"New link found: {config['base-url']}{link}")
                new_links.append(config['base-url'] + link)
        
        # Send Discord message containing new links
        if len(new_links) > 0:
            msg = "\n".join(new_links)
            webhook.send(msg)

    except Exception as e:
        print(f"Error: {e}")


while True:
    for i in range(1,21):
        print(f"Scanning page {i} of 20")
        updateLinks(f"{config['base-url']}/damages?pg={i}")
        time.sleep(1)
    # Wait for interval before next check
    time.sleep(interval)