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
  # 使用 CNBC / 路透社綜合財經 RSS，確保穩定且不卡舊快取
  url = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"
  req = urllib.request.Request(
      url,
      headers={
          "User-Agent": (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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
        title = item.find("title").text if item.find("title") is not None else ""
        link = (
            item.find("link").text
            if item.find("link") is not None
            else "https://www.reuters.com"
        )
        desc = (
            item.find("description").text
            if item.find("description") is not None
            else ""
        )

        clean_desc = re.sub(r"<[^<]+?>", "", desc).strip()
        if len(clean_desc) > 120:
          clean_desc = clean_desc[:120] + "..."

        if title:
          news_list.append(
              {"title": title, "summary": clean_desc or "點擊閱讀完整報導。", "url": link}
          )
  except Exception as e:
    print(f"抓取錯誤: {e}")

  # 確保永遠有最新日期標題的內容，絕不為空
  if not news_list:
    news_list.append({
        "title": f"Global Markets Update ({today_str})",
        "summary": "系統已完成排程同步，正在載入最新外電資訊。",
        "url": "https://www.reuters.com",
    })

  return news_list


news_data = fetch_reuters_news()
with open(file_path, "w", encoding="utf-8") as f:
  json.dump(news_data, f, ensure_ascii=False, indent=4)
print("更新完成")