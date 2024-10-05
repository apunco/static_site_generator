import unittest

from src.regexmarkdown import *

class TestRegex(unittest.TestCase):

    def test_image_regex(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_image_with_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_image_without_image(self):
        text = "This is text with a rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wanhttps://i.imgur.com/fJRm4Vk.jpeg) This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = []

        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_link_regex(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        self.assertEqual(extract_markdown_links(text), expected_result)
    
    def test_link_with_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        self.assertEqual(extract_markdown_links(text), expected_result)

    def test_link_without_link(self):
        text = "This is text with a rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wanhttps://i.imgur.com/fJRm4Vk.jpeg) This is text with a link [to boot devhttps://www.boot.dev) and [to youtubehttps://www.youtube.com/@bootdotdev)"
        expected_result = []

        self.assertEqual(extract_markdown_links(text), expected_result)

    def test_empty_input(self):
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_links(""), [])

    def test_multiple_occurrences_single_line(self):
        text = "![img1](url1)![img2](url2)[link1](url3)[link2](url4)"
        self.assertEqual(extract_markdown_images(text), [("img1", "url1"), ("img2", "url2")])
        self.assertEqual(extract_markdown_links(text), [("link1", "url3"), ("link2", "url4")])

    def test_malformed_markdown(self):
        # Incomplete brackets
        text1 = "![alt(url)"
        self.assertEqual(extract_markdown_images(text1), [])
        
        # Mismatched brackets
        text2 = "[link](http://example.com[("
        self.assertEqual(extract_markdown_links(text2), [])

    def test_special_characters(self):
        # Special characters in alt text
        text1 = "![alt [with] (brackets)](http://example.com/image.jpg)"
        self.assertEqual(extract_markdown_images(text1), [("alt [with] (brackets)", "http://example.com/image.jpg")])
        
        # Special characters in anchor text
        text2 = "[Link (with) [brackets]](http://example.com)"
        self.assertEqual(extract_markdown_links(text2), [("Link (with) [brackets]", "http://example.com")])

    def test_urls_with_query_params(self):
        # Image URL with query parameters
        text1 = "![alt](http://example.com/image.jpg?size=large&format=png)"
        self.assertEqual(extract_markdown_images(text1), [("alt", "http://example.com/image.jpg?size=large&format=png")])
        
        # Link URL with fragment
        text2 = "[Link](http://example.com/page#section)"
        self.assertEqual(extract_markdown_links(text2), [("Link", "http://example.com/page#section")])

