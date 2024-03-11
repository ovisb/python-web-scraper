"""python_web_scraper module"""
from __future__ import annotations

import string
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def validate_url(url: str) -> bool:
    """
    Validate if the given URL is valid.

    Args:
    url (str): The URL to validate.

    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    if "articles" not in url or "nature" not in url:
        print("Invalid page!")
        return False

    return True


def request_url(url) -> requests.Response:
    """
    Makes a GET request to the specified URL.

    Args:
    - url (str): The URL to make the request to.

    Returns:
    - requests.Response: The response object from the request.
    """
    r = requests.get(url, "headers={'Accept-Language': 'en-US,en;q=0.5'}")

    return r


def save_html(content: bytes | str, filename: str, mode: str, page_dir: str) -> None:
    """
    Save the HTML content to a file.

    Args:
    content (bytes/str): The HTML content to be saved.
    filename (str): The name of the file to save to.
    mode (str): The mode to open the file in (e.g., 'w' for write, 'a' for append).
    page_dir (str): The directory where the file will be saved.
    """
    with open(page_dir + filename, mode) as f:
        f.write(content)
        print("Content saved.")


def remove_punctuation(text: str) -> str:
    """
    Removes punctuation from the input text.

    Args:
    text (str): The input text containing punctuation.

    Returns:
    str: The input text with punctuation removed.
    """
    stripped_text = "".join(char for char in text if char not in string.punctuation)

    return stripped_text


def scrape(content: bytes) -> BeautifulSoup:
    """
    Scrapes the given HTML content using BeautifulSoup.

    Args:
    content (bytes): The HTML content to be scraped.

    Returns:
    BeautifulSoup: Parsed HTML content.
    """
    return BeautifulSoup(content, "html.parser")


def create_page_directory(page_number: int) -> str:
    """
    Create a directory for a given page number.

    Args:
    page_number (int): The page number for which the directory is to be created.

    Returns:
    str: The path of the created directory.
    """
    page_dir = f"Page_{page_number}/"
    Path(page_dir).mkdir(exist_ok=True)
    return page_dir


def extract_article_type(article) -> tuple[str, str, str]:
    """
    Extracts the type, title, and URL of the given article.

    Parameters:
    - article: The BeautifulSoup object representing the article.

    Returns:
    - A tuple containing the article type (str), title (str), and URL (str).
    """
    article_title = remove_punctuation(article.find("a").text.strip())
    anchor_text = article.find("a", {"data-track-action": "view article"})
    article_url = anchor_text.get("href")
    article_span = article.find("span", {"data-test": "article.type"})
    article_type = article_span.text

    return article_type, article_title, article_url


def file_name_from_article_title(article_title: str) -> str:
    """
    Convert the article title to a file name format by replacing spaces with underscores.

    Args:
    article_title (str): The title of the article.

    Returns:
    str: The file name generated from the article title.
    """
    return article_title.replace(" ", "_")


def process_article(url: str) -> BeautifulSoup:
    """
    Process the article content from the given URL.

    Args:
    url (str): The URL of the article.

    Returns:
    BeautifulSoup: The BeautifulSoup object containing the article content.
    """
    resp = request_url(url)
    s = scrape(resp.content)
    article_content = s.find("p", {"class": "article__teaser"})

    return article_content
