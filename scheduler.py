import schedule
import time
import os
from dotenv import load_dotenv

import config
from sources.rss_fetcher import RSSFetcher
from email_sender import EmailSender
from summarizer import Summarizer

load_dotenv()

SEND_HOUR = os.getenv("SEND_HOUR", "8")


def job():
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
    send_time = f"{int(SEND_HOUR):02d}:00"
    schedule.every().day.at(send_time).do(job)
    print(f"⏰ Scheduler başladı. Her gün {send_time}'de mail gönderilecek.")

    # Başlangıçta bir kez çalıştır (test için)
    job()

    while True:
        schedule.run_pending()
        time.sleep(60)