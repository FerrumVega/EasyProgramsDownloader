ВАЖНО! Переместите все исходники в папку D:\Projects\Python\EPD! Если вы хотите использовать другой путь, измените команды с учётом нового пути.\
**Вставте этот код в cmd**
```
D:
cd D:\Projects\Python\EPD
pyinstaller --noconfirm --onefile --windowed --icon "D:\Projects\Python\EPD\icon.ico" --add-data "D:\Projects\Python\EPD\icon.ico;."  "D:\Projects\Python\EPD\EPD.py"
```
