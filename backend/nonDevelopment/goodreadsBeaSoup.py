from bs4 import BeautifulSoup
import requests


start_urls = [
    'https://www.goodreads.com/review/list/61429830-taniya?ref=nav_mybooks&shelf=read',
    'https://www.goodreads.com/review/list/61429830-taniya?page=2&ref=nav_mybooks&shelf=read',
    'https://www.goodreads.com/review/list/61429830-taniya?page=3&ref=nav_mybooks&shelf=read',
    'https://www.goodreads.com/review/list/61429830-taniya?page=4&ref=nav_mybooks&shelf=read',
    'https://www.goodreads.com/review/list/61429830-taniya?page=5&ref=nav_mybooks&shelf=read',
]

for i in start_urls:
    response = requests.get(i)
    main_page_items = BeautifulSoup(response.text, 'html.parser')

    