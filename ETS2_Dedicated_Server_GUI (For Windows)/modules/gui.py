# modules/gui.py

import os
import shutil
import tkinter as tk
from tkinter import messagebox, scrolledtext
from modules import config_generator, server_launcher
import threading
import configparser

# 日誌路徑
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Euro Truck Simulator 2")
LOGS_DIR = os.path.join(DOCUMENTS_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "server.log")

os.makedirs(LOGS_DIR, exist_ok=True)

CONFIG_PATH = os.path.join(os.getcwd(), "config.ini")

# 固定生成的 .sii 檔名
SII_FILENAME = "server_config.sii"

class ServerConfigGUI:
    def __init__(self, master):
        self.master = master
        master.title("ETS2 Server Config Generator & Launcher")

        # 標籤
        labels = ["Lobby Name:", "Description:", "Welcome Message:", "Max Players:", "Password:", "Server Token:"]
        for i, text in enumerate(labels):
            tk.Label(master, text=text).grid(row=i, column=0, sticky="e")

        # 變數
        self.lobby_name_var = tk.StringVar(value="Euro Truck Simulator2 Dedicated server 128")
        self.description_var = tk.StringVar(value="128")
        self.welcome_var = tk.StringVar(value="Welcome, Have fun")
        self.max_players_var = tk.IntVar(value=128)
        self.password_var = tk.StringVar(value="")
        self.token_var = tk.StringVar()

        # Entry
        tk.Entry(master, textvariable=self.lobby_name_var, width=40).grid(row=0, column=1)
        tk.Entry(master, textvariable=self.description_var, width=40).grid(row=1, column=1)
        tk.Entry(master, textvariable=self.welcome_var, width=40).grid(row=2, column=1)
        tk.Entry(master, textvariable=self.max_players_var, width=40).grid(row=3, column=1)

        self.password_entry = tk.Entry(master, textvariable=self.password_var, width=40, fg="grey")
        self.password_entry.grid(row=4, column=1)
        self.password_entry.insert(0, "預設空白為無密碼")
        self.password_entry.bind("<FocusIn>", self.clear_password_placeholder)
        self.password_entry.bind("<FocusOut>", self.add_password_placeholder)

        # Token Entry
        token_from_config = self.read_token_from_config()
        if token_from_config:
            self.token_var.set(token_from_config)
        else:
            self.token_var.set("")

        self.token_entry = tk.Entry(master, textvariable=self.token_var, width=40, fg="grey")
        self.token_entry.grid(row=5, column=1)
        if not token_from_config:
            self.token_entry.insert(0, "必填項")
        self.token_entry.bind("<FocusIn>", self.clear_token_placeholder)
        self.token_entry.bind("<FocusOut>", self.add_token_placeholder)

        # 按鈕
        tk.Button(master, text="生成 .sii", command=self.generate_sii).grid(row=6, column=0, columnspan=3, pady=5)

        self.launch_btn = tk.Button(master, text="啟動伺服器", command=self.launch_server, bg="green", fg="white")
        self.launch_btn.grid(row=7, column=0, columnspan=1, pady=5)
        self.stop_btn = tk.Button(master, text="停止伺服器", command=self.stop_server, bg="red", fg="white")
        self.stop_btn.grid(row=7, column=2, columnspan=1, pady=5)

        # 日誌視窗
        tk.Label(master, text="伺服器日誌:").grid(row=8, column=0, columnspan=3)
        self.log_text = scrolledtext.ScrolledText(master, width=80, height=20, state="disabled")
        self.log_text.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

        self.generated_file = None
        self.refresh_log()

    # 密碼 placeholder
    def clear_password_placeholder(self, event):
        if self.password_var.get() == "預設空白為無密碼":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(fg="black")

    def add_password_placeholder(self, event):
        if not self.password_var.get():
            self.password_entry.insert(0, "預設空白為無密碼")
            self.password_entry.config(fg="grey")

    # Token placeholder
    def clear_token_placeholder(self, event):
        if self.token_var.get() == "必填項":
            self.token_entry.delete(0, tk.END)
            self.token_entry.config(fg="black")

    def add_token_placeholder(self, event):
        if not self.token_var.get():
            self.token_entry.insert(0, "必填項")
            self.token_entry.config(fg="grey")

    # 讀 token
    def read_token_from_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_PATH):
            config.read(CONFIG_PATH)
            if config.has_option("server", "server_token"):
                return config.get("server", "server_token")
        return None

    # 生成 .sii (固定名稱)
    def generate_sii(self):
        password = self.password_var.get()
        if password == "預設空白為無密碼":
            password = ""
        token = self.token_var.get()
        if token == "選填，可不填":
            token = ""

        settings = {
            "lobby_name": self.lobby_name_var.get(),
            "description": self.description_var.get(),
            "welcome_message": self.welcome_var.get(),
            "max_players": self.max_players_var.get(),
            "password": password,
            "server_logon_token": token
        }

        try:
            current_dir = os.getcwd()
            generated_dir = os.path.join(current_dir, "generated")
            os.makedirs(generated_dir, exist_ok=True)

            sii_output_path = os.path.join(generated_dir, SII_FILENAME)

            self.generated_file = config_generator.generate_server_sii(sii_output_path, settings)
            messagebox.showinfo("成功", f"已生成設定檔：\n{sii_output_path}")

            self.update_token_in_config(token)

            # 延遲搬移到 OneDrive
            def move_to_onedrive():
                try:
                    onedrive_docs_dir = os.path.join(os.path.expanduser("~"), "Documents", "Euro Truck Simulator 2")
                    os.makedirs(onedrive_docs_dir, exist_ok=True)

                    dest_path = os.path.join(onedrive_docs_dir, os.path.basename(self.generated_file))
                    shutil.copy2(self.generated_file, dest_path)

                    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
                    for filename in ["server_packages.dat", "server_packages.sii"]:
                        src = os.path.join(assets_dir, filename)
                        if os.path.exists(src):
                            shutil.copy2(src, os.path.join(onedrive_docs_dir, filename))
                            print(f"[INFO] 已搬移 {filename} 到 OneDrive")
                        else:
                            print(f"[WARN] 找不到 {filename}: {src}")

                    print(f"[INFO] 所有檔案已搬移到 {onedrive_docs_dir}")
                except Exception as e:
                    print(f"[ERROR] 搬移到 OneDrive 失敗: {e}")

            threading.Timer(1.0, move_to_onedrive).start()

        except Exception as e:
            messagebox.showerror("錯誤", str(e))

    # 更新 token 到 config.ini
    def update_token_in_config(self, token):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_PATH):
            config.read(CONFIG_PATH)
        if not config.has_section("server"):
            config.add_section("server")
        if token:
            config.set("server", "server_token", token)
        else:
            if config.has_option("server", "server_token"):
                config.remove_option("server", "server_token")
        with open(CONFIG_PATH, "w") as f:
            config.write(f)

    # 啟動伺服器
    def launch_server(self):
        if not self.generated_file or not os.path.exists(self.generated_file):
            messagebox.showwarning("提醒", "請先生成 .sii 配置檔！")
            return
        try:
            server_launcher.launch_server(self.generated_file)
        except Exception as e:
            messagebox.showerror("錯誤", str(e))

    # 停止伺服器
    def stop_server(self):
        server_launcher.stop_server()

    # 自動刷新日誌
    def refresh_log(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            self.log_text.config(state="normal")
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, content)
            self.log_text.config(state="disabled")
            self.log_text.see(tk.END)
        self.master.after(1000, self.refresh_log)


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerConfigGUI(root)
    root.mainloop()
