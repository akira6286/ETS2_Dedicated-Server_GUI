# modules/config_generator.py

import os
import shutil
from config_manager.sii_handler import SIIHandler

# 取得模組所在資料夾
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 模板檔案
TEMPLATE_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "config_manager", "templates", "server_config_template.sii")
)

# 專案內生成資料夾
LOCAL_GENERATED_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "generated"))

def generate_server_sii(output_name, settings_dict):
    """
    根據模板生成新的 server .sii，只生成有值的欄位
    :param output_name: 輸出檔名 (例如 server_config.sii)
    :param settings_dict: 要修改的設定字典
    :return: 生成檔案絕對路徑 (在 ./generated 資料夾內)
    """
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"模板檔案不存在: {TEMPLATE_PATH}")

    # 過濾掉空值的設定
    clean_settings = {k: v for k, v in settings_dict.items() if v != ""}

    # 確保生成資料夾存在
    os.makedirs(LOCAL_GENERATED_DIR, exist_ok=True)

    # 生成檔案路徑
    output_path = os.path.join(LOCAL_GENERATED_DIR, output_name)

    # 複製模板
    shutil.copy2(TEMPLATE_PATH, output_path)

    # 修改設定
    handler = SIIHandler(output_path)
    handler.batch_set(clean_settings)
    handler.save()  # 直接覆蓋 output_path

    print(f"[INFO] 已生成: {output_path}")
    return output_path

# 範例測試
if __name__ == "__main__":
    settings = {
        "lobby_name": "我的中文伺服器",
        "description": "128 玩家專用",
        "welcome_message": "歡迎加入！",
        "max_players": 128,
        "password": ""  # 空密碼將不生成 password 行
    }

    generated_file = generate_server_sii("server_config.sii", settings)
    print(f"生成完成: {generated_file}")
