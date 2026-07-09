import feedparser
from bs4 import BeautifulSoup


class RSSFetcher:
    
    def __init__(self,sources,news_per_source,min_summary_length):
        self.sources=sources
        self.news_per_source=news_per_source
        self.min_summary_length=min_summary_length

    def fetch_all(self):
        all_news = []

        for source in self.sources:
            feed=feedparser.parse(source)
            if not feed.entries:
                continue
            
            for news in feed.entries[:self.news_per_source]:
                raw_summary=getattr(news,"summary","")  or ""
                clean_summary =BeautifulSoup(raw_summary,"html.parser").get_text()
                news_dict={
                      "source":source,
                      "title":news.title,
                      "link":news.link,
                      "publish_date":news.published,
                      "summary":clean_summary if len(clean_summary.strip()) > self.min_summary_length else ""
                    }
                all_news.append(news_dict)
        return all_news


