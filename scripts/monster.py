import pygame
import random
from animation import AnimateSprite

class Monster(AnimateSprite):
    def __init__(self, game, name):
        super().__init__(name, size=(320, 320))
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.3  
        self.rect = self.image.get_rect()
        self.rect.x = 1600 + random.randint(0, 300)
        self.rect.y = 570
        self.loot = 10
        self.start_animation()
    
    def set_speed(self, speed):
        self.velocity = speed

    def set_loot_amount(self, amount):
        self.loot = amount

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.rect.x = 1980
            self.health = self.max_health
            # ajouter du score
            self.game.add_score(self.loot)
            self.game.add_money(10)
            
    def update_animation(self):
        self.animate(loop=True)

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 100, self.rect.y - 10, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 100, self.rect.y - 10, self.health, 5])
        
    def forward(self):
        if not self.game.check_collision(self, self.game.all_players):  
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)

# class Mummy
class Mummy(Monster):

    def __init__(self, game):
        super().__init__(game, "mummy")
        self.set_speed(8) # 18
        self.set_loot_amount(10)


# class Alien
class Alien(Monster):

    def __init__(self, game):
        super().__init__(game, "alien")
        self.attack = 0.7
        self.set_speed(5) # 8
        self.set_loot_amount(30)