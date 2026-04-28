import feedparser
from bs4 import BeautifulSoup

sources = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://openai.com/blog/rss.xml",
    "https://news.ycombinator.com/rss",
    "https://deepmind.google/blog/rss.xml",
    "https://engineering.stanford.edu/news/all/rss",
    "https://simonwillison.net/atom/everything/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
]

for source in sources:
    feed = feedparser.parse(source)
    print(f"===== KAYNAK: {source} =====")
    
    if not feed.entries:
        print(f"⚠️ Bu kaynaktan haber gelmedi!")
        print(f"bozo: {feed.bozo}")
        continue

    for index ,news in enumerate(feed.entries[:3],start =1):
        clean_summary= BeautifulSoup(news.summary , "html.parser").get_text()
        print(f"[{index}]{news.title}\nLink: {news.link}\nPublish Date: {news.published}")
        if len(clean_summary.strip()) > 20:
            print(f"Summary: {clean_summary}")



