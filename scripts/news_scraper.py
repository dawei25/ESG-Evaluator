import requests
import json

api_key = '4e85acf023754423859da7e73b722206'
company_name = 'Tesla'

url = f'https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}'

response = requests.get(url)
data = response.json()

# Print the articles
for article in data['articles']:
    print(f"Title: {article['title']}")
    print(f"Description: {article['description']}")
    print(f"URL: {article['url']}\n")


import csv

with open(f'{company_name}_news.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Description', 'URL'])

    for article in data['articles']:
        writer.writerow([article['title'], article['description'], article['url']])

