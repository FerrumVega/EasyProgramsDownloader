Как пользоваться:
1. EPD.py:
   Просто откройте файл. Если файл не открывается, значит на компьютере не установлен Python.
2. mysetup.exe:
   Откройте установщик и установите программу. Затем, файл будет доступен как программа.

Как создан mysetup.exe:
1. Pyinstaller'ом делаем из кода программу: `pyinstaller --noconsole --icon=C:\piton\icon.png --add-data "C:\piton\themes;themes" EPD.py`
2. Через Inno Setup делаем сетап и в качестве основного файла используем `C:\piton\dist\EPD\EPD.exe`, а также загружаем папку `C:\piton\dist\EPD\`
3. Добавляем иконку icon.ico
4. Готово! Сетап находится в `C:\piton\Output\mysetup.exe`
   
> [!IMPORTANT]
> Если вы видите белую тему, скачайте папку themes, и поместите в ту же директорию, что и программу.

> [!NOTE]
> folder/\
> ├── EPD.py\
> ├── themes/\
> └──
