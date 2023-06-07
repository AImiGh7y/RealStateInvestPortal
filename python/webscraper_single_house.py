import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import os

print("#2 python")

# specify the path of the directory you want to create
directory_path = "html_sapo"
directory_path_old = "html_sapo/old"

# use the makedirs() method to create the nested directory
os.makedirs(directory_path)
os.makedirs(directory_path_old)

# Connect to the SQLite database
conn = sqlite3.connect('houses.sqlite3')
c = conn.cursor()

# Get the links from the database
c.execute("SELECT link FROM houses")
links = c.fetchall()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

# Loop through the links and scrape the data
for link in links:
    link = link[0]

    response = requests.get(link, headers=headers)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Get the whole body tag
    tag = soup.body
    name = link[21:]
    name = name.replace("?", "-")


    if response.status_code == 410:
        with open('html_sapo/old/%s.html' % name, 'w', encoding='utf-8') as f:
            # Write data to the file
            f.write(str(tag))
        continue

    while response.status_code != 200:
        print('Waiting' + ' [' + str(response.status_code) + ']')
        time.sleep(300)
        response = requests.get(link, headers=headers)

    # Open a new file for writing
    with open('html_sapo/%s.html' % name, 'w', encoding='utf-8') as f:
        # Write data to the file
        f.write(str(tag))

conn.close()
print('DONE')