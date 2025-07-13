

class HandManager:
    def __init__(self, controller):
        self.max_slots = 7
        self.controller = controller
        self.tiles = []

    def add_tile(self, name):
        if len(self.tiles) >= self.max_slots:
            return False

        self.tiles.append(name)
        self.remove_completed(name)
        return True

    def remove_completed(self, name):
        if self.tiles.count(name) == 3:
            self.tiles = [item for item in self.tiles if item != name]
            self.controller.tile_count += 1
            self.controller.app.tile_count_label.configure(
                text=f"Tile Count: {self.controller.tile_count}")

    def count(self):
        return len(self.tiles)

    def has_matching_tile(self, name):
        return name in self.tiles

    def empty_slots(self):
        return max(0, self.max_slots - len(self.tiles))

    def get_unique_names(self):
        return list(set(self.tiles))

    def get_hand(self):
        return self.tiles
