#!/usr/bin/env python3

from dataclasses import dataclass
from pickle import SHORT_BINUNICODE
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import requests, csv, re, os

SINGLE_BOOK_URL="http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html" # Single book URL
OUTFILES="outfiles" # Path for outfiles
SHORTURI=urljoin(SINGLE_BOOK_URL, '/')

@dataclass
class book:
    """Class for keeping track of an item in inventory."""
    category: str = ""
    image_url: str = ""
    number_available: int = 0
    price_including_tax: float = 0.00
    price_excluding_tax: float = 0.00
    product_type: str = ""
    product_page_url: str = ""
    product_description: str = ""
    review_count: int = 0
    review_rating: int = 0
    tax:float = 0.00
    title: str = ""
    universal_product_code_upc: str = ""

def mkdir(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)

def touch(filename): # Single book
    filename = re.sub('[^A-Za-z0-9]+', '', filename)
    book_properties = book_info.__dict__.keys()
    with open(OUTFILES+"/"+filename+'.csv', 'w') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(book_properties)
        all = []
        for i in book_info.__dict__.values():
            all.append(i)
        writer.writerow(all)

def get_book(url):
    book_info = book()
    print("Requesting single book...")
    answer = requests.get(url)
    page = answer.content
    soup = BeautifulSoup(page, "html.parser")
    # Extract table
    for element in soup.select(".table-striped"):        
        for cell in element.select("tr"):
            #print(cell)
            if cell.th.text == "UPC":
                book_info.universal_product_code_upc = cell.td.text
            elif cell.th.text == "Product Type":
                book_info.product_type = cell.td.text            
            elif cell.th.text == "Price (excl. tax)":
                book_info.price_excluding_tax = cell.td.text
            elif cell.th.text == "Price (incl. tax)":
                book_info.price_including_tax = cell.td.text
            elif cell.th.text == "Tax":
                book_info.tax = cell.td.text
            elif cell.th.text == "Number of reviews":
                book_info.review_count = cell.td.text
            elif cell.th.text == "Availability":
                book_info.number_available =int("".join(filter(str.isdigit, cell.td.text)))
    book_info.title = soup.select(".product_main h1")[0].text
    book_info.product_description = soup.select("article > p")[0].text
    book_info.image_url = urljoin(SHORTURI, soup.find_all('div', {'class': 'carousel'})[0].find('img')['src'])
    book_info.category = soup.select("body > div > div > ul > li > a")[2].text
    book_info.product_page_url = url
    print("_______")
    return book_info

def main():
    mkdir(OUTFILES)
    global book_info
    book_info = get_book(SINGLE_BOOK_URL)
    print(book_info.category)
    touch("output")

main()