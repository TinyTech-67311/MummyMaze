import pygame
import os
import sys

from ui import graphics
from game import characters
from game import map_loader
from game import control
from game.audio_manager import AudioManager
from collections import deque
from path_utils import rpath

class set_pages:
    def __init__(self, login, register, homepage, world_map, result):
        self.login     = login
        self.register  = register
        self.homepage  = homepage
        self.world_map = world_map
        self.result    = result

        self.session   = {
            "logged_in": False,
            "account"  : None,
        }

    def get_login(self):
        return self.login

    def get_register(self):
        return self.register

    def get_homepage(self):
        return self.homepage

    def get_world_map(self):
        return self.world_map

    def get_result(self):
        return self.result

class game_state:
    def __init__(self, stage):
        """
        Giải thích vì sao có các kích thước bên dưới:
        - maze_rect = 360 vì chúng ta có mê cung 6x6, 8x8, 10x10. 360 đáp ứng chia hết cho 6, 8, 10
        - size_x, size_y kích cỡ backdrop
        - coor_x tính bằng (size_x - maze_rect) / 2
        - coor_y tính bằng (size_y - maze_rect) / 2
        """
        self.maze_rect           = 360
        self.screen_size_x       = 640
        self.screen_size_y       = 480
        self.coordinate_screen_x = 67
        self.coordinate_screen_y = 80
        self.stage               = stage
        self.undo_stack          = deque()

        # Tải maze và agents từ map_loader (không phụ thuộc biến global)
        project_path = os.path.dirname(os.path.abspath(__file__))
        map_path     = os.path.join(project_path, "assets", "map")
        agents_path  = os.path.join(map_path, "agents")
        maze_path    = os.path.join(map_path, "maze")
        file_name    = map_loader.read_world_map(stage)
        map_loader.get_input_maze(self, maze_path, file_name)
        map_loader.get_input_object(self, agents_path, file_name)

        # Cài đặt hướng cho nhân vật
        characters.set_direction(self)
        # Show console
        map_loader.show_information(self)

# Tạo đường dẫn đến hình ảnh
def load_image_login_path():
    project_path = os.path.dirname(os.path.abspath(__file__))
    image_path   = os.path.join(project_path, "assets", "image")

    login_background_path      = os.path.join(image_path, "authen_background.png")
    login_dialog_path          = os.path.join(image_path, "authen_dialog.png")
    login_title_path           = os.path.join(image_path, "authen_title.png")
    login_state_label_path     = os.path.join(image_path, "authen_state_login.png")
    login_user_field_path      = os.path.join(image_path, "authen_blank.png")
    login_password_field_path  = os.path.join(image_path, "authen_blank.png")
    login_button_login_path    = os.path.join(image_path, "authen_login.png")
    login_button_register_path = os.path.join(image_path, "authen_register.png")
    login_title_back_path      = os.path.join(image_path, "authen_back.png")
    login_button_back_path     = os.path.join(image_path, "back_btn.png")
    eye_path                   = os.path.join(image_path, "eye.png")
    lock_eye_path              = os.path.join(image_path, "lock_eye.png")

    return login_background_path, login_dialog_path, login_title_path, login_state_label_path, \
            login_user_field_path, login_password_field_path, login_button_login_path, login_button_register_path, \
            login_title_back_path, login_button_back_path, eye_path, lock_eye_path

def load_image_register_path():
    project_path = os.path.dirname(os.path.abspath(__file__))
    image_path   = os.path.join(project_path, "assets", "image")

    register_background_path      = os.path.join(image_path, "authen_background.png")
    register_dialog_path          = os.path.join(image_path, "authen_dialog.png")
    register_title_path           = os.path.join(image_path, "authen_title.png")
    register_state_label_path     = os.path.join(image_path, "authen_state_register.png")
    register_user_field_path      = os.path.join(image_path, "authen_blank.png")
    register_password_field_path  = os.path.join(image_path, "authen_blank.png")
    register_button_login_path    = os.path.join(image_path, "authen_login.png")
    register_button_register_path = os.path.join(image_path, "authen_register.png")
    register_title_back_path      = os.path.join(image_path, "authen_back.png")
    register_button_back_path     = os.path.join(image_path, "back_btn.png")
    eye_path                      = os.path.join(image_path, "eye.png")
    lock_eye_path                 = os.path.join(image_path, "lock_eye.png")

    return register_background_path, register_dialog_path, register_title_path, register_state_label_path, \
        register_user_field_path, register_password_field_path, register_button_login_path, register_button_register_path, \
        register_title_back_path, register_button_back_path, eye_path, lock_eye_path

def load_image_homepage_path():
    image_path             = rpath("assets", "image")

    background_path        = os.path.join(image_path, "background.png")
    title_path             = os.path.join(image_path, "Mummy_maze_title.png")
    lis_button_play_path   = [
        os.path.join(image_path, "buttons", "play_button.png"),
        os.path.join(image_path, "buttons", "play_button_hover.png")
    ]
    lis_button_sound_path  = [
        os.path.join(image_path, "buttons", "sound_button_on.png"),
        os.path.join(image_path, "buttons", "sound_button_off.png"),
    ]
    lis_button_music_path  = [
        os.path.join(image_path, "buttons", "music_button_on.png"),
        os.path.join(image_path, "buttons", "music_button_off.png"),
    ]

    return background_path, title_path,\
           lis_button_play_path, lis_button_sound_path, lis_button_music_path

def load_image_world_map():
    image_path     = rpath("assets", "image")

    background_world_map_path = os.path.join(image_path, "background_world_map.png")
    world_map_frame_path      = os.path.join(image_path, "world_map_frame.png")

    easy_level_path      = os.path.join(image_path, "easy_level.png")
    hard_level_path      = os.path.join(image_path, "hard_level.png")
    level_selection_path = os.path.join(image_path, "level_selection.png")

    back_path            = [
        os.path.join(image_path, "buttons", "back.png"),
        os.path.join(image_path, "buttons", "back_hover.png")
    ]
    level_path           = []
    for lv in range(1, 16):
        normal_image_path = os.path.join(image_path, "buttons", "level_" + str(lv) + ".png")
        hover_image_path  = os.path.join(image_path, "buttons", "level_" + str(lv) + "_hover.png")
        level_path.append([normal_image_path, hover_image_path])

    return (background_world_map_path, world_map_frame_path,
            easy_level_path, hard_level_path, level_selection_path,
            back_path, level_path)

def load_image_result_path():
    project_path = os.path.dirname(os.path.abspath(__file__))
    image_path   = os.path.join(project_path, "assets", "image")

    background_result_path   = os.path.join(image_path, "background_result.png")

    lis_title_path           = [
        os.path.join(image_path,"victory_title.png"),
        os.path.join(image_path,"failure_title.png")
    ]
    lis_key_path             = [
        os.path.join(image_path, "victory_key.png"),
        os.path.join(image_path, "failure_key.png"),
    ]
    lis_button_undomove_path = [
        os.path.join(image_path, "buttons", "undo_move.png"),
        os.path.join(image_path, "buttons", "undo_move_hover.png"),
    ]
    lis_button_tryagain_path = [
        os.path.join(image_path, "buttons", "try_again.png"),
        os.path.join(image_path, "buttons", "try_again_hover.png"),
    ]
    lis_button_worldmap_path = [
        os.path.join(image_path, "buttons", "world_map.png"),
        os.path.join(image_path, "buttons", "world_map_hover.png"),
    ]
    lis_button_home_path     = [
        os.path.join(image_path, "buttons", "home.png"),
        os.path.join(image_path, "buttons", "home_hover.png")
    ]

    return background_result_path, lis_title_path, lis_key_path, lis_button_undomove_path,\
           lis_button_worldmap_path, lis_button_tryagain_path, lis_button_home_path

def load_image_path(size):
    image_path          = rpath("assets", "image")

    menu_path           = os.path.join(image_path, "menu.png")
    map_head_path       = os.path.join(image_path, "maphead.png")
    backdrop_path       = os.path.join(image_path, "backdrop.png")
    floor_path          = os.path.join(image_path, "floor"          + str(size) + ".jpg")
    wall_path           = os.path.join(image_path, "walls"          + str(size) + ".png")
    key_path            = os.path.join(image_path, "key"            + str(size) + ".png")
    gate_path           = os.path.join(image_path, "gate"           + str(size) + ".png")
    trap_path           = os.path.join(image_path, "trap"           + str(size) + ".png")
    stair_path          = os.path.join(image_path, "stairs"         + str(size) + ".png")
    explorer_path       = os.path.join(image_path, "explorer"       + str(size) + ".png")
    mummy_white_path    = os.path.join(image_path, "mummy_white"    + str(size) + ".png")
    mummy_red_path      = os.path.join(image_path, "red_mummy"      + str(size) + ".png")
    scorpion_white_path = os.path.join(image_path, "white_scorpion" + str(size) + ".png")
    scorpion_red_path   = os.path.join(image_path, "red_scorpion"   + str(size) + ".png")
    white_fight_path    = os.path.join(image_path, "white_fight"    + str(size) + ".png")
    red_fight_path      = os.path.join(image_path, "red_fight"      + str(size) + ".png")
    stung_path          = os.path.join(image_path, "stung"          + str(size) + ".gif")
    dust_path           = os.path.join(image_path, "dust"           + str(size) + ".gif")

    return menu_path, map_head_path,\
           backdrop_path, floor_path, wall_path, key_path, gate_path, trap_path, stair_path,\
           explorer_path, mummy_white_path, mummy_red_path,\
           scorpion_white_path, scorpion_red_path,\
           white_fight_path, red_fight_path, stung_path, dust_path

def show_login(screen, pages, audio_manager):
    print("LOGIN")
    while True:
        action = control.control_login(screen, pages, audio_manager)
        if action == "login_success":
            show_homepage(screen, pages, 0, audio_manager)
            return
        if action == "to_register":
            show_register(screen, pages, audio_manager)
            return
        if action == "back_home":
            show_homepage(screen, pages, 0, audio_manager)
            return
        if action == "quit_game":
            return

def show_register(screen, pages, audio_manager):
    print("REGISTER")
    while True:
        action = control.control_register(screen, pages, audio_manager)
        if action in ("register_success", "to_login"):
            show_login(screen, pages, audio_manager)
            return
        if action == "back_home":
            show_homepage(screen, pages, 0, audio_manager)
            return
        if action == "quit_game":
            return

def show_homepage(screen, pages, start, audio_manger):
    print("HOMEPAGE")
    homepage  = pages.homepage
    world_map = pages.world_map

    if start == 1:
        for title_y in range (-70, 70, 1):
            homepage.draw(pages, screen, title_y)
            pygame.display.update()
            pygame.time.delay(7)
    else:
        homepage.draw(pages, screen, 70)

    action = control.control_homepage(screen, pages, audio_manger)
    if action:
        # Nếu chưa đăng nhập, bấm Play sẽ chuyển sang Login
        if not getattr(pages, 'session', {}).get('logged_in', False):
            show_login(screen, pages, audio_manger)
        else:
            show_worldmap(screen, pages, audio_manger)

def show_worldmap(screen, pages, audio_manager):
    print("CHOOSE MAP:")
    world_map = pages.world_map
    world_map.draw(screen, [0]*15, 0)
    pygame.display.update()

    back_state, stage = control.control_worldmap(screen, pages, audio_manager)
    if back_state:
        show_homepage(screen, pages, 0, audio_manager)
    else:
        if stage == -1:
            return
        else:
            world_map.draw(screen, [0]*15, 0)
            pygame.display.update()
            rungame(stage, screen, pages, audio_manager)

def show_result(screen, pages, state, audio_manager):
    result = pages.result
    result.draw(screen, state)
    pygame.display.update()

    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    pygame.event.clear(pygame.MOUSEBUTTONUP)

    next_state = control.control_result(screen, pages, state, audio_manager)
    audio_manager.play_music("musicgame")
    return next_state

# Tính toán tọa độ pixel từ vị trí trong mê cung
def cal_coordinates(game, position_x, position_y):
    x = game.coordinate_screen_x + game.cell_rect * (position_y // 2)
    y = game.coordinate_screen_y + game.cell_rect * (position_x // 2)
    # Đẩy nhân vật xuống 3 pixel để phần đầu không bị đè lên tường
    if game.maze[position_x - 1][position_y] == "%" or game.maze[position_x - 1][position_y] == "G":
        y += 3
    return [x, y]

def update_gate(character, screen, game, backdrop, floor,
                stair, stair_position, trap, trap_position, key, key_position,
                gate_sheet, gate, wall,
                explorer,
                mummy_white, mummy_red,
                scorpion_white, scorpion_red,
                audio_manager):
    if key_position:
        for i in range(len(key_position)):
            if character.get_x() == key_position[i][0] and character.get_y() == key_position[i][1]:
                gate["isClosed"] = not gate["isClosed"]
                audio_manager.play_sfx('gate')
                graphics.gate_animation(screen, game, backdrop, floor, stair, stair_position, trap, trap_position,
                                        key, key_position, gate_sheet, gate, wall, explorer, mummy_white, mummy_red,
                                        scorpion_white, scorpion_red)
                if gate["isClosed"]:
                    gate["cellIndex"] = 0
                else:
                    gate["cellIndex"] = -1

                break
    return gate

def check_explorer_is_killed(explorer_character,
                             mummy_white_character, mummy_red_character,
                             scorpion_white_character, scorpion_red_character,
                             trap_position):
    if trap_position:
        if explorer_character.get_x() == trap_position[0] and \
                explorer_character.get_y() == trap_position[1]:
            print("YOU HAVE BEEN TRAPPED")
            return "Trap"
    if mummy_white_character:
        for i in range(len(mummy_white_character)):
            if explorer_character.get_x() == mummy_white_character[i].get_x() and \
                    explorer_character.get_y() == mummy_white_character[i].get_y():
                print("YOU HAVE BEEN ATTACKED BY MUMMY WHITE")
                return "Mummy white"
    if mummy_red_character:
        for i in range(len(mummy_red_character)):
            if explorer_character.get_x() == mummy_red_character[i].get_x() and \
                    explorer_character.get_y() == mummy_red_character[i].get_y():
                print("YOU HAVE BEEN ATTACKED BY MUMMY RED")
                return "Mummy red"
    if scorpion_white_character:
        for i in range(len(scorpion_white_character)):
            if explorer_character.get_x() == scorpion_white_character[i].get_x() and \
                    explorer_character.get_y() == scorpion_white_character[i].get_y():
                print("YOU HAVE BEEN ATTACKED BY SCORPION WHITE")
                return "Scorpion"
    if scorpion_red_character:
        for i in range(len(scorpion_red_character)):
            if explorer_character.get_x() == scorpion_red_character[i].get_x() and \
                    explorer_character.get_y() == scorpion_red_character[i].get_y():
                print("YOU HAVE BEEN ATTACKED BY SCORPION RED")
                return "Scorpion"
    return False

def update_list_same_character(list_character, list_sprite_sheet_character):
    i = 0
    while i < len(list_character):
        j = 0
        while j < len(list_character):
            if j != i and list_character[i].check_same_position(list_character[j]):
                del list_character[j]
                del list_sprite_sheet_character[j]
            else:
                j += 1
        i += 1
    return list_character, list_sprite_sheet_character

def update_list_diff_character(list_strong_character, list_week_character, list_sprite_sheet_week_character):
    for i in range(len(list_strong_character)):
        j = 0
        while j < len(list_week_character):
            if list_strong_character[i].check_same_position(list_week_character[j]):
                del list_week_character[j]
                del list_sprite_sheet_week_character[j]
            else:
                j += 1
    return list_week_character, list_sprite_sheet_week_character

def get_collision_positions(mummy_white_character, mummy_red_character,
                            scorpion_white_character, scorpion_red_character):
    pos_count = {}

    def add_list(lst):
        if lst:
            for c in lst:
                key = (c.get_x(), c.get_y())
                pos_count[key] = pos_count.get(key, 0) + 1

    add_list(mummy_white_character)
    add_list(mummy_red_character)
    add_list(scorpion_white_character)
    add_list(scorpion_red_character)

    # Trả về các ô có từ 2 quái trở lên
    return [pos for pos, cnt in pos_count.items() if cnt >= 2]

def explorer_climb_stair(screen, game, backdrop, floor,
                         stair, trap, key, gate_sheet, wall,
                         explorer, explorer_character,
                         list_mummy_white, list_mummy_red,
                         list_scorpion_white, list_scorpion_red):

    x = explorer_character.get_x()
    y = explorer_character.get_y()
    maze = game.maze

    # Xác định cầu thang nằm ở phía nào so với explorer
    if   game.stair_position[0] == 0:
        explorer["direction"] = "UP"
    elif game.stair_position[0] == len(maze) - 1:
        explorer["direction"] = "DOWN"
    elif game.stair_position[1] == 0:
        explorer["direction"] = "LEFT"
    elif game.stair_position[1] == len(maze) - 1:
        explorer["direction"] = "RIGHT"

    # Gọi lại move_animation nhưng không đổi ô logic
    # -> nhân vật chỉ trượt 1 ô về phía cầu thang, rồi mình chuyển sang màn kết quả
    explorer_character.move(x, y,
                            screen, game, backdrop, floor,
                            stair, game.stair_position,
                            trap, game.trap_position,
                            key,  game.key_position,
                            gate_sheet, game.gate, wall,
                            explorer,
                            list_mummy_white, list_mummy_red,
                            list_scorpion_white, list_scorpion_red)
    pygame.time.delay(500)

def enemy_white_move(enemy_character, explorer_character,
                     game, audio_manager):
    past_position   = []
    new_position    = []
    for i in range(len(enemy_character)):
        past_position.append(
            [enemy_character[i].get_x(),
             enemy_character[i].get_y()]
        )
        # Cho mummy di chuyển
        enemy_character[i] = enemy_character[i].white_move(game.maze, game.gate, explorer_character, audio_manager)
        # Cập nhật lại vị trí mummy
        new_position.append(
            [enemy_character[i].get_x(),
             enemy_character[i].get_y()]
        )

    return past_position, new_position, enemy_character

def enemy_red_move(enemy_character, explorer_character,
                   game, audio_manager):
    past_position   = []
    new_position    = []
    for i in range(len(enemy_character)):
        past_position.append(
            [enemy_character[i].get_x(),
             enemy_character[i].get_y()]
        )
        # Cho mummy di chuyển
        enemy_character[i] = enemy_character[i].red_move(game.maze, game.gate,
                                                         explorer_character, game.stair_position, audio_manager)
        # Cập nhật lại vị trí mummy
        new_position.append(
            [enemy_character[i].get_x(),
             enemy_character[i].get_y()]
        )

    return past_position, new_position, enemy_character

def update_enemy_position(screen, game, pages, backdrop, floor,
                          stair, trap, key, gate, wall, dust_sheet,
                          explorer, explorer_character,
                          mummy_white_character, list_mummy_white,
                          mummy_red_character, list_mummy_red,
                          scorpion_white_character, list_scorpion_white,
                          scorpion_red_character, list_scorpion_red,
                          white_fight, red_fight, stung_sheet,
                          audio_manager):

    # ===== In console vị trí quái =====
    def print_enemy_positions(prefix, enemy_list, name):
        if not enemy_list:
            return
        for i in range(len(enemy_list)):
            print(f"{name} {i + 1}")
            print(f"{prefix}: {enemy_list[i].get_x()} {enemy_list[i].get_y()}")

    # ===== xử lý thua nếu explorer bị giết =====
    def defeat_if_any():
        killer = check_explorer_is_killed(explorer_character,
                                          mummy_white_character, mummy_red_character,
                                          scorpion_white_character, scorpion_red_character,
                                          game.trap_position)
        if not killer:
            return False

        # SFX theo killer
        if killer in ("Mummy white", "Mummy red"):
            audio_manager.play_sfx('pummel', 2)
        elif killer in ("Scorpion"):
            audio_manager.play_sfx('poison')

        # Bụi tại vị trí explorer
        collision_positions = [(explorer_character.get_x(), explorer_character.get_y())]
        graphics.dust_animation(collision_positions,
                                screen, game, backdrop, floor,
                                stair, game.stair_position,
                                trap, game.trap_position,
                                key, game.key_position,
                                gate, game.gate, wall,
                                explorer,
                                list_mummy_white, list_mummy_red,
                                list_scorpion_white, list_scorpion_red,
                                dust_sheet)

        # Hiệu ứng theo killer
        if killer == "Mummy white":
            graphics.fight_animation(screen, game, backdrop, floor,
                                     stair, game.stair_position,
                                     trap, game.trap_position,
                                     key, game.key_position,
                                     gate, game.gate, wall,
                                     explorer,
                                     mummy_white_character, list_mummy_white,
                                     mummy_red_character, list_mummy_red,
                                     list_scorpion_white, list_scorpion_red,
                                     explorer_character,
                                     white_fight)
        elif killer == "Mummy red":
            graphics.fight_animation(screen, game, backdrop, floor,
                                     stair, game.stair_position,
                                     trap, game.trap_position,
                                     key, game.key_position,
                                     gate, game.gate, wall,
                                     explorer,
                                     mummy_white_character, list_mummy_white,
                                     mummy_red_character, list_mummy_red,
                                     list_scorpion_white, list_scorpion_red,
                                     explorer_character,
                                     red_fight)
        elif killer == "Scorpion":
            graphics.stung_animation(screen, game, backdrop, floor,
                                     stair, game.stair_position,
                                     trap, game.trap_position,
                                     key, game.key_position,
                                     gate, game.gate, wall,
                                     explorer,
                                     list_mummy_white, list_mummy_red,
                                     list_scorpion_white, list_scorpion_red,
                                     scorpion_white_character, scorpion_red_character,
                                     explorer_character,
                                     stung_sheet)

        # Nhảy qua màn thua
        next_state = show_result(screen, pages, state=1, audio_manager=audio_manager)
        return next_state

    # ===== xử lý bụi + xoá quái khi quái đụng nhau =====
    def handle_enemy_collisions():
        nonlocal mummy_white_character, list_mummy_white
        nonlocal mummy_red_character, list_mummy_red
        nonlocal scorpion_white_character, list_scorpion_white
        nonlocal scorpion_red_character, list_scorpion_red

        collision_positions = get_collision_positions(mummy_white_character, mummy_red_character,
                                                     scorpion_white_character, scorpion_red_character)
        if collision_positions:
            audio_manager.play_sfx('pummel', 2)
            graphics.dust_animation(collision_positions,
                                    screen, game, backdrop, floor,
                                    stair, game.stair_position,
                                    trap, game.trap_position,
                                    key, game.key_position,
                                    gate, game.gate, wall,
                                    explorer,
                                    list_mummy_white, list_mummy_red,
                                    list_scorpion_white, list_scorpion_red,
                                    dust_sheet)

            # Xoá các quái cùng loại
            mummy_white_character, list_mummy_white = update_list_same_character(
                mummy_white_character, list_mummy_white
            )
            mummy_red_character, list_mummy_red = update_list_same_character(
                mummy_red_character, list_mummy_red
            )
            scorpion_white_character, list_scorpion_white = update_list_same_character(
                scorpion_white_character, list_scorpion_white
            )
            scorpion_red_character, list_scorpion_red = update_list_same_character(
                scorpion_red_character, list_scorpion_red
            )

            # Xoá khác loại theo sức mạnh: MW > MR > SW > SR
            if mummy_red_character:
                mummy_red_character, list_mummy_red = update_list_diff_character(
                    mummy_white_character, mummy_red_character, list_mummy_red
                )
            if scorpion_white_character:
                scorpion_white_character, list_scorpion_white = update_list_diff_character(
                    mummy_white_character, scorpion_white_character, list_scorpion_white
                )
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red = update_list_diff_character(
                    mummy_white_character, scorpion_red_character, list_scorpion_red
                )
            if scorpion_white_character:
                scorpion_white_character, list_scorpion_white = update_list_diff_character(
                    mummy_red_character, scorpion_white_character, list_scorpion_white
                )
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red = update_list_diff_character(
                    mummy_red_character, scorpion_red_character, list_scorpion_red
                )
            if scorpion_red_character:
                scorpion_red_character, list_scorpion_red = update_list_diff_character(
                    scorpion_white_character, scorpion_red_character, list_scorpion_red
                )

            graphics.draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                                 stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                 gate, game.gate, wall,
                                 explorer,
                                 list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)
            pygame.display.update()

    # ===== Helper: thực hiện 1 round enemy move và trả về past/new để animate =====
    def move_round(move_scorpions=True):
        nonlocal mummy_white_character, mummy_red_character
        nonlocal scorpion_white_character, scorpion_red_character

        mw_past, mw_new, mummy_white_character = enemy_white_move(
            mummy_white_character, explorer_character, game, audio_manager
        )
        mr_past, mr_new, mummy_red_character = enemy_red_move(
            mummy_red_character, explorer_character, game, audio_manager
        )

        if move_scorpions:
            sw_past, sw_new, scorpion_white_character = enemy_white_move(
                scorpion_white_character, explorer_character, game, audio_manager
            )
            sr_past, sr_new, scorpion_red_character = enemy_red_move(
                scorpion_red_character, explorer_character, game, audio_manager
            )
            if sw_past != sw_new or sr_past != sr_new:
                audio_manager.play_sfx('scorwalk')

        else:
            # scorpion đứng yên round 2
            sw_past = sw_new_position.copy() if 'sw_new_position' in locals() else []
            sr_past = sr_new_position.copy() if 'sr_new_position' in locals() else []
            sw_new = sw_past
            sr_new = sr_past

        return mw_past, mw_new, mr_past, mr_new, sw_past, sw_new, sr_past, sr_new

    # ===================== BẮT ĐẦU LOGIC CŨ (đã gom gọn) =====================

    # Update gate
    game.gate = update_gate(explorer_character, screen, game, backdrop, floor,
                            stair, game.stair_position,
                            trap, game.trap_position,
                            key, game.key_position,
                            gate, game.gate, wall,
                            explorer,
                            list_mummy_white, list_mummy_red,
                            list_scorpion_white, list_scorpion_red,
                            audio_manager)

    # Nếu chết ngay (trap/enemy đứng sẵn) thì xử lý thua luôn
    res = defeat_if_any()
    if res is not False:
        return res

    # ------------------ ROUND 1: tất cả quái đi ------------------
    mw_past_position, mw_new_position, mr_past_position, mr_new_position, \
    sw_past_position, sw_new_position, sr_past_position, sr_new_position = move_round(move_scorpions=True)

    print_enemy_positions("First move", mummy_white_character, "MUMMY WHITE")
    print_enemy_positions("First move", mummy_red_character, "MUMMY RED")
    print_enemy_positions("First move", scorpion_white_character, "SCORPION WHITE")
    print_enemy_positions("First move", scorpion_red_character, "SCORPION RED")

    graphics.enemy_move_animation(mw_past_position, mw_new_position,
                                  mr_past_position, mr_new_position,
                                  sw_past_position, sw_new_position,
                                  sr_past_position, sr_new_position,
                                  screen, game, backdrop, floor,
                                  stair, game.stair_position,
                                  trap, game.trap_position,
                                  key, game.key_position,
                                  gate, game.gate, wall,
                                  explorer,
                                  list_mummy_white, list_mummy_red,
                                  list_scorpion_white, list_scorpion_red)

    # Check thua sau round 1
    res = defeat_if_any()
    if res is not False:
        return res

    # Bụi + xoá quái sau round 1
    handle_enemy_collisions()

    # ------------------ ROUND 2: chỉ mummy đi ------------------
    # giữ past = new của scorpion để animation không giật
    sw_past_position = sw_new_position.copy()
    sr_past_position = sr_new_position.copy()

    mw_past_position, mw_new_position, mummy_white_character = enemy_white_move(
        mummy_white_character, explorer_character, game, audio_manager
    )
    mr_past_position, mr_new_position, mummy_red_character = enemy_red_move(
        mummy_red_character, explorer_character, game, audio_manager
    )

    print_enemy_positions("Second move", mummy_white_character, "MUMMY WHITE")
    print_enemy_positions("Second move", mummy_red_character, "MUMMY RED")

    graphics.enemy_move_animation(mw_past_position, mw_new_position,
                                  mr_past_position, mr_new_position,
                                  sw_past_position, sw_new_position,
                                  sr_past_position, sr_new_position,
                                  screen, game, backdrop, floor,
                                  stair, game.stair_position,
                                  trap, game.trap_position,
                                  key, game.key_position,
                                  gate, game.gate, wall,
                                  explorer,
                                  list_mummy_white, list_mummy_red,
                                  list_scorpion_white, list_scorpion_red)

    # Check thua sau round 2
    res = defeat_if_any()
    if res is not False:
        return res

    # Bụi + xoá quái sau round 2 (nếu có)
    handle_enemy_collisions()

    # ------------------ Check WIN ------------------
    if game.maze[explorer_character.get_x() - 1][explorer_character.get_y()] == "S" or \
       game.maze[explorer_character.get_x() + 1][explorer_character.get_y()] == "S" or \
       game.maze[explorer_character.get_x()][explorer_character.get_y() - 1] == "S" or \
       game.maze[explorer_character.get_x()][explorer_character.get_y() + 1] == "S":

        print("==== YOU HAVE ESCAPED MAZE SUCCESSFULLY ====")
        print("==== YOU WIN ====")

        explorer_climb_stair(screen, game, backdrop, floor,
                             stair, trap, key, gate, wall,
                             explorer, explorer_character,
                             list_mummy_white, list_mummy_red,
                             list_scorpion_white, list_scorpion_red)

        return show_result(screen, pages, state=0, audio_manager=audio_manager)

    return True

def rungame(stage, screen, pages, audio_manager):
    pages.session["current_stage"] = stage

    # Lấy trạng thái game
    game = game_state(stage)

    # Load image path
    menu_path, map_head_path,\
    backdrop_path, floor_path, wall_path, key_path, gate_path, trap_path, stair_path, \
    explorer_path, mummy_white_path, mummy_red_path, scorpion_white_path, scorpion_red_path, \
    white_fight_path, red_fight_path, stung_path, dust_path = load_image_path(game.maze_size)

    # Load image
    load_image = True
    if load_image:
        menu                 = pygame.image.load(menu_path).convert_alpha()
        map_head             = pygame.image.load(map_head_path).convert_alpha()
        map_head             = pygame.transform.scale(map_head, (15, 14))
        backdrop             = pygame.image.load(backdrop_path).convert_alpha()
        floor                = pygame.image.load(floor_path).convert_alpha()
        wall                 = graphics.wall_spritesheet(wall_path, game.maze_size)
        key                  = graphics.key_spritesheet(key_path)
        gate                 = graphics.gate_spritesheet(gate_path)
        trap                 = graphics.trap_spritesheet(trap_path)
        stair                = graphics.stairs_spritesheet(stair_path)
        explorer_sheet       = graphics.character_spritesheet(explorer_path)
        mummy_white_sheet    = graphics.character_spritesheet(mummy_white_path)
        mummy_red_sheet      = graphics.character_spritesheet(mummy_red_path)
        scorpion_white_sheet = graphics.character_spritesheet(scorpion_white_path)
        scorpion_red_sheet   = graphics.character_spritesheet(scorpion_red_path)
        white_fight          = pygame.image.load(white_fight_path).convert_alpha()
        red_fight            = pygame.image.load(red_fight_path).convert_alpha()
        stung_sheet          = graphics.stung_spritesheet(stung_path)
        dust_sheet           = graphics.dust_spritesheet(dust_path)
    game.sheets = {
        "explorer": explorer_sheet,
        "mw": mummy_white_sheet,
        "mr": mummy_red_sheet,
        "sw": scorpion_white_sheet,
        "sr": scorpion_red_sheet,
    }
    # Objects
    # Mỗi object sẽ là một dict tương tự như struct bên C++ chứa 4 thứ
    # 1. sprite_sheet: Một hình ảnh chứa các ô frame trạng thái của object
    # 2. coordinates: Tọa độ hiện tại của object
    # 3. direction: Hướng quay của object (UP, DOWN, RIGHT, LEFT)
    # 4. cellIndex: Vị trí ô frame cần vẽ trong sprite_sheet
    initialize_objects = True
    if initialize_objects:
        def set_objects(character_sheet,
                        position_x, position_y,
                        direction):
            character = {
                "sprite_sheet": character_sheet,
                "coordinates" : cal_coordinates(game,
                                                position_x, position_y),
                "direction"   : direction,
                "cellIndex"   : 0
            }
            return character

        explorer = set_objects(explorer_sheet,
                               game.explorer_position[0], game.explorer_position[1],
                               game.explorer_direction)

        list_mummy_white = []
        for i in range(len(game.mummy_white_position)):
            mummy_white     = set_objects(mummy_white_sheet,
                                          game.mummy_white_position[i][0], game.mummy_white_position[i][1],
                                          game.mummy_white_direction[i])
            list_mummy_white.append(mummy_white)

        list_mummy_red = []
        for i in range(len(game.mummy_red_position)):
            mummy_red       = set_objects(mummy_red_sheet,
                                          game.mummy_red_position[i][0], game.mummy_red_position[i][1],
                                          game.mummy_red_direction[i])
            list_mummy_red.append(mummy_red)

        list_scorpion_white = []
        for i in range(len(game.scorpion_white_position)):
            scorpion_white  = set_objects(scorpion_white_sheet,
                                          game.scorpion_white_position[i][0], game.scorpion_white_position[i][1],
                                          game.scorpion_white_direction[i])
            list_scorpion_white.append(scorpion_white)

        list_scorpion_red = []
        for i in range(len(game.scorpion_red_position)):
            scorpion_red    = set_objects(scorpion_red_sheet,
                                          game.scorpion_red_position[i][0], game.scorpion_red_position[i][1],
                                          game.scorpion_red_direction[i])
            list_scorpion_red.append(scorpion_red)

    # Thiết lập các chỉ số cơ bản
    set_base = True
    if set_base:
        # Vẽ màn hình hiển thị ban đầu
        graphics.draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                             stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                             gate, game.gate, wall,
                             explorer,
                             list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)
        screen.blit(menu, (494, 0))
        map_head_coordinate = map_loader.read_map_head_menu(game.stage)
        screen.blit(map_head, map_head_coordinate)
        pygame.display.update()

    # Tạo các class của objects
    initialize_objects_class = True
    if initialize_objects_class:
        explorer_character       = characters.Explorer(game.explorer_position[0], game.explorer_position[1])
        mummy_white_character    = []
        if game.mummy_white_position:
            for i in range(len(game.mummy_white_position)):
                mummy_white_character.append(
                    characters.mummy_white(game.mummy_white_position[i][0], game.mummy_white_position[i][1]))
                if stage >= 10:
                    mummy_white_character[i].set_move_strategy(0)
        mummy_red_character      = []
        if game.mummy_red_position:
            for i in range(len(game.mummy_red_position)):
                mummy_red_character.append(
                    characters.mummy_red(game.mummy_red_position[i][0], game.mummy_red_position[i][1]))
                if stage >= 10:
                    mummy_red_character[i].set_move_strategy(0)
        scorpion_white_character = []
        if game.scorpion_white_position:
            for i in range(len(game.scorpion_white_position)):
                scorpion_white_character.append(
                    characters.scorpion_white(game.scorpion_white_position[i][0],
                                              game.scorpion_white_position[i][1]))
                if stage >= 10:
                    scorpion_white_character[i].set_move_strategy(0)
        scorpion_red_character   = []
        if game.scorpion_red_position:
            for i in range(len(game.scorpion_red_position)):
                scorpion_red_character.append(
                    characters.scorpion_red(game.scorpion_red_position[i][0], game.scorpion_red_position[i][1]))
                if stage >= 10:
                    scorpion_red_character[i].set_move_strategy(0)

    control.control_explorer(screen, game, pages, menu, backdrop, floor,
                             stair, trap, key, gate, wall, dust_sheet,
                             explorer, explorer_character,
                             mummy_white_character, list_mummy_white,
                             mummy_red_character, list_mummy_red,
                             scorpion_white_character, list_scorpion_white,
                             scorpion_red_character, list_scorpion_red,
                             white_fight, red_fight, stung_sheet,
                             audio_manager)


# Điều kiện này làm cho các câu lệnh bên dưới chỉ chạy từ file gốc này
# Khi import file main cho các file khác if sẽ sai -> Không chạy game
if __name__ == "__main__":
    # TẠO ĐƯỜNG DẪN
    project_path = os.path.dirname(os.path.abspath(__file__))
    map_path     = os.path.join(project_path, "assets", "map")
    agents_path  = os.path.join(map_path, "agents")
    maze_path    = os.path.join(map_path, "maze")

    pygame.init()
    pygame.display.set_caption("Mummy Maze")
    FPS = 100
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))

    # Login
    login_background_path, login_dialog_path, login_title_path, login_state_label_path, \
    login_user_field_path, login_password_field_path, login_button_login_path, login_button_register_path, \
    login_title_back_path, login_button_back_path, eye_path, lock_eye_path = load_image_login_path()

    login = graphics.login(login_background_path, login_dialog_path, login_title_path, login_state_label_path,
                           login_user_field_path, login_password_field_path, login_button_login_path, login_button_register_path,
                           login_title_back_path, login_button_back_path, eye_path, lock_eye_path)

    # Register
    register_background_path, register_dialog_path, register_title_path, register_state_label_path, \
    register_user_field_path, register_password_field_path, register_button_login_path, register_button_register_path, \
    register_title_back_path, register_button_back_path, eye_path, lock_eye_path = load_image_register_path()

    register = graphics.register(register_background_path, register_dialog_path, register_title_path, register_state_label_path,
                                 register_user_field_path, register_password_field_path, register_button_login_path, register_button_register_path,
                                 register_title_back_path, register_button_back_path, eye_path, lock_eye_path)
    # Homepage
    background_path, title_path,\
    lis_button_play_path, lis_button_sound_path, lis_button_music_path = load_image_homepage_path()

    homepage  = graphics.homepage(background_path, title_path,
                                 lis_button_play_path, lis_button_sound_path, lis_button_music_path)
    # World_map
    background_world_map_path, world_map_frame_path, \
    easy_level_path, hard_level_path, level_selection_path,\
    back_path, level_path = load_image_world_map()

    world_map = graphics.world_map(284, 382,
                                   background_world_map_path, world_map_frame_path,
                                   easy_level_path, hard_level_path, level_selection_path,
                                   back_path, level_path)

    # Result
    background_result_path, lis_title_path, lis_key_path, lis_button_undomove_path, \
    lis_button_worldmap_path, lis_button_tryagain_path, lis_button_home_path = load_image_result_path()

    result    = graphics.result(background_result_path, lis_title_path, lis_key_path, lis_button_undomove_path,
                                lis_button_worldmap_path, lis_button_tryagain_path, lis_button_home_path)

    pages = set_pages(login, register, homepage, world_map, result)

    # Audio_manager
    audio_manager = AudioManager()
    show_homepage(screen, pages, 1, audio_manager)