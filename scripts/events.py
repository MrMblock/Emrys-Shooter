import pygame
import time

class EventManager:
    def __init__(self, game):
        self.game = game
        self.last_saiyan_cost_time = 0
        self.saiyan_cost_interval = 0.1

        self.saiyan1_image = pygame.image.load("assets/transformations/saiyan1/aura.gif")
        scale_factor = 1.5
        new_width = self.saiyan1_image.get_width() * scale_factor
        new_height = self.saiyan1_image.get_height() * scale_factor
        self.saiyan1_image = pygame.transform.scale(self.saiyan1_image, (new_width, new_height))
        self.is_saiyan1 = False

        self.kage_bunshin_no_jutsu_active = False
        self.kage_stop = False
        self.clone_timer = 0
        self.clone_delay = 1500  
        self.clone_count = 0
        self.max_clones = 3
        self.clones = []

        self.pause = False

    def saiyan1(self):
        if not self.kage_stop:
            self.game.sound_manager.play('saiyan1')
            aura_x = self.game.player.rect.x - 80
            aura_y = self.game.player.rect.y
            self.game.screen.blit(self.saiyan1_image, (aura_x, aura_y))
            self.saiyan1boost()

    def update_saiyan_status(self):
        if self.is_saiyan1 and not self.kage_stop:
            self.saiyan1()
            current_time = time.time()

            if current_time - self.last_saiyan_cost_time >= self.saiyan_cost_interval:
                self.last_saiyan_cost_time = current_time
                if self.game.money > 0:
                    self.game.money -= 1
                else:
                    self.is_not_saiyan_anymore()

    def is_not_saiyan_anymore(self):
        self.saiyan1stopboost()
        self.is_saiyan1 = False
        self.game.sound_manager.stop("saiyan1")

    def saiyan1boost(self):
        self.game.player.velocity = 12
        self.game.player.fire_rate = 0.115
        self.game.player.attack = 15

    def saiyan1stopboost(self):
        self.game.player.velocity = 5
        self.game.player.fire_rate = 0.118
        self.game.player.attack = 10

    def kage_bunshin_no_jutsu(self):
        if not self.kage_bunshin_no_jutsu_active:
            self.kage_bunshin_no_jutsu_active = True

        current_time = pygame.time.get_ticks()

        if self.clone_count < self.max_clones and current_time - self.clone_timer >= self.clone_delay:
            self.clone_timer = current_time
            clone_image = self.game.player.image.copy()
            clone_rect = self.game.player.rect.copy()
            clone_rect.x += 200 * (self.clone_count + 1)

            self.clones.append((clone_image, clone_rect))
            self.clone_count += 1

            self.game.sound_manager.play("kbnj_apparition")

        for clone_image, clone_rect in self.clones:
            self.game.screen.blit(clone_image, clone_rect)

    def end_kage_bunshin_no_jutsu(self):
        self.clones.clear()
        self.clone_count = 0
        self.kage_bunshin_no_jutsu_active = False
        self.kage_stop = False
        
        self.game.last_move_time = time.time()

    def pause_jeu(self):
        self.pause = True
        self.kage_stop = True

    def end_pause(self):
        self.pause = False
        self.kage_stop = False
        self.game.last_move_time = time.time()