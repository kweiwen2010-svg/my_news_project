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


def fetch_news():
  # 改用專門聚合路透社世界與市場焦點的 RSS 來源
  url = "https://news.google.com/rss/search?q=when:24h+site:reuters.com&hl=en-US&gl=US&ceid=US:en"
  req = urllib.request.Request(
      url,
      headers={
          "User-Agent": (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
              " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
          )
      },
  )

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

        title = (
            title_elem.text if title_elem is not None and title_elem.text else ""
        )
        link = (
            link_elem.text
            if link_elem is not None and link_elem.text
            else "https://www.reuters.com"
        )
        desc = (
            desc_elem.text if desc_elem is not None and desc_elem.text else ""
        )

        clean_desc = re.sub(r"<[^<]+?>", "", desc).strip()
        if len(clean_desc) > 120:
          clean_desc = clean_desc[:120] + "..."

        if title:
          news_list.append({
              "title": title.strip(),
              "summary": clean_desc or "點擊閱讀完整路透社報導。",
              "url": link.strip(),
          })
  except Exception as e:
    print(f"抓取錯誤: {e}")

  if not news_list:
    news_list.append({
        "title": f"全球路透焦點更新中 ({today_str})",
        "summary": "正在等待系統排程同步最新路透外電，請稍後重新整理。",
        "url": "https://www.reuters.com",
    })

  return news_list


news_data = fetch_news()
with open(file_path, "w", encoding="utf-8") as f:
  json.dump(news_data, f, ensure_ascii=False, indent=4)
print("更新完成")