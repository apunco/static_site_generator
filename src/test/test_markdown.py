import unittest
from src.markdown import *

class Markdown_Unittest(unittest.TestCase):
    def test_markdown_to_html_node_empty(self):
        result = markdown_to_html_node("")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 0)

    def test_markdown_to_html_node_heading(self):
        markdown = "# Heading 1"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "h1")

    def test_block_node_to_html_node_quote(self):
        block = "> This is a quote"
        result = block_node_to_html_node(block, BlockType.quote)
        self.assertEqual(result.tag, "blockquote")

    def test_extract_title(self):
        # Test when markdown string has a single h1 header.
        assert extract_title("# My Title") == "My Title"

        # Test when markdown string has leading and trailing whitespaces.
        assert extract_title("#   Spaced Title  ") == "Spaced Title"

        # Test when there is no h1 header in the markdown string.
        try:
            extract_title("## No h1 header here")
        except Exception as e:
            assert isinstance(e, Exception)

        # Test when the h1 header contains special characters.
            assert extract_title("# Title!@#$") == "Title!@#$"


