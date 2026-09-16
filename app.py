from datetime import datetime
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

DATA_DIR = "news_data"
os.makedirs(DATA_DIR, exist_ok=True)

today_str = datetime.now().strftime("%Y-%m-%d")
file_path = os.path.join(DATA_DIR, f"{today_str}.json")


def fetch_reuters_news():
  # 改用多個更直接的國際財經 RSS 來源，避開 Google 搜尋快取
  urls = [
      (
          "https://news.google.com/rss/search?q=when:24h+site:reuters.com/business"
          "&hl=en-US&gl=US&ceid=US:en"
      ),
      (
          "https://news.google.com/rss/search?q=when:24h+site:reuters.com/markets"
          "&hl=en-US&gl=US&ceid=US:en"
      ),
      (
          "https://news.google.com/rss/search?q=Reuters+market+news&hl=en-US&gl=US&ceid=US:en"
      ),
  ]

  news_list = []
  seen_titles = set()

  for url in urls:
    if len(news_list) >= 3:
      break
    try:
      req = urllib.request.Request(
          url,
          headers={
              "User-Agent": (
                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
              )
          },
      )
      with urllib.request.urlopen(req) as response:
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        items = root.findall(".//item")

        for item in items:
          if len(news_list) >= 3:
            break

          title_elem = item.find("title")
          link_elem = item.find("link")
          desc_elem = item.find("description")

          raw_title = (
              title_elem.text if title_elem is not None else ""
          ).strip()
          link = (
              link_elem.text
              if link_elem is not None
              else "https://www.reuters.com"
          )
          desc = desc_elem.text if desc_elem is not None else ""

          # 清理標題雜訊
          title = raw_title
          for sep in [" - reuters.com", " - Reuters", " | Reuters", " - 路透社"]:
            if sep in title:
              title = title.split(sep)[0].strip()

          # 濾除重複或過舊/無關的標題
          if not title or title in seen_titles or title.lower() == "reuters.com":
            continue

          seen_titles.add(title)

          # 清理摘要
          clean_desc = re.sub(r"<[^<]+?>", "", desc).strip()
          clean_desc = clean_desc.replace("reuters.com", "").strip()

          if (
              not clean_desc
              or clean_desc == title
              or len(clean_desc) < 5
              or title in clean_desc
          ):
            clean_desc = (
                "點擊下方「閱讀原文」連結，即可前往路透社閱讀詳細報導內容。"
            )
          elif len(clean_desc) > 120:
            clean_desc = clean_desc[:120] + "..."

          news_list.append({"title": title, "summary": clean_desc, "url": link})
    except Exception as e:
      print(f"抓取發生錯誤: {e}")

  # 確保至少有三則
  while len(news_list) < 3:
    news_list.append({
        "title": "Global Market Live Updates",
        "summary": "System is synchronizing the latest international financial news.",
        "url": "https://www.reuters.com",
    })

  return news_list


# 執行抓取並寫入今日 JSON
news_data = fetch_reuters_news()
with open(file_path, "w", encoding="utf-8") as f:
  json.dump(news_data, f, ensure_ascii=False, indent=4)

print(f"成功更新今日即時新聞：{file_path}")