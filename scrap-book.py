#!/usr/bin/env python3

from curses import keyname
from dataclasses import dataclass
from pickle import SHORT_BINUNICODE
from unicodedata import category
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import requests, csv, re, os

MAIN_URL="http://books.toscrape.com/"
CATEGORY="History"
SINGLE_BOOK_URL="http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html" # Single book URL
OUTFILES="outfiles" # Path for outfiles
OUTPUT="output"
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

def touch(filename): # Create outfile
    filename = re.sub('[^A-Za-z0-9]+', '', filename)
    book_properties = book().__dict__.keys()
    with open(OUTFILES+"/"+filename+'.csv', 'w') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(book_properties)

def append_book(filename): # Feed outfile
    filename = re.sub('[^A-Za-z0-9]+', '', filename)
    with open(OUTFILES+"/"+filename+'.csv', 'a') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        all = []
        for i in book_info.__dict__.values():
            all.append(i)
        writer.writerow(all)

def get_categories():
    print("Requesting category...")
    request_category = requests.get(MAIN_URL)
    soup = BeautifulSoup(request_category.content, 'html.parser')
    # Get first <ul>
    get_first_ul = soup.find('ul', {"class": "nav-list"})
    # <ul> containing list of categories
    get_ul = get_first_ul.find('ul')
    list_books_category = get_ul.find_all('li')
    category_link_list = []

    for li in list_books_category:
        
        #category_name_in_link = li.find('a')['href'].split('/')[3] # Get only category link name
        category_link = MAIN_URL+li.find('a')['href']
        category_link_list.append(category_link)
    
    return category_link_list 

def get_book_list(category_link):
    book_url_list = []
    answer = requests.get(category_link)
    page = answer.content
    soup = BeautifulSoup(page, "html.parser")
    cat_name = category_link.split('/')[6]
    paginate = soup.find("li", {"class": "current"})
    print("_______")
    print("Get list from category ID : " + cat_name)

    if paginate is None:
        find_book_url_list = soup.find_all('h3')
        for h3 in find_book_url_list:
            link_to_books = h3.select('a')
            for a in link_to_books:
                link_to_book = a['href'].split('/')[3]
                url_book = MAIN_URL + 'catalogue/' + link_to_book
                book_url_list.append(url_book)

    else:
        paginate = str(paginate)
        paginate = paginate.split()[5]
        count_page = int(paginate)

        for i in range(count_page + 1):
            url = "https://books.toscrape.com/catalogue/category/books/" + cat_name + "/page-" + str(i) + ".html"
            response = requests.get(url)
            if response.ok:
                find_book_url_list = soup.find_all('h3')
                for h3 in find_book_url_list:
                    link_to_books = h3.select('a')
                    for a in link_to_books:
                        link_to_book = a['href'].split('/')[3]
                        url_book = MAIN_URL + 'catalogue/' + link_to_book
                        book_url_list.append(url_book)
    return book_url_list

def get_book(url):
    book_info = book()
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
    tmp_desc = soup.select("article > p")[0].text
    if tmp_desc.isspace():
        book_info.product_description = "Description not available."
    else:
        book_info.product_description = tmp_desc
    book_info.image_url = urljoin(MAIN_URL, soup.find_all('div', {'class': 'carousel'})[0].find('img')['src'])
    book_info.category = soup.select("body > div > div > ul > li > a")[2].text
    # Save image
    book_info.product_page_url = url
    img_data = requests.get(book_info.image_url).content
    img_file = book_info.title.replace(" ", "_")
    mkdir(OUTFILES+"/"+"medias")
    with open(OUTFILES+"/"+"medias"+"/"+img_file+'.jpg', 'wb') as handler:
        handler.write(img_data)

    print("Book" + ' "'+book_info.title+'" ' + "imported.")

    return book_info

def main():
    mkdir(OUTFILES)
    global book_info

    for url in get_categories():
        filename = url.split('/')[6]
        touch(filename)
        for book in get_book_list(url):
            book_info = get_book(book)
            append_book(filename)

main()