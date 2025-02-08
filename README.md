> [!WARNING]
> Program is using Azure theme, which is under MIT license.
> Copyright (c) 2021 rdbende

Как пользоваться:
1. EPD.py:
   Просто откройте файл. Если файл не открывается, значит на компьютере не установлен Python.
2. EPD.exe:
   Откройте программу.

Как создан EPD.exe:
1. Pyinstaller'ом делаем из кода программу: `pyinstaller --onefile --noconsole --icon=C:\piton\icon.png --add-data "C:\piton\themes;themes" EPD.py`
2. Готово! Exe'шник находится в `C:\piton\Output\mysetup.exe`
   
> [!IMPORTANT]
> Если вы видите белую тему, скачайте папку themes, и поместите в ту же директорию, что и программу.

> [!NOTE]
> folder/\
> ├── EPD.py\
> ├── themes/\
> └──
