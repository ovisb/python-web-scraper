"""Main module"""
from python_web_scraper import (  # type: ignore
    create_page_directory,
    extract_article_type,
    file_name_from_article_title,
    process_article,
    request_url,
    save_html,
    scrape,
)


def main() -> None:
    url = "https://www.nature.com/nature"
    query = "/articles?sort=PubDate&year=2020"

    files_created = []
    page_number = int(input("Enter max number of pages to look for articles: (e.g '4')"))
    filter_article = input("Enter article type: (e.g 'News')")

    for i in range(1, page_number + 1):
        page_dir = create_page_directory(i)
        page = f"&page={i}"
        r = request_url(url + query + page)
        soup = scrape(r.content)

        for article in soup.find_all("article"):
            article_type, article_title, article_url = extract_article_type(article)

            file_name = file_name_from_article_title(article_title)

            if article_type == filter_article:
                print(article_type)
                print(article_title)

                article_content = process_article(url + article_url)

                save_html(article_content.text, f"{file_name}.txt", "w", page_dir)
                files_created.append(f"{file_name}.txt")

    print(f"Saved articles: {str(files_created)}")


if __name__ == "__main__":
    main()
