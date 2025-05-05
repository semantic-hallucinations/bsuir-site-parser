from concurrent.futures import ThreadPoolExecutor
from typing import Set, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from organisation_utils.logging_config import logger_factory

from data_loading import (
    DataContainer,
    DataLoader,
    LocalLoader,
    RemoteDataLoader,
    loading_settings,
)
from limits import ParsingLimiter


class BsuirParser:
    def __init__(self):
        self.base_url: str = "https://www.bsuir.by"
        self.logger = logger_factory.get_logger("__parser__")
        self.urls = set()
        self.parsed_urls = set()
        self.loader: DataLoader = (
            RemoteDataLoader() if loading_settings.use_remote_loader else LocalLoader()
        )

    def create_soup(self, url: str) -> BeautifulSoup:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, allow_redirects=False, headers=headers)
        return BeautifulSoup(response.content, "html.parser")

    def extract_urls(self, soup: BeautifulSoup, section: str) -> None:
        if section := soup.find(section):
            for a in section.find_all("a", href=True):
                url = a["href"]
                absolute_url = urljoin(self.base_url, url)
                if url.startswith(self.base_url):
                    self.urls.add(absolute_url)

    def get_navigation_urls(self) -> None:
        soup = self.create_soup(self.base_url)
        self.extract_urls(soup, "header")
        self.extract_urls(soup, "footer")

    def scrap_page_content(self, url: str) -> Tuple[str | None, Set[str]]:
        urls = set()

        try:
            soup = self.create_soup(url)
            main_content = soup.select_one("main, .main")

            assert main_content, "Main element was't found on page"

            for img in main_content.find_all("img"):
                img.decompose()

            for breadcrumb in main_content.find_all(class_="breadcrumbs"):
                breadcrumb.decompose()

            for show_more in main_content.find_all(class_="showMore"):
                show_more.decompose()

            for a in main_content.find_all("a", href=True):
                url = a["href"]
                url = urljoin(self.base_url, url).strip().lower()
                if url.startswith("javascript:"):
                    del a["href"]
                else:
                    a["href"] = url

                if url.startswith(self.base_url):
                    if ParsingLimiter.in_save_extensions(url):
                        continue

                    a.replace_with(a.get_text(separator=" ", strip=True))

                    if not ParsingLimiter.in_drop_extensions(url):
                        urls.add(url)

            self.logger.info(f"Scrapped data from page {url}")
            return md(str(main_content), heading_style="ATX"), urls

        except Exception as e:
            self.loggerlogger.error(f"Error in scrapping {url} content: {e}")
            return None, urls

    def parse(self) -> None:
        with ThreadPoolExecutor() as executor:
            self.logger.info("Parsing started...")
            self.get_navigation_urls()
            self.urls.add(self.base_url)
            new_urls = set()

            while self.urls:
                for url in self.urls:
                    if ParsingLimiter.in_drop_topics(url):
                        self.logger.warning(f"Invalid topic: {url}")
                        continue
                    try:
                        self.logger.debug(f"Performing parsing for {url}")
                        md_data, page_urls = self.scrap_page_content(url)
                        if md_data:
                            data = DataContainer(md_data, url)
                            executor.submit(self.loader.load, data)
                        new_urls.update(page_urls)
                    except Exception as e:
                        self.logger.error(f"Can't load {url} content with error: {e}")

                self.parsed_urls.update(self.urls)
                self.urls = new_urls - self.parsed_urls
                new_urls.clear()

            self.logger.info("Parsing finished")
