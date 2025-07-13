class GameAnalyzer:
    def __init__(self, tile_matches):
        self.tile_matches = tile_matches

    def group_tiles(self):
        groups = {}
        for tile in self.tile_matches:
            name = tile['name']
            if name not in groups:
                groups[name] = []
            groups[name].append(tile)
        return groups

    # def get_best(self, hand_tiles):
    #     groups = self.group_tiles()
    #     possible_moves = []

    #     for name, tiles in groups.items():
    #         if len(tiles) >= 1:
    #             sorted_tiles = sorted(
    #                 tiles, key=lambda x: x['score'], reverse=True)
    #             move = {
    #                 'name': name,
    #                 'tiles': sorted_tiles[:min(3, len(sorted_tiles))]
    #             }
    #             possible_moves.append(move)

    #     # Ưu tiên nhóm đã có trong khay
    #     def move_priority(move):
    #         priority = 1 if move['name'] in hand_tiles else 0
    #         score_avg = sum(t['score']
    #                         for t in move['tiles']) / len(move['tiles'])
    #         return (priority, score_avg)

    #     possible_moves.sort(key=move_priority, reverse=True)
    #     return possible_moves

    def get_best(self, hand_tiles):
        groups = self.group_tiles()
        possible_moves = []

        for name, tiles in groups.items():
            if len(tiles) >= 1:
                sorted_tiles = sorted(
                    tiles, key=lambda x: x['score'], reverse=True)
                move = {
                    'name': name,
                    'tiles': sorted_tiles[:1]  # Chỉ lấy 1 tile tốt nhất
                }
                possible_moves.append(move)

        # Ưu tiên moves có tile trùng với hand hiện tại
        possible_moves.sort(
            key=lambda m: m['name'] in hand_tiles, reverse=True)
        return possible_moves
