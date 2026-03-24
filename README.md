# Text2Image API

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

**在 Discord、LINE、Telegram 等平台直接嵌入文字圖片的 API 服務**

只需一個 URL，就能在Discord自動顯示文字圖片。無需手動上傳檔案，瞬間產生梗圖字幕。

> 💬 **核心功能**: Discord 會自動識別 `Content-Type: image/png` 回應標頭，直接將 API 連結預覽為圖片。

## ✨ 為什麼需要這個？

在 Discord 聊天平台，貼上圖片連結時：
- ✅ **如果回應是 `image/png`** → 平台自動嵌入顯示圖片
- ❌ **如果回應是 HTML** → 只顯示普通連結

**這個 API 讓你用 URL 直接生成並嵌入文字圖片，無需手動製作和上傳！**

## 🎯 功能特色

- 💬 **直接嵌入** - 在 Discord 貼上連結即可顯示圖片
- 🌏 **支援中文** - 完整支援繁體、簡體中文及 CJK 字元
- 🎨 **清晰易讀** - 白色文字 + 黑色描邊，任何背景都清楚
- ⚡ **秒速回應** - 智慧快取系統，相同文字立即返回
- 🐳 **一鍵部署** - Docker Compose 快速啟動

## 🚀 使用範例

### 在 Discord 中使用

直接貼上連結，Discord 會自動顯示圖片：

```
http://127.0.0.1:3000/image?text=我是一台邪惡的卡車
http://127.0.0.1:3000/image?text=你是狂派變形金剛喔
http://127.0.0.1:3000/image?text=海上的大風像碎玻璃一樣%20猛刮我的小臉蛋
```

![我是一台邪惡的卡車](generated_images/3db785fbd38e69a066f58ebdfa9cbf525f78494576375ada1deebd4f014e3ae4.png)
![你是狂派變形金剛喔](generated_images/5a14db09abf7c04a12700adf894b62c158313c6a955492eecca0dd675dbc51c1.png)
![海上的大風像碎玻璃一樣%20猛刮我的小臉蛋](generated_images/93547159f48922e5673a09d846e9a0e6f35bca6293007d36a97827bd7f86394f.png)


### URL 編碼

如果文字包含空格或特殊符號，需要進行 URL 編碼：
```
# 空格 → %20
http://127.0.0.1:3000/image?text=Hello%20World

# 也可以用 + 代替空格
http://127.0.0.1:3000/image?text=Hello+World
```

## 📦 部署方式

### Docker Compose（推薦）

```bash
# 1. 下載專案
git clone https://github.com/hua9239/Text2Image.git
cd Text2Image

# 2. 啟動服務
docker-compose up -d

# 3. 測試（在瀏覽器開啟）
http://localhost:3000/image?text=測試文字
```

### 本地執行

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動服務
python main.py

# 訪問 http://localhost:3000
```

### 公開到網路

部署到有公網 IP 的伺服器，就能在任何地方使用：

1. **自架主機** - 使用自己的 VPS（需開放 3000 port）
2. **雲端平台** - 部署到 Heroku、Railway、Render 等
3. **Ngrok** - 快速測試用（免費臨時網址）

```bash
# 使用 Ngrok 快速取得公開網址
ngrok http 3000
# 會得到類似 https://abc123.ngrok.io 的網址
```

## 🔧 API 規格

### `GET /image?text={文字內容}`

**參數:**
- `text` - 要顯示的文字（最多 100 字）

**回應:**
- Content-Type: `image/png`
- 透明背景 PNG 圖片
- 白色文字 + 黑色描邊（易讀）

**圖片規格:**
- 高度: 100px
- 寬度: 自動適配文字長度
- 字體: Noto Sans CJK（支援中文）

## 💡 常見問題

<details>
<summary><b>為什麼 Discord 沒有自動顯示圖片？</b></summary>

確認以下幾點：
1. URL 是否正確（能在瀏覽器開啟並顯示圖片）
2. Discord 是否啟用「連結預覽」功能
3. 伺服器是否可從外部訪問（localhost 無法在 Discord 顯示）
</details>

<details>
<summary><b>如何修改文字樣式？</b></summary>

編輯 [main.py](main.py#L18-L23) 中的配置：
```python
FONT_SIZE = 72          # 字體大小
IMAGE_HEIGHT = 100      # 圖片高度
TEXT_COLOR = "#FFFFFF"  # 文字顏色
STROKE_COLOR = "#000000"  # 描邊顏色
STROKE_WIDTH = 3        # 描邊寬度
```
</details>

## 📄 授權

MIT License - 詳見 [LICENSE](LICENSE)
