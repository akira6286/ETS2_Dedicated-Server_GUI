# modules/gui.py

import os
import shutil
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from modules import config_generator, server_launcher
import threading

# 日誌路徑（保持原本指向 Documents，但可不搬移）
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Euro Truck Simulator 2")
LOGS_DIR = os.path.join(DOCUMENTS_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "server.log")

os.makedirs(LOGS_DIR, exist_ok=True)

class ServerConfigGUI:
    def __init__(self, master):
        self.master = master
        master.title("ETS2 Server Config Generator & Launcher")

        # 標籤
        labels = ["Lobby Name:", "Description:", "Welcome Message:", "Max Players:", "Password:", "輸出 .sii 檔案:"]
        for i, text in enumerate(labels):
            tk.Label(master, text=text).grid(row=i, column=0, sticky="e")

        # 變數
        self.lobby_name_var = tk.StringVar(value="Euro Truck Simulator2 Dedicated server 128")
        self.description_var = tk.StringVar(value="128")
        self.welcome_var = tk.StringVar(value="Welcome, Have fun")
        self.max_players_var = tk.IntVar(value=128)
        self.password_var = tk.StringVar(value="")
        self.sii_file_var = tk.StringVar(value="server_config.sii")

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

        tk.Entry(master, textvariable=self.sii_file_var, width=40).grid(row=5, column=1)

        # 按鈕
        tk.Button(master, text="選擇自訂路徑", command=self.select_sii_path).grid(row=5, column=2, padx=5)
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

    # 選擇生成路徑
    def select_sii_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".sii",
            filetypes=[("SII files", "*.sii")],
            initialdir=os.getcwd(),
            title="選擇輸出 .sii 檔案"
        )
        if path:
            self.sii_file_var.set(os.path.basename(path))

    # 生成 .sii (只生成到 ./generated，1 秒後搬到 OneDrive)
    def generate_sii(self):
        password = self.password_var.get()
        if password == "預設空白為無密碼":
            password = ""
        settings = {
            "lobby_name": self.lobby_name_var.get(),
            "description": self.description_var.get(),
            "welcome_message": self.welcome_var.get(),
            "max_players": self.max_players_var.get(),
            "password": password
        }
        try:
            os.makedirs("generated", exist_ok=True)
            self.generated_file = config_generator.generate_server_sii(self.sii_file_var.get(), settings)
            messagebox.showinfo("成功", f"已生成 {self.generated_file} (./generated)")

            # 延遲 1 秒搬檔案到 OneDrive
            def move_to_onedrive():
                try:
                    onedrive_docs_dir = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Euro Truck Simulator 2")
                    os.makedirs(onedrive_docs_dir, exist_ok=True)

                    # 搬 server_config.sii
                    dest_path = os.path.join(onedrive_docs_dir, os.path.basename(self.generated_file))
                    shutil.copy2(self.generated_file, dest_path)

                    # 找 ../assets 資料夾
                    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
                    for filename in ["server_packages.dat", "server_packages.sii"]:
                        src = os.path.join(assets_dir, filename)
                        if os.path.exists(src):
                            shutil.copy2(src, os.path.join(onedrive_docs_dir, filename))
                            print(f"[INFO] 已搬移 {filename} 到 OneDrive")
                        else:
                            print(f"[WARN] 找不到 {filename}: {src}")

                    print(f"[INFO] 已搬移所有檔案到 {onedrive_docs_dir}")
                except Exception as e:
                    print(f"[ERROR] 搬移到 OneDrive 失敗: {e}")

            threading.Timer(1.0, move_to_onedrive).start()

        except Exception as e:
            messagebox.showerror("錯誤", str(e))

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
