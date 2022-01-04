from typing import List, Union
from urllib.parse import urljoin

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fastapi import HTTPException
from fastapi import status as http_status

from app.core.config import QUOTES_SITE_ENTRYPOINT
from app.quotes.schemas import Author, Quote, SearchQuery, Tag


async def get_html(url: str) -> BeautifulSoup:
    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

            if response.status == 200:
                html = BeautifulSoup(markup=text, features="lxml")

                return html

    raise HTTPException(status_code=http_status.HTTP_501_NOT_IMPLEMENTED,
                        detail=f"Scraper didn't succeed in getting data:\n"
                               f"\turl: {url}\n"
                               f"\tstatus code: {response.status}\n"
                               f"\tresponse text: {text}")


def filter_urls(elements: List[BeautifulSoup], include: List[str], first: bool = False) -> Union[List[str], str]:
    urls = [a.get("href", "") for a in elements]
    urls = [urljoin(QUOTES_SITE_ENTRYPOINT, a) for a in urls if any([s in a for s in include])]

    if first:
        return urls[0] if len(urls) > 0 else None
    else:
        return urls


def get_text(element: BeautifulSoup, selector: str, strip: bool = True, delimiter: str = "\n") -> str:
    text = ""

    elements = element.select(selector=selector) if selector else [element]
    for el in elements:
        el_text = el.text if el else ""
        if strip:
            text += " ".join(el_text.split()) + delimiter
        else:
            text += el_text + delimiter

    return text.strip()


def parse_quotes(html: BeautifulSoup) -> List[Quote]:
    quotes = []

    for element in html.select(".quote"):
        text = get_text(element=element, selector=".text")

        author = Author(name=get_text(element=element, selector=".author"),
                        url=filter_urls(elements=element.select("a"), include=["/author/"], first=True))

        tags = []
        for raw_tag in element.select(".tag"):
            tags.append(Tag(name=get_text(element=raw_tag, selector=""),
                            url=filter_urls(elements=[raw_tag], include=["/tag/"], first=True)))

        quotes.append(Quote(text=text, author=author, tags=tags))

    return quotes


async def get_quotes(data: SearchQuery) -> List[Quote]:
    url = QUOTES_SITE_ENTRYPOINT
    if data.tag:
        url = f"{url}/tag/{data.tag}/"

    entrypoint_page = await get_html(url)
    quotes = parse_quotes(html=entrypoint_page)

    quotes_per_page = len(quotes)
    if quotes_per_page == 0:
        return []

    page = data.offset // quotes_per_page + 1
    start_from_item = data.offset % quotes_per_page

    if page == 1:
        quotes = quotes[start_from_item:]
        start_from_item = 0
        page += 1
    else:
        quotes = []

    while len(quotes) < data.limit:

        url = f"{QUOTES_SITE_ENTRYPOINT}page/{page}/"

        page_html = await get_html(url=url)
        new_quotes = parse_quotes(html=page_html)[start_from_item:]
        if not new_quotes:
            break

        quotes += new_quotes

        start_from_item = 0
        page += 1

    return quotes[:data.limit]
