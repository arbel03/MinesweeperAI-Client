class Tile:
    def __init__(self):
        self.is_mine = False
        self.state = 0 # 0 = unclicked, 1 = clicked, 2 = flagged
        self.nearby_mines = 0
        self.exploded = False
