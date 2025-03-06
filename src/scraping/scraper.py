import aiohttp
import asyncio
from bs4 import BeautifulSoup

# Load predefined sources
SOURCES = [
    "https://news.google.com/search?q={query}",
    "https://www.reuters.com/search/news?blob={query}",
    "https://www.bbc.co.uk/search?q={query}",
    "https://www.aljazeera.com/search/{query}",
    "https://www.npr.org/search?query={query}"
]

async def fetch_article(session, url):
    """Fetches and extracts the main text of an article."""
    try:
        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                return None
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            paragraphs = soup.find_all("p")
            article_text = " ".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])

            return article_text if len(article_text.split()) > 100 else None  # Ignore short texts
    except:
        return None

async def fetch_alternative_sources(original_text):
    """Finds alternative articles covering similar topics."""
    keywords = original_text.split()[:100]  # Extract first 10 words for search
    search_query = "+".join(keywords)

    alternative_articles = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_article(session, source.format(query=search_query)) for source in SOURCES]
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results):
            if result:
                alternative_articles.append({"source": SOURCES[i], "text": result})

    return alternative_articles
