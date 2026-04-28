import config
from sources.rss_fetcher import RSSFetcher

fetcher = RSSFetcher(
    sources=config.SOURCES,
    news_per_source=config.NEWS_PER_SOURCE,
    min_summary_length=config.MIN_SUMMARY_LENGTH
)

all_news=fetcher.fetch_all()

for index ,news in enumerate(all_news,start=1):
    print(f"[{index}]\nTitle:{news['title']}\nLink:{news['link']}\nPublish Date:{news['publish_date']}")
    if  news["summary"] :
        print(f"Summary: {news['summary']}")
    print()