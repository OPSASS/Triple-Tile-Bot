from config.config_manager import ConfigManager
import cv2
import os


class TileDetector:
    def __init__(self):
        self.config = ConfigManager()
        self.templates = self.load_templates()

    def load_templates(self):
        pack_name = self.config.get(
            "settings.selected_template_pack")
        templates_path = self.config.get_template_pack_path(pack_name)
        templates = {}
        for filename in os.listdir(templates_path):
            if filename.endswith(".png"):
                name = os.path.splitext(filename)[0]
                path = os.path.join(templates_path, filename)
                image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                templates[name] = image
        return templates

    def find_tiles(self, screenshot):
        threshold = self.config.get("settings.tile_match_threshold")
        matches = []

        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        for name, template in self.templates.items():
            if len(template.shape) == 3:
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            else:
                template_gray = template

            screenshot_gray = screenshot_gray.astype("uint8")
            template_gray = template_gray.astype("uint8")

            res = cv2.matchTemplate(
                screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)

            loc = zip(*((res >= threshold).nonzero()[::-1]))
            for pt in loc:
                matches.append({
                    "name": name,
                    "position": pt,
                    "score": res[pt[1], pt[0]]
                })

        return matches
