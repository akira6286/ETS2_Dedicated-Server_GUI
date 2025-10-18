# modules/config_generator.py

import os

# 專案內生成資料夾
LOCAL_GENERATED_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Euro Truck Simulator 2")
os.makedirs(LOCAL_GENERATED_DIR, exist_ok=True)

def generate_server_sii(output_name, settings):
    """
    直接生成完整 server_config 區塊，不依賴模板或 SIIHandler
    :param output_name: 輸出檔名 (例如 server_config.sii)
    :param settings: 設定字典，包含 lobby_name, description, welcome_message, password, max_players, server_logon_token
    :return: 生成檔案完整路徑
    """
    output_path = os.path.join(LOCAL_GENERATED_DIR, output_name)

    token_line = f'    server_logon_token: "{settings.get("server_logon_token", "")}"' if settings.get("server_logon_token") else "    server_logon_token:"

    content = f"""SiiNunit
{{
server_config : _nameless.25e.b6cc.40a0 {{
    lobby_name : "{settings['lobby_name']}"
    description : "{settings['description']}"
    welcome_message : "{settings['welcome_message']}"
    password : "{settings['password']}"
    max_players : {settings['max_players']}
    max_vehicles_total: 500
    max_ai_vehicles_player: 200
    max_ai_vehicles_player_spawn: 200
    connection_virtual_port: 100
    query_virtual_port: 101
    connection_dedicated_port: 27015
    query_dedicated_port: 27016
{token_line}
    player_damage: false
    traffic: true
    hide_in_company: false
    hide_colliding: true
    force_speed_limiter: false
    mods_optioning: true
    timezones: 0
    service_no_collision: false
    in_menu_ghosting: false
    name_tags: true
    friends_only: false
    show_server: true
    moderator_list: 0
}}
}}
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[INFO] 已生成 .sii: {output_path}")
    return output_path


# 測試用
if __name__ == "__main__":
    settings = {
        "lobby_name": "Euro Truck Simulator2 Dedicated server 128",
        "description": "128",
        "welcome_message": "Welcome, Have fun",
        "password": "",
        "max_players": 128,
        "server_logon_token": "MYTOKEN123"
    }
    file_path = generate_server_sii("server_config.sii", settings)
    print(f"生成完成: {file_path}")
