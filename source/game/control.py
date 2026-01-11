import pygame
import os
from collections import deque
from ui import graphics
from game import map_loader
from game import characters
from main import rungame, show_worldmap, show_homepage, update_enemy_position, cal_coordinates
from path_utils import exe_dir
import json

USERS_FILE = os.path.join(exe_dir(), "users.json")
PROGRESS_FILE = os.path.join(exe_dir(), "progress.json")

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_progress(progress):
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=4)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def draw_toast(screen, text, center_pos, font, text_color=(255, 255, 255),
               bg_alpha=160, pad_x=18, pad_y=10, radius=14, border=True):
    if not text:
        return

    text_surf = font.render(text, True, text_color)
    w = text_surf.get_width() + pad_x * 2
    h = text_surf.get_height() + pad_y * 2

    rect = pygame.Rect(0, 0, w, h)
    rect.center = center_pos

    # nền mờ
    glass = pygame.Surface((w, h), pygame.SRCALPHA)
    glass.fill((0, 0, 0, bg_alpha))
    screen.blit(glass, rect.topleft)

    # viền trắng nhẹ
    if border:
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=radius)

    # vẽ chữ
    screen.blit(text_surf, text_surf.get_rect(center=rect.center))

def control_login(screen, pages, audio_manager):
    login   = pages.get_login()
    running = True

    d_x = login.dialog_rect.x
    d_y = login.dialog_rect.y
    username_rect   = pygame.Rect(d_x + 130, d_y + 90,  251, 51)
    password_rect   = pygame.Rect(d_x + 130, d_y + 145, 251, 51)
    toggle_pw_rect  = pygame.Rect(d_x + 330, d_y + 147, 45,  45)
    button_login    = pygame.Rect(d_x + 190, d_y + 205, 127, 52)
    button_register = pygame.Rect(d_x + 190, d_y + 265, 127, 52)
    button_back     = pygame.Rect(d_x + 230, d_y + 335, 50,  50)
    show_password   = False

    username_text   = ""
    password_text   = ""
    active_username = False
    active_password = False
    max_len_username = 18
    max_len_password = 24
    font = pygame.font.Font("font/static/Roboto-Bold.ttf", 28)

    status_text = ""
    status_color = (255, 90, 90)
    status_until = 0
    status_font = pygame.font.Font("font/static/Roboto-Bold.ttf", 20)
    toast_center = (login.dialog_rect.centerx, d_y + 190)

    pygame.key.start_text_input()
    clock = pygame.time.Clock()

    while running:
        login.draw(screen, show_password)

        if username_text == "" and not active_username:
            text_surface = font.render("Username", True, (255, 255, 255))
        else:
            text_surface = font.render(username_text,   True, (255, 255, 255))

        screen.blit(text_surface, (username_rect.x + 12, username_rect.y + 10))

        if password_text == "" and not active_password:
            text_surface = font.render("Password", True, (255, 255, 255))
        else:
            visible = password_text if show_password else ("*" * len(password_text))
            text_surface = font.render(visible, True, (255, 255, 255))

        screen.blit(text_surface, (password_rect.x + 12, password_rect.y + 10))

        now = pygame.time.get_ticks()
        if status_text and now < status_until:
            draw_toast(
                screen,
                status_text,
                toast_center,
                status_font,
                text_color=status_color,
                bg_alpha=160
            )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos

                if username_rect.collidepoint(click):
                    audio_manager.play_sfx('click')
                    active_username = True
                    active_password = False
                elif password_rect.collidepoint(click):
                    audio_manager.play_sfx('click')
                    active_password = True
                    active_username = False

                if button_back.collidepoint(click):
                    audio_manager.play_sfx('click')
                    pygame.key.stop_text_input()
                    return "back_home"

                if button_register.collidepoint(click):
                    audio_manager.play_sfx('click')
                    pygame.key.stop_text_input()
                    return "to_register"

                if toggle_pw_rect.collidepoint(click):
                    audio_manager.play_sfx('click')
                    show_password = not show_password

                if button_login.collidepoint(click):
                    audio_manager.play_sfx('click')
                    users = load_users()

                    if username_text in users and users[username_text] == password_text:
                        pages.session["logged_in"] = True
                        pages.session["account"] = username_text
                        status_text = "Đăng nhập thành công!"
                        status_color = (120, 255, 120)
                        status_until = pygame.time.get_ticks() + 600
                        print(status_text)
                        print("Xin chào", username_text, "!!!")
                        return "login_success"
                    else:
                        status_text = "Tài khoản hoặc mật khẩu chưa chính xác"
                        status_color = (255, 90, 90)
                        status_until = pygame.time.get_ticks() + 1800
                        print(status_text)

            if event.type == pygame.KEYDOWN:
                if active_username:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    elif event.unicode.isalnum() or event.unicode in "._":
                        if len(username_text) < max_len_username:
                            username_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        active_username = False
                        active_password = True

                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    elif event.unicode.isalnum() or event.unicode in "._":
                        if len(password_text) < max_len_password:
                            password_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        users = load_users()

                        if username_text in users and users[username_text] == password_text:
                            pages.session["logged_in"] = True
                            pages.session["account"] = username_text
                            print("===== Đăng nhập thành công =====")
                            print("Xin chào", username_text, "!!!")
                            return "login_success"
                        else:
                            status_text = "Tài khoản hoặc mật khẩu chưa chính xác"
                            status_color = (255, 90, 90)
                            status_until = pygame.time.get_ticks() + 1800
                            print(status_text)
        clock.tick(60)
    pygame.key.stop_text_input()
    return "quit_game"

def control_register(screen, pages, audio_manager):
    register = pages.get_register()
    running  = True

    d_x = register.dialog_rect.x
    d_y = register.dialog_rect.y
    username_rect   = pygame.Rect(d_x + 130, d_y + 90,  251, 51)
    password_rect   = pygame.Rect(d_x + 130, d_y + 145, 251, 51)
    toggle_pw_rect  = pygame.Rect(d_x + 330, d_y + 147, 45,  45)
    button_login    = pygame.Rect(d_x + 190, d_y + 265, 127, 52)
    button_register = pygame.Rect(d_x + 190, d_y + 205, 127, 52)
    button_back     = pygame.Rect(d_x + 230, d_y + 335, 50,  50)
    show_password   = False

    username_text = ""
    password_text = ""
    active_username = False
    active_password = False
    min_len_username = 5
    min_len_password = 8
    max_len_username = 18
    max_len_password = 24
    font = pygame.font.Font("font/static/Roboto-Bold.ttf", 28)

    status_text = ""
    status_color = (255, 90, 90)
    status_until = 0
    status_font = pygame.font.Font("font/static/Roboto-Bold.ttf", 20)
    toast_center = (register.dialog_rect.centerx, d_y + 190)

    pygame.key.start_text_input()
    clock = pygame.time.Clock()

    while running:
        register.draw(screen, show_password)

        if username_text == "" and not active_username:
            text_surface = font.render("Username", True, (255, 255, 255))
        else:
            text_surface = font.render(username_text,   True, (255, 255, 255))

        screen.blit(text_surface, (username_rect.x + 12, username_rect.y + 10))

        if password_text == "" and not active_password:
            text_surface = font.render("Password", True, (255, 255, 255))
        else:
            visible = password_text if show_password else ("*" * len(password_text))
            text_surface = font.render(visible, True, (255, 255, 255))

        screen.blit(text_surface, (password_rect.x + 12, password_rect.y + 10))
        now = pygame.time.get_ticks()
        if status_text and now < status_until:
            draw_toast(
                screen,
                status_text,
                toast_center,
                status_font,
                text_color=status_color,
                bg_alpha=160
            )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = event.pos

                if username_rect.collidepoint(click):
                    audio_manager.play_sfx('click')
                    active_username = True
                    active_password = False
                elif password_rect.collidepoint(click):
                    audio_manager.play_sfx('click')
                    active_password = True
                    active_username = False

                if button_back.collidepoint(click):
                    audio_manager.play_sfx('click')
                    pygame.key.stop_text_input()
                    return "back_home"

                if button_login.collidepoint(click):
                    audio_manager.play_sfx('click')
                    pygame.key.stop_text_input()
                    return "to_login"

                if toggle_pw_rect.collidepoint(click):
                    audio_manager.play_sfx('click')
                    show_password = not show_password

                if button_register.collidepoint(click):
                    audio_manager.play_sfx('click')
                    users = load_users()

                    if username_text in users:
                        status_text = "Username đã tồn tại"
                        status_color = (255, 90, 90)
                        status_until = pygame.time.get_ticks() + 1800
                        print(status_text)
                    elif len(username_text) < min_len_username:
                        status_text = "Username quá ngắn"
                        status_color = (255, 90, 90)
                        status_until = pygame.time.get_ticks() + 1800
                        print(status_text)
                    elif len(password_text) < min_len_password:
                        status_text = "Password quá ngắn"
                        status_color = (255, 90, 90)
                        status_until = pygame.time.get_ticks() + 1800
                        print(status_text)
                    else:
                        users[username_text] = password_text
                        save_users(users)

                        status_text = "Tạo tài khoản thành công"
                        status_color = (255, 90, 90)
                        status_until = pygame.time.get_ticks() + 1800
                        print(status_text)
                        pygame.key.stop_text_input()
                        return "register_success"

            if event.type == pygame.KEYDOWN:
                if active_username:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    elif event.unicode.isalnum() or event.unicode in "._":
                        if len(username_text) < max_len_username:
                            username_text += event.unicode
                    if event.key == pygame.K_RETURN:
                        active_username = False
                        active_password = True

                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    elif event.unicode.isalnum() or event.unicode in "._":
                        if len(password_text) < max_len_password:
                            password_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        users = load_users()

                        if username_text in users:
                            status_text = "Username đã tồn tại"
                            status_color = (255, 90, 90)
                            status_until = pygame.time.get_ticks() + 1800
                            print(status_text)
                        elif len(username_text) < min_len_username:
                            status_text = "Username quá ngắn"
                            status_color = (255, 90, 90)
                            status_until = pygame.time.get_ticks() + 1800
                            print(status_text)
                        elif len(password_text) < min_len_password:
                            status_text = "Password quá ngắn"
                            status_color = (255, 90, 90)
                            status_until = pygame.time.get_ticks() + 1800
                            print(status_text)
                        else:
                            users[username_text] = password_text
                            save_users(users)

                            status_text = "Tạo tài khoản thành công"
                            status_color = (255, 90, 90)
                            status_until = pygame.time.get_ticks() + 1800
                            print(status_text)
                            pygame.key.stop_text_input()
                            return "register_success"
        clock.tick(60)
    pygame.key.stop_text_input()
    return "quit_game"

def control_homepage(screen, pages, audio_manager):
    button_play  = pygame.Rect(212, 300, 216, 90)
    button_sound = pygame.Rect(52,  300, 90,  90)
    button_music = pygame.Rect(497, 300, 90,  90)

    homepage     = pages.homepage
    running      = True
    to_world_map = False

    button_play_state  = homepage.get_button_play()
    button_sound_state = homepage.get_button_sound()
    button_music_state = homepage.get_button_music()

    lock_hover_sound   = False
    lock_hover_music   = False

    clock = pygame.time.Clock()

    while running:
        # Cập nhật vị trí trỏ chuột liên tục
        mouse_pos = pygame.mouse.get_pos()

        # Xử lý Hover
        if button_play.collidepoint(mouse_pos):
            homepage.set_button_play(not button_play_state)
        else:
            homepage.set_button_play(button_play_state)

        if button_music.collidepoint(mouse_pos):
            if not lock_hover_music:
                homepage.set_button_music(not button_music_state)
        else:
            lock_hover_music = False
            homepage.set_button_music(button_music_state)

        if button_sound.collidepoint(mouse_pos):
            if not lock_hover_sound:
                homepage.set_button_sound(not button_sound_state)
        else:
            lock_hover_sound = False
            homepage.set_button_sound(button_sound_state)

        homepage.draw(pages, screen, 70)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra vị trí click
                click_pos = event.pos

                # ===== LOGOUT: ưu tiên xử lý trước các nút khác =====
                if pages.session.get("logged_in", False):
                    logout_rect = getattr(homepage, "logout_rect", None)
                    if logout_rect and logout_rect.collidepoint(click_pos):
                        audio_manager.play_sfx("click")
                        pages.session["logged_in"] = False
                        pages.session["account"] = None

                        # Vẽ lại homepage ngay để thấy thay đổi lập tức
                        homepage.draw(pages, screen, 70)
                        pygame.display.update()
                        continue

                # Biến cờ để theo dõi xem có nút nào được nhấn hay không
                button_was_clicked = False

                if button_play.collidepoint(click_pos):
                    button_was_clicked = True
                    homepage.set_button_play(0)
                    to_world_map = True
                    running      = False

                elif button_sound.collidepoint(event.pos):
                    button_was_clicked = True
                    button_sound_state = not button_sound_state
                    print("Sound closed" if button_sound_state else "Sound opened")
                    homepage.set_button_sound(button_sound_state)
                    lock_hover_sound   = True
                    audio_manager.toggle_sfx()

                elif button_music.collidepoint(event.pos):
                    button_was_clicked = True
                    button_music_state = not button_music_state
                    print("Music closed" if button_music_state else "Music opened")
                    homepage.set_button_music(button_music_state)
                    lock_hover_music   = True
                    audio_manager.toggle_music()

                # PHÁT ÂM THANH: CHỈ PHÁT NẾU MỘT TRONG CÁC NÚT ĐƯỢC NHẤN
                if button_was_clicked:
                    audio_manager.play_sfx('click')
                pygame.display.update()

            if running == False:
                break
        clock.tick(60)

    return to_world_map

def control_worldmap(screen, pages, audio_manager):
    list_stages = [
        [100, 150, 80, 35],  # Stage 1
        [100, 205, 80, 35],  # Stage 2
        [100, 260, 80, 35],  # Stage 3
        [100, 315, 80, 35],  # Stage 4
        [100, 370, 80, 35],  # Stage 5
        [220, 150, 80, 35],  # Stage 6
        [220, 205, 80, 35],  # Stage 7
        [220, 260, 80, 35],  # Stage 8
        [220, 315, 80, 35],  # Stage 9
        [220, 370, 80, 35],  # Stage 10
        [460, 150, 80, 35],  # Stage 11
        [460, 205, 80, 35],  # Stage 12
        [460, 260, 80, 35],  # Stage 13
        [460, 315, 80, 35],  # Stage 14
        [460, 370, 80, 35],  # Stage 15
    ]

    stages = []
    for i in range(len(list_stages)):
        stages.append(pygame.Rect(list_stages[i][0], list_stages[i][1],
                                  list_stages[i][2], list_stages[i][3]))
    back = pygame.Rect(10, 395, 75, 75)

    world_map    = pages.world_map
    running      = True
    stage        = -1
    back_state   = 0
    clicked_back = False

    level_state = [0] * 15

    status_text = ""
    status_color = (255, 90, 90)
    status_until = 0

    status_font = pygame.font.Font("font/static/Roboto-Bold.ttf", 22)
    toast_center = (320, 240)

    account = pages.session.get("account", None)
    progess = load_progress()
    max_unlocked = 1
    if account:
        max_unlocked = int(progess.get(account, 1))

    clock = pygame.time.Clock()

    while running:
        # Cập nhật vị trí trỏ chuột liên tục
        mouse_pos = pygame.mouse.get_pos()

        # Xử lý Hover
        for i in range(15):
            if (i + 1) <= max_unlocked and stages[i].collidepoint(mouse_pos):
                level_state[i] = 1
            else:
                level_state[i] = 0

        if back.collidepoint(mouse_pos):
            back_state = 1
        else:
            back_state = 0
        world_map.draw(screen, level_state, back_state)
        now = pygame.time.get_ticks()
        if status_text and now < status_until:
            draw_toast(
                screen,
                status_text,
                toast_center,
                status_font,
                text_color=status_color,
                bg_alpha=160
            )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                button_was_clicked = False

                if back.collidepoint(click_pos):
                    button_was_clicked = True
                    clicked_back       = True
                    running            = False
                for i in range(len(stages)):
                    if stages[i].collidepoint(click_pos):
                        if (i + 1) <= max_unlocked:
                            button_was_clicked = True
                            stage = i
                            running = False
                        else:
                            status_text = "Bạn chưa mở khóa màn này"
                            status_color = (255, 90, 90)
                            status_until = pygame.time.get_ticks() + 1800

                            audio_manager.play_sfx('click')
                        break

                if button_was_clicked:
                    audio_manager.play_sfx('click')

            if running == False:
                break
        clock.tick(60)

    if stage != -1:
        if stage < 10:
            print("YOU CHOOSE EASY MAP:", stage+1)
        else:
            print("YOU CHOOSE HARD MAP:", stage-9)
    return clicked_back, stage

def control_result(screen, pages, state, audio_manager):
    def unlock_next_stage(pages):
        if not pages.session.get("logged_in"):
            return
        account = pages.session.get("account")
        if not account:
            return

        cur = pages.session.get("current_stage", None)
        if cur is None:
            return

        progress = load_progress()
        max_unlocked = int(progress.get(account, 1))

        cleared_stage = cur + 1
        new_unlocked = max(max_unlocked, cleared_stage + 1)

        # Không vượt quá 15 màn
        if new_unlocked > 15:
            new_unlocked = 15

        progress[account] = new_unlocked
        save_progress(progress)

    if state:
        audio_manager.play_music("lose_game")
    else:
        audio_manager.play_music("win_game")

    button_undomove = pygame.Rect(167, 300, 75, 75)
    button_tryagain = pygame.Rect(247, 300, 75, 75)
    button_worldmap = pygame.Rect(327, 300, 75, 75)
    button_home     = pygame.Rect(407, 300, 75, 75)

    result   = pages.result

    button_undomove_state = result.get_button_undomove()
    button_tryagain_state = result.get_button_tryagain()
    button_worldmap_state = result.get_button_worldmap()
    button_home_state     = result.get_button_home()

    running = True
    next_state = -1
    clock = pygame.time.Clock()

    while running:
        # Cập nhật vị trí trỏ chuột liên tục
        mouse_pos = pygame.mouse.get_pos()

        # Xử lý Hover
        if button_undomove.collidepoint(mouse_pos):
            result.set_button_undomove(not button_undomove_state)
        else:
            result.set_button_undomove(button_undomove_state)

        if button_tryagain.collidepoint(mouse_pos):
            result.set_button_tryagain(not button_tryagain_state)
        else:
            result.set_button_tryagain(button_tryagain_state)

        if button_worldmap.collidepoint(mouse_pos):
            result.set_button_worldmap(not button_worldmap_state)
        else:
            result.set_button_worldmap(button_worldmap_state)

        if button_home.collidepoint(mouse_pos):
            result.set_button_home(not button_home_state)
        else:
            result.set_button_home(button_home_state)

        result.draw(screen, state)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos          = event.pos

                if button_undomove.collidepoint(click_pos):
                    audio_manager.play_sfx('click')
                    result.set_button_undomove(0)
                    next_state = 0
                    running = False
                elif button_tryagain.collidepoint(click_pos):
                    audio_manager.play_sfx('click')
                    result.set_button_tryagain(0)
                    next_state = 1
                    running = False
                elif button_worldmap.collidepoint(click_pos):
                    audio_manager.play_sfx('click')
                    if state == False:
                        unlock_next_stage(pages)
                    result.set_button_worldmap(0)
                    next_state = 2
                    running = False
                elif button_home.collidepoint(click_pos):
                    audio_manager.play_sfx('click')
                    if state == False:
                        unlock_next_stage(pages)
                    result.set_button_home(0)
                    next_state = 3
                    running = False

                pygame.display.update()
            if running == False:
                break
        clock.tick(60)

    return next_state

def control_explorer(screen, game, pages, menu, backdrop, floor,
                     stair, trap, key, gate, wall, dust_sheet,
                     explorer, explorer_character,
                     mummy_white_character, list_mummy_white,
                     mummy_red_character, list_mummy_red,
                     scorpion_white_character, list_scorpion_white,
                     scorpion_red_character, list_scorpion_red,
                     white_fight, red_fight, stung_sheet,
                     audio_manager):
    def capture_snapshot():
        # Lưu dữ liệu nguyên thủy + hướng để restore đúng hình quay
        return {
            "gate": dict(game.gate),
            "explorer": (
                explorer_character.get_x(),
                explorer_character.get_y(),
                explorer.get("direction", "DOWN")
            ),
            "mw": [(c.get_x(), c.get_y(), list_mummy_white[i].get("direction", "DOWN"))
                   for i, c in enumerate(mummy_white_character)],
            "mr": [(c.get_x(), c.get_y(), list_mummy_red[i].get("direction", "DOWN"))
                   for i, c in enumerate(mummy_red_character)],
            "sw": [(c.get_x(), c.get_y(), list_scorpion_white[i].get("direction", "DOWN"))
                   for i, c in enumerate(scorpion_white_character)],
            "sr": [(c.get_x(), c.get_y(), list_scorpion_red[i].get("direction", "DOWN"))
                   for i, c in enumerate(scorpion_red_character)],
        }

    def apply_snapshot(snap):
        # 1) restore gate
        game.gate = dict(snap["gate"])

        # 2) restore explorer (logic + sprite)
        ex, ey, edir = snap["explorer"]
        explorer_character.set_x(ex)
        explorer_character.set_y(ey)
        explorer["direction"] = edir
        explorer["cellIndex"] = 0
        explorer["coordinates"] = cal_coordinates(game, ex, ey)

        # 3) restore enemies (hồi sinh nếu thiếu)
        def restore(char_list, sprite_list, pos_list, enemy_key, cls):
            # nếu hiện tại nhiều hơn snapshot: cắt bớt
            del char_list[len(pos_list):]
            del sprite_list[len(pos_list):]

            # nếu hiện tại ít hơn snapshot: hồi sinh thêm
            while len(char_list) < len(pos_list):
                x, y, d = pos_list[len(char_list)]
                obj = cls(x, y)
                # giữ đúng logic chiến lược hard map
                if game.stage >= 10:
                    obj.set_move_strategy(0)
                char_list.append(obj)

                sp = {
                    "sprite_sheet": game.sheets[enemy_key],
                    "coordinates": cal_coordinates(game, x, y),
                    "direction": d,
                    "cellIndex": 0
                }
                sprite_list.append(sp)

            # set lại vị trí cho tất cả
            for i, (x, y, d) in enumerate(pos_list):
                char_list[i].set_x(x)
                char_list[i].set_y(y)
                sprite_list[i]["sprite_sheet"] = game.sheets[enemy_key]
                sprite_list[i]["coordinates"] = cal_coordinates(game, x, y)
                sprite_list[i]["direction"] = d
                sprite_list[i]["cellIndex"] = 0

        restore(mummy_white_character, list_mummy_white, snap["mw"], "mw", characters.mummy_white)
        restore(mummy_red_character, list_mummy_red, snap["mr"], "mr", characters.mummy_red)
        restore(scorpion_white_character, list_scorpion_white, snap["sw"], "sw", characters.scorpion_white)
        restore(scorpion_red_character, list_scorpion_red, snap["sr"], "sr", characters.scorpion_red)

        # 4) redraw
        graphics.draw_screen(screen, game.maze, backdrop, floor, game.maze_size, game.cell_rect,
                             stair, game.stair_position, trap, game.trap_position,
                             key, game.key_position, gate, game.gate, wall,
                             explorer,
                             list_mummy_white, list_mummy_red,
                             list_scorpion_white, list_scorpion_red)
        screen.blit(menu, (494, 0))
        pygame.display.update()

    def print_console_undo():
        print("===== UNDO STATE =====")

        # Explorer
        print(f"Explorer: ({explorer_character.get_x()}, {explorer_character.get_y()})")

        # Mummy White
        if mummy_white_character:
            for i, c in enumerate(mummy_white_character):
                print(f"Mummy White {i + 1}: ({c.get_x()}, {c.get_y()})")

        # Mummy Red
        if mummy_red_character:
            for i, c in enumerate(mummy_red_character):
                print(f"Mummy Red {i + 1}: ({c.get_x()}, {c.get_y()})")

        # Scorpion White
        if scorpion_white_character:
            for i, c in enumerate(scorpion_white_character):
                print(f"Scorpion White {i + 1}: ({c.get_x()}, {c.get_y()})")

        # Scorpion Red
        if scorpion_red_character:
            for i, c in enumerate(scorpion_red_character):
                print(f"Scorpion Red {i + 1}: ({c.get_x()}, {c.get_y()})")

        print("======================")

    running         = True
    # HÀNG ĐỢI LỆNH DI CHUYỂN
    move_queue      = deque()   # mỗi phần tử chứa: (new_x, new_y, direction)
    is_moving       = False     # đang chạy animation Explorer + Mummy
    last_input_time = 0         # thời gian lần nhận input gần nhất (ms)
    INPUT_DELAY     = 300       # không nhận input quá dày (< 300ms)
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                now = pygame.time.get_ticks()
                if now - last_input_time < INPUT_DELAY:
                    continue  # bỏ qua click này

                # Lấy vị trí hiện tại
                explorer_x = explorer_character.get_x()
                explorer_y = explorer_character.get_y()
                explorer_new_x = explorer_x
                explorer_new_y = explorer_y

                if event.key == pygame.K_UP:
                    explorer_new_x -= 2
                    direction = "UP"
                if event.key == pygame.K_DOWN:
                    explorer_new_x += 2
                    direction = "DOWN"
                if event.key == pygame.K_LEFT:
                    explorer_new_y -= 2
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT:
                    explorer_new_y += 2
                    direction = "RIGHT"

                # Nếu vị trí mới khác vị trí cũ
                if (explorer_new_x != explorer_x or explorer_new_y != explorer_y):
                    # Kiểm tra có đi hợp lệ không
                    if explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y,
                                                                  explorer_new_x, explorer_new_y):
                        # CHỈ THÊM VÀO HÀNG ĐỢI
                        move_queue.append((explorer_new_x, explorer_new_y, direction))
                        last_input_time = now

            # Xử lí click chuột
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                # Lấy tọa độ x, y pixel
                mouse_x, mouse_y = event.pos

                # ================== MENU ==================
                undo_move    = pygame.Rect(503, 135, 116, 32)
                reset_maze   = pygame.Rect(499, 178, 116, 32)
                world_map    = pygame.Rect(499, 229, 116, 32)
                quit_game    = pygame.Rect(499, 274, 116, 32)
                quit_to_main = pygame.Rect(499, 435, 116, 32)

                if undo_move.collidepoint(event.pos):
                    audio_manager.play_sfx('click')
                    if len(game.undo_stack):
                        snap = game.undo_stack.pop()
                        move_queue.clear()
                        is_moving = False
                        apply_snapshot(snap)
                        print_console_undo()
                    continue

                elif reset_maze.collidepoint(event.pos):
                    print("RESET MAZE")
                    audio_manager.play_sfx('click')
                    rungame(game.stage, screen, pages, audio_manager)
                    return

                elif world_map.collidepoint(event.pos):
                    audio_manager.play_sfx('click')
                    show_worldmap(screen, pages, audio_manager)
                    return

                elif quit_game.collidepoint(event.pos):
                    audio_manager.play_sfx('click')
                    return

                elif quit_to_main.collidepoint(event.pos):
                    audio_manager.play_sfx('click')
                    show_homepage(screen, pages, 0, audio_manager)
                    return


                now = pygame.time.get_ticks()
                if now - last_input_time < INPUT_DELAY or is_moving:
                    continue

                # Lấy vị trí explorer tại thời điểm click
                explorer_x = explorer_character.get_x()
                explorer_y = explorer_character.get_y()

                # 1. Đổi từ pixel sang ô (target_row, target_col) trong matrix
                target_row = (mouse_y - game.coordinate_screen_y) // game.cell_rect
                target_col = (mouse_x - game.coordinate_screen_x) // game.cell_rect

                # 2. Đổi từ matrix (row, col) sang chỉ số trong maze (ASCII)
                explorer_new_x = int(target_row * 2 + 1)
                explorer_new_y = int(target_col * 2 + 1)

                # 3. Chỉ cho click vào ô kề cạnh
                is_neighbor = (
                        (abs(explorer_x - explorer_new_x) == 2 and explorer_y == explorer_new_y) or
                        (abs(explorer_y - explorer_new_y) == 2 and explorer_x == explorer_new_x)
                )

                if is_neighbor and explorer_character.eligible_character_move(game.maze, game.gate, explorer_x,
                                                                              explorer_y,
                                                                              explorer_new_x, explorer_new_y):
                    # 4. Xác định hướng di chuyển
                    if explorer_new_x == explorer_x - 2:
                        direction = "UP"
                    elif explorer_new_x == explorer_x + 2:
                        direction = "DOWN"
                    elif explorer_new_y == explorer_y - 2:
                        direction = "LEFT"
                    elif explorer_new_y == explorer_y + 2:
                        direction = "RIGHT"
                    else:
                        pass

                    move_queue.append((explorer_new_x, explorer_new_y, direction))
                    last_input_time = now

        # ================== XỬ LÝ HÀNG ĐỢI LỆNH DI CHUYỂN ==================
        if (not is_moving) and move_queue:
            # Lấy lệnh đầu tiên trong queue (FIFO)
            target_x, target_y, direction = move_queue.popleft()

            # Lấy lại vị trí hiện tại của Explorer
            explorer_x = explorer_character.get_x()
            explorer_y = explorer_character.get_y()
            audio_manager.play_sfx('move')

            # Chỉ cho phép di chuyển nếu vẫn kề cạnh + hợp lệ tại thời điểm thực thi
            is_neighbor = (
                    (abs(explorer_x - target_x) == 2 and explorer_y == target_y) or
                    (abs(explorer_y - target_y) == 2 and explorer_x == target_x)
            )

            if is_neighbor and explorer_character.eligible_character_move(game.maze, game.gate, explorer_x, explorer_y,
                                                                          target_x, target_y):
                # Set hướng
                explorer["direction"] = direction

                # Thêm trạng thái game cũ
                game.undo_stack.append(capture_snapshot())

                # Bắt đầu animation → khóa input
                is_moving = True

                explorer_character.move(target_x, target_y, screen, game, backdrop, floor,
                                        stair, game.stair_position, trap, game.trap_position, key, game.key_position,
                                        gate, game.gate, wall,
                                        explorer,
                                        list_mummy_white, list_mummy_red, list_scorpion_white, list_scorpion_red)

                print("Explorer position: {} {}".format(explorer_character.get_x(), explorer_character.get_y()))
                # Sau khi người chơi đi xong thì cho quái di chuyển
                running = update_enemy_position(screen, game, pages, backdrop, floor,
                                                stair, trap, key, gate, wall, dust_sheet,
                                                explorer, explorer_character,
                                                mummy_white_character, list_mummy_white,
                                                mummy_red_character, list_mummy_red,
                                                scorpion_white_character, list_scorpion_white,
                                                scorpion_red_character, list_scorpion_red,
                                                white_fight, red_fight, stung_sheet,
                                                audio_manager)
                if running is True:
                    pass
                elif running == 0:
                    # UNDO từ result
                    if len(game.undo_stack):
                        snap = game.undo_stack.pop()
                        move_queue.clear()
                        is_moving = False
                        apply_snapshot(snap)
                        print_console_undo()
                    running = True

                elif running == 1:
                    rungame(game.stage, screen, pages, audio_manager)
                    return
                elif running == 2:
                    show_worldmap(screen, pages, audio_manager)
                    return
                elif running == 3:
                    show_homepage(screen, pages, 0, audio_manager)
                    return
                elif running is None:
                    return

                # Kết thúc lượt → mở khóa
                is_moving = False
        clock.tick(60)
