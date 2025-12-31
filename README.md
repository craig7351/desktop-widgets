# Desktop Widget (時間 & 天氣)

這是一個使用 Python 與 PyQt6 開發的美觀桌面小工具。

## 功能特色
- **即時時間**：每秒精準更新。
- **即時天氣**：透過 `wttr.in` 獲取當前氣溫與天氣狀態。
- **玻璃擬態 (Glassmorphism)**：現代化的 UI 設計。
- **可調整透明度**：滑桿即時預覽。
- **風格切換**：支援暗色/亮色與毛玻璃質感。

## 安裝與執行

1. **建立虛擬環境**
   ```bash
   python -m venv venv
   ```

2. **啟動虛擬環境**
   ```bash
   # Windows
   .\venv\Scripts\activate
   ```

3. **安裝依賴**
   ```bash
   pip install PyQt6 requests
   ```

4. **執行程式**
   ```bash
   python main.py
   ```

## 開發工具
- **Python 3.x**
- **PyQt6**
- **Requests**
