import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import os

class EasyProgramsDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy Programs Downloader")
        self.save_path = ""
        
        self.choose_path_menu()
    
    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Добро пожаловать в EPD!", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Этот скрипт создан FerrumVega для лёгкого и быстрого скачивания программ.", wraplength=400).pack(pady=10)
        
        tk.Button(self.root, text="Перейти в Telegram канал FerrumVega", command=lambda: os.system("start https://t.me/FerrumVega")).pack(pady=5)
        tk.Button(self.root, text="Выбрать путь для сохранения файлов", command=self.choose_path_menu).pack(pady=5)
        tk.Button(self.root, text="Сохранить все программы", command=self.download_all).pack(pady=5)
        tk.Button(self.root, text="Готовые пакеты", command=self.prebuilt_packages_menu).pack(pady=5)
        tk.Button(self.root, text="Выбрать программы", command=self.custom_selection_menu).pack(pady=5)
        tk.Button(self.root, text="Выйти", command=self.root.quit).pack(pady=5)
    
    def choose_path_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Выберите путь для сохранения файлов", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self.root, text="Сохранить в загрузки в папку Programs", command=lambda: self.set_save_path(os.path.join(os.path.expanduser("~"), "Downloads", "Programs"))).pack(pady=5)
        tk.Button(self.root, text="Сохранить на рабочий стол в папку Programs", command=lambda: self.set_save_path(os.path.join(os.path.expanduser("~"), "Desktop", "Programs"))).pack(pady=5)
        tk.Button(self.root, text="Указать свой путь", command=self.set_custom_path).pack(pady=5)
        tk.Button(self.root, text="Назад", command=self.main_menu).pack(pady=5)
    
    def set_save_path(self, path):
        self.save_path = path
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        messagebox.showinfo("Путь сохранения", f"Файлы будут сохранены по пути: {self.save_path}")
        self.main_menu()

    def set_custom_path(self):
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
            messagebox.showinfo("Путь сохранения", f"Файлы будут сохранены по пути: {self.save_path}")
        self.main_menu()
    
    def prebuilt_packages_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Следующие готовые пакеты доступны", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Минимальный пакет (Telegram, Google Chrome)", command=self.download_minimal_package).pack(pady=5)
        tk.Button(self.root, text="Игровой пакет (Steam, Discord)", command=self.download_gaming_package).pack(pady=5)
        tk.Button(self.root, text="Назад", command=self.main_menu).pack(pady=5)
    
    def custom_selection_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Выберите программы для скачивания", font=("Arial", 14)).pack(pady=10)
        
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
            tk.Checkbutton(self.root, text=program, variable=var).pack(anchor='w')
        
        tk.Button(self.root, text="Скачать выбранные программы", command=self.download_selected_programs).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.main_menu).pack(pady=5)
    
    def download_all(self):
        programs = {
            "WinRAR": "https://www.rarlab.com/rar/winrar-x64-620ru.exe",
            "Total Commander": "https://totalcommander.ch/1150/tcmd1150x32.exe",
            "Rainmeter": "https://github.com/rainmeter/rainmeter/releases/download/v4.5.20.3803/Rainmeter-4.5.20.exe",
            "Steam": "https://cdn.steamstatic.com/client/installer/SteamSetup.exe",
            "Discord": "https://discordapp.com/api/download?platform=win",
            "Telegram": "https://telegram.org/dl/desktop/win",
            "Google Chrome": "https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463c-AFF1-A69D9E530F96%7D%26iid%3D%7BFCAC4F22-1EC1-C40A-EBE7-92E9141F63B7%7D%26lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%20Chrome%26needsadmin%3Dfalse/ChromeStandaloneSetup.exe",
            "AnyDesk": "https://download.anydesk.com/AnyDesk.exe",
            "Яндекс": "https://browser.yandex.ru/download?os=win",
        }
        self.download_programs(programs)
    
    def download_minimal_package(self):
        programs = {
            "Telegram": "https://telegram.org/dl/desktop/win",
            "Google Chrome": "https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463c-AFF1-A69D9E530F96%7D%26iid%3D%7BFCAC4F22-1EC1-C40A-EBE7-92E9141F63B7%7D%26lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%20Chrome%26needsadmin%3Dfalse/ChromeStandaloneSetup.exe",
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
            "Google Chrome": "https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463c-AFF1-A69D9E530F96%7D%26iid%3D%7BFCAC4F22-1EC1-C40A-EBE7-92E9141F63B7%7D%26lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%20Chrome%26needsadmin%3Dfalse/ChromeStandaloneSetup.exe",
            "AnyDesk": "https://download.anydesk.com/AnyDesk.exe",
            "Яндекс": "https://browser.yandex.ru/download?os=win",
        }
        selected_programs = {k: v for k, v in programs.items() if self.program_vars[k].get()}
        self.download_programs(selected_programs)
    
    def download_programs(self, programs):
        for name, url in programs.items():
            self.download_file(name, url)
        messagebox.showinfo("Загрузка завершена", "Все выбранные программы были успешно загружены.")
    
    def download_file(self, name, url):
        if not self.save_path:
            messagebox.showwarning("Путь не выбран", "Пожалуйста, выберите путь для сохранения файлов.")
            return
        response = requests.get(url)
        file_path = os.path.join(self.save_path, f"{name}.exe")
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Скачан {name}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EasyProgramsDownloader(root)
    root.mainloop()
