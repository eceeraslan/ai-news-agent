import feedparser

fp_parser = feedparser.parse("https://techcrunch.com/category/artificial-intelligence/feed/")

fp_news = fp_parser.entries

for news in fp_news[:5]:
    print(news.title)


