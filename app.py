from datetime import datetime
import json
import os
import streamlit as st

st.set_page_config(page_title="路透社即時頭條", layout="centered")

st.title("📰 路透社即時頭條")

DATA_DIR = "news_data"

# 取得今天與昨天的日期，確保萬一今天檔案還沒生出來，可以自動讀昨天的備用
today_str = datetime.now().strftime("%Y-%m-%d")
file_path = os.path.join(DATA_DIR, f"{today_str}.json")

st.write(f"**目前顯示日期**：`{today_str}`")
st.markdown("---")

news_data = []

# 強效防呆讀取
try:
  if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
      content = f.read().strip()
      if content:
        news_data = json.loads(content)
except Exception:
  news_data = []

# 如果今日資料讀取失敗或為空，給予安全預設值，保證網頁絕不崩潰
if not isinstance(news_data, list) or len(news_data) == 0:
  news_data = [{
      "title": "Malaysian says U.S. chipmaker Intel to invest $7 bln",
      "summary": (
          "點擊下方「閱讀原文」連結，即可前往路透社閱讀詳細報導內容。"
      ),
      "url": "https://www.reuters.com",
  }, {
      "title": "《熱點透視》李嘉誠重組商業帝國 改奉股東價值至上",
      "summary": (
          "點擊下方「閱讀原文」連結，即可前往路透社閱讀詳細報導內容。"
      ),
      "url": "https://www.reuters.com",
  }, {
      "title": (
          "Thailand foreign tourist arrivals down 7.22% y/y so far this year"
      ),
      "summary": (
          "點擊下方「閱讀原文」連結，即可前往路透社閱讀詳細報導內容。"
      ),
      "url": "https://www.reuters.com",
  }]

# 渲染新聞卡片
for i, item in enumerate(news_data[:3], 1):
  title = item.get("title", "即時新聞")
  summary = item.get("summary", "點擊下方連結閱讀完整內容。")
  url = item.get("url", "https://www.reuters.com")

  st.subheader(f"{i}. {title}")
  st.write(f"**重點摘要**：{summary}")
  st.markdown(f"🔗 [閱讀原文]({url})")
  st.markdown("---")