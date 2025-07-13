from config.config_manager import ConfigManager
from gui.controller import AppController
from gui.widgets import create_button, create_label, create_frame, create_textbox
import customtkinter as ctk
import os


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config = ConfigManager()
        self.controller = AppController(self)
        # ROOT
        self.root = self.create_root_window()
        # UI
        self.create_widgets()
        self.setup_layout()

    def create_root_window(self):
        self.title(self.config.get("settings.app_title"))
        self.geometry(self.config.get("settings.window_size"))
        icon_path = os.path.join("assets", "icons", "app_icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

    def create_widgets(self):
        # ACTIONS
        self.action_frame = create_frame(self)
        self.action_label = create_label(
            self.action_frame, "Actions", size=18, weight="bold", anchor="center")
        self.start_btn = create_button(
            self.action_frame, f"({self.config.get("settings.hotkeys.toggle_bot")}) Start", state=ctk.DISABLED, command=self.controller.handle_toggle)
        self.refresh_btn = create_button(
            self.action_frame, f"({self.config.get("settings.hotkeys.refresh_bot")}) Refresh", command=self.controller.handle_reset)
        self.settings_button = create_button(
            self.action_frame,
            f"({self.config.get("settings.hotkeys.settings")}) Settings",
            command=self.controller.open_settings,
        )

        # SELECT ACTIONS
        self.select_frame = create_frame(self)
        self.select_label = create_label(
            self.select_frame, "Select Actions", size=14, weight="bold")
        # Board
        self.select_board_btn = create_button(
            self.select_frame, f"({self.config.get("settings.hotkeys.select_board")}) Select Board", command=self.controller.handle_select_area)
        self.coord_label = create_label(
            self.select_frame, "Coordinates: (x=0, y=0, w=0, h=0)")
        self.select_status = create_label(
            self.select_frame, "Status: Not selected yet")
        self.select_status.configure(text_color="red")
        # Hand
        self.select_hand_btn = create_button(
            self.select_frame, f"({self.config.get("settings.hotkeys.select_hand")}) Select Hand", command=self.controller.handle_select_area)
        self.coord_label = create_label(
            self.select_frame, "Coordinates: (x=0, y=0, w=0, h=0)")
        self.select_status = create_label(
            self.select_frame, "Status: Not selected yet")
        self.select_status.configure(text_color="red")
        # Skill
        self.select_skills_btn = create_button(
            self.select_frame, f"({self.config.get("settings.hotkeys.select_skills")}) Select Skill", command=self.controller.handle_select_area)
        self.coord_label = create_label(
            self.select_frame, "Coordinates: (x=0, y=0, w=0, h=0)")
        self.select_status = create_label(
            self.select_frame, "Status: Not selected yet")
        self.select_status.configure(text_color="red")

        # self.select_skills_btn = create_button(
        #     self.select_frame, "Select Skills", command=self.controller.handle_select_area)
        # self.coord_label = create_label(
        #     self.select_frame, "Coordinates: (x=0, y=0, w=0, h=0)")
        # self.select_status = create_label(
        #     self.select_frame, "Status: Not selected yet")
        # self.select_status.configure(text_color="red")

        # DEVICE ACTIONS
        self.device_frame = create_frame(self)
        self.device_label = create_label(
            self.device_frame, "Device Actions", size=14, weight="bold")
        self.connect_btn = create_button(
            self.device_frame, f"({self.config.get("settings.hotkeys.device_connect")}) Connect Device", command=self.controller.handle_connect_toggle)
        self.device_name = create_label(self.device_frame, "Device: None")
        self.device_status = create_label(
            self.device_frame, "Status: Disconnected")
        self.device_status.configure(text_color="red")

        # INFOMATION
        self.status_frame = create_frame(self)
        self.status_label = create_label(
            self.status_frame, "Information", size=14, weight="bold")
        self.app_status = create_label(self.status_frame, "App Status: Idle")
        self.time_label = create_label(self.status_frame, "Time: --:--")
        self.tile_count_label = create_label(
            self.status_frame, "Tile Count: 0")

        # LOG
        self.log_frame = create_frame(self)
        self.log_header_frame = create_frame(
            self.log_frame, fg_color="transparent")
        self.log_label = create_label(
            self.log_header_frame, "Log", size=14, weight="bold")
        self.clear_log_btn = create_button(
            self.log_header_frame, f"({self.config.get("settings.hotkeys.clear_log")}) Clear", width=60, command=self.controller.clear_log)
        self.log_textbox = create_textbox(self.log_frame, height=200)

    def setup_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # ===================== LEFT ======================
        # ACTIONS
        self.action_frame.grid(row=0, column=0, rowspan=3,
                               sticky="nswe", padx=(20, 5), pady=(20, 10))
        self.action_label.pack(padx=10, pady=(10, 20))
        self.start_btn.pack(pady=(10, 5), fill="x", padx=10)
        self.refresh_btn.pack(pady=5, fill="x", padx=10)
        self.settings_button.pack(pady=5, fill="x", padx=10)

        # ===================== RIGHT =======================
        # SELECT
        # Board
        self.select_frame.grid(row=0, column=1, sticky="ew",
                               padx=(5, 20), pady=(20, 10))
        self.select_label.pack(anchor="w", padx=10, pady=(5, 5))
        self.select_board_btn.pack(fill="x", padx=10, pady=2)
        self.coord_label.pack(anchor="w", padx=10, pady=2)
        self.select_status.pack(anchor="w", padx=10, pady=2)
        # Hand
        self.select_label.pack(anchor="w", padx=10, pady=(5, 5))
        self.select_hand_btn.pack(fill="x", padx=10, pady=2)
        self.coord_label.pack(anchor="w", padx=10, pady=2)
        self.select_status.pack(anchor="w", padx=10, pady=2)
        # Skills
        self.select_label.pack(anchor="w", padx=10, pady=(5, 5))
        self.select_skills_btn.pack(fill="x", padx=10, pady=2)
        self.coord_label.pack(anchor="w", padx=10, pady=2)
        self.select_status.pack(anchor="w", padx=10, pady=2)

        # DEVICE
        self.device_frame.grid(row=1, column=1, sticky="ew",
                               padx=(5, 20), pady=(0, 10))
        self.device_label.pack(anchor="w", padx=10, pady=(5, 5))
        self.connect_btn.pack(fill="x", padx=10, pady=2)
        self.device_name.pack(anchor="w", padx=10, pady=2)
        self.device_status.pack(anchor="w", padx=10, pady=2)

        # INFORMATION
        self.status_frame.grid(row=2, column=1, sticky="ew",
                               padx=(5, 20), pady=(0, 10))
        self.status_label.pack(anchor="w", padx=10, pady=(5, 5))
        self.app_status.pack(anchor="w", padx=10, pady=2)
        self.time_label.pack(anchor="w", padx=10, pady=2)
        self.tile_count_label.pack(anchor="w", padx=10, pady=2)

        # LOG
        self.log_frame.grid(row=3, column=0, columnspan=2,
                            sticky="nsew", padx=20, pady=(0, 20))
        self.log_header_frame.pack(fill="x", padx=10, pady=(5, 0))
        self.log_label.pack(side="left")
        self.clear_log_btn.pack(side="right")
        self.log_textbox.pack(fill="both", expand=True, padx=10, pady=10)
