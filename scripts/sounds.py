import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {
            'click': pygame.mixer.Sound("assets/sounds/tbgz.mp3"),
            'game_over': pygame.mixer.Sound("assets/sounds/tbgz.mp3"),
            'meteorite': pygame.mixer.Sound("assets/sounds/meteorite.ogg"),
            'tir': pygame.mixer.Sound("assets/sounds/tir.ogg"),
            'terroriste': pygame.mixer.Sound("assets/sounds/terroriste.mp3"),
            'saiyan1': pygame.mixer.Sound("assets/sounds/saiyan1.mp3"),
            'kbnj': pygame.mixer.Sound("assets/transformations/kbnj/jutsu.mp3"),
            'kbnj_apparition': pygame.mixer.Sound("assets/transformations/kbnj/apparition.mp3")
        }

        self.sounds['click'].set_volume(0.8)         
        self.sounds['game_over'].set_volume(1)     
        self.sounds['meteorite'].set_volume(0.6)     
        self.sounds['tir'].set_volume(0)           
        self.sounds['terroriste'].set_volume(1)    
        self.sounds['saiyan1'].set_volume(1)       

    def play(self, name):
        self.sounds[name].play()

    def stop(self, name):
        self.sounds[name].stop()
        
    def stop_all_sounds(self):
        pygame.mixer.stop()

    def play_background_music(self):
        # Load and play background music with a lower volume
        pygame.mixer.music.load("assets/sounds/bg_music.mp3")
        pygame.mixer.music.set_volume(0.1)  
        pygame.mixer.music.play(-1)         

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def mute(self):
        pygame.mixer.music.set_volume(0)
        self.sounds['click'].set_volume(0)         
        self.sounds['game_over'].set_volume(0)     
        self.sounds['meteorite'].set_volume(0)     
        self.sounds['tir'].set_volume(0)           
        self.sounds['terroriste'].set_volume(0)    
        self.sounds['saiyan1'].set_volume(0) 


    def unmute(self):
        pygame.mixer.music.set_volume(0.6) 
        self.sounds['click'].set_volume(0.8)         
        self.sounds['game_over'].set_volume(1)     
        self.sounds['meteorite'].set_volume(0.6)     
        self.sounds['tir'].set_volume(0.6)           
        self.sounds['terroriste'].set_volume(1)    
        self.sounds['saiyan1'].set_volume(1)