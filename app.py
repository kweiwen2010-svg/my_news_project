from datetime import datetime
import json
import os
import streamlit as st

st.set_page_config(page_title="即時財經頭條", layout="centered")

st.title("📰 即時財經頭條")

DATA_DIR = "news_data"
today_str = datetime.now().strftime("%Y-%m-%d")
file_path = os.path.join(DATA_DIR, f"{today_str}.json")

st.write(f"**目前顯示日期**：`{today_str}`")
st.markdown("---")

news_data = []
try:
  if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
      content = f.read().strip()
      if content:
        news_data = json.loads(content)
except Exception:
  news_data = []

if not news_data:
  news_data = [{
      "title": "全球市場即時動態更新中",
      "summary": "系統正在同步最新外電與市場資訊，請稍後重新整理查看。",
      "url": "https://www.reuters.com",
  }]

for i, item in enumerate(news_data[:3], 1):
  st.subheader(f"{i}. {item.get('title', '新聞')}")
  st.write(f"**重點摘要**：{item.get('summary', '')}")
  st.markdown(f"🔗 [閱讀原文]({item.get('url', 'https://www.reuters.com')})")
  st.markdown("---")