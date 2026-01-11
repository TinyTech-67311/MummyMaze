import pygame
import os

from path_utils import rpath

class AudioManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.is_sfx_on   = True
        self.is_music_on = True
        sound_path   = rpath("assets", "sound")

        try:
            self.click_sfx    = pygame.mixer.Sound(os.path.join(sound_path, 'click.wav'))
            self.move_sfx     = pygame.mixer.Sound(os.path.join(sound_path, 'expwalk30.mp3'))
            self.pummel_sfx   = pygame.mixer.Sound(os.path.join(sound_path, 'pummel.mp3'))
            self.poison_sfx   = pygame.mixer.Sound(os.path.join(sound_path, 'poison.mp3'))
            self.gate_sfx     = pygame.mixer.Sound(os.path.join(sound_path, 'gate.mp3'))
            self.mumwalk_sfx  = pygame.mixer.Sound(os.path.join(sound_path, 'mumwalk30.mp3'))
            self.scorwalk_sfx = pygame.mixer.Sound(os.path.join(sound_path, 'scorwalk.mp3'))
            self.click_sfx.set_volume(0.7)
            self.move_sfx.set_volume(0.7)
            self.pummel_sfx.set_volume(0.7)
            self.poison_sfx.set_volume(0.7)
            self.gate_sfx.set_volume(0.7)
            self.mumwalk_sfx.set_volume(0.7)
            self.scorwalk_sfx.set_volume(0.7)

        except pygame.error as e:
            self.click_sfx = self.move_sfx = self.pummel_sfx = \
            self.poison_sfx = self.gate_sfx = self.mumwalk_sfx = self.scorwalk_sfx = None
        self.play_music("musicgame")

    def toggle_music(self):
        self.is_music_on = not self.is_music_on
        if not self.is_music_on:
            pygame.mixer.music.stop()
        else:
            self.play_music("musicgame")

    def toggle_sfx(self):
        self.is_sfx_on = not self.is_sfx_on
        if not self.is_sfx_on:
            pygame.mixer.stop()

    def play_music(self, music_key, loops = -1):
        if self.is_music_on:
            sound_path   = os.path.join("assets", "sound")
            pygame.mixer.music.load(os.path.join(sound_path, music_key + ".mp3"))
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops)

    def play_sfx(self, sfx_key, loops = 0):
        if self.is_sfx_on:
            sound_to_play = None
            if sfx_key   == 'click'   and self.click_sfx:
                sound_to_play = self.click_sfx
            elif sfx_key == 'move'    and self.move_sfx:
                sound_to_play = self.move_sfx
            elif sfx_key == 'mumwalk' and self.mumwalk_sfx:
                sound_to_play = self.mumwalk_sfx
            elif sfx_key == 'pummel'  and self.pummel_sfx:
                sound_to_play = self.pummel_sfx
            elif sfx_key == 'poison'  and self.poison_sfx:
                sound_to_play = self.poison_sfx 
            elif sfx_key == 'gate'    and self.gate_sfx:
                sound_to_play = self.gate_sfx
            elif sfx_key == 'scorwalk' and self.scorwalk_sfx:
                sound_to_play = self.scorwalk_sfx
            if sound_to_play:
                sound_to_play.play(loops)  

    def get_music_state(self):
        return self.is_music_on  
         
    def get_sfx_state(self):
        return self.is_sfx_on