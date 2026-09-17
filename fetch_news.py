from datetime import datetime
import json
import os
import streamlit as st

st.set_page_config(page_title="全球熱門焦點頭條", page_icon="📰", layout="centered")

st.title("📰 全球熱門焦點頭條")

today_str = datetime.now().strftime("%Y-%m-%d")
st.write(f"目前顯示日期：`{today_str}`")
st.markdown("---")

DATA_DIR = "news_data"
file_path = os.path.join(DATA_DIR, f"{today_str}.json")

news_list = []

# 1. 先嘗試讀取今天的檔案
if os.path.exists(file_path):
  try:
    with open(file_path, "r", encoding="utf-8") as f:
      news_list = json.load(f)
  except Exception as e:
    print(f"讀取今日 JSON 失敗: {e}")

# 2. 如果今天檔案不存在或裡面是空的，自動找最近一天的歷史 JSON 檔案
if not news_list and os.path.exists(DATA_DIR):
  files = sorted(
      [f for f in os.listdir(DATA_DIR) if f.endswith(".json")], reverse=True
  )
  if files:
    latest_file = os.path.join(DATA_DIR, files[0])
    try:
      with open(latest_file, "r", encoding="utf-8") as f:
        news_list = json.load(f)
    except Exception as e:
      print(f"讀取歷史 JSON 失敗: {e}")

# 3. 如果還是都沒有，給予預設新聞資料
if not news_list:
  news_list = [{
      "title": "全球市場即時動態更新中",
      "summary": (
          "系統正在同步最新外電與市場資訊，請稍後重新整理或檢查 GitHub"
          " Actions 執行狀態。"
      ),
      "url": "https://www.bbc.com/news",
  }]

# 渲染畫面上的新聞卡片
for i, news in enumerate(news_list[:3], 1):
  st.subheader(f"{i}. {news.get('title', '')}")
  st.write(f"**重點摘要**：{news.get('summary', '')}")
  st.markdown(f"[🔗 閱讀原文]({news.get('url', '#')})")
  st.markdown("---")