# Python Version 2.7.3
# File: minesweeper.py

import Tkinter as tk
import tkMessageBox
import random
import com
from collections import deque

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
                self.set_image(Minesweeper.MINE_IMAGE)
        elif tile.state == 2: # Flagged
            self.cover()
            self.set_image(Minesweeper.FLAG_IMAGE)
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

class Tile:
    def __init__(self):
        self.is_mine = False
        self.state = 0 # 0 = unclicked, 1 = clicked, 2 = flagged
        self.nearby_mines = 0
        self.exploded = False

class Minesweeper:
    ROWS = 10
    COLS = 10
    BOMBS = 10

    def __init__(self, master):
        # set up frame
        frame = tk.Frame(master)
        frame.pack(fill=tk.BOTH, expand=True)

        # create flag and clicked tile variables
        self.flags = 0
        self.mines = 0

        # Add UI elements
        from Tkinter import N, S, E, W

        self.label2 = tk.Label(frame, text = "Mines: "+str(self.mines))
        self.label2.grid(row=0, column=0, sticky=N+W)

        self.label3 = tk.Label(frame, text = "Flags: "+str(self.flags))
        self.label3.grid(row=0, column=1, sticky=N+E)
        
        self.board = BoardFrame(frame)
        self.board.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
        self.board.set_board((Minesweeper.ROWS, Minesweeper.COLS))
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        frame.grid_propagate(True)
        self.board.grid_propagate(True)
        # create buttons
        self.data = list()

        for _ in range(Minesweeper.ROWS):
            row_list = list()
            for _ in range(Minesweeper.COLS):
                row_list.append(Tile())
            self.data.append(row_list)

        for index in range(Minesweeper.ROWS*Minesweeper.COLS):
            self.board.get_view_at(index).set_tile(self.tile_at_index(index))
            self.board.get_view_at(index).canvas.bind('<Button-1>', self.lclicked_wrapper(index))
            self.board.get_view_at(index).canvas.bind('<Button-3>', self.rclicked_wrapper(index))

        while self.mines < Minesweeper.BOMBS:
            while True:
                bomb_index = random.randint(0, Minesweeper.COLS * Minesweeper.ROWS - 1)
                tile = self.tile_at_index(bomb_index)
                if not tile.is_mine:
                    tile.is_mine = True
                    self.mines += 1

                    pos = (bomb_index/Minesweeper.COLS, bomb_index%Minesweeper.COLS)
                    for row in range(max(pos[0]-1, 0), pos[0]+2):
                        for col in range(max(pos[1]-1, 0), pos[1]+2):
                            try:
                                tile = self.data[row][col]
                                tile.nearby_mines += 1
                            except IndexError:
                                continue
                    break

        self.flags = self.mines
        self.game_ended = False

    def solve_myself(self):
        communicator = com.Communicator("132.76.204.248", 8080)
        while 1:
            if self.game_ended:
                break
            for index in range(Minesweeper.COLS * Minesweeper.ROWS):
                if self.game_ended:
                    break
                tile = self.tile_at_index(index)
                if tile.state == 0:
                    data = self.get_state(index)
                    data = reduce(lambda x, y: x+y, data)
                    result = communicator.get_result(data)
                    if result:
                        if result == 1:
                            self.lclicked(index)
                        elif result == 2:
                            self.rclicked(index)

    def tile_at_index(self, index):
        return self.data[index/Minesweeper.COLS][index%Minesweeper.COLS]

    def check_for_mines(self, key):
        try:
            if self.tile_at_index(key).is_mine:
                return True
        except KeyError:
            pass

    def update(self):
        for row in range(Minesweeper.ROWS):
            for col in range(Minesweeper.COLS):
                tile_view = self.board.get_view_at((row, col))
                tile_view.set_tile(self.data[row][col])

    def lclicked_wrapper(self, index):
        return lambda x: self.lclicked(index)

    def rclicked_wrapper(self, index):
        return lambda x: self.rclicked(index)

    def lclicked(self, x):
        tile = self.tile_at_index(x)
        tile_view = self.board.get_view_at(x)
        if tile.is_mine: #if a mine
            self.print_state(x, False)
            tile.exploded = True
            # end game
            self.gameover()
            return
        else:
            self.print_state(x, True)
            #change image
            if tile.nearby_mines == 0:
                pos = (x/Minesweeper.COLS, x%Minesweeper.COLS)
                self.clear_empty_tiles(pos)
            # if not already set as clicked, change state and count
            if tile.state != 1:
                tile.state = 1
        self.update()

    def rclicked(self, x):
        tile = self.tile_at_index(x)
        tile_view = self.board.get_view_at(x)

        # if not clicked
        if tile.state == 0:
            if tile.is_mine:
                self.print_state(x, False)
            tile.state = 2
            tile_view.unbind('<Button-1>')
            self.flags += 1
            self.update_flags()
        # if flagged, unflag
        elif tile.state == 2:
            tile.state = 0
            tile_view.bind('<Button-1>', self.lclicked_wrapper(x))
            self.flags -= 1
            self.update_flags()
        self.update()

    def get_state(self, x):
        tile = self.tile_at_index(x)
        # This function prints the state of the board surrounding a given cell index
        row = x/10
        col = x%10
        print [row, col]
        row_range = range(row-2, row+3)
        col_range = range(col-2,col+3)
        # If cell is uncovered
        return [[self.get_tile_number(row, col) for col in col_range] for row in row_range]

    def print_state(self, x, good_answer):
        tile = self.tile_at_index(x)
        if tile.state == 0:
            data = self.get_state(x)
            data_file = open('data_file.txt', 'a+')
            data_file.write(str([data, int(good_answer)])+"\n")
            data_file.close()
            for row in data:
                print row
            print "Should click there?", good_answer

    def get_tile_number(self, row, column):
        try:
            tile = self.data[row][column]
            # tile is flagged
            if tile.state == 2:
                return -2
            elif tile.state == 0:
                return -1
            else:
                return tile.nearby_mines
        except IndexError:
            return 0

    def check_tile(self, pos, queue):
        try:
            tile = self.data[pos[0]][pos[1]] 
            tile_view = self.board.get_view_at(pos)
            if tile.state == 0:
                if tile.nearby_mines == 0:
                    queue.append(pos)
                tile.state = 1
        except IndexError:
            return

    def clear_empty_tiles(self, pos):
        queue = deque([pos])

        while len(queue) != 0:
            pos = queue.popleft()
            for row in range(max(pos[0]-1, 0), pos[0]+2):
                for col in range(max(pos[1]-1, 0), pos[1]+2):
                    if row == pos[0] and col == pos[1]:
                        continue
                    self.check_tile((row, col), queue)        
    
    def ignore_interaction(self):
        for row in range(Minesweeper.ROWS):
            for col in range(Minesweeper.COLS):
                self.board.get_view_at((row, col)).canvas.unbind('<Button-3>')
                self.board.get_view_at((row, col)).canvas.unbind('<Button-1>')

    def gameover(self):
        # show all mines and check for flags
        for row in range(Minesweeper.ROWS):
            for col in range(Minesweeper.COLS):
                tile = self.data[row][col]
                if tile.is_mine and tile.state == 0:
                    # Uncover bomb
                    tile.state = 1
        self.update()
        self.ignore_interaction()
        tkMessageBox.showinfo("Game Over", "You Lose!")
        self.game_ended = True

    def victory(self):
        self.ignore_interaction()
        tkMessageBox.showinfo("Game Over", "You Win!")
        self.game_ended = True

    def update_flags(self):
        self.label3.config(text = "Flags: "+str(self.flags))

### END OF CLASSES ###

def main():
    global root
    # create Tk widget
    root = tk.Tk()
    # set program title
    root.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(root)
    root.geometry('500x500+200+200')

    Minesweeper.MINE_IMAGE = tk.PhotoImage(file = "images/mine.gif")
    Minesweeper.FLAG_IMAGE = tk.PhotoImage(file="images/flag.gif")

    root.after(0, minesweeper.solve_myself)
    # run event loop
    root.mainloop()

if __name__ == "__main__":
    main()
