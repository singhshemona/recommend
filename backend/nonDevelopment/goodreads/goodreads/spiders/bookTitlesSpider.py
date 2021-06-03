import scrapy


class BookTitlesSpider(scrapy.Spider):
    name = "bookTitles"
    start_urls = [
        'https://www.goodreads.com/review/list/61429830-taniya?ref=nav_mybooks&shelf=read',
        'https://www.goodreads.com/review/list/61429830-taniya?page=2&ref=nav_mybooks&shelf=read',
        'https://www.goodreads.com/review/list/61429830-taniya?page=3&ref=nav_mybooks&shelf=read',
        'https://www.goodreads.com/review/list/61429830-taniya?page=4&ref=nav_mybooks&shelf=read',
        'https://www.goodreads.com/review/list/61429830-taniya?page=5&ref=nav_mybooks&shelf=read',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'bookTitles-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

