import Tkinter as tk
from model import Tile

class TileFrame(tk.Frame):

    PADDING = int(0.15*50)

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.pack_propagate(False)
        self.tile = None

    def configure(self, event):
        self.set_tile(self.tile)

    def set_tile(self, tile):
        if not self.tile:
            self.bind('<Configure>', self.configure)
        self.tile = tile
        self.canvas.delete("all")
        if tile.state == 1: # Clicked
            self.uncover()
            if tile.nearby_mines != 0:
                self.set_number(tile.nearby_mines)
            if tile.exploded:
                self.canvas.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), fill="red")
            if tile.is_mine:
                self.set_image(Tile.MINE_IMAGE)
        elif tile.state == 2: # Flagged
            self.cover()
            self.set_image(Tile.FLAG_IMAGE)
            if not tile.is_mine:
                self.show_wrong_flag()
        elif tile.state == 0:
            self.cover()

    def show_wrong_flag(self):
        width = self.winfo_width()
        height = self.winfo_height()
        self.canvas.create_line(TileFrame.PADDING, TileFrame.PADDING, width-TileFrame.PADDING, height-TileFrame.PADDING, fill='black')
        self.canvas.create_line(width-TileFrame.PADDING, TileFrame.PADDING, TileFrame.PADDING, height-TileFrame.PADDING, fill='black')

    def cover(self):
        width = self.winfo_width()
        height = self.winfo_height()
        left_side = [0, 0, TileFrame.PADDING, TileFrame.PADDING, TileFrame.PADDING, height - TileFrame.PADDING, width - TileFrame.PADDING, height - TileFrame.PADDING, width, height, 0, height, 0, 0]
        self.canvas.create_polygon(left_side, fill='white')
        right_side = [0, 0, TileFrame.PADDING, TileFrame.PADDING, width - TileFrame.PADDING, TileFrame.PADDING, width - TileFrame.PADDING, height - TileFrame.PADDING, width, height, width, 0, 0, 0]
        self.canvas.create_polygon(right_side, fill='#8C8C8C')

    def set_image(self, image):
        self.canvas.create_image(25, 25, image=image)
        
    def uncover(self):
        width = self.winfo_width()
        height = self.winfo_height()
        self.canvas.create_rectangle(0, 0, width, height, fill="#C0C0C0")

    def set_number(self, number):
        colors = ['#0100FE', '#017F01', '#FE0000', '#010080', '#810102', '#008081', '#000000', '#7E7E7E']
        self.canvas.create_text(25, 25, fill=colors[number-1], font="Times 24 bold", text=str(number), anchor=tk.CENTER)

class BoardFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.board_size = (0, 0)
        self.buttons = list()

    def set_board(self, board_size):
        from Tkinter import N, S, E, W
        self.board_size = board_size
        (rows, columns) = self.board_size
        for row in range(rows):
            row_list = list()
            for column in range(columns):
                tile = TileFrame(self, width=50, height=50)
                tile.grid(row=row, column=column, sticky=N+S+E+W)
                row_list.append(tile)
            self.buttons.append(row_list) 
            self.grid_rowconfigure(row, weight=1)

        for col in range(columns):
            self.grid_columnconfigure(col, weight=1)

    def get_view_at(self, index_or_pos):
        if type(index_or_pos) == tuple:
            return self.buttons[index_or_pos[0]][index_or_pos[1]]
        else:
            cols = self.board_size[1]
            return self.buttons[index_or_pos/cols][index_or_pos%cols]
