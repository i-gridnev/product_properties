import os
import unittest
import requests_mock
from src.main import RozetkaShoesParser


class TestParser(unittest.TestCase):

    def setUp(self) -> None:
        file = "txt.txt"
        url = "http://mock.com"
        self.parser = RozetkaShoesParser(url, file)
        if os.path.exists(file):
            os.remove(file)

    def tearDown(self) -> None:
        if os.path.exists(self.parser.file):
            os.remove(self.parser.file)

    def test_save_ptroduct(self):
        pr_name = "abraabra"
        pr_props = [["Color", "Blue"],
                    ["Sky", "Red"]]

        with open("tests/test_save.txt", "r", encoding="utf-8") as reader:
            expected = reader.read()

        self.parser.save(pr_name, pr_props)
        with open(self.parser.file, "r", encoding="utf-8") as reader:
            result = reader.read()

        self.assertEqual(result, expected)

    def test_get_product_link_with_existing_product_name(self):
        pr_name = "Кросівки New Balance ML393VY1 Світло-сірі із синім"
        expected = "https://rozetka.com.ua/ua/new_balance_195173210629/p293274978/characteristics/"
        with open("tests/test_page.txt", "r", encoding="utf-8") as reader:
            html = reader.read()
        with requests_mock.mock() as mock:
            mock.get(self.parser.url, text=html)
            result = self.parser.get_product_link(pr_name)
        self.assertEqual(result, expected)

    def test_get_product_link_with_notexisting_product_name(self):
        pr_name = "Кросsdgdgsdgsdgdsgdgнм"
        expected = False
        with open("tests/test_page.txt", "r", encoding="utf-8") as reader:
            html = reader.read()
        with requests_mock.mock() as mock:
            mock.get(self.parser.url, text=html)
            result = self.parser.get_product_link(pr_name)
        self.assertEqual(result, expected)
