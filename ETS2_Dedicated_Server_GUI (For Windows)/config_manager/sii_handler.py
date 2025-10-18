# config_manager/sii_handler.py

import os
import re
import shutil

class SIIHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []       # 原始檔案每行內容
        self.key_map = {}     # key -> line index
        self.load_file()

    def load_file(self):
        """讀取 .sii 並解析 key 與對應行號"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"{self.file_path} 不存在")

        with open(self.file_path, "r", encoding="utf-8") as f:
            self.lines = f.readlines()

        # 建立 key -> line index 映射
        self.key_map = {}
        pattern = re.compile(r'(\S+)\s*:\s*(.+)')
        for idx, line in enumerate(self.lines):
            stripped = line.strip()
            if stripped.startswith('//') or not stripped:
                continue
            match = pattern.match(stripped)
            if match:
                key, value = match.groups()
                self.key_map[key] = idx

    def get(self, key, default=None):
        """取得設定值"""
        idx = self.key_map.get(key)
        if idx is not None:
            line = self.lines[idx].strip()
            return line.split(':', 1)[1].strip()
        return default

    def set(self, key, value):
        """修改或新增單個 key-value"""
        value = str(value)
        idx = self.key_map.get(key)
        if idx is not None:
            self.lines[idx] = f"{key} : {value}\n"
        else:
            self.lines.append(f"{key} : {value}\n")
            self.key_map[key] = len(self.lines) - 1

    def batch_set(self, kv_dict):
        """一次批量修改多個 key-value"""
        if not isinstance(kv_dict, dict):
            raise TypeError("batch_set 需要傳入 dict")
        for key, value in kv_dict.items():
            self.set(key, value)

    def save(self, backup=True):
        """存回 .sii 檔案，保留註解與排版"""
        if backup:
            backup_path = self.file_path + ".bak"
            shutil.copy2(self.file_path, backup_path)

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.writelines(self.lines)


if __name__ == "__main__":
    # 範例使用
    sii_file = "your_server_config.sii"
    handler = SIIHandler(sii_file)

    print("原始設定：")
    for key in handler.key_map:
        print(f"{key} = {handler.get(key)}")

    # 單獨修改
    handler.set("lobby_name", "我的中文伺服器")

    # 批量修改
    handler.batch_set({
        "max_players": 128,
        "description": "這是一個中文伺服器，歡迎加入！",
        "welcome_message": "大家好～"
    })

    handler.save()
    print(f"已存回 {sii_file} 並備份舊檔")
