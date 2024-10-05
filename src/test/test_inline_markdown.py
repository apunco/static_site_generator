import unittest
from src.inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

from src.textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_split_image_single_occurence(self):
        node = TextNode("This is text with a image ![to boot dev](https://www.boot.gif) and ", text_type_text,)           
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with a image ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.gif"),
                TextNode(" and ", text_type_text),
            ],
            new_nodes,
        )


    def test_split_image_multiple_occurences(self):
        node = TextNode("This is text with a image ![to boot dev](https://www.boot.gif) and ![to youtube](https://www.youtube.jpeg)", text_type_text,)           
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with a image ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.gif"),
                TextNode(" and ", text_type_text),
                TextNode("to youtube", text_type_image, "https://www.youtube.jpeg")
            ],
            new_nodes,
        )

    def test_split_image_no_occurence(self):
        node = TextNode("This is text with a image to boot dev](https://www.boot.gif and ", text_type_text,)           
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with a image to boot dev](https://www.boot.gif and ", text_type_text)
            ],
            new_nodes,
        )        

    def test_split_image_edge_cases(self):
        node = TextNode("![to boot dev](https://www.boot.gif) and to youtube](https://www.youtube.jpeg)", text_type_text,)           
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("to boot dev", text_type_image, "https://www.boot.gif"),
                TextNode(" and to youtube](https://www.youtube.jpeg)", text_type_text)
            ],
            new_nodes,
        )  

        node = TextNode("and to youtube](https://www.youtube.jpeg) ![to boot dev](https://www.boot.gif)", text_type_text,)           
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("and to youtube](https://www.youtube.jpeg) ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.gif")                
            ],
            new_nodes,
        )    

        node = TextNode("This is text with a image ![to boot dev](https://www.boot.gif)![to youtube](https://www.youtube.jpeg)", text_type_text,)           
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with a image ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.gif"),             
                TextNode("to youtube", text_type_image, "https://www.youtube.jpeg")                
            ],
            new_nodes,
        )

        node = TextNode("![to boot dev](https://www.boot.gif)![to youtube](https://www.youtube.jpeg)", text_type_text,)           
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("to boot dev", text_type_image, "https://www.boot.gif"),             
                TextNode("to youtube", text_type_image, "https://www.youtube.jpeg")                
            ],
            new_nodes,
        )            


        # Links
    def test_split_link_single_occurence(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and ", text_type_text,)
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
            ],
            new_nodes,
        )


    def test_split_image_multiple_occurences(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text,)
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_image_no_occurence(self):
        node = TextNode("This is text with a link to boot dev]https://www.boot.dev) and [to youtubehttps://www.youtube.com/@bootdotdev)", text_type_text,)
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link to boot dev]https://www.boot.dev) and [to youtubehttps://www.youtube.com/@bootdotdev)", text_type_text),
            ],
            new_nodes,
        )

    def test_split_image_edge_cases(self):
        node = TextNode("[to boot dev](https://www.boot.gif) and to youtube](https://www.youtube.jpeg)", text_type_text,)           
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("to boot dev", text_type_link, "https://www.boot.gif"),
                TextNode(" and to youtube](https://www.youtube.jpeg)", text_type_text)
            ],
            new_nodes,
        )  

        node = TextNode("and to youtube](https://www.youtube.jpeg) [to boot dev](https://www.boot.gif)", text_type_text,)           
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("and to youtube](https://www.youtube.jpeg) ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.gif")                
            ],
            new_nodes,
        )    

        node = TextNode("This is text with a image [to boot dev](https://www.boot.gif)[to youtube](https://www.youtube.jpeg)", text_type_text,)           
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a image ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.gif"),             
                TextNode("to youtube", text_type_link, "https://www.youtube.jpeg")                
            ],
            new_nodes,
        )

        node = TextNode("[to boot dev](https://www.boot.gif)[to youtube](https://www.youtube.jpeg)", text_type_text,)           
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("to boot dev", text_type_link, "https://www.boot.gif"),             
                TextNode("to youtube", text_type_link, "https://www.youtube.jpeg")                
            ],
            new_nodes,
        )   

class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "Hello, world!"
        expected = [TextNode("Hello, world!", text_type_text)]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text.", text_type_text)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = "This is *italic* text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text.", text_type_text)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_code_text(self):
        text = "This is `code` text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(" text.", text_type_text)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_image_formatting(self):
        text = "This is an image: ![alt text](http://example.com/image.png) and some text."
        expected = [
            TextNode("This is an image: ", text_type_text),
            TextNode("alt text", text_type_image, "http://example.com/image.png"),
            TextNode(" and some text.", text_type_text)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_link_formatting(self):
        text = "This is a link: [OpenAI](http://openai.com) and some text."
        expected = [
            TextNode("This is a link: ", text_type_text),
            TextNode("OpenAI", text_type_link, "http://openai.com"),
            TextNode(" and some text.", text_type_text)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)





if __name__ == "__main__":
    unittest.main()
