import json
import os
from typing import Dict, Any, List


class ConfigManager:
    def __init__(self):
        self.default_config_path = "config/settings.json"
        self.user_config_path = "config/user_settings.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        # Tạo thư mục config nếu chưa tồn tại
        os.makedirs("config", exist_ok=True)

        # Tạo file cấu hình mặc định nếu không tồn tại
        if not os.path.exists(self.default_config_path):
            self._create_default_config()

        # Đọc cấu hình mặc định
        try:
            with open(self.default_config_path, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Lỗi đọc file cấu hình mặc định: {e}")
            config = self._create_default_config()

        # Đọc và hợp nhất cấu hình người dùng nếu tồn tại
        if os.path.exists(self.user_config_path):
            try:
                with open(self.user_config_path, 'r') as f:
                    user_config = json.load(f)
                    config = self._merge_dicts(
                        config, user_config
                    )
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Lỗi đọc file cấu hình người dùng: {e}")

        return config

    def _create_default_config(self) -> Dict[str, Any]:
        default_config = {
            "settings": {
                "app_title": "Triple Tile Auto Bot",
                "window_size": "500x650",
                "speed": 1.0,
                "tile_match_threshold": 0.85,
                "max_hand_size": 7,
                "template_packs": {
                    "tripletile": "assets/templates/tiles/tripletile",
                    "weplay": "assets/templates/tiles/weplay"
                },
                "selected_template_pack": "tripletile",
                "hotkeys": {
                    "toggle_bot": "F1",
                    "refresh_bot": "F2",
                    "settings": "F3",
                    "select_board": "b",
                    "select_hand": "h",
                    "select_skills": "s",
                    "device_connect": "d",
                    "clear_log": "c",
                },
                "appearance": {
                    "theme": "system",
                    "accent_color": "blue"
                }
            }
        }

        try:
            with open(self.default_config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
        except Exception as e:
            print(f"Không thể tạo file cấu hình mặc định: {e}")

        return default_config

    def _merge_dicts(self, base: Dict, custom: Dict) -> Dict:
        for key in custom:
            if key in base and isinstance(base[key], dict) and isinstance(custom[key], dict):
                self._merge_dicts(base[key], custom[key])
            else:
                base[key] = custom[key]
        return base

    def save_user_config(self):
        user_config = {
            "settings": {
                "speed": self.get("settings.speed"),
                "tile_match_threshold": self.get("settings.tile_match_threshold"),
                "max_hand_size": self.get("settings.max_hand_size"),
                "selected_template_pack": self.get("settings.selected_template_pack"),
                "hotkeys": {
                    "toggle_bot": self.get("settings.hotkeys.toggle_bot"),
                    "refresh_bot": self.get("settings.hotkeys.refresh_bot"),
                    "settings": self.get("settings.hotkeys.settings"),
                    "select_board": self.get("settings.hotkeys.select_board"),
                    "select_hand": self.get("settings.hotkeys.select_hand"),
                    "select_skills": self.get("settings.hotkeys.select_skills"),
                    "device_connect": self.get("settings.hotkeys.device_connect"),
                    "clear_log": self.get("settings.hotkeys.clear_log"),
                },
                "appearance": {
                    "theme": self.get("settings.appearance.theme"),
                    "accent_color": self.get("settings.appearance.accent_color")
                },
            }
        }

        try:
            with open(self.user_config_path, 'w') as f:
                json.dump(user_config, f, indent=4)
        except Exception as e:
            print(f"Không thể lưu cấu hình người dùng: {e}")

    def get(self, key_path: str):
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, {})
            else:
                return None
        return value if value != {} else None

    def set(self, key_path: str, value: Any):
        keys = key_path.split('.')
        current = self.config
        for key in keys[:-1]:
            current = current.setdefault(key, {})
        current[keys[-1]] = value
        self.save_user_config()

    def get_template_packs(self) -> List[str]:
        return list(self.get("settings.template_packs").keys())

    def get_template_pack_path(self, pack_name: str) -> str:
        packs = self.get("settings.template_packs")
        return packs.get(pack_name, "")
