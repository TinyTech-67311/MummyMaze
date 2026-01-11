import pygame
import os
import sys

from path_utils import rpath

class login:
    def __init__(self, login_background_path, login_dialog_path, login_title_path, login_state_label_path,
                       login_user_field_path, login_password_field_path, login_button_login_path, login_button_register_path,
                       login_title_back_path, login_button_back_path, eye_path, lock_eye_path):
        def load_and_rescale(path, size):
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (size[0], size[1]))
            return image

        self.background      = load_and_rescale(login_background_path,      (640, 480))
        self.dialog          = load_and_rescale(login_dialog_path,          (510, 383))
        self.title           = load_and_rescale(login_title_path,           (350, 43))
        self.state_label     = load_and_rescale(login_state_label_path,     (196, 69))
        self.user_field      = load_and_rescale(login_user_field_path,      (251, 51))
        self.password_field  = load_and_rescale(login_password_field_path,  (251, 51))
        self.button_login    = load_and_rescale(login_button_login_path,    (127, 52))
        self.button_register = load_and_rescale(login_button_register_path, (127, 52))
        self.title_back      = load_and_rescale(login_title_back_path,      (200, 30))
        self.button_back     = load_and_rescale(login_button_back_path,     (50,  50))
        self.eye             = load_and_rescale(eye_path,                   (45,  45))
        self.lock_eye        = load_and_rescale(lock_eye_path,              (45,  45))

        self.dialog_rect     = self.dialog.get_rect(center=(640 // 2, 480 // 2))

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def draw_dialog(self, screen):
        screen.blit(self.dialog, self.dialog_rect)

    def draw_title(self, screen):
        screen.blit(self.title, (self.dialog_rect.x + 90, self.dialog_rect.y - 30))

    def draw_state_label(self, screen):
        screen.blit(self.state_label, (self.dialog_rect.x + 160, self.dialog_rect.y + 20))

    def draw_user_field(self, screen):
        screen.blit(self.user_field, (self.dialog_rect.x + 130, self.dialog_rect.y + 90))

    def draw_password_field(self, screen):
        screen.blit(self.password_field, (self.dialog_rect.x + 130, self.dialog_rect.y + 145))

    def draw_button_login(self, screen):
        screen.blit(self.button_login, (self.dialog_rect.x + 190, self.dialog_rect.y + 205))

    def draw_button_register(self, screen):
        screen.blit(self.button_register, (self.dialog_rect.x + 190, self.dialog_rect.y + 265))

    def draw_title_back(self, screen):
        screen.blit(self.title_back, (self.dialog_rect.x + 160, self.dialog_rect.y + 380))

    def draw_button_back(self, screen):
        screen.blit(self.button_back, (self.dialog_rect.x + 230, self.dialog_rect.y + 335))

    def draw_icon_eye(self, screen, show_password):
        if show_password:
            screen.blit(self.eye, (self.dialog_rect.x + 330, self.dialog_rect.y + 147))
        else:
            screen.blit(self.lock_eye, (self.dialog_rect.x + 330, self.dialog_rect.y + 147))

    def draw(self, screen, show_password):
        self.draw_background(screen)
        self.draw_dialog(screen)
        self.draw_title(screen)
        self.draw_state_label(screen)
        self.draw_user_field(screen)
        self.draw_password_field(screen)
        self.draw_button_login(screen)
        self.draw_button_register(screen)
        self.draw_title_back(screen)
        self.draw_button_back(screen)
        self.draw_icon_eye(screen, show_password)

class register:
    def __init__(self, register_background_path, register_dialog_path, register_title_path, register_state_label_path,
                       register_user_field_path, register_password_field_path, register_button_login_path, register_button_register_path,
                       register_title_back_path, register_button_back_path, eye_path, lock_eye_path):
        def load_and_rescale(path, size):
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (size[0], size[1]))
            return image

        self.background      = load_and_rescale(register_background_path,      (640, 480))
        self.dialog          = load_and_rescale(register_dialog_path,          (510, 383))
        self.title           = load_and_rescale(register_title_path,           (350, 43))
        self.state_label     = load_and_rescale(register_state_label_path,     (196, 69))
        self.user_field      = load_and_rescale(register_user_field_path,      (251, 51))
        self.password_field  = load_and_rescale(register_password_field_path,  (251, 51))
        self.button_login    = load_and_rescale(register_button_login_path,    (127, 52))
        self.button_register = load_and_rescale(register_button_register_path, (127, 52))
        self.title_back      = load_and_rescale(register_title_back_path,      (200, 30))
        self.button_back     = load_and_rescale(register_button_back_path,     (50,  50))
        self.eye             = load_and_rescale(eye_path,                      (45, 45))
        self.lock_eye        = load_and_rescale(lock_eye_path,                 (45, 45))

        self.dialog_rect     = self.dialog.get_rect(center=(640 // 2, 480 // 2))

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def draw_dialog(self, screen):
        screen.blit(self.dialog, self.dialog_rect)

    def draw_title(self, screen):
        screen.blit(self.title, (self.dialog_rect.x + 90, self.dialog_rect.y - 30))

    def draw_state_label(self, screen):
        screen.blit(self.state_label, (self.dialog_rect.x + 160, self.dialog_rect.y + 20))

    def draw_user_field(self, screen):
        screen.blit(self.user_field, (self.dialog_rect.x + 130, self.dialog_rect.y + 90))

    def draw_password_field(self, screen):
        screen.blit(self.password_field, (self.dialog_rect.x + 130, self.dialog_rect.y + 145))

    def draw_button_register(self, screen):
        screen.blit(self.button_register, (self.dialog_rect.x + 190, self.dialog_rect.y + 205))

    def draw_button_login(self, screen):
        screen.blit(self.button_login, (self.dialog_rect.x + 190, self.dialog_rect.y + 265))

    def draw_title_back(self, screen):
        screen.blit(self.title_back, (self.dialog_rect.x + 160, self.dialog_rect.y + 380))

    def draw_button_back(self, screen):
        screen.blit(self.button_back, (self.dialog_rect.x + 230, self.dialog_rect.y + 335))

    def draw_icon_eye(self, screen, show_password):
        if show_password:
            screen.blit(self.eye, (self.dialog_rect.x + 330, self.dialog_rect.y + 147))
        else:
            screen.blit(self.lock_eye, (self.dialog_rect.x + 330, self.dialog_rect.y + 147))

    def draw(self, screen, show_password):
        self.draw_background(screen)
        self.draw_dialog(screen)
        self.draw_title(screen)
        self.draw_state_label(screen)
        self.draw_user_field(screen)
        self.draw_password_field(screen)
        self.draw_button_register(screen)
        self.draw_button_login(screen)
        self.draw_title_back(screen)
        self.draw_button_back(screen)
        self.draw_icon_eye(screen, show_password)
        
class homepage:
    def __init__(self, background_path, title_path,
                 lis_button_play_path, lis_button_sound_path, lis_button_music_path):
        self.background = pygame.image.load(background_path).convert_alpha()
        self.background = pygame.transform.scale(self.background, (640, 480))

        self.title = pygame.image.load(title_path).convert_alpha()
        self.title = pygame.transform.scale(self.title, (300, 150))

        self.button_play_status  = 0
        self.button_play         = []
        self.button_sound_status = 0
        self.button_sound        = []
        self.button_music_status = 0
        self.button_music        = []
        for i in range(2):
            button_play  = pygame.image.load(lis_button_play_path[i]).convert_alpha()
            button_play  = pygame.transform.scale(button_play, (216, 96))
            self.button_play.append(button_play)
            button_sound = pygame.image.load(lis_button_sound_path[i]).convert_alpha()
            button_sound = pygame.transform.scale(button_sound, (90, 90))
            self.button_sound.append(button_sound)
            button_music = pygame.image.load(lis_button_music_path[i]).convert_alpha()
            button_music = pygame.transform.scale(button_music, (90, 90))
            self.button_music.append(button_music)

        self.hello_rect = None
        self.logout_rect = None
        self.logout_hover = False

    def get_button_play(self):
        return self.button_play_status

    def get_button_sound(self):
        return self.button_sound_status

    def get_button_music(self):
        return self.button_music_status

    def set_button_play(self, state):
        self.button_play_status = state

    def set_button_sound(self, state):
        self.button_sound_status = state

    def set_button_music(self, state):
        self.button_music_status = state

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def draw_title(self, screen, title_y):
        screen.blit(self.title, (170, title_y))

    def draw_button_play(self, screen):
        screen.blit(self.button_play[self.get_button_play()],   (212, 300))

    def draw_button_sound(self, screen):
        screen.blit(self.button_sound[self.get_button_sound()], (52, 300))

    def draw_button_music(self, screen):
        screen.blit(self.button_music[self.get_button_music()], (497, 300))

    def draw_hello(self, screen, text):
        font = pygame.font.Font(rpath("font", "static", "Roboto-Bold.ttf"), 24)

        # Thanh nền mờ
        bar_rect = pygame.Rect(10, 8, 360, 46)
        self._draw_glass_rect(screen, bar_rect, alpha=120, border_radius=14, border=True)

        # Avatar tròn (lấy chữ cái đầu)
        avatar_center = (bar_rect.x + 24, bar_rect.y + bar_rect.height // 2)
        pygame.draw.circle(screen, (255, 255, 255), avatar_center, 16, 2)

        initial = "?"
        if text and len(text) > 0:
            parts = text.split(",")
            if len(parts) >= 2 and parts[1].strip():
                initial = parts[1].strip()[0].upper()
            else:
                initial = text[0].upper()

        init_surf = font.render(initial, True, (255, 255, 255))
        init_rect = init_surf.get_rect(center=avatar_center)
        screen.blit(init_surf, init_rect)

        # Text
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midleft = (bar_rect.x + 52, bar_rect.y + bar_rect.height // 2)
        screen.blit(text_surface, text_rect)

        self.hello_rect = bar_rect
        return bar_rect

    def draw_log_out(self, screen):
        font = pygame.font.Font(rpath("font", "static", "Roboto-Bold.ttf"), 24)

        label = "Đăng xuất"
        text_surface = font.render(label, True, (255, 255, 255))
        text_rect = text_surface.get_rect()

        # Nút pill nằm góc phải
        padding_x = 18
        padding_y = 10
        btn_w = text_rect.width + padding_x * 2
        btn_h = text_rect.height + padding_y * 2

        btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
        btn_rect.topright = (630, 10)

        # nền mờ + hover sáng hơn
        alpha = 160 if self.logout_hover else 110
        self._draw_glass_rect(screen, btn_rect, alpha=alpha, border_radius=18, border=True)
        if self.logout_hover:
            pygame.draw.rect(screen, (255, 215, 120), btn_rect, 3, border_radius=18)

        # chữ canh giữa nút
        text_rect.center = btn_rect.center
        screen.blit(text_surface, text_rect)

        self.logout_rect = btn_rect
        return btn_rect

    def _draw_glass_rect(self, screen, rect, alpha=140, border_radius=12, border=True):
        # Tạo một surface trong suốt để vẽ nền mờ
        glass = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        glass.fill((0, 0, 0, alpha))  # nền đen trong suốt
        screen.blit(glass, (rect.x, rect.y))

        if border:
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=border_radius)

    def draw(self, pages, screen, title_y):
        mouse_pos = pygame.mouse.get_pos()

        self.draw_background(screen)
        self.draw_title(screen, title_y)
        self.draw_button_play(screen)
        self.draw_button_sound(screen)
        self.draw_button_music(screen)
        if pages.session["logged_in"]:
            # cập nhật hover dựa theo rect tạm (ta sẽ có rect sau khi vẽ, nên làm 2 bước)
            self.logout_hover = False
            self.draw_hello(screen, "Xin chào, " + pages.session["account"])
            # vẽ logout lần 1 để có rect
            logout_rect = self.draw_log_out(screen)
            self.logout_hover = logout_rect.collidepoint(mouse_pos)
            # vẽ lại để hover có hiệu lực (đơn giản, hiệu quả)
            self.draw_log_out(screen)
        else:
            self.draw_hello(screen, "Đăng nhập để chơi")


class world_map:
    def __init__(self, x, y,
                 background_world_map_path, world_map_frame_path,
                 easy_level_path, hard_level_path, level_selection_path,
                 back_path, level_path):
        self.background_world_map  = pygame.image.load(background_world_map_path).convert_alpha()
        self.background_world_map  = pygame.transform.scale(self.background_world_map, (640, 480))

        self.easy_level      = pygame.image.load(easy_level_path).convert_alpha()
        self.easy_level      = pygame.transform.scale(self.easy_level,     (150, 25))
        self.hard_level      = pygame.image.load(hard_level_path).convert_alpha()
        self.hard_level      = pygame.transform.scale(self.hard_level,     (150, 30))
        self.level_selection = pygame.image.load(level_selection_path).convert_alpha()
        self.level_selection = pygame.transform.scale(self.level_selection,(350, 150))

        self.world_map_frame = pygame.image.load(world_map_frame_path).convert_alpha()
        self.world_map_frame = pygame.transform.scale(self.world_map_frame, (670, 510))

        self.level = []
        for i in range(0, 15):
            normal_image = pygame.image.load(level_path[i][0]).convert_alpha()
            normal_image = pygame.transform.scale(normal_image, (80, 35))
            hover_image  = pygame.image.load(level_path[i][1]).convert_alpha()
            hover_image  = pygame.transform.scale(hover_image,  (80, 35))
            self.level.append([normal_image, hover_image])

        self.back = []
        for i in range(2):
            back_image   = pygame.image.load(back_path[i]).convert_alpha()
            back_image   = pygame.transform.scale(back_image, (75, 75))
            self.back.append(back_image)

    def draw_background_world_map(self, screen):
        screen.blit(self.background_world_map, (0, 0))

    def draw_word(self, screen):
        screen.blit(self.easy_level,      (125,  100))
        screen.blit(self.hard_level,      (430,  97)) #430
        screen.blit(self.level_selection, (145, -20))
        
    def draw_frame(self, screen):
        screen.blit(self.world_map_frame, (-20, -20))

    def draw_level(self, screen, state):
        for lv in range(0, 5):
            screen.blit(self.level[lv]      [state[lv]],      (100, 130 + (lv + 1)*20 + lv*35))
        for lv in range(0, 5):
            screen.blit(self.level[lv + 5]  [state[lv + 5]],  (220, 130 + (lv + 1)*20 + lv*35))
        for lv in range(0, 5):
            screen.blit(self.level[lv + 10] [state[lv + 10]], (460, 130 + (lv + 1)*20 + lv*35))

    def draw_back(self, screen, state):
        screen.blit(self.back[state], (10, 395))

    def draw(self, screen, level_state, back_state):
        self.draw_background_world_map(screen)
        self.draw_frame(screen)
        self.draw_word(screen)
        self.draw_level(screen, level_state)
        self.draw_back(screen, back_state)

class result:
    def __init__(self, background_result_path, lis_title_path, lis_key_path, lis_button_undomove_path,
                 lis_button_worldmap_path, lis_button_tryagain_path, lis_button_home_path):
        self.background_result = pygame.image.load(background_result_path).convert_alpha()
        self.background_result = pygame.transform.scale(self.background_result, (512, 384))

        self.title = []
        self.key   = []
        for i in range(2):
            title = pygame.image.load(lis_title_path[i]).convert_alpha()
            title = pygame.transform.scale(title, (300, 150))
            self.title.append(title)
            key   = pygame.image.load(lis_key_path[i]).convert_alpha()
            key   = pygame.transform.scale(key,   (205, 153))
            self.key.append(key)

        self.button_undomove_status = 0
        self.button_undomove        = []
        self.button_worldmap_status = 0
        self.button_worldmap        = []
        self.button_tryagain_status = 0
        self.button_tryagain        = []
        self.button_home_status     = 0
        self.button_home            = []
        for i in range(2):
            button_undomove = pygame.image.load(lis_button_undomove_path[i]).convert_alpha()
            button_undomove = pygame.transform.scale(button_undomove, (75, 75))
            self.button_undomove.append(button_undomove)
            button_worldmap = pygame.image.load(lis_button_worldmap_path[i]).convert_alpha()
            button_worldmap = pygame.transform.scale(button_worldmap, (75, 75))
            self.button_worldmap.append(button_worldmap)
            button_tryagain = pygame.image.load(lis_button_tryagain_path[i]).convert_alpha()
            button_tryagain = pygame.transform.scale(button_tryagain, (75, 75))
            self.button_tryagain.append(button_tryagain)
            button_home     = pygame.image.load(lis_button_home_path[i]).convert_alpha()
            button_home     = pygame.transform.scale(button_home,     (75, 75))
            self.button_home.append(button_home)

    def get_button_undomove(self):
        return self.button_undomove_status

    def get_button_worldmap(self):
        return self.button_worldmap_status

    def get_button_tryagain(self):
        return self.button_tryagain_status

    def get_button_home(self):
        return self.button_home_status

    def set_button_undomove(self, state):
        self.button_undomove_status = state

    def set_button_worldmap(self, state):
        self.button_worldmap_status = state

    def set_button_tryagain(self, state):
        self.button_tryagain_status = state

    def set_button_home(self, state):
        self.button_home_status = state

    def draw_background(self, screen):
        screen.blit(self.background_result, (64, 48))

    def draw_title(self, screen, state):
        screen.blit(self.title[state], (0, 0))

    def draw_key(self, screen, state):
        screen.blit(self.key[state], (217, 164))

    def draw_button_undomove(self, screen):
        screen.blit(self.button_undomove[self.get_button_undomove()], (167, 300))

    def draw_button_tryagain(self, screen):
        screen.blit(self.button_tryagain[self.get_button_tryagain()], (247, 300))

    def draw_button_worldmap(self, screen):
        screen.blit(self.button_worldmap[self.get_button_worldmap()], (327, 300))

    def draw_button_home(self, screen):
        screen.blit(self.button_home[self.get_button_home()], (407, 300))

    def draw(self, screen, state):
        self.draw_background(screen)
        self.draw_title(screen, state)
        self.draw_key(screen, state)
        self.draw_button_undomove(screen)
        self.draw_button_tryagain(screen)
        self.draw_button_worldmap(screen)
        self.draw_button_home(screen)

class character_spritesheet:
    def __init__(self, image_spritesheet_path):
        # Một character sẽ có 20 frame chứa trong 4 hàng 5 cột
        self.sheet = pygame.image.load(image_spritesheet_path).convert_alpha()
        self.rows = 4
        self.cols = 5
        self.totalCell = self.rows * self.cols

        # Tính toán chiều rộng, cao của mỗi ô frame phục vụ cho việc trích xuất
        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / self.cols
        h = self.cellHeight = self.rect.height / self.rows

        # Lần lượt thêm các frame vào list theo thứ tự sau:
        # 0 1 2 3 4
        # 5 .......
        # ......18 19
        self.cells = list()
        for y in range(self.rows):
            for x in range(self.cols):
                self.cells.append([x * w, y * h, w, h])

    def draw(self, surface, x, y, cellIndex, direction):
        """
        Image chứa theo logic sau:
        - Hàng thứ 1 chứa 5 frame object quay lên trên      UP
        - Hàng thứ 2 chứa 5 frame object quay bên phải      RIGHT
        - Hàng thứ 3 chứa 5 frame object quay xuống dưới    DOWN
        - Hàng thứ 4 chứa 5 frame object quay bên trái      LEFT
        """
        if direction == "UP":
            pass
        if direction == "RIGHT":
            cellIndex += 5
        if direction == "DOWN":
            cellIndex += 10
        if direction == "LEFT":
            cellIndex += 15
        # Vẽ ô thứ cellIndex trong sprite_sheet từ tọa độ (x, y) lên surface
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class wall_spritesheet:
    def __init__(self, image_spritesheet_path, maze_size):
        self.sheet = pygame.image.load(image_spritesheet_path).convert_alpha()
        self.left_wall = []
        self.right_wall = []
        self.up_wall = []
        # Mỗi bộ 4 thông số bên dưới ý nghĩa là: x, y, width, height
        # Cắt từ ảnh bắt đầu từ tọa độ (x, y) cắt ngang width và xuống height
        # Anh tính sẵn cho mình lấy sử dụng là được
        if maze_size == 6:
            self.left_wall = [0, 0, 12, 78]
            self.right_wall = [84, 0, 12, 78]
            self.up_wall = [12, 0, 72, 18]
            self.up_wall_no_shadow = [12, 0, 66, 18]
        elif maze_size == 8:
            self.left_wall = [0, 0, 12, 63]
            self.right_wall = [69, 0, 12, 63]
            self.up_wall = [12, 0, 57, 18]
            self.up_wall_no_shadow = [12, 0, 51, 18]
        elif maze_size == 10:
            self.left_wall = [0, 0, 8, 48]
            self.right_wall = [52, 0, 8, 48]
            self.up_wall = [8, 0, 44, 12]
            self.up_wall_no_shadow = [8, 0, 38, 12]

    # Lệnh surface.blit(source, (x, y), area) có nghĩa:
    # Vẽ lên bề mặt surface ở tọa độ (x, y) một area của source ảnh
    def draw_left_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.left_wall)

    def draw_right_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.right_wall)

    def draw_up_wall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.up_wall)

    def draw_up_wall_no_shadow(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.up_wall_no_shadow)

class key_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path).convert_alpha()
        self.rect = self.sheet.get_rect()
        self.cell = [0, 0, self.rect.width, self.rect.height]

    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.cell)

class gate_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path).convert_alpha()
        self.rect = self.sheet.get_rect()
        # Số frame trong sheet gate là 8 trên cùng một hàng
        number_gate_sheet = 8
        # Tính toán chiều rộng chiều cao của frame để phục vụ cho việc trích xuất
        w = self.rect.width / number_gate_sheet
        h = self.rect.height
        self.cells = []
        for x in range(number_gate_sheet):
            self.cells.append([x * w, 0, w, h])

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class trap_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path).convert_alpha()
        self.rect = self.sheet.get_rect()
        self.cell = [0, 0, self.rect.width, self.rect.height]

    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.cell)

class stairs_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path).convert_alpha()
        self.rect = self.sheet.get_rect()

        # Tính toán chiều rộng, cao của mỗi ô frame phục vụ cho việc trích xuất
        self.cell_w = self.rect.width // 4
        self.cell_h = self.rect.height

        # Lần lượt thêm các frame vào list theo thứ tự sau: 0 1 2 3
        self.stairs = []
        for x in range(4):
            self.stairs.append(
                [x * self.cell_w, 0, self.cell_w, self.cell_h]
            )

    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.stairs[cellIndex])

class stung_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path).convert_alpha()
        bg_color   = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(bg_color)

        self.rect   = self.sheet.get_rect()
        self.cell_h = self.rect.height
        self.cols   = self.rect.width // self.cell_h
        self.total_frames = self.cols

        self.cells = []
        for i in range(self.cols):
            self.cells.append([i * self.cell_h, 0, self.cell_h, self.cell_h])

    def draw(self, surface, x, y, cellIndex):
        if self.total_frames == 0:
            return
        cellIndex = max(0, min(cellIndex, self.total_frames - 1))
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class dust_spritesheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path).convert_alpha()
        bg_color = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(bg_color)
        self.rect  = self.sheet.get_rect()

        # Giả sử mỗi frame là hình vuông, nằm trên 1 hàng
        self.cell_h = self.rect.height
        self.cols   = self.rect.width // self.cell_h
        self.total_frames = self.cols

        self.cells = []
        for i in range(self.cols):
            self.cells.append(
                [i * self.cell_h, 0, self.cell_h, self.cell_h]
            )

    def draw(self, surface, x, y, cellIndex):
        cellIndex = max(0, min(cellIndex, self.total_frames - 1))
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

def draw_screen(screen, input_maze, backdrop, floor, maze_size, cell_rect,
                stair, stair_position, trap, trap_position, key, key_position,
                gate_sheet, gate, wall,
                explorer,
                mummy_white, mummy_red, scorpion_white, scorpion_red):
    # Tọa độ bắt đầu của mê cung đồng bộ với trong file main
    coordinate_X = 67
    coordinate_Y = 80

    # Vẽ Backdrop và Floor
    draw_backdrop_and_floor = True
    if draw_backdrop_and_floor:
        # Phải vẽ backdrop trước rồi tới floor để floor đè lên phần đen trong backdrop
        screen.blit(backdrop, (0, 0))
        screen.blit(floor, (coordinate_X, coordinate_Y))

    # Vẽ Stair
    draw_stair = True
    if draw_stair:
        # Tính xem Stair nằm trong ô nào trong mê cung
        stair_px = stair_position[1] // 2
        stair_py = stair_position[0] // 2
        # Từ đó biến thành tọa độ pixel
        stair_x = coordinate_X + cell_rect * (stair_px)
        stair_y = coordinate_Y + cell_rect * (stair_py)
        # stair_index = (0, 1, 2, 3) lần lượt ứng với trạng thái (UP, RIGHT, DOWN, LEFT)
        # Các trường hợp bên dưới tưởng tượng để xét nó nằm ở cạnh nào trong mê cung hình vuông

        # STAIR IS UP
        stair_index = 0
        # STAIR IS RIGHT
        if stair_px == maze_size:
            stair_index = 1
        # STAIR IS DOWN
        elif stair_py == maze_size:
            stair_index = 2
        # STAIR IS LEFT
        elif stair_px == 0:
            stair_index = 3

        # Nếu là UP chỉnh sửa một chút
        # Dịch cầu thang lên trên stair.cell_h pixel
        # Nếu không thì cầu thang bị đè lên mê cung
        if (stair_index == 0):
            stair_y = coordinate_Y - stair.cell_h
        # Nếu là LEFT cũng sửa một chút
        # Dịch cầu thang sang trái stair.cell_w
        if (stair_index == 3):
            stair_x = coordinate_X - stair.cell_w

        stair.draw(screen, stair_x, stair_y, stair_index)

    # Vẽ Trap
    if trap_position:
        trap_x = coordinate_X + cell_rect * (trap_position[1] // 2)
        trap_y = coordinate_Y + cell_rect * (trap_position[0] // 2)
        trap.draw(screen, trap_x, trap_y)

    # Vẽ Key
    if key_position:
        for i in range(len(key_position)):
            key_x = coordinate_X + cell_rect * (key_position[i][1] // 2)
            key_y = coordinate_Y + cell_rect * (key_position[i][0] // 2)
            key.draw(screen, key_x, key_y)

    # Vẽ Gate
    if gate["gate_position"]:
        gate_x = coordinate_X + cell_rect * (gate["gate_position"][1] // 2)
        gate_y = coordinate_Y + cell_rect * (gate["gate_position"][0] // 2)
        if maze_size == 6 or maze_size == 8:
            gate_x -= 6
            gate_y -= 12
        elif maze_size == 10:
            gate_x -= 3
            gate_y -= 9
        gate_sheet.draw(screen, gate_x, gate_y, gate["cellIndex"])

    # Vẽ Explorer
    if explorer["coordinates"]:
        # Các tham số truyền vào đọc hàm draw trong character_spritesheet để hiểu
        explorer["sprite_sheet"].draw(screen,
                                      explorer["coordinates"][0],
                                      explorer["coordinates"][1],
                                      explorer["cellIndex"],
                                      explorer["direction"])

    # Vẽ Mummy White
    if mummy_white:
        for i in range(len(mummy_white)):
            mummy_white[i]["sprite_sheet"].draw(screen,
                                                mummy_white[i]["coordinates"][0],
                                                mummy_white[i]["coordinates"][1],
                                                mummy_white[i]["cellIndex"],
                                                mummy_white[i]["direction"])

    # Vẽ Mummy Red
    if mummy_red:
        for i in range(len(mummy_red)):
            mummy_red[i]["sprite_sheet"].draw(screen,
                                              mummy_red[i]["coordinates"][0],
                                              mummy_red[i]["coordinates"][1],
                                              mummy_red[i]["cellIndex"],
                                              mummy_red[i]["direction"])

    # Vẽ Scorpion White
    if scorpion_white:
        for i in range(len(scorpion_white)):
            scorpion_white[i]["sprite_sheet"].draw(screen,
                                                   scorpion_white[i]["coordinates"][0],
                                                   scorpion_white[i]["coordinates"][1],
                                                   scorpion_white[i]["cellIndex"],
                                                   scorpion_white[i]["direction"])

    # Vẽ Scorpion Red
    if scorpion_red:
        for i in range(len(scorpion_red)):
            scorpion_red[i]["sprite_sheet"].draw(screen,
                                                 scorpion_red[i]["coordinates"][0],
                                                 scorpion_red[i]["coordinates"][1],
                                                 scorpion_red[i]["cellIndex"],
                                                 scorpion_red[i]["direction"])

    # Vẽ Wall
    draw_wall = True
    if draw_wall:
        # Horizontal Wall (Tường ngang)
        # Hàng chẵn chứa tường ngang
        # Tường nằm giữa 2 ô trống ngang nên ở cột lẻ
        for i in range(2, len(input_maze) - 1, 2):
            for j in range(1, len(input_maze[i]), 2):
                if input_maze[i][j] == "%":
                    # Tính tọa độ tương tự hàm cal_coordinate bên main
                    wall_x = coordinate_X + cell_rect * (j // 2)
                    wall_y = coordinate_Y + cell_rect * (i // 2)
                    # Trừ lại cho nó không bị lệch
                    # Anh test sẵn mình sử dụng thôi
                    if maze_size == 6 or maze_size == 8:
                        wall_x -= 6
                        wall_y -= 12
                    if maze_size == 10:
                        wall_x -= 3
                        wall_y -= 9
                    wall.draw_up_wall(screen, wall_x, wall_y)
        # Vertical Wall (Tường dọc)
        # Cột chẵn chứa tường dọc
        # Tường nằm giữa 2 ô trống dọc nên ở hàng lẻ
        for j in range(2, len(input_maze) - 1, 2):
            for i in range(1, len(input_maze[j]), 2):
                if input_maze[i][j] == "%":
                    wall_x = coordinate_X + cell_rect * (j // 2)
                    wall_y = coordinate_Y + cell_rect * (i // 2)
                    if maze_size == 6 or maze_size == 8:
                        wall_x -= 6
                        wall_y -= 12
                    elif maze_size == 10:
                        wall_x -= 3
                        wall_y -= 9
                    # Trường hợp mà tường tạo góc vuông thì sài right_wall bởi nó ngắn nó mới khớp
                    # Đây chính là trường hợp tường hình chữ L
                    if (input_maze[i + 1][j + 1] == "%"):
                        wall.draw_right_wall(screen, wall_x, wall_y)
                        # Redraw ở đây là vẽ lại phần ngang của chữ L cho nó không thừa
                        redraw_x = coordinate_X + cell_rect * ((j + 1) // 2)
                        redraw_y = coordinate_Y + cell_rect * ((i + 1) // 2)
                        if maze_size == 6 or maze_size == 8:
                            redraw_x -= 6
                            redraw_y -= 12
                        if maze_size == 10:
                            redraw_x -= 3
                            redraw_y -= 9
                        # Vẽ lại tường ngang không bóng đổ
                        if (i + 1 < maze_size * 2 and j + 1 < maze_size * 2):
                            wall.draw_up_wall_no_shadow(screen, redraw_x, redraw_y)
                    else:
                        wall.draw_left_wall(screen, wall_x, wall_y)

def gate_animation(screen, game, backdrop, floor,
                   stair, stair_position, trap, trap_position, key, key_position,
                   gate_sheet, gate, wall,
                   explorer,
                   mummy_white, mummy_red,
                   scorpion_white, scorpion_red):
    for i in range(8):
        if gate["isClosed"]:
            gate["cellIndex"] = -(i + 1)
        else:
            gate["cellIndex"] = i
        draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                    stair, stair_position, trap, trap_position, key, key_position,
                    gate_sheet, gate, wall,
                    explorer,
                    mummy_white, mummy_red,
                    scorpion_white, scorpion_red)
        pygame.time.delay(60)
        pygame.display.update()

def stung_animation(screen, game, backdrop, floor,
                    stair, stair_position, trap, trap_position, key, key_position,
                    gate_sheet, gate, wall,
                    explorer,
                    mummy_white, mummy_red,
                    scorpion_white, scorpion_red,
                    scorpion_white_character, scorpion_red_character,
                    explorer_character,
                    stung_sheet):
    x = explorer_character.get_x()
    y = explorer_character.get_y()

    # Chuyển sang pixel
    px = game.coordinate_screen_x + game.cell_rect * (y // 2)
    py = game.coordinate_screen_y + game.cell_rect * (x // 2)

    # Vẽ lại nền + tất cả đối tượng (trừ explorer và killer)
    fake_explorer = {
        "sprite_sheet": explorer["sprite_sheet"],
        "coordinates": [-9999, -9999],  # đẩy explorer ra ngoài screen
        "direction": "DOWN",
        "cellIndex": 0
    }
    new_scorpion_white = []
    new_scorpion_red   = []
    if scorpion_white_character:
        for i in range(len(scorpion_white_character)):
            if scorpion_white_character[i].get_x() != x or scorpion_white_character[i].get_y() != y:
                new_scorpion_white.append(scorpion_white[i])
    if scorpion_red_character:
        for i in range(len(scorpion_red_character)):
            if scorpion_red_character[i].get_x()   != x or scorpion_red_character[i].get_y()   != y:
                new_scorpion_red.append(scorpion_red[i])

    # Nếu phía trên là tường / cổng thì dịch xuống 3 pixel như explorer
    if x > 0 and (game.maze[x - 1][y] == "%" or game.maze[x - 1][y] == "G"):
        py += 3

    for frame in range(stung_sheet.total_frames):
        # Vẽ lại màn hình bình thường (không bụi nữa)
        draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                    stair, stair_position, trap, trap_position, key, key_position,
                    gate_sheet, gate, wall,
                    fake_explorer,
                    mummy_white, mummy_red,
                    new_scorpion_white, new_scorpion_red)

        # Vẽ explorer trúng độc
        stung_sheet.draw(screen, px, py, frame)

        pygame.display.update()
        pygame.time.delay(80)

def fight_animation(screen, game, backdrop, floor,
                    stair, stair_position, trap, trap_position, key, key_position,
                    gate_sheet, gate, wall,
                    explorer,
                    mummy_white_character, mummy_white,
                    mummy_red_character, mummy_red,
                    scorpion_white, scorpion_red,
                    explorer_character,
                    fight_img):
    # Tính vị trí explorer trong pixel
    x = explorer_character.get_x()
    y = explorer_character.get_y()

    px = game.coordinate_screen_x + game.cell_rect * (y // 2)
    py = game.coordinate_screen_y + game.cell_rect * (x // 2)

    # Giống explorer animation: dịch xuống 3px nếu phía trên là tường/gate
    if x > 0 and (game.maze[x - 1][y] == "%" or game.maze[x - 1][y] == "G"):
        py += 3

    # Vẽ lại nền + tất cả đối tượng (trừ explorer và killer)
    fake_explorer = {
        "sprite_sheet": explorer["sprite_sheet"],
        "coordinates": [-9999, -9999],  # đẩy explorer ra ngoài screen
        "direction": "DOWN",
        "cellIndex": 0
    }
    new_mummy_white = []
    new_mummy_red   = []
    if mummy_white_character:
        for i in range(len(mummy_white_character)):
            if mummy_white_character[i].get_x() != x or mummy_white_character[i].get_y() != y:
                new_mummy_white.append(mummy_white[i])
    if mummy_red_character:
        for i in range(len(mummy_red_character)):
            if mummy_red_character[i].get_x()   != x or mummy_red_character[i].get_y()   != y:
                new_mummy_red.append(mummy_red[i])
    draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                stair, stair_position, trap, trap_position, key, key_position,
                gate_sheet, gate, wall,
                fake_explorer,
                new_mummy_white, new_mummy_red,
                scorpion_white, scorpion_red)

    # Canh giữa trong ô
    rect = fight_img.get_rect()

    px += (game.cell_rect - rect.width) // 2
    py += game.cell_rect - rect.height

    screen.blit(fight_img, (px, py))
    pygame.display.update()

    pygame.time.delay(800)

def dust_animation(collision_positions,
                   screen, game, backdrop, floor,
                   stair, stair_position, trap, trap_position, key, key_position,
                   gate_sheet, gate, wall,
                   explorer,
                   mummy_white, mummy_red,
                   scorpion_white, scorpion_red,
                   dust_sheet):
    if not collision_positions:
        return

    for frame in range(dust_sheet.total_frames):
        # Vẽ lại màn hình hiện tại
        draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                    stair, stair_position, trap, trap_position, key, key_position,
                    gate_sheet, gate, wall,
                    explorer,
                    mummy_white, mummy_red,
                    scorpion_white, scorpion_red)

        # Vẽ bụi tại từng vị trí va chạm
        for (cx, cy) in collision_positions:
            dust_x = game.coordinate_screen_x + game.cell_rect * (cy // 2)
            dust_y = game.coordinate_screen_y + game.cell_rect * (cx // 2)
            dust_sheet.draw(screen, dust_x, dust_y, frame)

        pygame.time.delay(30)
        pygame.display.update()

def determine_moving_direction(past_position, new_position):
    if past_position[0] == new_position[0] + 2:  # Move Up
        return "UP"
    if past_position[0] == new_position[0] - 2:  # Move Down
        return "DOWN"
    if past_position[1] == new_position[1] + 2:  # Move Left
        return "LEFT"
    if past_position[1] == new_position[1] - 2:  # Move Right
        return "RIGHT"

# Cập nhật bước đi nhỏ trong 1 bước của từng Enemy
def enemy_move_animation(mw_past_position, mw_new_position,
                         mr_past_position, mr_new_position,
                         sw_past_position, sw_new_position,
                         sr_past_position, sr_new_position,
                         screen, game, backdrop, floor,
                         stair, stair_position, trap, trap_position, key, key_position,
                         gate_sheet, gate, wall,
                         explorer,
                         mummy_white, mummy_red,
                         scorpion_white, scorpion_red):
    def determine_coor_and_direction(past_position, new_position,
                                     check_movement, enemy):
        start_coordinate = []
        for i in range(len(past_position)):
            start_x = game.coordinate_screen_x + game.cell_rect * (past_position[i][1] // 2)
            start_y = game.coordinate_screen_y + game.cell_rect * (past_position[i][0] // 2)
            if game.maze[new_position[i][0] - 1][new_position[i][1]] == "%" or \
                    game.maze[new_position[i][0] - 1][new_position[i][1]] == "G":
                start_y += 3
            start_coordinate.append([start_x, start_y])
            if past_position[i][0] != new_position[i][0] or \
                    past_position[i][1] != new_position[i][1]:
                check_movement[i] = True
            if check_movement[i]:
                enemy[i]["direction"] = determine_moving_direction(past_position[i], new_position[i])
        for i in range(len(enemy)):
            enemy[i]["coordinates"] = start_coordinate[i]
        return check_movement, enemy

    mw_check_movement = [False] * len(mw_past_position)
    mr_check_movement = [False] * len(mr_past_position)
    sw_check_movement = [False] * len(sw_past_position)
    sr_check_movement = [False] * len(sr_past_position)

    # Mummy white
    mw_check_movement, mummy_white = determine_coor_and_direction(mw_past_position, mw_new_position,
                                                                  mw_check_movement, mummy_white)
    # Mummy red
    mr_check_movement, mummy_red = determine_coor_and_direction(mr_past_position, mr_new_position,
                                                                mr_check_movement, mummy_red)
    # Scorpion white
    sw_check_movement, scorpion_white = determine_coor_and_direction(sw_past_position, sw_new_position,
                                                                     sw_check_movement, scorpion_white)
    # Scorpion Red
    sr_check_movement, scorpion_red = determine_coor_and_direction(sr_past_position, sr_new_position,
                                                                   sr_check_movement, scorpion_red)

    step_stride = game.cell_rect // 5

    for i in range(6):
        for j in range(len(mummy_white)):
            if i < 5:
                if mummy_white[j]["direction"] == "UP" and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][1] -= step_stride
                if mummy_white[j]["direction"] == "DOWN" and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][1] += step_stride
                if mummy_white[j]["direction"] == "LEFT" and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][0] -= step_stride
                if mummy_white[j]["direction"] == "RIGHT" and mw_check_movement[j]:
                    mummy_white[j]["coordinates"][0] += step_stride
            if mw_check_movement[j]:
                mummy_white[j]["cellIndex"] = i % 5

        for j in range(len(mummy_red)):
            if i < 5:
                if mummy_red[j]["direction"] == "UP" and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][1] -= step_stride
                if mummy_red[j]["direction"] == "DOWN" and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][1] += step_stride
                if mummy_red[j]["direction"] == "LEFT" and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][0] -= step_stride
                if mummy_red[j]["direction"] == "RIGHT" and mr_check_movement[j]:
                    mummy_red[j]["coordinates"][0] += step_stride
            if mr_check_movement[j]:
                mummy_red[j]["cellIndex"] = i % 5

        for j in range(len(scorpion_white)):
            if i < 5:
                if scorpion_white[j]["direction"] == "UP" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][1] -= step_stride
                if scorpion_white[j]["direction"] == "DOWN" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][1] += step_stride
                if scorpion_white[j]["direction"] == "LEFT" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][0] -= step_stride
                if scorpion_white[j]["direction"] == "RIGHT" and sw_check_movement[j]:
                    scorpion_white[j]["coordinates"][0] += step_stride
            if sw_check_movement[j]:
                scorpion_white[j]["cellIndex"] = i % 5

        for j in range(len(scorpion_red)):
            if i < 5:
                if scorpion_red[j]["direction"] == "UP" and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][1] -= step_stride
                if scorpion_red[j]["direction"] == "DOWN" and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][1] += step_stride
                if scorpion_red[j]["direction"] == "LEFT" and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][0] -= step_stride
                if scorpion_red[j]["direction"] == "RIGHT" and sr_check_movement[j]:
                    scorpion_red[j]["coordinates"][0] += step_stride
            if sr_check_movement[j]:
                scorpion_red[j]["cellIndex"] = i % 5

        draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                    stair, stair_position, trap, trap_position, key, key_position,
                    gate_sheet, gate, wall,
                    explorer,
                    mummy_white, mummy_red,
                    scorpion_white, scorpion_red)
        pygame.time.delay(60)
        pygame.display.update()