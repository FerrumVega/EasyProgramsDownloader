import tkinter as tk
from tkinter import filedialog, ttk
import requests
import os
import sys
import threading
import time
import pygame
import random

skin = "def"

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
        ttk.Button(self.root, text="Коржик (Игра кликер)", command=self.start_korik_thread).pack(pady=5)
        ttk.Button(self.root, text="Выйти", command=self.root.quit).pack(pady=5)

    def choose_path_menu(self):
        self.clear_window_except_download_info()
        ttk.Label(self.root, text="Выберите путь для сохранения файлов", font=("Arial", 14)).pack(pady=10)
        
        ttk.Button(self.root, text="Сохранить в загрузки в папку Programs", command=lambda: self.set_save_path(os.path.join(os.path.expanduser("~"), "Downloads", "Programs"))).pack(pady=5)
        ttk.Button(self.root, text="Сохранить на рабочий стол в папку Programs", command=lambda: self.set_save_path(os.path.join(os.path.expanduser("~"), "Desktop", "Programs"))).pack(pady=5)
        ttk.Button(self.root, text="Указать свой путь", command=self.set_custom_path).pack(pady=5)
        ttk.Button(self.root, text="Назад", command=self.main_menu).pack(pady=5)

    def start_korik_thread(self):
        threading.Thread(target=self.korik).start()

    def korik(self):
        def get_theme_path(file_name):
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            theme_path = os.path.join(base_path, "themes")
            return os.path.join(theme_path, file_name)

        # Инициализация Pygame
        pygame.init()

        # Настройки экрана
        WIDTH = 800
        HEIGHT = 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Коржик")

        # Цвета
        WHITE = (255, 255, 255)
        GRAY = (200, 200, 200)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        DARK_GRAY = (50, 50, 50)
        GOLD = (255, 215, 0)
        GREEN = (0, 255, 0)
        PURPLE = (128, 0, 128)

        # Загружаем фоновое изображение
        background_image = pygame.Surface(screen.get_size())
        background_image.fill(DARK_GRAY)  # Задаем темный фон

        # Шрифты
        font = pygame.font.SysFont('Arial', 20)

        # Игровые переменные
        coins = 0
        click_value = 1
        coins_per_second = 0
        coin_color = GOLD  # Начальный цвет монеты
        coin_size = 100  # Начальный размер монеты
        global skin
        skin = "DEF"  # Ensure skin is initialized

        upgrades = {
            "Стоимость клика": {"cost": 10, "function": "upgrade_click_value"},
            "Монет в секунду": {"cost": 15, "function": "upgrade_cps"},
            "Скин монеты (собака)": {"cost": 30, "function": "change_coin_dog"},
            "Скин монеты (кроль)": {"cost": 30, "function": "change_coin_habbit"},
            "Скин монеты (обычный)": {"cost": 30, "function": "change_coin_def"},
            "Увеличить размер монеты": {"cost": 50, "function": "increase_coin_size"}
        }

        # Частицы
        particles = []

        class Particle:
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.size = random.randint(5, 15)
                self.color = random.choice([WHITE, RED, BLUE])
                self.life = 30
                self.dx = random.uniform(-1, 1)
                self.dy = random.uniform(-1, 1)

            def update(self):
                self.x += self.dx
                self.y += self.dy
                self.life -= 1

            def draw(self, surface):
                if self.life > 0:
                    pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

        def draw_coin(surface, x, y, size):
            global skin
            if skin == "DOG":
                coin_image_path = get_theme_path('icon-round-dog.png')
            elif skin == "HABBIT":
                coin_image_path = get_theme_path('icon-round-habbit.png')
            elif skin == "DEF":
                coin_image_path = get_theme_path('icon-round.png')
            else:
                coin_image_path = get_theme_path('icon-round.png')

            coin_image = pygame.image.load(coin_image_path).convert_alpha()
            coin_image = pygame.transform.scale(coin_image, (size * 2, size * 2))  # Изменяем размер изображения
            coin_rect = coin_image.get_rect(center=(x, y))
            surface.blit(coin_image, coin_rect)

        def upgrade_click_value():
            nonlocal click_value
            click_value += 1

        def upgrade_cps():
            nonlocal coins_per_second
            coins_per_second += 1

        def change_coin_habbit():
            global skin
            skin = "HABBIT"

        def change_coin_dog():
            global skin
            skin = "DOG"

        def change_coin_def():
            global skin
            skin = "DEF"

        def increase_coin_size():
            nonlocal coin_size
            coin_size += 10

        # Основной игровой цикл
        running = True
        clock = pygame.time.Clock()
        last_update_time = pygame.time.get_ticks()
        coin_x, coin_y = 130, 300  # Центрируем монету по горизонтали и смещаем ниже по вертикали

        while running:
            # Заполняем экран фоновым цветом или изображением
            screen.blit(background_image, (0, 0))

            # Магазин
            shop_width = 450
            shop_height = 500
            shop_x = WIDTH - shop_width - 100
            shop_y = 60  # Было 110, теперь выше на 50 пикселей
            pygame.draw.rect(screen, GRAY, (shop_x, shop_y, shop_width, shop_height), border_radius=30)
            shop_text = font.render("Магазин", True, BLACK)
            screen.blit(shop_text, (shop_x + 150, shop_y + 10))

            # Отображение информации на экране
            coins_text = font.render(f"Монеты: {int(coins)}", True, WHITE)
            click_value_text = font.render(f"Стоимость клика: {click_value}", True, WHITE)
            cps_text = font.render(f"Монет в секунду: {coins_per_second}", True, WHITE)

            screen.blit(coins_text, (20, 20))
            screen.blit(click_value_text, (20, 60))
            screen.blit(cps_text, (20, 100))

            # Отображение монеты под информацией
            draw_coin(screen, coin_x, coin_y, coin_size)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левый клик или касание
                        mouse_x, mouse_y = event.pos
                        if pygame.Rect(coin_x - coin_size, coin_y - coin_size, coin_size * 2, coin_size * 2).collidepoint(mouse_x, mouse_y):
                            coins += click_value
                            particles.append(Particle(mouse_x, mouse_y))
                        else:
                            # Проверка на покупку улучшений
                            for index, (upgrade_name, upgrade) in enumerate(upgrades.items()):
                                button_height = 50  # Уменьшаем высоту кнопок до 50
                                button_rect = pygame.Rect(shop_x + 10, shop_y + 50 + index * (button_height + 10), shop_width - 20, button_height)
                                if button_rect.collidepoint(mouse_x, mouse_y) and upgrade["cost"] <= coins:
                                    coins -= upgrade["cost"]
                                    if upgrade["function"] == "upgrade_click_value":
                                        upgrade_click_value()
                                    elif upgrade["function"] == "upgrade_cps":
                                        upgrade_cps()
                                    elif upgrade["function"] == "change_coin_dog":
                                        change_coin_dog()
                                    elif upgrade["function"] == "change_coin_habbit":
                                        change_coin_habbit()
                                    elif upgrade["function"] == "change_coin_def":
                                        change_coin_def()
                                    elif upgrade["function"] == "increase_coin_size":
                                        increase_coin_size()
                                    # Увеличиваем стоимость улучшений
                                    upgrades[upgrade_name]["cost"] = int(upgrade["cost"] * 1.5)

            # Обновление частиц
            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)

            # Автоматическое получение монет
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time >= 1000:  # Обновление каждую секунду
                coins += coins_per_second
                last_update_time = current_time

            # Отображение частиц
            for particle in particles:
                particle.draw(screen)

            # Кнопки для улучшений
            button_height = 50  # Определение button_height
            for index, (upgrade_name, upgrade) in enumerate(upgrades.items()):
                button_rect = pygame.draw.rect(screen, (150, 150, 150), (shop_x + 10, shop_y + 50 + index * (button_height + 10), shop_width - 20, button_height), border_radius=5)
                upgrade_text = font.render(f"{upgrade_name}: {upgrade['cost']} монет", True, BLACK)
                screen.blit(upgrade_text, (shop_x + 15, shop_y + 55 + index * (button_height + 10)))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

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
