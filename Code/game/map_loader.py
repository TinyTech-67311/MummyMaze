import pygame
import os


def read_world_map(stage):
    stages = [
        "map6_1.txt",
        "map6_2.txt",
        "map6_3.txt",
        "map6_4.txt",
        "map6_5.txt",
        "map8_1.txt",
        "map8_2.txt",
        "map8_3.txt",
        "map8_4.txt",
        "map8_5.txt",
        "map10_1.txt",
        "map10_2.txt",
        "map10_3.txt",
        "map10_4.txt",
        "map10_5.txt"
    ]

    return stages[stage]

def read_map_head_menu(stage):
    stages_coordinates = [
        (512, 402),  # Stage 1
        (533, 402),  # Stage 2
        (555, 402),  # Stage 3
        (574, 402),  # Stage 4
        (594, 402),  # Stage 5
        (584, 387),  # Stage 6
        (564, 387),  # Stage 7
        (544, 387),  # Stage 8
        (524, 387),  # Stage 9
        (534, 372),  # Stage 10
        (555, 372),  # Stage 11
        (575, 372),  # Stage 12
        (564, 357),  # Stage 13
        (544, 357),  # Stage 14
        (555, 337)   # Stage 15
    ]

    return stages_coordinates[stage]

def get_input_maze(self, maze_path, file_name):
    # Lấy dữ liệu mê cung ASCII lưu vào maze
    self.maze           = []
    self.stair_position = ()
    self.trap_position  = ()
    self.key_position   = []
    self.gate = {
        "gate_position": None,
        "isClosed":      True,
        "cellIndex":     0
    }

    with open(os.path.join(maze_path, file_name), "r") as file:
        for line in file:
            row = []
            for chr in line:
                if chr != '\n':
                    row.append(chr)
            self.maze.append(row)

    # Mê cung ASCII vừa biểu diễn đường đi vừa biểu diễn tường nên size nó gấp đôi
    # Ô thứ tự lẻ là tường, ô thứ tự chẵn là đường đi
    self.maze_size = len(self.maze) // 2
    self.cell_rect = self.maze_rect // self.maze_size

    # Tìm vị trí các vật phẩm trong mê cung
    for i in range(len(self.maze)):
        for j in range(len(self.maze[i])):
            if self.maze[i][j] == 'S':
                self.stair_position        = (i, j)
            if self.maze[i][j] == 'T':
                self.trap_position         = (i, j)
            if self.maze[i][j] == 'K':
                self.key_position.append     ((i, j))
            if self.maze[i][j] == 'G':
                self.gate["gate_position"] = (i, j)

def get_input_object(self, agents_path, file_name):
    # Tìm position ban đầu của người chơi và các quái
    self.mummy_white_position    = []
    self.mummy_red_position      = []
    self.scorpion_white_position = []
    self.scorpion_red_position   = []
    with open(os.path.join(agents_path, file_name), "r") as file:
        for line in file:
            x = line.split()
            if x[0] == "E":
                self.explorer_position = [int(x[1]), int(x[2])]
            if x[0] == "MW":
                self.mummy_white_position.append(
                    [int(x[1]), int(x[2])]
                )
            if x[0] == "MR":
                self.mummy_red_position.append(
                    [int(x[1]), int(x[2])]
                )
            if x[0] == "SW":
                self.scorpion_white_position.append(
                    [int(x[1]), int(x[2])]
                )
            if x[0] == "SR":
                self.scorpion_red_position.append(
                    [int(x[1]), int(x[2])]
                )
def show_information(self):
        print("Maze: ")
        for i in range(len(self.maze)):
            print(self.maze[i])
        print("Stair position: {}".format(self.stair_position))
        if self.trap_position:
            print("Trap position: {}".format(self.trap_position))
        else: print("Trap doesn't exist in this map")
        if self.key_position:
            for i in range(len(self.key_position)):
                print("Key position:", i + 1, "{}".format(self.key_position[i]))
            print("Gate position: {}".format(self.gate["gate_position"]))
        else:
            print("Key and gate don't exist in this map")
        print("Explorer position: {}".format(self.explorer_position))
        for i in range(len(self.mummy_white_position)):
            print("Mummy white number {}: {}".format(i+1, self.mummy_white_position[i]))
        for i in range(len(self.mummy_red_position)):
            print("Mummy red number {}: {}".format(i+1, self.mummy_red_position[i]))
        for i in range(len(self.scorpion_white_position)):
            print("Scorpion white number {}: {}".format(i+1, self.scorpion_white_position[i]))
        for i in range(len(self.scorpion_red_position)):
            print("Scorpion red number {}: {}".format(i+1, self.scorpion_red_position[i]))