@echo off
chcp 65001

:: Скачать содержимое по URL и записать в файл
powershell -command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/FerrumVega/EasyProgramsDownloader/refs/heads/main/script.bat' -OutFile '%~dp0/%~nx0'"

echo Файл %~nx0 заполнен содержимым из указанного URL.

pause
:hello
cls
echo ==============================
echo Добро пожаловать!
echo этот скрипт создан FerrumVega
echo для лёгкого и быстрого скачивания програм.
echo Вы можете свободно изменять 
echo и распространять этот скрипт
echo без необходимости получения разрешения
echo ==============================
echo [1] Перейти в Telegram канал FerrumVeg'и
echo [0] Выйти
echo [Другая клавиша] Продолжить
echo ==============================
set /p hello="Выберите опцию: "
if "%hello%"=="0" (
    exit
) else if "%hello%"=="1" (
    start https://t.me/FerrumVega
    pause
    goto hello
)

:: Меню выбора пути для сохранения файлов
:choose_path
cls
echo ==============================
echo     Выбор пути для сохранения
echo ==============================
echo [1] Сохранить в загрузки в папку Programs
echo [2] Сохранить на рабочий стол в папку Programs
echo [3] Сохранить на флешку в папку Programs
echo [4] Указать свой путь
echo [0] Назад
echo ==============================
set /p path_choice="Выберите опцию: "

if "%path_choice%"=="1" (
    set "save_path=%USERPROFILE%\Downloads\Programs"
) else if "%path_choice%"=="2" (
    set "save_path=%USERPROFILE%\Desktop\Programs"
) else if "%path_choice%"=="3" (
    set /p drive_letter="Укажите букву диска флешки, соблюдая формат! (например, E:\): "
    set "save_path=%drive_letter%\Programs"
) else if "%path_choice%"=="4" (
    set /p save_path="Укажите путь для сохранения файлов (например, C:\Users\ВашеИмя\Desktop\): "
) else if "%path_choice%"=="0" (
    goto hello
) else (
    echo Неверный выбор, попробуйте снова. 
    pause
    goto choose_path
)
if not exist "%save_path%" (
    mkdir "%save_path%"
)

:menu
cls
echo ==============================
echo        Главное меню
echo ==============================
echo [1] Сохранить все программы
echo [2] Готовые пакеты
echo [3] Выбрать программы
echo [0] Назад
echo ==============================
set /p main_choice="Выберите опцию: "

if "%main_choice%"=="1" goto download_all
if "%main_choice%"=="2" goto prebuilt_packages
if "%main_choice%"=="3" goto custom_selection
if "%main_choice%"=="0" goto choose_path

echo Неверный выбор, попробуйте снова.
pause
goto menu

:download_all
cls
echo ==============================
echo Скачиваем все программы...
powershell -command "Invoke-WebRequest -Uri 'https://www.rarlab.com/rar/winrar-x64-620ru.exe' -OutFile '%save_path%\winrar-x64-620ru.exe'"
powershell -command "Invoke-WebRequest -Uri 'https://totalcommander.ch/1150/tcmd1150x32.exe' -OutFile '%save_path%\tcmd1150x32.exe'"
powershell -command "Invoke-WebRequest -Uri 'https://github.com/rainmeter/rainmeter/releases/download/v4.5.20.3803/Rainmeter-4.5.20.exe' -OutFile '%save_path%\Rainmeter-4.5.20.exe'"
powershell -command "Invoke-WebRequest -Uri 'https://cdn.steamstatic.com/client/installer/SteamSetup.exe' -OutFile '%save_path%\SteamSetup.exe'"
powershell -command "Invoke-WebRequest -Uri 'https://discordapp.com/api/download?platform=win' -OutFile '%save_path%\discord.exe'"
powershell -command "Invoke-WebRequest -Uri 'https://telegram.org/dl/desktop/win' -OutFile '%save_path%\telegram.exe'"
powershell -command "Invoke-WebRequest -Uri 'https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463c-AFF1-A69D9E530F96%7D%26iid%3D%7BFCAC4F22-1EC1-C40A-EBE7-92E9141F63B7%7D%26lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%20Chrome%26needsadmin%3Dtrue/edgedl/chrome/install/GoogleChromeStandaloneEnterprise64.msi' -OutFile '%save_path%\GoogleChromeStandaloneEnterprise64.msi'"
powershell -command "Invoke-WebRequest -Uri 'https://download.anydesk.com/AnyDesk.exe' -OutFile '%save_path%\AnyDesk.exe'"
powershell -command "Invoke-WebRequest -Uri 'https://browser.yandex.ru/download?os=win' -OutFile '%save_path%\yandex.exe'"
echo ==============================
call :openme
pause
goto menu

:prebuilt_packages
cls
echo ==============================
echo Следующие готовые пакеты доступны:
echo [1] Минимальный пакет (Telegram, Google Chrome)
echo [2] Игровой пакет (Steam, Discord)
echo [0] Назад
echo ==============================
set /p package_choice="Выберите готовый пакет: "

if "%package_choice%"=="1" (
    powershell -command "Invoke-WebRequest -Uri 'https://telegram.org/dl/desktop/win' -OutFile '%save_path%\telegram.exe'"
    powershell -command "Invoke-WebRequest -Uri 'https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463c-AFF1-A69D9E530F96%7D%26iid%3D%7BFCAC4F22-1EC1-C40A-EBE7-92E9141F63B7%7D%26lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%20Chrome%26needsadmin%3Dtrue/edgedl/chrome/install/GoogleChromeStandaloneEnterprise64.msi' -OutFile '%save_path%\GoogleChromeStandaloneEnterprise64.msi'"
    call :openme
    goto prebuilt_packages
) else if "%package_choice%"=="2" (
    powershell -command "Invoke-WebRequest -Uri 'https://cdn.steamstatic.com/client/installer/SteamSetup.exe' -OutFile '%save_path%\SteamSetup.exe'"
    powershell -command "Invoke-WebRequest -Uri 'https://discordapp.com/api/download?platform=win' -OutFile '%save_path%\discord.exe'"
    call :openme
    goto prebuilt_packages
) else if "%package_choice%"=="0" (
    goto menu
) else (
    echo Неверный выбор, попробуйте снова. 
    pause
    goto prebuilt_packages
)
echo ==============================

:custom_selection
cls
echo ==============================
echo Выберите программы для скачивания:
echo [1] Discord
echo [2] Telegram
echo [3] WinRAR
echo [4] Total Commander
echo [5] Rainmeter
echo [6] Steam
echo [7] Google Chrome
echo [8] AnyDesk
echo [9] Яндекс
echo [0] Назад
echo ==============================
set /p custom_choice="Выберите опции через запятую (например, 1,3,5): "
set custom_choice=%custom_choice:,= %

if "%custom_choice%"=="0" goto menu

:: Проверка на валидность выбора программ
for %%i in (%custom_choice%) do (
    if not "%%i"=="1" if not "%%i"=="2" if not "%%i"=="3" if not "%%i"=="4" if not "%%i"=="5" if not "%%i"=="6" if not "%%i"=="7" if not "%%i"=="8" if not "%%i"=="9" (
        echo Неверный выбор, попробуйте снова.
        pause
        goto custom_selection
    )
)

for %%i in (%custom_choice%) do (
    if "%%i"=="1" (
        powershell -command "Invoke-WebRequest -Uri 'https://discordapp.com/api/download?platform=win' -OutFile '%save_path%\discord.exe'"
    )
    if "%%i"=="2" (
        powershell -command "Invoke-WebRequest -Uri 'https://telegram.org/dl/desktop/win' -OutFile '%save_path%\telegram.exe'"
    )
    if "%%i"=="3" (
        powershell -command "Invoke-WebRequest -Uri 'https://www.rarlab.com/rar/winrar-x64-620ru.exe' -OutFile '%save_path%\winrar-x64-620ru.exe'"
    )
    if "%%i"=="4" (
        powershell -command "Invoke-WebRequest -Uri 'https://totalcommander.ch/1150/tcmd1150x32.exe' -OutFile '%save_path%\tcmd1150x32.exe'"
    )
    if "%%i"=="5" (
        powershell -command "Invoke-WebRequest -Uri 'https://github.com/rainmeter/rainmeter/releases/download/v4.5.20.3803/Rainmeter-4.5.20.exe' -OutFile '%save_path%\Rainmeter-4.5.20.exe'"
    )
    if "%%i"=="6" (
        powershell -command "Invoke-WebRequest -Uri 'https://cdn.steamstatic.com/client/installer/SteamSetup.exe' -OutFile '%save_path%\SteamSetup.exe'"
    )
    if "%%i"=="7" (
        powershell -command "Invoke-WebRequest -Uri 'https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463c-AFF1-A69D9E530F96%7D%26iid%3D%7BFCAC4F22-1EC1-C40A-EBE7-92E9141F63B7%7D%26lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%20Chrome%26needsadmin%3Dtrue/edgedl/chrome/install/GoogleChromeStandaloneEnterprise64.msi' -OutFile '%save_path%\GoogleChromeStandaloneEnterprise64.msi'"
    )
    if "%%i"=="8" (
        powershell -command "Invoke-WebRequest -Uri 'https://download.anydesk.com/AnyDesk.exe' -OutFile '%save_path%\AnyDesk.exe'"
    )
    if "%%i"=="9" (
        powershell -command "Invoke-WebRequest -Uri 'https://browser.yandex.ru/download?os=win' -OutFile '%save_path%\yandex.exe'"
    )
)

call :openme

pause

REM Возвращаемся к главному меню
goto custom_selection


:openme
REM Создаем папку OpenMe в директории Programs, если её нет
if not exist "%save_path%\OpenMe" (
    mkdir "%save_path%\OpenMe"
)

REM Копируем скрипт и создаем readme.txt внутри OpenMe
(
    echo Спасибо за использование моего скрипта.
    echo.
    echo Вы можете свободно изменять и распространять этот скрипт без необходимости получения разрешения.
    echo Скрипт был скопирован в папку OpenMe.
    echo.
    echo Частые проблемы:
    echo 1. Ошибка при скачивании Discord.
    echo Решение: Включите ВПН и запустите скрипт заново либо скачайте Discord через браузер используя ссылку ниже.
    echo.
    echo Источники файлов:
    echo [1] Discord: https://discordapp.com/api/download?platform=win
    echo [2] Telegram: https://telegram.org/dl/desktop/win
    echo [3] WinRAR: https://www.rarlab.com/rar/winrar-x64-620ru.exe
    echo [4] Total Commander: https://totalcommander.ch/1150/tcmd1150x32.exe
    echo [5] Rainmeter: https://github.com/rainmeter/rainmeter/releases/download/v4.5.20.3803/Rainmeter-4.5.20.exe
    echo [6] Steam: https://cdn.steamstatic.com/client/installer/SteamSetup.exe
    echo [7] Google Chrome: https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463c-AFF1-A69D9E530F96%7D%26iid%3D%7BFCAC4F22-1EC1-C40A-EBE7-92E9141F63B7%7D%26lang%3Dru%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%20Chrome%26needsadmin%3Dtrue/edgedl/chrome/install/GoogleChromeStandaloneEnterprise64.msi'
    echo [8] AnyDesk: https://download.anydesk.com/AnyDesk.exe
    echo [9] Яндекс: https://browser.yandex.ru/download?os=win
    echo.
    echo By FerrumVega 
    echo Telegram: https://t.me/FerrumVega
) > "%save_path%\OpenMe\readme.txt"

copy "%~f0" "%save_path%\OpenMe\script.bat"
goto :eof

