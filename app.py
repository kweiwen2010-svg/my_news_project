import json
import os
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="路透社每日必讀精選", page_icon="📰", layout="wide"
)

# 資料儲存目錄
DATA_DIR = "news_data"


def get_available_dates():
  if not os.path.exists(DATA_DIR):
    return []
  files = [f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")]
  return sorted(files, reverse=True)  # 由新到舊排序


# --- 側邊欄：歷史存檔查詢 ---
st.sidebar.title("📰 路透社早報")
available_dates = get_available_dates()

selected_date = None
if available_dates:
  st.sidebar.subheader("歷史存檔查詢")
  # 預設選取最新日期
  selected_date = st.sidebar.selectbox("選擇日期", available_dates)
else:
  st.sidebar.info("目前尚無歷史存檔資料")

# --- 主畫面顯示邏輯 ---
st.title("🔥 路透社必讀新聞三則")

if selected_date:
  st.markdown(f"**目前顯示日期：** `{selected_date}`")

  # 讀取對應日期的 JSON 檔案
  file_path = os.path.join(DATA_DIR, f"{selected_date}.json")
  if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
      news_list = json.load(f)

    # 呈現三則新聞
    for idx, item in enumerate(news_list, 1):
      with st.container():
        st.markdown(f"### {idx}. {item['title']}")
        st.markdown(f"**重點摘要：** {item['summary']}")
        st.markdown(f"[🔗 閱讀原文]({item['url']})")
        st.divider()
  else:
    st.warning("找不到該日期的資料檔案。")
else:
  st.info("請等待每日自動抓取程式執行，或手動建立今日資料。")