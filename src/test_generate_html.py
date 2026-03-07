import unittest
from generate_html import *

class test_extract_title(unittest.TestCase):

    def test_None_input(self):
        with self.assertRaises(Exception):
            result = extract_title(None)
        
    def test_empty_input(self):
        with self.assertRaises(Exception):
            result = extract_title("")
            
    def test_no_h1_in_mkdown(self):
        with self.assertRaises(Exception):
            result = extract_title("this is a markdown file")

    def test_h1_found(self):
        self.assertEqual(extract_title("# this is the right title"), "this is the right title")

    def test_h2_found(self):
        with self.assertRaises(Exception):
            result = extract_title("## this is a markdown file")

if __name__ == "__main__":
    unittest.main()