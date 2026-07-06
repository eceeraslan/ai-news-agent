import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()


class EmailSender:

    def __init__(self):
        self.gmail_user = os.getenv("GMAIL_USER")
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")
        self.mail_to = os.getenv("MAIL_TO")

    def build_html(self, news_list):
        items = ""
        for i, news in enumerate(news_list, start=1):
            link = news['link']
            title = news['title']
            source = news['source']
            pub_date = news['publish_date']
            summary_html = f"<p style='color:#555;font-size:14px;'>{news['summary']}</p>" if news["summary"] else ""

            items += f"""
            <div style='border-left:4px solid #4A90E2;padding:10px 16px;margin-bottom:20px;background:#f9f9f9;border-radius:4px;'>
                <span style='font-size:12px;color:#999;'>[{i}]</span>
                <h3 style='margin:4px 0;'><a href="{link}" style='color:#222;text-decoration:none;'>{title}</a></h3>
                <span style='font-size:12px;color:#aaa;'>{pub_date}</span>
                {summary_html}
            </div>
            """

        return f"""
        <html><body style='font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;'>
            <h2 style='color:#4A90E2;border-bottom:2px solid #4A90E2;padding-bottom:8px;'>🗞️ Günlük AI Haberleri</h2>
            {items}
            <p style='font-size:12px;color:#bbb;text-align:center;margin-top:30px;'>ai-news-agent tarafından gönderildi.</p>
        </body></html>
        """

    def send(self, news_list):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🗞️ Günlük AI Haberleri ({len(news_list)} haber)"
        msg["From"] = self.gmail_user
        msg["To"] = self.mail_to

        html_content = self.build_html(news_list)

        plain = MIMEText("Haberleri görmek için HTML destekli bir mail istemcisi kullanın.", "plain", "utf-8")
        html = MIMEText(html_content, "html", "utf-8")

        msg.attach(plain)
        msg.attach(html)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(self.gmail_user, self.mail_to, msg.as_string())

        print(f"✅ Mail gönderildi → {self.mail_to}")