import pygame
from scripts.comet import Comet

class CometFallEvent:
    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 0.02
        self.game = game

        # définir un groupe de sprite pour stocker nos comètes
        self.all_comets = pygame.sprite.Group()

    def add_percent(self):
        self.percent += self.percent_speed 

    def is_full_loaded(self):
        return self.percent >= 1
    
    def reset_percent(self):
        self.percent = 0
    
    def meteor_fall(self):
        self.all_comets.add(Comet(self))

    def attempt_fall(self):
        if self.is_full_loaded():
            self.meteor_fall()
            self.reset_percent()

    def update_bar(self, surface):
        self.add_percent()
        self.attempt_fall()

        # barre noire de fond
        pygame.draw.rect(surface, (0, 0, 0), [
            0, # x
            surface.get_height() - 70, 
            surface.get_width(),
            10 
        ])
        # barre rouge
        pygame.draw.rect(surface, (187, 11, 11), [
            0, # x
            surface.get_height() - 70, 
            (surface.get_width()) * self.percent, 
            10 
        ])