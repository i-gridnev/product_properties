from datetime import datetime
import sys
from bs4 import BeautifulSoup
import requests


class RozetkaShoesParser:
    headers = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, url, file):
        self.url = url
        self.file = file
        self.props = []
        self.title = ""

    def get_product_link(self, product_name):
        search = requests.get(self.url, headers=self.headers).text
        soup = BeautifulSoup(search, 'html.parser')
        for match in soup.find_all("span", class_="goods-tile__title"):
            title = match.contents[4].strip()
            if title == product_name:
                link = match.parent.attrs["href"] + "characteristics/"
                return link
        return False

    def get_product_properties(self, product_url):
        search = requests.get(product_url, headers=self.headers).text
        soup = BeautifulSoup(search, 'html.parser')
        props = soup.find_all("div", class_="characteristics-full__item")
        ans = []
        for prop in props:
            prop_name = prop.contents[0].getText()
            prop_value = prop.contents[1].getText(" | ")
            ans.append([prop_name, prop_value])
        return ans

    def process_product(self, product_name):
        product_link = self.get_product_link(product_name)
        if product_link:
            properties = self.get_product_properties(product_link)
        else:
            properties = [["Not found", str(datetime.now())]]
        self.save(product_name, properties)

    def save(self, title, props):
        data = f"-----{title}-----"
        for prop in props:
            data += f"\n  {prop[0]} ---- {prop[1]}"
        with open(self.file, "w", encoding="utf-8") as stream:
            stream.write(data)


if __name__ == "__main__":
    URL = "https://rozetka.com.ua/ua/shoes_clothes/c1162030/producer=new-balance/"
    FILE = "result.txt"
    # product_name_ = "Кросівки New Balance 500 GW500CT1 Блакитні"

    try:
        product_name_ = sys.argv[1]
    except IndexError:
        print('Please set product name as string (with "something")')
        sys.exit(0)

    p = RozetkaShoesParser(url=URL, file=FILE)
    p.process_product(product_name_)
