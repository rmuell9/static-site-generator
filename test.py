import re

def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((https?://.*?)\)", text)
    print(images)
text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
extract_markdown_images(text)
