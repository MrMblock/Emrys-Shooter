import pygame
from scripts.projectile import Projectile
import animation
import time

class Player(animation.AnimateSprite):
    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 760
        self.rect.y = 340   
        self.fire_rate = 0.118
        self.last_shot_time = 0

        self.last_position = (self.rect.x, self.rect.y)
        self.last_move_time = time.time()
        self.stationary_limit = 3

    def damage(self, amount):
        if self.health - amount > 0:
            self.health -= amount
        else:
            self.game.game_over()

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 200, self.rect.y + 180, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 200, self.rect.y + 180, self.health, 5])
    
    def launch_projectile(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.fire_rate:
            self.last_shot_time = current_time
            self.all_projectiles.add(Projectile(self))
            self.game.sound_manager.play('tir')

    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def tucampes(self):
        if (self.rect.x, self.rect.y) != self.last_position:
            self.last_position = (self.rect.x, self.rect.y)
            self.last_move_time = time.time()
        elif time.time() - self.last_move_time > self.stationary_limit:
            self.terroriste()

    def terroriste(self):
        self.game.trigger_terrorist_event()