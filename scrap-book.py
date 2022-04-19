#!/usr/bin/env python3

from dataclasses import dataclass
from bs4 import BeautifulSoup
from pathlib import Path
import requests, csv, re

SINGLE_BOOK_URL="http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

@dataclass
class book:
    category: str
    #image_url: str
    number_available: int
    price_including_tax: float
    price_excluding_tax: float
    product_page_url: str
    product_description: str
    review_count: int
    review_rating: int
    tax:float
    title: str
    universal_product_code_upc: str

def mkdir(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)

def get_book(url):
    book_info = book(category="",
                    number_available=0,
                    price_including_tax=0.00,
                    price_excluding_tax=0.00,
                    product_page_url=url,
                    product_description="",
                    review_count=0,
                    review_rating=0,
                    tax=0.00,
                    title="",
                    universal_product_code_upc=""
                    )

    print("Requesting single book...")
    answer = requests.get(url)
    page = answer.content
    soup = BeautifulSoup(page, "html.parser")
    
    # Extract table
    for element in soup.select(".table-striped"):        
        for cell in element.select("tr"):
            print(cell)
            if cell.th.text == "UPC":
                book_info.universal_product_code_upc = cell.td.text
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
    book_info.product_description = soup.find_all("p", class_="article") #soup.select("article > p")[0]

    print("_______")
    return book_info


def main():
    
    print(get_book(SINGLE_BOOK_URL))

main()