import unittest

from src.block_markdown import *

class TestBlockMarkdown(unittest.TestCase):
    def test_basic_separation(self):
        input_str = "# Heading\n\nParagraph text.\n\n* List item"
        expected_output = [
            "# Heading",
            "Paragraph text.",
            "* List item"
        ]
        self.assertEqual(markdown_to_blocks(input_str), expected_output)

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_leading_trailing_whitespace(self):
        input_str = "  # Heading   \n\n   Paragraph"
        expected_output = [
            "# Heading",
            "Paragraph"
        ]
        self.assertEqual(markdown_to_blocks(input_str), expected_output)     

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.heading)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.heading)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.heading)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.code)
        self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), BlockType.code)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.quote)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.quote)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), BlockType.unordered_list)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.unordered_list)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second"), BlockType.ordered_list)
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), BlockType.ordered_list)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.paragraph)
        self.assertEqual(block_to_block_type("This is a\nmulti-line paragraph."), BlockType.paragraph)

    def test_invalid_heading(self):
        self.assertEqual(block_to_block_type("#Not a heading"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("####### Too many hashtags"), BlockType.paragraph)

    def test_invalid_code(self):
        self.assertEqual(block_to_block_type("``Not a code block``"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("```\nUnclosed code block"), BlockType.paragraph)

    def test_invalid_quote(self):
        self.assertEqual(block_to_block_type(">No space after >"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("> Quote\nNot a quote"), BlockType.paragraph)

    def test_invalid_unordered_list(self):
        self.assertEqual(block_to_block_type("*No space after asterisk"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("* Item 1\nNot an item"), BlockType.paragraph)

    def test_invalid_ordered_list(self):
        self.assertEqual(block_to_block_type("1.No space after number"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("1. First\n3. Third"), BlockType.paragraph)

    def test_empty_string(self):
        self.assertEqual(block_to_block_type(""), BlockType.paragraph)