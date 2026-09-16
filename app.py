from datetime import datetime
import json
import os
import streamlit as st

st.set_page_config(page_title="路透社即時頭條", page_chars="📰", layout="centered")

st.title("📰 路透社即時頭條")

DATA_DIR = "news_data"

# 取得今天日期
today_str = datetime.now().strftime("%Y-%m-%d")
file_path = os.path.join(DATA_DIR, f"{today_str}.json")

st.write(f"**目前顯示日期**：`{today_str}`")
st.markdown("---")

news_data = []

# 安全讀取 JSON 檔案，防止檔案毀損或空白導致畫面死當
if os.path.exists(file_path):
  try:
    with open(file_path, "r", encoding="utf-8") as f:
      content = f.read().strip()
      if content:
        news_data = json.loads(content)
  except Exception as e:
    st.warning(f"正在載入最新資料，請稍後重新整理... (錯誤提示: {e})")

# 如果沒有資料或讀取失敗，提供預設顯示
if not news_data:
  news_data = [{
      "title": "全球市場即時動態更新中",
      "summary": "系統正在同步最新外電與市場資訊，請稍後重新整理查看。",
      "url": "https://www.reuters.com",
  }]

# 渲染新聞卡片
for i, item in enumerate(news_data[:3], 1):
  st.subheader(f"{i}. {item.get('title', '無標題')}")
  st.write(f"**重點摘要**：{item.get('summary', '無摘要')}")
  st.markdown(f"🔗 [閱讀原文]({item.get('url', 'https://www.reuters.com')})")
  st.markdown("---")