from config.config_manager import ConfigManager
from core.auto_player import AutoPlayer
from datetime import datetime
from gui.settings import SettingsWindow
from threading import Thread
import customtkinter as ctk
import os
import pygetwindow as gw
import re
import subprocess
import time
from gui.notification import Notification


class AppController:
    def __init__(self, app):
        self.app = app
        self.config = ConfigManager()
        self.running = False
        self.tile_count = 0
        self.start_time = 0
        self.elapsed_time = 0
        self.scrcpy_path = os.path.join("scrcpy", "scrcpy.exe")
        self.device = None
        self.device_code = None
        self.device_name = None
        self.device_connected = False
        self.window_x, self.window_y, self.width, self.height = 100, 100, 1080, 2400
        self.select_area_coords = False
        self.speed_control = 1.0
        self.scrcpy_process = None
        self.current_mode = ctk.get_appearance_mode()
        self.default_mode = "dark" if self.current_mode == "Light" else "light"
        self.default_color = "black" if self.current_mode == "Light" else "white"
        self.auto_player = None
        self.update_clock()
        self.setup_appearance()
        self.setup_keyboard_shortcuts()

    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.update_label()
        self.app.after(100, self.update_clock)

    def update_label(self):
        mins, secs = divmod(int(self.elapsed_time), 60)
        self.app.time_label.configure(text=f"Time: {mins:02}:{secs:02}")

    def handle_toggle(self, text='pause'):
        self.auto_player = AutoPlayer(self)
        if self.running:
            self.running = False
            self.app.start_btn.configure(
                text=f"({self.config.get("settings.hotkeys.toggle_bot")}) Start")
            if text == 'pause':
                self.log("Has paused")
                self.app.app_status.configure(
                    text=f"App Status: Is pause", text_color='yellow')
            else:
                self.log("Finished")
                self.app.app_status.configure(
                    text=f"App Status: Is finished", text_color='green')

        else:
            if text != 'pause':
                self.handle_reset(False)
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            Thread(target=self.auto_player.run, daemon=True).start()
            self.app.start_btn.configure(
                text=f"({self.config.get("settings.hotkeys.toggle_bot")}) Pause")
            self.log("Is starting")
            self.show_notification("Hold the esc key to pause")
            self.app.app_status.configure(
                text="App Status: Is running", text_color="blue")

    def handle_reset(self, log=True):
        self.app.app_status.configure(
            text="App Status: Idle", text_color=self.default_color)
        self.running = False
        self.elapsed_time = 0
        self.tile_count = 0
        self.update_label()
        self.app.start_btn.configure(
            text=f"({self.config.get("settings.hotkeys.toggle_bot")}) Start")
        self.app.tile_count_label.configure(
            text="Tile Count: 0")
        if log:
            self.log("Restarted")

    def handle_select_area(self):
        self.app.withdraw()
        self.app.app_status.configure(
            text="App Status: Idle", text_color=self.default_color)
        selector = ctk.CTkToplevel(self.app)
        selector.attributes('-fullscreen', True)
        selector.attributes('-alpha', 0.2)
        selector.configure(bg='black')
        selector.title("Select Area")
        selector.attributes('-topmost', True)

        canvas = ctk.CTkCanvas(selector, bg="black")
        canvas.pack(fill=ctk.BOTH, expand=True)

        self.start_x = self.start_y = self.rect = None

        def on_mouse_down(event):
            self.start_x, self.start_y = event.x, event.y
            self.rect = canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y,
                outline="red", width=3)

        def on_mouse_drag(event):
            canvas.coords(self.rect, self.start_x,
                          self.start_y, event.x, event.y)

        def on_mouse_up(event):
            x, y = self.start_x, self.start_y
            w = abs(event.x - x)
            h = abs(event.y - y)
            x1 = min(event.x, x)
            y1 = min(event.y, y)
            self.app.coord_label.configure(
                text=f"Coordinates: (x={x1}, y={y1}, w={w}, h={h})")
            self.app.select_status.configure(
                text="Status: Selected", text_color="green")
            self.window_x, self.window_y, self.width, self.height = x1, y1, w, h
            self.log("Coordinates selected")
            self.app.device_name.configure(
                text="Device: None")
            self.app.device_status.configure(
                text="Status: Disconnected", text_color="red")
            self.app.start_btn.configure(state=ctk.NORMAL)
            self.device_connected = False
            self.select_area_coords = True
            self.app.app_status.configure(
                text="App Status: Ready", text_color="green")
            self.app.connect_btn.configure(
                text=f"({self.config.get("settings.hotkeys.device_connect")}) Connect Device")
            self.setup_keyboard_shortcuts()
            self.app.deiconify()
            selector.destroy()

        canvas.bind("<Button-1>", on_mouse_down)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_mouse_up)

    def handle_connect_toggle(self):
        if self.device_connected:
            self.handle_device_disconnection()
        else:
            self.handle_device_connection()

    def handle_device_connection(self):
        if not self.device_connected:
            self.app.app_status.configure(
                text="App Status: Idle", text_color=self.default_color)
            if not os.path.exists(self.scrcpy_path):
                self.log("'scrcpy.exe' not found")
                self.app.device_status.configure(
                    text="Connection error", text_color="red")
                return

            Thread(target=self._connect_device, daemon=True).start()
        else:
            self.log("The device is connected.")

    def _connect_device(self):
        try:
            self.log("Connecting...")
            self.app.connect_btn.configure(text=f'({self.config.get("settings.hotkeys.device_connect")}) Connecting...',
                                           state=ctk.DISABLED)
            self.device = subprocess.Popen(
                [self.scrcpy_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            time.sleep(2)
            if self.device.poll() == 1:
                self.log(
                    "Please link the charging cable from the computer to the device")
                return

            for line in self.device.stdout:
                if "Device:" in line:
                    device_name = line.split("Device:")[1].strip()
                    self.device_connected = True
                    self.select_area_coords = False
                    self.app.device_name.configure(
                        text=f"Device: {device_name}")
                    self.app.device_status.configure(
                        text="Status: Connected", text_color="green")
                    self.log("Connected successfully!")
                    match = re.search(
                        r'\[(.*?)\]\s+(\w+)\s+(\w+)\s+\(Android\s+(\d+)\)', line)
                    self.device_code = match.group(3)
                    self.app.connect_btn.configure(
                        text=f"({self.config.get("settings.hotkeys.device_connect")}) Disconnect Device", state=ctk.NORMAL)
                    break

            self.device.wait()
            if self.device.returncode == 0:
                self.handle_device_disconnection()

        except Exception as e:
            self.log(f"Err scrcpy: {str(e)}")

    def handle_device_disconnection(self):
        if self.device_connected:
            self.log("Disconnecting device...")
            self.app.connect_btn.configure(
                state=ctk.DISABLED)
            self.device.terminate()
            self.device.wait()
            self.log("Disconnected.")
            self.device_connected = False
            self.device_code = None
            self.app.device_name.configure(
                text="Device: None")
            self.app.device_status.configure(
                text="Status: Disconnected", text_color="red")
            self.app.connect_btn.configure(
                text=f"({self.config.get("settings.hotkeys.device_connect")}) Connect Device", state=ctk.NORMAL)
        else:
            self.log("No devices are connected.")

    def open_settings(self):
        try:
            if hasattr(self, 'settings_window'):
                if self.settings_window.winfo_exists():
                    self.settings_window.lift()
                    self.settings_window.focus()
                    return

            self.settings_window = SettingsWindow(
                self,
                self.app,
                self.config,
            )

            self.settings_window.protocol(
                "WM_DELETE_WINDOW", self.on_settings_close)

        except Exception as e:
            print(f"Lỗi khi mở cửa sổ cài đặt: {e}")

    def on_settings_close(self):
        if hasattr(self, 'settings_window') and self.settings_window.winfo_exists():
            self.settings_window.grab_release()
            self.settings_window.destroy()

    def setup_appearance(self):
        theme_mode = self.config.get("settings.appearance.theme")
        if theme_mode in ["dark", "light"]:
            ctk.set_appearance_mode(theme_mode)
        else:
            ctk.set_appearance_mode("system")

        color_theme = self.config.get(
            "settings.appearance.accent_color")
        available_themes = ["blue", "green", "dark-blue"]
        if color_theme in available_themes:
            ctk.set_default_color_theme(color_theme)
        else:
            ctk.set_default_color_theme("blue")

    def setup_keyboard_shortcuts(self):
        for key in ["<F1>", "<F2>", "F3", "s", "b", "d", "c"]:
            self.app.unbind(key)

        toggle_bot = f"<{self.config.get('settings.hotkeys.toggle_bot')}>"
        refresh_bot = f"<{self.config.get('settings.hotkeys.refresh_bot')}>"
        settings = f"<{self.config.get('settings.hotkeys.settings')}>"
        select_board = f"<{self.config.get('settings.hotkeys.select_board')}>"
        select_hand = f"<{self.config.get('settings.hotkeys.select_hand')}>"
        select_skills = f"<{self.config.get('settings.hotkeys.select_skills')}>"
        device_connect = f"<{self.config.get('settings.hotkeys.device_connect')}>"
        clear_log = f"<{self.config.get('settings.hotkeys.clear_log')}>"

        if self.select_area_coords:
            self.app.bind(toggle_bot, lambda e: self.handle_toggle())
            self.app.bind(refresh_bot, lambda e: self.handle_reset())
            self.app.bind(settings, lambda e: self.open_settings())
            self.app.bind(select_board, lambda e: self.handle_select_area())
            self.app.bind(select_hand, lambda e: self.handle_select_area())
            self.app.bind(select_skills, lambda e: self.handle_select_area())
            self.app.bind(device_connect,
                          lambda e: self.handle_connect_toggle())
            self.app.bind(clear_log, lambda e: self.clear_log())

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.app.log_textbox.insert(ctk.END, f"[{timestamp}]: {message}\n")
        self.app.log_textbox.see(ctk.END)

    def clear_log(self):
        self.app.log_textbox.delete("1.0", ctk.END)
        self.log("Log cleared")

    def show_notification(self, message="Thông báo", duration=3000):
        Notification(self.app, message, duration)
