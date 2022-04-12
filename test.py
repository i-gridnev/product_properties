import os
import unittest
from main import RozetkaShoesParser

class TestParser(unittest.TestCase):

    def setUp(self) -> None:
        file = "txt.txt"
        url = ""
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
        expected = f"-----{pr_name}-----\n  {pr_props[0][0]} ---- {pr_props[0][1]}\n  {pr_props[1][0]} ---- {pr_props[1][1]}"

        self.parser.save(pr_name, pr_props)
        with open(self.parser.file, "r", encoding="utf-8") as reader:
            result = reader.read()

        self.assertEqual(result, expected)




