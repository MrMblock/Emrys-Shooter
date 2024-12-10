import pygame
from scripts.player import Player
from scripts.comet_event import CometFallEvent
from scripts.monster import Mummy, Alien
from scripts.sounds import SoundManager
from scripts.comet import Comet
from scripts.events import EventManager
from scripts.video_manager import VideoManager  
import time

class Game:
    def __init__(self):
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.comet_event = CometFallEvent(self)
        self.all_monsters = pygame.sprite.Group()
        self.sound_manager = SoundManager()
        self.pressed = {}
        self.font = pygame.font.SysFont("monospace", 25)
        self.score = 0
        self.money = 0
        self.last_position = (self.player.rect.x, self.player.rect.y)
        self.last_move_time = time.time()
        self.stationary_limit = 3
        self.screen = None
        self.event_manager = EventManager(self)
        self.campeur_image = pygame.image.load('assets/POURQUOI TU CAMPES.png')
        self.campeur_image = pygame.transform.scale(self.campeur_image, (400, 150))
        self.video_manager = VideoManager(self)  

    def start(self): 
        self.is_playing = True
        self.last_move_time = time.time()  
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)
        self.sound_manager.play("game_over")
        self.sound_manager.play_background_music()


    def add_score(self, loot):
        self.score += loot

    def add_money(self, amount):
        self.money += amount

    def potion(self):
        if self.money >= 50:
            self.money -= 50
            if self.player.health + 20 > self.player.max_health:
                self.player.health = self.player.max_health
            else:
                self.player.health += 20

    def game_over(self):
        self.sound_manager.stop_all_sounds()
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.is_playing = False
        self.score = 0
        self.sound_manager.play("game_over")
        self.sound_manager.stop_all_sounds()
        pygame.quit()

    def update(self, screen):
        self.screen = screen

        # Affichage du score et de l'argent
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (300, 150))

        money_text = self.font.render(f"{self.money}$", True, (255, 255, 255))
        screen.blit(money_text, (screen.get_width() - money_text.get_width() - 300, 150))

        # Vérifier si le score est supérieur ou égal à 50 et jouer la vidéo
        if self.score >= 5000000 and not self.video_manager.video_finished:
            self.video_manager.play_video_and_sound()

        # Gestion des transformations Saiyan et Kage Bunshin no Jutsu
        self.event_manager.update_saiyan_status()

        if self.event_manager.kage_bunshin_no_jutsu_active:
            self.event_manager.kage_bunshin_no_jutsu()

        # Blitter le joueur par-dessus l'aura/les clones
        screen.blit(self.player.image, self.player.rect)

        # Blitter les monstres
        self.all_monsters.draw(screen)

        if not self.event_manager.kage_stop:
            # Gestion des mouvements du joueur
            if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < 1600:
                self.player.move_right()
            elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > -200:
                self.player.move_left()

            # Vérification de l'inactivité pour afficher l'événement "campeur"
            self.tucampes()

            # Blitter les comètes et les gérer
            self.comet_event.all_comets.draw(screen)
            for comet in self.comet_event.all_comets:
                comet.fall()

            # Mise à jour de la barre de progression des comètes
            self.comet_event.update_bar(screen)

            # Mise à jour de la barre de santé du joueur
            self.player.update_health_bar(screen)

            # Déplacement des projectiles du joueur
            for projectile in self.player.all_projectiles:
                projectile.move()

            # Gestion des monstres
            for monster in self.all_monsters:
                monster.forward()
                monster.update_health_bar(screen)
                monster.update_animation()

            # Blitter les projectiles du joueur
            self.player.all_projectiles.draw(screen)

    def tucampes(self):
        # S'assurer que le jeu est en cours avant de vérifier l'inactivité
        if self.is_playing and not self.event_manager.kage_bunshin_no_jutsu_active and not self.event_manager.kage_stop:
            if (self.player.rect.x, self.player.rect.y) != self.last_position:
                self.last_position = (self.player.rect.x, self.player.rect.y)
                self.last_move_time = time.time()
            elif time.time() - self.last_move_time > self.stationary_limit:
                self.player.terroriste()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
    
    def spawn_monster(self, monster_class):
        self.all_monsters.add(monster_class(self))

    def trigger_terrorist_event(self):
        # Vérifier si le jeu est en cours avant de déclencher l'événement terroriste
        if self.is_playing and not self.event_manager.kage_stop and not self.event_manager.kage_bunshin_no_jutsu_active:
            if self.screen:
                campeur_image_rect = self.campeur_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                self.screen.blit(self.campeur_image, campeur_image_rect)

            comet = Comet(self.comet_event)
            comet.rect.x = self.player.rect.x + (self.player.rect.width // 2) - (comet.rect.width // 2)
            comet.rect.y = 0
            self.comet_event.all_comets.add(comet)

            self.sound_manager.play('terroriste')

            for monster in self.all_monsters:
                monster.velocity = 0
            self.player.velocity = 0
