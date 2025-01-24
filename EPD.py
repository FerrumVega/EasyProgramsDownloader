import tkinter as tk
from tkinter import filedialog, ttk
import requests
import os
import sys
import threading
import time

class EasyProgramsDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy Programs Downloader")
        self.apply_azure_theme()
        self.save_path = ""
        
        # Create a frame for download information
        self.download_info_frame = ttk.Frame(self.root)
        self.download_info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # Create labels for download information
        self.current_download_label = ttk.Label(self.download_info_frame, text="")
        self.progress_label = ttk.Label(self.download_info_frame, text="")
        self.remaining_label = ttk.Label(self.download_info_frame, text="")
        self.current_download_label.pack()
        self.progress_label.pack()
        self.remaining_label.pack()
        
        self.choose_path_menu()

    def apply_azure_theme(self):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        theme_path = os.path.join(base_path, "themes")
        azure_path = os.path.join(theme_path, "azure.tcl")
        print(azure_path)
        if os.path.exists(azure_path):
            self.root.tk.call("source", azure_path)
            self.root.tk.call("set_theme", "dark")

    def main_menu(self):
        self.clear_window_except_download_info()
        ttk.Label(self.root, text="Добро пожаловать в EPD!", font=("Arial", 14)).pack(pady=10)
        ttk.Label(self.root, text="Этот скрипт создан FerrumVega для лёгкого и быстрого скачивания программ.", wraplength=400).pack(pady=10)
        
        ttk.Button(self.root, text="Перейти в Telegram канал FerrumVega", command=lambda: os.system("start https://t.me/FerrumVega")).pack(pady=5)
        ttk.Button(self.root, text="Выбрать путь для сохранения файлов", command=self.choose_path_menu).pack(pady=5)
        ttk.Button(self.root, text="Сохранить все программы", command=self.download_all).pack(pady=5)
        ttk.Button(self.root, text="Готовые пакеты", command=self.prebuilt_packages_menu).pack(pady=5)
        ttk.Button(self.root, text="Выбрать программы", command=self.custom_selection_menu).pack(pady=5)
        ttk.Button(self.root, text="Выйти", command=self.root.quit).pack(pady=5)

    def choose_path_menu(self):
        self.clear_window_except_download_info()
        ttk.Label(self.root, text="Выберите путь для сохранения файлов", font=("Arial", 14)).pack(pady=10)
        
        ttk.Button(self.root, text="Сохранить в загрузки в папку Programs", command=lambda: self.set_save_path(os.path.join(os.path.expanduser("~"), "Downloads", "Programs"))).pack(pady=5)
        ttk.Button(self.root, text="Сохранить на рабочий стол в папку Programs", command=lambda: self.set_save_path(os.path.join(os.path.expanduser("~"), "Desktop", "Programs"))).pack(pady=5)
        ttk.Button(self.root, text="Указать свой путь", command=self.set_custom_path).pack(pady=5)
        ttk.Button(self.root, text="Назад", command=self.main_menu).pack(pady=5)
    
    def set_save_path(self, path):
        self.save_path = path
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        self.main_menu()

    def set_custom_path(self):
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
        self.main_menu()
    
    def prebuilt_packages_menu(self):
        self.clear_window_except_download_info()
        ttk.Label(self.root, text="Следующие готовые пакеты доступны", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Минимальный пакет (Telegram, Google Chrome)", command=self.download_minimal_package).pack(pady=5)
        ttk.Button(self.root, text="Игровой пакет (Steam, Discord)", command=self.download_gaming_package).pack(pady=5)
        ttk.Button(self.root, text="Назад", command=self.main_menu).pack(pady=5)
    
    def custom_selection_menu(self):
        self.clear_window_except_download_info()
        ttk.Label(self.root, text="Выберите программы для скачивания", font=("Arial", 14)).pack(pady=10)
        
        self.program_vars = {
            "Discord": tk.BooleanVar(),
            "Telegram": tk.BooleanVar(),
            "WinRAR": tk.BooleanVar(),
            "Total Commander": tk.BooleanVar(),
            "Rainmeter": tk.BooleanVar(),
            "Steam": tk.BooleanVar(),
            "Google Chrome": tk.BooleanVar(),
            "AnyDesk": tk.BooleanVar(),
            "Яндекс": tk.BooleanVar(),
        }
        
        for program, var in self.program_vars.items():
            ttk.Checkbutton(self.root, text=program, variable=var).pack(anchor='w')
        
        ttk.Button(self.root, text="Скачать выбранные программы", command=self.download_selected_programs).pack(pady=10)
        ttk.Button(self.root, text="Назад", command=self.main_menu).pack(pady=5)
    
    def download_all(self):
        programs = {
            "WinRAR": "https://www.rarlab.com/rar/winrar-x64-620ru.exe",
            "Total Commander": "https://totalcommander.ch/1150/tcmd1150x32.exe",
            "Rainmeter": "https://github.com/rainmeter/rainmeter/releases/download/v4.5.20.3803/Rainmeter-4.5.20.exe",
            "Steam": "https://cdn.steamstatic.com/client/installer/SteamSetup.exe",
            "Discord": "https://discordapp.com/api/download?platform=win",
            "Telegram": "https://telegram.org/dl/desktop/win",
            "Google Chrome": "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
            "AnyDesk": "https://download.anydesk.com/AnyDesk.exe",
            "Яндекс": "https://browser.yandex.ru/download?os=win",
        }
        self.download_programs(programs)
    
    def download_minimal_package(self):
        programs = {
            "Telegram": "https://telegram.org/dl/desktop/win",
            "Google Chrome": "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
        }
        self.download_programs(programs)
    
    def download_gaming_package(self):
        programs = {
            "Steam": "https://cdn.steamstatic.com/client/installer/SteamSetup.exe",
            "Discord": "https://discordapp.com/api/download?platform=win",
        }
        self.download_programs(programs)
    
    def download_selected_programs(self):
        programs = {
            "Discord": "https://discordapp.com/api/download?platform=win",
            "Telegram": "https://telegram.org/dl/desktop/win",
            "WinRAR": "https://www.rarlab.com/rar/winrar-x64-620ru.exe",
            "Total Commander": "https://totalcommander.ch/1150/tcmd1150x32.exe",
            "Rainmeter": "https://github.com/rainmeter/rainmeter/releases/download/v4.5.20.3803/Rainmeter-4.5.20.exe",
            "Steam": "https://cdn.steamstatic.com/client/installer/SteamSetup.exe",
            "Google Chrome": "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
            "AnyDesk": "https://download.anydesk.com/AnyDesk.exe",
            "Яндекс": "https://browser.yandex.ru/download?os=win",
        }
        selected_programs = {k: v for k, v in programs.items() if self.program_vars[k].get()}
        self.download_programs(selected_programs)
    
    def download_programs(self, programs):
        threading.Thread(target=self._download_programs, args=(programs,)).start()

    def _download_programs(self, programs):
        total_programs = len(programs)
        self.root.after(0, self.remaining_label.config, {'text': f"Осталось: {total_programs} программ"})
        
        for name, url in programs.items():
            self.download_file(name, url)
            total_programs -= 1
            self.root.after(0, self.remaining_label.config, {'text': f"Осталось: {total_programs} программ"})

        self.root.after(0, self.remaining_label.config, {'text': "Все выбранные программы были успешно загружены."})
    
    def download_file(self, name, url):
        if not self.save_path:
            return
        
        self.root.after(0, self.current_download_label.config, {'text': f"Скачивание {name}..."})

        response = requests.get(url, stream=True)
        file_path = os.path.join(self.save_path, f"{name}.exe")
        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 1024
        downloaded_size = 0
        start_time = time.time()
        
        with open(file_path, 'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                downloaded_size += len(data)
                elapsed_time = time.time() - start_time
                speed = (downloaded_size / 1024) / elapsed_time if elapsed_time > 0 else 0
                self.root.after(0, self.progress_label.config, {'text': f"{downloaded_size // (1024 * 1024)} MB / {total_size // (1024 * 1024)} MB, {speed:.2f} KB/s"})
        
        print(f"Скачан {name}")
        self.root.after(0, self.progress_label.config, {'text': ''})
        self.root.after(0, self.current_download_label.config, {'text': ''})

    def clear_window_except_download_info(self):
        for widget in self.root.winfo_children():
            if widget not in [self.download_info_frame]:
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EasyProgramsDownloader(root)
    root.mainloop()
