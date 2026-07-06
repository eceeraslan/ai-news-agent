"""GitHub Actions tarafından zamanında bir kez çalıştırılır."""
import config
from sources.rss_fetcher import RSSFetcher
from email_sender import EmailSender
from summarizer import Summarizer


def main():
    print("📰 Haberler çekiliyor...")
    fetcher = RSSFetcher(
        sources=config.SOURCES,
        news_per_source=config.NEWS_PER_SOURCE,
        min_summary_length=config.MIN_SUMMARY_LENGTH
    )
    news_list = fetcher.fetch_all()
    print(f"✅ {len(news_list)} haber çekildi.")

    print("🤖 Haberler AI ile özetleniyor...")
    summarizer = Summarizer()
    news_list = summarizer.summarize_all(news_list)
    print("✅ Özetler hazır.")

    sender = EmailSender()
    sender.send(news_list)


if __name__ == "__main__":
    main()