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
  # 改用 Yahoo 提供的即時路透社 RSS，徹底避開 Google 搜尋快取
  url = "https://news.yahoo.com/rss/reuters"
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

        raw_title = (
            title_elem.text if title_elem is not None else ""
        ).strip()
        link = (
            link_elem.text
            if link_elem is not None
            else "https://www.reuters.com"
        )
        desc = desc_elem.text if desc_elem is not None else ""

        title = raw_title
        if not title or title in seen_titles:
          continue

        seen_titles.add(title)

        # 清理摘要 HTML 標籤
        clean_desc = re.sub(r"<[^<]+?>", "", desc).strip()
        if not clean_desc or len(clean_desc) < 5:
          clean_desc = (
              "點擊下方「閱讀原文」連結，即可前往閱讀詳細報導內容。"
          )
        elif len(clean_desc) > 120:
          clean_desc = clean_desc[:120] + "..."

        news_list.append({"title": title, "summary": clean_desc, "url": link})
  except Exception as e:
    print(f"抓取錯誤: {e}")

  # 如果真的抓不到，顯示乾淨的即時同步提示，絕對不放舊新聞
  while len(news_list) < 3:
    news_list.append({
        "title": "市場最新動態同步中 (Market News Syncing)",
        "summary": "系統正在擷取最新外電資訊，請稍後重新整理。",
        "url": "https://www.reuters.com",
    })

  return news_list


# 執行抓取並覆寫今日檔案
news_data = fetch_reuters_news()
with open(file_path, "w", encoding="utf-8") as f:
  json.dump(news_data, f, ensure_ascii=False, indent=4)

print(f"成功更新今日即時新聞：{file_path}")