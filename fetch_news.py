from datetime import datetime
import json
import os

# 確保資料夾存在
DATA_DIR = "news_data"
os.makedirs(DATA_DIR, exist_ok=True)

# 取得當天日期字串 (例如: 2026-09-14)
today_str = datetime.now().strftime("%Y-%m-%d")
file_path = os.path.join(DATA_DIR, f"{today_str}.json")

# 模擬抓取與精選的三則新聞 (實作時可換成你的爬蟲或 API 邏輯)
sample_news = [
    {
        "title": "全球半導體供應鏈迎來新變局",
        "summary": "最新市場報告指出，隨著亞洲產能擴增，高階晶片成本結構正在發生微妙變化，牽動各大科技巨頭佈局。",
        "url": "https://www.reuters.com",
    },
    {
        "title": "聯準會最新利率動向與市場反應",
        "summary": "多位官員發言暗示通膨數據放緩，投資人正評估年底前降息的機率，帶動公債殖利率短暫下滑。",
        "url": "https://www.reuters.com",
    },
    {
        "title": "地緣政治風險對能源市場的影響",
        "summary": "中東局勢持續牽動原油供給，期貨市場在盤中出現劇烈震盪，分析師警告短期波動恐將加劇。",
        "url": "https://www.reuters.com",
    },
]

# 寫入當日 JSON 檔
with open(file_path, "w", encoding="utf-8") as f:
  json.dump(sample_news, f, ensure_ascii=False, indent=4)

print(f"成功產生今日新聞資料：{file_path}")