# ETS2_Dedicated_Server_GUI (For Windows)

![Windows](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Language-Python%2fEXE-green)

## 專案簡介  
這是一款專為 Windows 平台打造的 **ETS2 Dedicated Server 管理 GUI 工具**。  
目標是讓玩家可以在 Windows 上：  
- 一鍵下載 / 安裝 Dedicated Server  
- 自動生成伺服器設定檔  
- 啟動伺服器並查看日誌  
- 完全不必進入遊戲、手動搬檔或在命令列操作  

---

## 功能特色  
- **自動下載與更新伺服器**  
  使用 SteamCMD 自動安裝與更新 ETS2 Dedicated Server。  
- **GUI 設定面板**  
  提供伺服器名稱、地圖、密碼、最大玩家數、公開模式等設定項目。  
- **自動生成設定檔**  
  根據模板自動寫入 `server_config.sii` 等關鍵設定。  
- **啟動與日誌監控**  
  點擊按鈕即可啟動伺服器，並在 GUI 中即時顯示伺服器輸出（console log）。  
- **路徑管理**  
  自動偵測 SteamCMD 路徑與 Dedicated Server 安裝路徑，或讓用戶手動選擇。  
- **EULA 授權流程**  
  安裝時顯示使用者授權協議 (EULA)，並在設定檔/Log 中記錄同意狀態。  

---

## 系統需求  
- Windows 10 或更新版本  
- 64-bit 系統  
- Internet 連線（用於下載伺服器檔案）  
- 約 2 GB 可用磁碟空間  

---

## 安裝方式  

1. 從 GitHub 克隆或下載本專案：  
   ```bash
   git clone https://github.com/<你的帳號>/ets2-server-helper.git
   cd ets2-server-helper
