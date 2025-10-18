# modules/server_launcher.py

import os
import subprocess
import configparser
from tkinter import filedialog, messagebox

CONFIG_FILE = "config.ini"
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Euro Truck Simulator 2")
LOGS_DIR = os.path.join(DOCUMENTS_DIR, "logs")

# 全域儲存 server subprocess
server_process = None

def get_server_path():
    """自動偵測或選擇 ETS2 Dedicated Server exe 路徑"""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        path = config.get("server", "exe_path", fallback=None)
        if path and os.path.exists(path):
            return path

    # 嘗試自動搜尋常見 Steam 路徑
    common_paths = [
        r"E:\SteamLibrary\steamapps\common\Euro Truck Simulator 2 Dedicated Server\bin\win_x64\eurotrucks2_server.exe",
        r"C:\Program Files (x86)\Steam\steamapps\common\Euro Truck Simulator 2 Dedicated Server\bin\win_x64\eurotrucks2_server.exe",
        r"C:\Program Files\Steam\steamapps\common\Euro Truck Simulator 2 Dedicated Server\bin\win_x64\eurotrucks2_server.exe"
    ]
    for p in common_paths:
        if os.path.exists(p):
            save_path_to_config(p)
            return p

    # 找不到，要求使用者選擇
    root = filedialog.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="選擇 ETS2 Dedicated Server exe",
        filetypes=[("EXE files", "*.exe")]
    )
    if path:
        save_path_to_config(path)
        return path
    return None

def save_path_to_config(path):
    config = configparser.ConfigParser()
    config["server"] = {"exe_path": path}
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

def launch_server(sii_file_name="server_config.sii"):
    """啟動伺服器"""
    global server_process
    if server_process and server_process.poll() is None:
        messagebox.showwarning("提醒", "伺服器已在運行中！")
        return

    server_path = get_server_path()
    if not server_path or not os.path.exists(server_path):
        messagebox.showerror("錯誤", "找不到 ETS2 Dedicated Server exe")
        return

    sii_path = os.path.join(DOCUMENTS_DIR, sii_file_name)
    if not os.path.exists(sii_path):
        messagebox.showerror("錯誤", f"找不到 .sii 設定檔: {sii_path}")
        return

    os.makedirs(LOGS_DIR, exist_ok=True)
    log_file = os.path.join(LOGS_DIR, "server.log")

    # 讀 token，如果有就帶上
    config = configparser.ConfigParser()
    token_args = []
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        token = config.get("server", "server_token", fallback="")
        if token:
            token_args = ["-steam_server_token", token]

    cmd = [server_path, "-config", sii_path, "-log", log_file] + token_args

    try:
        # 使用 cwd 指向 Dedicated Server 所在資料夾
        server_process = subprocess.Popen(cmd, cwd=os.path.dirname(server_path))
        messagebox.showinfo("成功", f"伺服器已啟動！日誌: {log_file}")
    except Exception as e:
        messagebox.showerror("錯誤", str(e))

def stop_server():
    """停止伺服器"""
    global server_process
    if server_process and server_process.poll() is None:
        server_process.terminate()
        server_process.wait()
        server_process = None
        messagebox.showinfo("成功", "伺服器已停止")
    else:
        messagebox.showinfo("提醒", "伺服器未在運行中")
