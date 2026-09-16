from datetime import datetime
import json
import os
import random
import re
import urllib.request
import xml.etree.ElementTree as ET

# 確保資料夾存在
DATA_DIR = "news_data"
os.makedirs(DATA_DIR, exist_ok=True)

# 取得當天日期字串
today_str = datetime.now().strftime("%Y-%m-%d")
file_path = os.path.join(DATA_DIR, f"{today_str}.json")


def fetch_reuters_news():
  # 加入時間戳記參數避免 Google RSS 快取舊資料
  timestamp = int(datetime.now().timestamp())
  url = f"https://news.google.com/rss/search?q=site:reuters.com&hl=zh-TW&gl=TW&ceid=TW:zh-Hant&tbm=nws&_t={timestamp}"
  req = urllib.request.Request(
      url,
      headers={
          "User-Agent": (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
          )
      },
  )

  news_list = []
  seen_titles = set()
  try:
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

        raw_title = title_elem.text if title_elem is not None else ""
        link = (
            link_elem.text if link_elem is not None else "https://www.reuters.com"
        )
        desc = desc_elem.text if desc_elem is not None else ""

        # 清理標題
        title = raw_title
        for sep in [" - reuters.com", " - Reuters", " | Reuters"]:
          if sep in title:
            title = title.split(sep)[0].strip()

        if " - " in title and (
            "reuters" in title.lower() or "路透" in title
        ):
          title = title.rsplit(" - ", 1)[0].strip()

        # 過濾重複或無效標題
        if not title or title in seen_titles or title == "reuters.com":
          continue
        seen_titles.add(title)

        # 清理摘要
        clean_desc = re.sub(r"<[^<]+?>", "", desc)
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
    print(f"抓取即時新聞發生錯誤: {e}")

  # 備用防線
  while len(news_list) < 3:
    news_list.append({
        "title": "全球市場即時動態更新中",
        "summary": "系統正在同步最新外電與市場資訊，請稍後重新整理查看。",
        "url": "https://www.reuters.com",
    })

  return news_list


# 取得動態新聞資料
news_data = fetch_reuters_news()

# 寫入當日 JSON 檔
with open(file_path, "w", encoding="utf-8") as f:
  json.dump(news_data, f, ensure_ascii=False, indent=4)

print(f"成功產生今日即時新聞資料：{file_path}")