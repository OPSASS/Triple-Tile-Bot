from core.game_analyzer import GameAnalyzer
from core.hand_manager import HandManager
from core.skill_manager import SkillManager
from core.tile_detector import TileDetector
from utils.screen_capture import capture_game_region
import keyboard
import pyautogui
import time


class AutoPlayer:
    def __init__(self, controller):
        self.controller = controller
        self.detector = TileDetector()
        self.region = (self.controller.window_x, self.controller.window_y,
                       self.controller.width, self.controller.height)
        self.hand = HandManager(self.controller)
        self.skills = SkillManager(self.region)
        self.config = self.controller.config
        self.delay = 0.2

    def convert_to_screen_position(self, tile_position):
        tile_x, tile_y = tile_position
        return self.region[0] + tile_x + 32, self.region[1] + tile_y + 32

    def click_tile(self, abs_x, abs_y):
        pyautogui.moveTo(abs_x, abs_y, duration=0.1)
        pyautogui.click()

    def run(self):
        while self.controller.running:
            if keyboard.is_pressed('esc'):
                self.controller.handle_toggle()
                break

            screenshot = capture_game_region(region=self.region)
            tile_matches = self.detector.find_tiles(screenshot)
            analyzer = GameAnalyzer(tile_matches)
            best_moves = analyzer.get_best(self.hand.get_hand())
            print(best_moves)
            if len(best_moves) == 0:
                if self.hand.empty_slots() < 2:
                    self.controller.log(
                        "⚠️ Chỉ còn 1 slot và không còn tile hợp lệ. Dùng Shuffle kiểm tra lần cuối.")
                    # self.skills.use_shuffle()
                    time.sleep(0.8)
                    continue
                else:
                    self.controller.handle_toggle(
                        text='finished')
                    break

            # Kiểm tra khay đầy trước khi xử lý bất kỳ move nào
            if self.hand.empty_slots() < 2:
                self.controller.log(
                    "⚠️ Khay đã đầy, không thể nhặt thêm tile.")
                self.controller.handle_toggle()
                time.sleep(0.5)
                continue

            # move = best_moves[0]
            # for move in best_moves:
            #     move_name = move['name']

            #     for tile in move['tiles']:
            #         pos = self.convert_to_screen_position(tile['position'])
            #         self.click_tile(*pos)
            #         time.sleep(0.05)
            #         self.hand.add_tile(move_name)

            #     self.hand.remove_completed_sets()
            #     break
            for move in best_moves:
                move_name = move['name']

                # Kiểm tra nếu là tile mới và khay gần đầy
                if self.hand.empty_slots() < 2:
                    self.controller.log(
                        f"🚫 Không nhặt tile mới vì khay gần đầy.")
                    break

                # Click vào tile đầu tiên trong danh sách (tile tốt nhất)
                tile = move['tiles'][0]
                pos = self.convert_to_screen_position(tile['position'])
                self.click_tile(*pos)
                self.hand.add_tile(move_name)
                break

            time.sleep(self.config.get("settings.speed"))

    def set_speed(self, speed):
        self.delay = 1.0 / speed
