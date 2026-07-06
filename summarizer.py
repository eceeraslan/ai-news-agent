import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class Summarizer:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
        self.model = "qwen-plus"

    def summarize(self, title, content):
        """Tek bir haberi Türkçe olarak kısaca özetler."""
        if not content or len(content.strip()) < 20:
            content = title

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Sen bir teknoloji haber editörüsün. Verilen haberi 1-2 cümlede, sade ve akıcı Türkçe ile özetle. Sadece özeti yaz, başka bir şey ekleme."
                    },
                    {
                        "role": "user",
                        "content": f"Başlık: {title}\n\nİçerik: {content}"
                    }
                ],
                temperature=0.3,
                max_tokens=150,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ Özet alınamadı: {e}")
            return content  # hata olursa orijinal içeriği döndür

    def summarize_all(self, news_list):
        """Tüm haberlere Türkçe özet ekler."""
        total = len(news_list)
        for i, news in enumerate(news_list, start=1):
            print(f"  🤖 Özetleniyor {i}/{total}: {news['title'][:50]}...")
            news["summary"] = self.summarize(news["title"], news["summary"])
        return news_list