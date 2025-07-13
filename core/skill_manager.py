import pyautogui
import time


SKILL_POS = {
    "undo": (750, 750),
    "shuffle": (850, 750),
    "bomb": (950, 750)
}


class SkillManager:
    def __init__(self, game_region):
        self.region = game_region

    def get_absolute_pos(self, skill_name):
        rel_x, rel_y = SKILL_POS[skill_name]
        abs_x = self.region[0] + rel_x
        abs_y = self.region[1] + rel_y
        return abs_x, abs_y

    def use_skill(self, skill_name):
        x, y = self.get_absolute_pos(skill_name)
        print(f"🧠 Dùng kỹ năng: {skill_name.upper()} tại ({x}, {y})")
        # pyautogui.moveTo(x, y, duration=0.1)
        # pyautogui.click()
        # time.sleep(1)
