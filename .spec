python -m PyInstaller --noconfirm --onefile --windowed main.py ^
--icon=assets\icons\app_icon.ico ^
--add-data "assets;assets" ^
--add-data "config;config" ^
--add-data "core;core" ^
--add-data "gui;gui" ^
--add-data "scrcpy;scrcpy" ^
--add-data "utils;utils"
