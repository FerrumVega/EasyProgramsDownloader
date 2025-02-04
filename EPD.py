import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import os
import sys
import threading
import time

class EasyProgramsDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy Programs Downloader")
        self.save_path = ""
        self.current_category_index = 0
        self.root.geometry("550x500")
        self.apply_azure_theme()

    def apply_azure_theme(self):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        theme_path = os.path.join(base_path, "themes")
        azure_path = os.path.join(theme_path, "azure.tcl")
        print(azure_path)
        if os.path.exists(azure_path):
            self.root.tk.call("source", azure_path)
            self.root.tk.call("set_theme", "dark")

        self.download_info_frame = ttk.Frame(self.root)
        self.download_info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.current_download_label = ttk.Label(self.download_info_frame, text="")
        self.progress_label = ttk.Label(self.download_info_frame, text="")
        self.remaining_label = ttk.Label(self.download_info_frame, text="")
        self.current_download_label.pack()
        self.progress_label.pack()
        self.remaining_label.pack()
        
        self.programs = {
            "Браузеры": {
                "Vivaldi": {"url": "https://downloads.vivaldi.com/stable/Vivaldi.6.7.3329.44.exe", "description": "Браузер с очень гибкой настройкой внешнего вида основанный на Chromium.", "pros": ["Гибкость", "Много функций"], "cons": ["Требует времени для настройки"]},
                "Firefox": {"url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=ru", "description": "Открытый браузер с поддержкой расширений.", "pros": ["Открытый исходный код", "Много расширений"], "cons": ["Может быть медленным"]},
                "Waterfox": {"url": "https://cdn.waterfox.net/releases/win64/installer/Waterfox%20G6.0.12%20Setup.exe", "description": "Браузер на основе Firefox, ориентированный на приватность.", "pros": ["Приватность", "Совместимость с Firefox"], "cons": ["Меньше расширений"]},
                "Google Chrome": {"url": "https://dl.google.com/chrome/install/latest/chrome_installer.exe", "description": "Популярный браузер от Google.", "pros": ["Быстрый", "Много расширений"], "cons": ["Требляет много памяти"]},
                "Brave": {"url": "https://referrals.brave.com/latest/BraveBrowserSetup.exe", "description": "Браузер с блокировкой рекламы и трекеров.", "pros": ["Приватность", "Блокировка рекламы"], "cons": ["Меньше расширений"]},
            },
            "Социальные сети": {
                "Telegram": {"url": "https://telegram.org/dl/desktop/win64", "description": "Мессенджер с поддержкой шифрования.", "pros": ["Безопасность", "Кроссплатформенность"], "cons": ["Нет звонков на ПК"]},
                "64Gram": {"url": "https://github.com/TDesktop-x64/tdesktop/releases/download/v1.1.35/64Gram-setup-x64.1.1.35.exe", "description": "Форк Telegram с дополнительными функциями.", "pros": ["Дополнительные функции", "Приватность"], "cons": ["Меньше поддержки"]},
                "Discord": {"url": "https://dl.discordapp.net/distro/app/stable/win/x86/1.0.9012/DiscordSetup.exe", "description": "Платформа для общения геймеров.", "pros": ["Голосовые каналы", "Интеграции"], "cons": ["Требует много ресурсов"]},
                "Vencord": {"url": "https://github.com/Vencord/Installer/releases/latest/download/VencordInstaller.exe", "description": "Форк для Discord с дополнительными функциями.", "pros": ["Обход ограничений Nitro", "Поддержка плагинов"], "cons": ["Меньше поддержки"]},
            },
            "Плееры": {
                "VLC": {"url": "https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe", "description": "Популярнейший медиаплеер с открытым исходным кодом.", "pros": ["Открытый исходный код", "Поддержка ТВ-Каналов"], "cons": ["Не всегда удобен"]},
                "MPC-HC": {"url": "https://github.com/clsid2/mpc-hc/releases/download/1.9.18/mpc-hc-1.9.18-x64.exe", "description": "Удобный видеоплеер с поддержкой многих кодеков.", "pros": ["Поддержка кодеков", "Простота использования"], "cons": ["Устаревший интерфейс"]},
                "iTunes": {"url": "https://secure-appldnld.apple.com/itunes12/002-67830-20220125-46C2F7A4-14E7-11EC-8E9F-1A8E216E98BC/iTunes64Setup.exe", "description": "Плеер от Apple для управления музыкой и рингтонами на iPhone.", "pros": ["Поддержка iPhone", "Большая библиотека"], "cons": ["Медленный"]},
            },
            "Библиотеки": {
                "Java 8": {"url": "https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248242_ce59cff5c23f4e2eaf4e778a117d4c5b", "description": "Лучшая версия для Minecraft до 1.12", "pros": ["Стабильность", "Поддержка Minecraft"], "cons": ["Старое ПО"]},
                "Java 17": {"url": "https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe", "description": "Лучшая версия для Minecraft до 1.20", "pros": ["Стабильность", "Поддержка Minecraft"], "cons": ["Необходимость обновлений"]},
                "Java 21": {"url": "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe", "description": "Самый оптимальный и актуальный вариант", "pros": ["Оптимизация", "Поддержка новых версий"], "cons": ["Требует обновлений"]},
                "VS0813": {"url": "https://download.microsoft.com/download/2/E/6/2E61CFA4-993B-4DD4-91DA-3737CD5CD6E3/vcredist_x64.exe", "description": "Microsoft Visual C++ Redistributable 2008 - 2013", "pros": ["Необходим для старых программ", "Широкое применение"], "cons": ["Старое ПО"]},
                "VS1522": {"url": "https://aka.ms/vs/17/release/vc_redist.x64.exe", "description": "Microsoft Visual C++ Redistributable 2015 - 2022", "pros": ["Необходим для новых программ", "Широкое применение"], "cons": ["Большой объем"]},
            },
            "Игры": {
                "Steam": {"url": "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe", "description": "Лучшая площадка для покупки игр и обмена вещами в инвентаре.", "pros": ["Большая библиотека игр", "Социальные функции"], "cons": ["Платные игры"]},
                "Epic Games": {"url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "description": "Популярная площадка с регулярными раздачами игр.", "pros": ["Раздачи игр", "Инди проекты"], "cons": ["Меньше игр, чем в Steam"]},
            },
            "Редакторы": {
                "Audacity": {"url": "https://github.com/audacity/audacity/releases/download/Audacity-3.4.2/audacity-win-3.4.2-64bit.exe", "description": "Полезный инструмент для редактирования аудио.", "pros": ["Функциональность", "Простота использования"], "cons": ["Ограниченный интерфейс"]},
                "CapCut": {"url": "https://lf16-capcut.faceulv.com/obj/capcutpc-packages-us/packages/CapCut_1_6_0_128_capcutpc_0.exe", "description": "Простой монтажёр для новичков.", "pros": ["Простота использования", "Бесплатность"], "cons": ["Ограниченный функционал"]},
                "PDN": {"url": "https://www.getpaint.net/download.html#download", "description": "Простой аналог Adobe Photoshop с поддержкой плагинов.", "pros": ["Простота использования", "Поддержка плагинов"], "cons": ["Ограниченный функционал"]},
            },
            "Утилиты": {
                "7-Zip": {"url": "https://www.7-zip.org/a/7z2301-x64.exe", "description": "Лучший архиватор файлов.", "pros": ["Высокая степень сжатия", "Бесплатность"], "cons": ["Ограниченный интерфейс"]},
                "OBS": {"url": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-29.1.3-Full-Installer-x64.exe", "description": "Лучшая программа для стриминга.", "pros": ["Функциональность", "Бесплатность"], "cons": ["Сложность настройки"]},
                "Handbrake": {"url": "https://github.com/HandBrake/HandBrake/releases/download/1.6.1/HandBrake-1.6.1-x86_64-Win_GUI.exe", "description": "Полезная утилита для конвертации видео.", "pros": ["Функциональность", "Бесплатность"], "cons": ["Сложность использования"]},
                "AHK": {"url": "https://www.autohotkey.com/download/ahk-install.exe", "description": "Программа для автоматизации действий на клавиатуре.", "pros": ["Автоматизация", "Бесплатность"], "cons": ["Сложность настройки"]},
                "ShareX": {"url": "https://github.com/ShareX/ShareX/releases/download/v15.0.0/ShareX-15.0.0-setup.exe", "description": "Мощный инструмент для создания скриншотов.", "pros": ["Широкие возможности", "Высокая кастомизация"], "cons": ["Сложность освоения"]},
                "Radmin VPN": {"url": "https://download.radmin-vpn.com/download/radmin-vpn-1.3.4567.1.exe", "description": "Простейший инструмент для эмуляции локальной игры.", "pros": ["Простота использования", "Эмуляция локальной игры"], "cons": ["Ограниченные возможности"]},
                "Hamachi": {"url": "https://secure.logmein.com/hamachi.msi", "description": "Хороший аналог RadminVPN.", "pros": ["Меньший пинг", "Простота использования"], "cons": ["Лимит в 5 человек"]},
                "TwitchLink": {"url": "https://github.com/devhotteok/TwitchLink/releases/download/3.2.0/TwitchLinkSetup-3.2.0.exe", "description": "Программа для скачивания стримов из Twitch.", "pros": ["Скачивание стримов", "Простота использования"], "cons": ["Ограниченные возможности"]},
                "qBitTorrent": {"url": "https://www.fosshub.com/qBittorrent.html?dwl=qbittorrent_4.6.2_x64_setup.exe", "description": "Популярнейший торрент клиент.", "pros": ["Быстрота", "Простота использования"], "cons": ["Необходимость настройки"]},
                "NanaZIP": {"url": "https://github.com/M2Team/NanaZip/releases/download/1.1.367.0/NanaZip-1.1.367.0-x64.exe", "description": "Лучший форк 7-Zip с дизайном из Windows 11.", "pros": ["Дизайн Windows 11", "Поддержка алгоритмов сжатия"], "cons": ["Ограниченная поддержка"]},
                "AnyDesk": {"url": "https://download.anydesk.com/AnyDesk.exe", "description": "Лучшая программа для управления удалённым рабочим столом.", "pros": ["Управление удалённым рабочим столом", "Простота использования"], "cons": ["Ограниченная функциональность"]},
                "Dr.Web CureIt": {"url": "https://free.drweb.ru/download+cureit+free/", "description": "Программа для сканирования на вирусы.", "pros": ["Сканирование на вирусы", "База данных обновляется каждый день"], "cons": ["Ограниченная функциональность"]},
                "Scrcpy": {"url": "https://github.com/Genymobile/scrcpy/releases/download/v2.0/scrcpy-win64-v2.0.zip", "description": "Программа для отображения изображения из Android.", "pros": ["Отображение изображения из Android", "Управление смартфоном"], "cons": ["Ограниченная поддержка"]},
            },
            "Для разработчиков": {
                "VSCODE": {"url": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user", "description": "Простой редактор кода от Microsoft.", "pros": ["Простота использования", "Большая поддержка расширений"], "cons": ["Требует настроек"]},
                "VSTUDIO": {"url": "https://download.visualstudio.microsoft.com/download/pr/17b6759f-1af0-41bc-ab12-209ba0377779/e8d02195dbf1434b940e0f48ae8d5e50/vs_Community.exe", "description": "Функциональная среда разработки от Microsoft.", "pros": ["Поддержка многих языков программирования", "Интеграции с другими инструментами"], "cons": ["Сложность освоения"]},
                "PyCharm": {"url": "https://download.jetbrains.com/python/pycharm-community-2023.2.2.exe", "description": "Среда разработки для Python.", "pros": ["Поддержка Python", "Функциональность"], "cons": ["Необходимость настроек"]},
            },
            "Виртуальные машины": {
                "VirtualBox": {"url": "https://download.virtualbox.org/virtualbox/7.0.10/VirtualBox-7.0.10-158379-Win.exe", "description": "Простая виртуальная машина.", "pros": ["Простота использования", "Бесплатность"], "cons": ["Ограниченная поддержка"]},
            },
            "Твики": {
                "StartIsBack": {"url": "https://startisback.com/StartIsBackPlusPlus_setup.exe", "description": "Программа для изменения разрешения экрана.", "pros": ["Изменение разрешения", "Поддержка высокой герцовки"], "cons": ["Сложность настройки"]},
                "ExplorerPatcher": {"url": "https://github.com/valinet/ExplorerPatcher/releases/download/22000.2582.57.3/ExplorerPatcher-amd64-22000.2582.57.3.exe", "description": "Популярный твикер с открытым исходным кодом.", "pros": ["Открытый исходный код", "Широкая поддержка"], "cons": ["Сложность освоения"]},
            },
            "Работа с флешками": {
                "Rufus": {"url": "https://github.com/pbatard/rufus/releases/download/v4.2/rufus-4.2.exe", "description": "Программа для записи ISO образов на флешку.", "pros": ["Быстрота", "Надёжность"], "cons": ["Ограниченный функционал"]},
                "BalenaEtcher": {"url": "https://github.com/balena-io/etcher/releases/download/v1.18.11/balenaEtcher-Setup-1.18.11.exe", "description": "Программа для записи образов Linux на флешку.", "pros": ["Быстрота", "Простота использования"], "cons": ["Ограниченный функционал"]},
                "Ventoy": {"url": "https://github.com/ventoy/Ventoy/releases/download/v1.0.96/ventoy-1.0.96-windows.zip", "description": "Программа для записи нескольких образов на флешку.", "pros": ["Поддержка нескольких образов", "Простота использования"], "cons": ["Ограниченная поддержка"]},
            },
            "Диагностика": {
                "CPU-Z": {"url": "https://download.cpuid.com/cpu-z/cpu-z_2.07-en.exe", "description": "Просмотр информации о процессоре.", "pros": ["Информация о процессоре", "Простота использования"], "cons": ["Ограниченная функциональность"]},
                "GPU-Z": {"url": "https://www.techpowerup.com/download/techpowerup-gpu-z/", "description": "Просмотр информации о видеокарте.", "pros": ["Информация о видеокарте", "Простота использования"], "cons": ["Ограниченная функциональность"]},
                "CrystalDiskInfo": {"url": "https://osdn.net/dl/crystaldiskinfo/CrystalDiskInfo8_17_14.exe", "description": "Просмотр информации о жестких дисках и SSD.", "pros": ["Информация о жестких дисках", "Процент износа"], "cons": ["Ограниченная поддержка"]},
                "CrystalDiskMark": {"url": "https://osdn.net/dl/crystaldiskmark/CrystalDiskMark8_0_4c.exe", "description": "Проверка скорости жесткого диска или SSD.", "pros": ["Проверка скорости", "Простота использования"], "cons": ["Ограниченный функционал"]},
            },
            "VPN Клиенты": {
                "Outline": {"url": "https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe", "description": "Outline VPN клиент.", "pros": ["Простота использования", "Поддержка"], "cons": ["Ограниченная поддержка"]},
                "Amnezia": {"url": "https://github.com/AmneziaVPN/desktop-client/releases/download/2.2.0/AmneziaVPN-2.2.0.exe", "description": "Amnezia VPN клиент.", "pros": ["Простота использования", "Поддержка"], "cons": ["Ограниченная поддержка"]},
            },
            "Драйвера": {
                "AMD": {"url": "https://drivers.amd.com/drivers/installer/22.20/whql/amd-software-adrenalin-edition-22.20.00.33.exe", "description": "Панель управления графикой AMD.", "pros": ["Поддержка AMD", "Функциональность"], "cons": ["Требует обновлений"]},
                "NVIDIA": {"url": "https://us.download.nvidia.com/Windows/528.24/528.24-desktop-win10-win11-64bit-international-dch-whql.exe", "description": "Приложение для управления видеокартами NVIDIA.", "pros": ["Поддержка NVIDIA", "Функциональность"], "cons": ["Требует обновлений"]},
            }
        }

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.checked_programs = {}  # Store the state of each checkbox
        self.choose_path_menu()

    def main_menu(self):
        self.clear_window_except_download_info()
        ttk.Label(self.root, text="Добро пожаловать в EPD!", font=("Arial", 14)).pack(pady=10)
        ttk.Label(self.root, text="Этот скрипт создан FerrumVega для лёгкого и быстрого скачивания программ.", wraplength=400).pack(pady=10)
        
        ttk.Button(self.root, text="Перейти в Telegram канал FerrumVega", command=lambda: os.system("start https://t.me/FerrumVega")).pack(pady=5)
        ttk.Button(self.root, text="Выбрать путь для сохранения файлов", command=self.choose_path_menu).pack(pady=5)
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
    
    def custom_selection_menu(self):
        self.clear_window_except_download_info()
        self.button_frame.pack_forget()
        ttk.Label(self.root, text="Выберите программы для скачивания", font=("Arial", 14)).pack(pady=10)
        
        self.program_vars = {}
        self.program_buttons = {}
        
        self.total_pages = len(self.programs)
        self.show_page(self.current_category_index)
        
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        ttk.Button(self.button_frame, text="Назад", command=self.prev_page).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.button_frame, text="Вперед", command=self.next_page).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.button_frame, text="Скачать выбранные программы", command=self.download_selected_programs).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.button_frame, text="Главное меню", command=self.main_menu).pack(side=tk.LEFT, padx=10)
    
    def show_page(self, page_index):
        self.clear_window_except_download_info()
        category = list(self.programs.keys())[page_index]

        programs = self.programs[category]
        ttk.Label(self.root, text=f"Категория: {category}", font=("Arial", 12)).pack(pady=5)
        
        for program, data in programs.items():
            frame = ttk.Frame(self.root)
            frame.pack(anchor='w')
            self.program_vars[program] = tk.BooleanVar(value=self.checked_programs.get(program, False))
            ttk.Checkbutton(frame, text=program, variable=self.program_vars[program], command=lambda p=program: self.update_checked_programs(p)).pack(side=tk.LEFT)
            self.program_buttons[program] = ttk.Button(frame, text="Подробнее", command=lambda p=program: self.show_program_details(p))
            self.program_buttons[program].pack(side=tk.LEFT)

    def update_checked_programs(self, program):
        self.checked_programs[program] = self.program_vars[program].get()
        print(f"Updated checked_programs: {self.checked_programs}")  # Debugging statement

    def prev_page(self):
        if self.current_category_index > 0:
            self.current_category_index -= 1
            self.show_page(self.current_category_index)
    
    def next_page(self):
        if self.current_category_index < self.total_pages - 1:
            self.current_category_index += 1
            self.show_page(self.current_category_index)
    
    def show_program_details(self, program):
        details = self.get_program_details(program)
        messagebox.showinfo(program, details)
    
    def get_program_details(self, program):
        for category, programs in self.programs.items():
            if program in programs:
                data = programs[program]
                description = data.get("description", "Описание отсутствует.")
                pros = "\nПлюсы:\n- " + "\n- ".join(data.get("pros", []))
                cons = "\nМинусы:\n- " + "\n- ".join(data.get("cons", []))
                return f"{description}{pros}{cons}"
        return "Информация о программе отсутствует."
    
    def download_selected_programs(self):
        selected_programs = {}
        for category, programs in self.programs.items():
            for program, data in programs.items():
                if self.checked_programs.get(program, False):
                    selected_programs[program] = data["url"]
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
            if widget not in [self.download_info_frame, self.button_frame]:
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EasyProgramsDownloader(root)
    root.mainloop()

