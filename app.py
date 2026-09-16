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
  url = "https://news.google.com/rss/search?q=site:reuters.com&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

  news_list = []
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

        title = raw_title
        for sep in [" - reuters.com", " - Reuters", " | Reuters"]:
          if sep in title:
            title = title.split(sep)[0].strip()

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

        if title and title != "reuters.com":
          news_list.append(
              {"title": title, "summary": clean_desc, "url": link}
          )
  except Exception as e:
    print(f"發生錯誤: {e}")

  # 確保萬一抓不到時也有預設資料，絕不為空
  while len(news_list) < 3:
    news_list.append({
        "title": "全球市場即時動態更新中",
        "summary": "系統正在同步最新外電與市場資訊，請稍後重新整理查看。",
        "url": "https://www.reuters.com",
    })

  return news_list


# 執行並寫入
news_data = fetch_reuters_news()
with open(file_path, "w", encoding="utf-8") as f:
  json.dump(news_data, f, ensure_ascii=False, indent=4)

print(f"成功更新：{file_path}")