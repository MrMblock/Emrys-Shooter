import pygame
from scripts.game import Game
from scripts.sounds import SoundManager

pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 240

sound_manager = SoundManager()

# générer la première fenêtre
pygame.display.set_caption("Emrys Shooter") 
screen = pygame.display.set_mode((1920, 1080))

black = (0, 0, 0)
screen.fill(black)

bg = pygame.image.load('assets/bg.png')

# la bannière de jeu
banner = pygame.image.load('assets/banner.png')
banner_rect = banner.get_rect()
banner_rect.x = screen.get_width() / 3.5
  
# importer et charger notre bouton pour la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = screen.get_width() / 2.55
play_button_rect.y = screen.get_height() / 1.8 

game = Game()

running = True

while running:
    # appliquer le fond 
    screen.blit(bg, (0, 0))

    # vérifier si le jeu a commencé
    if game.is_playing:
        # lancer le jeu
        game.update(screen)
    else:
        # écran de jeu
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)
    
    # mettre à jour l'écran
    pygame.display.flip()        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_p:
                game.potion()

            if event.key == pygame.K_1:
                game.event_manager.is_saiyan1 = True  

            if event.key == pygame.K_2:
                game.event_manager.is_not_saiyan_anymore()

            if event.key == pygame.K_k:
                if not game.event_manager.kage_bunshin_no_jutsu_active:
                    game.event_manager.kage_bunshin_no_jutsu_active = True
                    game.event_manager.kage_stop = True
                    game.event_manager.is_not_saiyan_anymore()
                    sound_manager.play("kbnj")
 
            if event.key == pygame.K_l: 
                game.event_manager.end_kage_bunshin_no_jutsu()
  
            if event.key == pygame.K_t:
                game.sound_manager.play("game_over")
                  
            if event.key == pygame.K_a:
                if game.event_manager.pause == False:
                    game.event_manager.pause_jeu()
                else:
                    game.event_manager.end_pause()

            if event.key == pygame.K_s:
                game.sound_manager.mute()

            if event.key == pygame.K_u:
                game.sound_manager.unmute()
                
            if event.key == pygame.K_m:
                game.event_manager.kamehameha()

            # touche espace -> projectile
            if event.key == pygame.K_SPACE:
                if game.is_playing and not game.event_manager.kage_stop:
                    game.player.launch_projectile()
                    
   
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # souris collision avec le bouton de jeu au début   
            if play_button_rect.collidepoint(event.pos):
                game.start()
                game.sound_manager.play('click')
   
    clock.tick(FPS)