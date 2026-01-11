import pygame
import os
import collections
from ui import graphics

class character():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def check_same_position(self, character):
        return (character.x == self.x) and (character.y == self.y)

    def eligible_character_move(self, maze, gate, x, y, new_x, new_y):
        # Vượt ra ngoài mê cung thì False
        if new_x < 1 or new_x >= len(maze) or new_y < 1 or new_y >= len(maze):
            return False
        # Check xem các trường hợp đi có đụng tường hay vô cổng đóng không
        # Move Down
        if new_x == x + 2:
            if maze[x + 1][y] == "%" or (maze[x + 1][y] == "G" and gate["isClosed"]):
                return False
        # Move Up
        if new_x == x - 2:
            if maze[x - 1][y] == "%" or (maze[x - 1][y] == "G" and gate["isClosed"]):
                return False
        # Move Right
        if new_y == y + 2:
            if maze[x][y + 1] == "%" or (maze[x][y + 1] == "G" and gate["isClosed"]):
                return False
        # Move Left
        if new_y == y - 2:
            if maze[x][y - 1] == "%" or (maze[x][y - 1] == "G" and gate["isClosed"]):
                return False
        return True

    def move_animation(self, x, y, screen, game, backdrop, floor,
                       stair, stair_position, trap, trap_position, key, key_position,
                       gate_sheet, gate, wall,
                       explorer,
                       mummy_white, mummy_red, scorpion_white, scorpion_red):
        raise NotImplementedError("This is base class method")

    def move(self, new_x, new_y, screen, game, backdrop, floor,
             stair, stair_position, trap, trap_position, key, key_position,
             gate_sheet, gate, wall,
             explorer,
             mummy_white, mummy_red, scorpion_white, scorpion_red):

        self.move_animation(new_x, new_y, screen, game, backdrop, floor,
                            stair, stair_position, trap, trap_position, key, key_position,
                            gate_sheet, gate, wall,
                            explorer,
                            mummy_white, mummy_red, scorpion_white, scorpion_red)
        self.x = new_x
        self.y = new_y

    def move_xy(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class Explorer(character):
    def move_animation(self, x, y, screen, game, backdrop, floor,
                       stair, stair_position, trap, trap_position, key, key_position,
                       gate_sheet, gate, wall,
                       explorer,
                       mummy_white, mummy_red, scorpion_white, scorpion_red):
        # Tính toán tọa độ pixel của nhân vật
        explorer_start_x = game.coordinate_screen_x + game.cell_rect * (self.y // 2)
        explorer_start_y = game.coordinate_screen_y + game.cell_rect * (self.x // 2)
        # Nếu bên trên là tường hoặc cổng dịch nhân vật xuống 3 pixel để đầu không đụng tường
        if (x > 0) and (game.maze[x - 1][y] == "%" or game.maze[x - 1][y] == "G"):
            explorer_start_y += 3
        explorer["coordinates"] = [explorer_start_x, explorer_start_y]
        # Tính toán khoảng cách pixel của mỗi bước đi
        step_stride = game.cell_rect // 5
        coordinates = list(explorer["coordinates"])
        for i in range(6):
            # 5 Bước đầu là di chuyển
            # Bước thứ 6 là đến nơi
            if i < 5:
                if explorer["direction"] == "UP":
                    coordinates[1] -= step_stride
                if explorer["direction"] == "DOWN":
                    coordinates[1] += step_stride
                if explorer["direction"] == "LEFT":
                    coordinates[0] -= step_stride
                if explorer["direction"] == "RIGHT":
                    coordinates[0] += step_stride
            explorer["coordinates"] = list(coordinates)
            explorer["cellIndex"] = i % 5
            graphics.draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                                 stair, stair_position, trap, trap_position, key, key_position,
                                 gate_sheet, gate, wall,
                                 explorer,
                                 mummy_white, mummy_red, scorpion_white, scorpion_red)
            pygame.time.delay(60)
            pygame.display.update()

class enemy(character):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move_Vertical(self, maze, gate, explorer, audio_manager):
        new_x = self.get_x() + 2 * sign(explorer.get_x() - self.get_x())
        new_y = self.get_y()
        moved = False

        if self.eligible_character_move(maze, gate, self.get_x(), self.get_y(), new_x, new_y):
            self.move_xy(new_x, new_y)
            moved = True

        return self, moved

    def move_Horizontal(self, maze, gate, explorer, audio_manager):
        new_x = self.get_x()
        new_y = self.get_y() + 2 * sign(explorer.get_y() - self.get_y())
        moved = False

        if self.eligible_character_move(maze, gate, self.get_x(), self.get_y(), new_x, new_y):
            self.move_xy(new_x, new_y)
            moved = True

        return self, moved

    def bfs_shortest_path(self, maze, gate, target_x, target_y):
        start_x, start_y = self.x, self.y

        queue = collections.deque([(start_x, start_y, [])])
        visited = set([(start_x, start_y)])

        # Các hướng đi có thể (bước 2 ô)
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]

        while queue:
            current_x, current_y, path = queue.popleft()

            if current_x == target_x and current_y == target_y:
                return path[0] if path else None

            for dx, dy in directions:
                new_x = current_x + dx
                new_y = current_y + dy

                if self.eligible_character_move(maze, gate, current_x, current_y, new_x, new_y):
                    if (new_x, new_y) not in visited:
                        visited.add((new_x, new_y))
                        new_path = path + [(new_x, new_y)]
                        queue.append((new_x, new_y, new_path))

        return None

class mummy_white(enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        # BFS là 0, Greedy là 1
        self.current_strategy = 1

    def set_move_strategy(self, strategy):
        self.current_strategy = strategy

    def white_move(self, maze, gate, explorer, audio_manager):
        if self.check_same_position(explorer):
            return self
        if self.current_strategy == 0:
            target_x, target_y = explorer.get_x(), explorer.get_y()
            next_step = None
            next_step = self.bfs_shortest_path(maze, gate, target_x, target_y)
            # Cập nhật vị trí sau BFS
            if next_step is not None:
                next_x, next_y = next_step
                self.move_xy(next_x, next_y)
                audio_manager.play_sfx('mumwalk')
        else:
            moved = False
            # Ưu tiên đuổi theo hàng ngang
            if self.get_y() != explorer.get_y():
                self, moved = self.move_Horizontal(maze, gate, explorer, audio_manager)

            # Nếu không di chuyển ngang được thì di chuyển dọc
            if not moved:
                if self.get_x() != explorer.get_x():
                    self, moved = self.move_Vertical(maze, gate, explorer, audio_manager)

            if moved:
                audio_manager.play_sfx('mumwalk')
        return self

class mummy_red(enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        # BFS là 0, Greedy là 1
        self.current_strategy = 1

    def set_move_strategy(self, strategy):
        self.current_strategy = strategy

    def red_move(self, maze, gate, explorer, stair_position, audio_manager):
        if self.check_same_position(explorer):
            return self
        if self.current_strategy == 0:
            target_x, target_y = stair_position[0], stair_position[1]
            if   stair_position[0] == 0:
                target_x += 1
            elif stair_position[0] == len(maze) - 1:
                target_x -= 1
            elif stair_position[1] == 0:
                target_y += 1
            elif stair_position[1] == len(maze) - 1:
                target_y -= 1
            next_step = None
            next_step = self.bfs_shortest_path(maze, gate, target_x, target_y)
            # Cập nhật vị trí sau BFS
            if next_step is not None:
                next_x, next_y = next_step
                self.move_xy(next_x, next_y)
                audio_manager.play_sfx('mumwalk')
        else:
            moved = False
            # Ưu tiên đuổi theo hàng dọc
            if self.get_x() != explorer.get_x():
                self, moved = self.move_Vertical(maze, gate, explorer, audio_manager)

            # Nếu không di chuyển dọc được thì di chuyển ngang
            if not moved:
                if self.get_y() != explorer.get_y():
                    self, moved = self.move_Horizontal(maze, gate, explorer, audio_manager)

            if moved:
                audio_manager.play_sfx('mumwalk')
        return self

class scorpion_white(mummy_white):
    def __init__(self, x, y):
        super().__init__(x, y)

class scorpion_red(mummy_red):
    def __init__(self, x, y):
        super().__init__(x, y)

def set_direction(self):
    # Set hướng ban đầu cho nhân vật
    # Mặc định người chơi nửa trái bản đồ thì hướng phải và ngược lại
    set_explorer_direction_default = True
    if set_explorer_direction_default:
        if self.explorer_position[1] // 2 <= self.maze_size // 2:
            self.explorer_direction = "RIGHT"
        else:
            self.explorer_direction = "LEFT"

    # Set hướng ban đầu cho các quái
    # Mặc định ban đầu hướng xuống
    set_objects_direction_default = True
    if set_objects_direction_default:
        self.mummy_white_direction    = ["DOWN"] * len(self.mummy_white_position)
        self.mummy_red_direction      = ["DOWN"] * len(self.mummy_red_position)
        self.scorpion_white_direction = ["DOWN"] * len(self.scorpion_white_position)
        self.scorpion_red_direction   = ["DOWN"] * len(self.scorpion_red_position)

def sign(x):
    if x == 0:
        return 0
    else:
        return x // abs(x)