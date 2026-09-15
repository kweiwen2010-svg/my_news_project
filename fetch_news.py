from datetime import datetime
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

# 確保資料夾存在
DATA_DIR = "news_data"
os.makedirs(DATA_DIR, exist_ok=True)

# 取得當天日期字串 (例如: 2026-09-15)
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

        # 清理標題：移除結尾的 " - reuters.com" 等雜訊
        if " - " in raw_title:
          title = raw_title.rsplit(" - ", 1)[0]
        else:
          title = raw_title

        # 清除 HTML 標籤
        clean_desc = re.sub(r"<[^<]+?>", "", desc)
        if not clean_desc or clean_desc == "reuters.com":
          clean_desc = "點擊下方連結即可前往路透社閱讀完整外電報導內容。"
        elif len(clean_desc) > 100:
          clean_desc = clean_desc[:100] + "..."

        # 避免抓到無效或重複標題
        if title and title != "reuters.com":
          news_list.append(
              {"title": title, "summary": clean_desc, "url": link}
          )
  except Exception as e:
    print(f"抓取即時新聞發生錯誤: {e}")

  # 如果抓取不足三則，補上備用預設值
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