import customtkinter as ctk


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, app,  config, *args, **kwargs):
        kwargs.setdefault(
            "fg_color", ctk.ThemeManager.theme["CTkFrame"]["fg_color"])

        super().__init__(app, *args, **kwargs)

        if not hasattr(app, 'tk'):
            raise ValueError("Parent phải là một widget Tkinter hợp lệ")

        self.app = app
        self.parent = parent
        self.config = config
        self.title(self.config.get("settings.setting_title"))
        self.geometry(self.config.get("settings.setting_window_size"))
        self.minsize(350, 500)
        self.resizable(True, True)

        # Thiết lập quan hệ với cửa sổ cha
        self.transient(app)
        self.grab_set()

        # Giao diện
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab view
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)

        # Thêm các tab
        self.tabview.add("Gameplay")
        self.tabview.add("Giao diện")
        self.tabview.add("Hotkeys")

        # Tab Gameplay
        self.setup_gameplay_tab()

        # Tab Giao diện
        self.setup_appearance_tab()

        # Tab Hotkeys
        self.setup_hotkeys_tab()

        # Nút lưu và đóng
        self.save_button = ctk.CTkButton(
            self.main_frame,
            text="Save",
            command=self.save_settings,
        )
        self.save_button.pack(pady=10)

    def setup_appearance_tab(self):
        tab = self.tabview.tab("Giao diện")

        # Theme mode
        self.theme_label = ctk.CTkLabel(tab, text="Chế độ giao diện:")
        self.theme_label.pack(pady=(10, 0))

        self.theme_var = ctk.StringVar(
            value=self.config.get("settings.appearance.theme"))

        self.size_var = ctk.StringVar(
            value=self.config.get("settings.window_size"))

        self.theme_menu = ctk.CTkOptionMenu(
            tab,
            values=["dark", "light", "system"],
            variable=self.theme_var
        )
        self.theme_menu.pack(fill="x", padx=20, pady=5)

        # Color theme
        self.color_label = ctk.CTkLabel(tab, text="Màu chủ đạo:")
        self.color_label.pack(pady=(10, 0))

        self.color_var = ctk.StringVar(value=self.config.get(
            "settings.appearance.accent_color"))
        self.color_menu = ctk.CTkOptionMenu(
            tab,
            values=["blue", "green", "dark-blue"],
            variable=self.color_var
        )
        self.color_menu.pack(fill="x", padx=20, pady=5)

    def setup_gameplay_tab(self):
        tab = self.tabview.tab("Gameplay")

        # Template pack
        self.template_label = ctk.CTkLabel(tab, text="Gói tile template:")
        self.template_label.pack(pady=(10, 0))

        self.template_var = ctk.StringVar(
            value=self.config.get("settings.selected_template_pack"))

        self.template_menu = ctk.CTkOptionMenu(
            tab,
            values=self.config.get_template_packs(),
            variable=self.template_var
        )
        self.template_menu.pack(fill="x", padx=20, pady=5)

        # Match threshold
        self.threshold_label = ctk.CTkLabel(
            tab, text="Ngưỡng nhận diện tile (0.5-1.0):")
        self.threshold_label.pack(pady=(10, 0))

        self.threshold_slider = ctk.CTkSlider(
            tab,
            from_=0.5,
            to=1.0,
            number_of_steps=50,
            command=self.update_threshold_display
        )
        self.threshold_slider.set(self.config.get(
            "settings.tile_match_threshold"))
        self.threshold_slider.pack(fill="x", padx=20, pady=5)

        self.threshold_value = ctk.CTkLabel(
            tab,
            text=f"Giá trị hiện tại: {self.config.get('settings.tile_match_threshold'):.2f}"
        )
        self.threshold_value.pack()

        # Max hand size
        self.handsize_label = ctk.CTkLabel(
            tab, text="Số tile tối đa trên khay:")
        self.handsize_label.pack(pady=(10, 0))

        self.handsize_var = ctk.StringVar(
            value=str(self.config.get("settings.max_hand_size")))
        self.handsize_entry = ctk.CTkEntry(
            tab,
            textvariable=self.handsize_var
        )
        self.handsize_entry.pack(fill="x", padx=20, pady=5)

    def setup_hotkeys_tab(self):
        parent_tab = self.tabview.tab("Hotkeys")

        scrollable_frame = ctk.CTkScrollableFrame(parent_tab)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def add_entry(label_text, var_name):
            label = ctk.CTkLabel(scrollable_frame, text=label_text)
            label.pack(pady=(10, 0))
            var = ctk.StringVar(value=self.config.get(var_name))
            entry = ctk.CTkEntry(scrollable_frame, textvariable=var)
            entry.pack(fill="x", padx=20, pady=5)
            return var

        self.toggle_hotkey_var = add_entry(
            "Phím Start/Pause bot:", "settings.hotkeys.toggle_bot")
        self.refresh_hotkey_var = add_entry(
            "Phím Refresh bot:", "settings.hotkeys.refresh_bot")
        self.settings_hotkey_var = add_entry(
            "Phím Setting:", "settings.hotkeys.settings")
        self.select_board_hotkey_var = add_entry(
            "Phím Select Board:", "settings.hotkeys.select_board")
        self.select_hand_hotkey_var = add_entry(
            "Phím Select Hand:", "settings.hotkeys.select_hand")
        self.select_skills_hotkey_var = add_entry(
            "Phím Select Skills:", "settings.hotkeys.select_skills")
        self.device_hotkey_var = add_entry(
            "Phím Device Connect:", "settings.hotkeys.device_connect")
        self.clear_hotkey_var = add_entry(
            "Phím Clear log:", "settings.hotkeys.clear_log")

    def update_threshold_display(self, value):
        self.threshold_value.configure(
            text=f"Giá trị hiện tại: {float(value):.2f}"
        )

    def save_settings(self):
        try:
            # Lưu các cài đặt
            self.config.set("settings.appearance.theme",
                            self.theme_var.get())
            self.config.set(
                "settings.appearance.accent_color", self.color_var.get())
            self.config.set("settings.window_size",
                            self.size_var.get())
            self.config.set(
                "settings.selected_template_pack", self.template_var.get())
            self.config.set("settings.tile_match_threshold",
                            round(self.threshold_slider.get(), 2))
            self.config.set("settings.max_hand_size",
                            int(self.handsize_var.get()))
            self.config.set("settings.hotkeys.toggle_bot",
                            self.toggle_hotkey_var.get())
            self.config.set("settings.hotkeys.refresh_bot",
                            self.refresh_hotkey_var.get())
            self.config.set("settings.hotkeys.settings",
                            self.settings_hotkey_var.get())
            self.config.set("settings.hotkeys.select_board",
                            self.select_board_hotkey_var.get())
            self.config.set("settings.hotkeys.select_hand",
                            self.select_hand_hotkey_var.get())
            self.config.set("settings.hotkeys.select_skills",
                            self.select_skills_hotkey_var.get())
            self.config.set("settings.hotkeys.device_connect",
                            self.device_hotkey_var.get())
            self.config.set("settings.hotkeys.clear_log",
                            self.clear_hotkey_var.get())

            self.parent.log(f"Setting saved")
            self.parent.setup_appearance()
            self.parent.setup_keyboard_shortcuts()
            # Đóng cửa sổ cài đặt
            self.destroy()

        except Exception as e:
            print(f"Lỗi khi lưu cài đặt: {e}")
