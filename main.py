import os
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv
from network import BlacklistDownloader
from logic import IPProcessor

# ตั้งค่า Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

load_dotenv(resource_path(".env"))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IP Blacklist Pro")
        self.geometry("500x350")
        self.blacklist_data = set()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self, text="IP Comparison Tool", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Status Frame
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="สถานะ: รอการดึงข้อมูล Blacklist", text_color="yellow")
        self.status_label.pack(pady=10)

        # Buttons
        self.btn_fetch = ctk.CTkButton(self, text="ดึงข้อมูล Blacklist (URL)", command=self.update_blacklist, height=45)
        self.btn_fetch.grid(row=2, column=0, padx=40, pady=10, sticky="ew")

        self.btn_upload = ctk.CTkButton(self, text="อัปโหลดไฟล์ & เปรียบเทียบ (CSV, Excel)", 
                                        command=self.process_file, state="disabled", 
                                        fg_color="transparent", border_width=2, height=45)
        self.btn_upload.grid(row=3, column=0, padx=40, pady=10, sticky="ew")

    def update_blacklist(self):
        url = os.getenv("DB_URL")
        user = os.getenv("DB_USER")
        pw = os.getenv("DB_PASS")
        
        try:
            downloader = BlacklistDownloader(url, user, pw)
            self.blacklist_data = downloader.fetch_blacklist()
            
            self.status_label.configure(text=f"โหลดข้อมูลแล้ว: {len(self.blacklist_data)} รายการ", text_color="#4ade80")
            self.btn_upload.configure(state="normal", fg_color=["#3B8ED0", "#1F6AA5"])
            messagebox.showinfo("Success", "อัปเดตฐานข้อมูล Blacklist เรียบร้อย")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def process_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Supported files", "*.csv *.xlsx *.xls"), ("CSV", "*.csv"), ("Excel", "*.xlsx *.xls")]
        )
        if not file_path: return

        try:
            matched, not_found = IPProcessor.compare_ips(file_path, self.blacklist_data)
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel file", "*.xlsx")])
            
            if save_path:
                IPProcessor.save_to_excel(matched, not_found, save_path)
                messagebox.showinfo("Complete", f"เปรียบเทียบเสร็จสิ้น!\nเจอ: {len(matched)} | ไม่เจอ: {len(not_found)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()