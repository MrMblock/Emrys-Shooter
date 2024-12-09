import pygame
import cv2

class VideoManager:
    def __init__(self, game):
        self.game = game
        self.video_path = 'assets/videos/video.mp4'
        self.sound_path = 'assets/videos/sounds/wave1.mp3'
        self.video_finished = False
        self.video_capture = None

    def play_video_and_sound(self):
        # Arrêter la musique de fond du jeu
        self.game.sound_manager.stop_background_music()

        # Mettre l'état du jeu en pause si nécessaire
        self.game.event_manager.kage_stop = True

        # Charger la vidéo
        self.video_capture = cv2.VideoCapture(self.video_path)
        
        # Obtenir le framerate de la vidéo
        fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        clock = pygame.time.Clock()

        # Démarrer le son
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.music.play()

        # Jouer la vidéo frame par frame
        while self.video_capture.isOpened():
            ret, frame = self.video_capture.read()

            if not ret:
                # Si on ne récupère plus de frame, la vidéo est terminée
                break

            # Convertir la frame en format compatible avec pygame (de BGR à RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.transpose(frame)  # Optionnel, si nécessaire selon orientation de la vidéo
            frame_surface = pygame.surfarray.make_surface(frame)

            # Afficher la vidéo dans la fenêtre Pygame
            self.game.screen.blit(frame_surface, (0, 0))
            pygame.display.update()

            # Gestion des événements Pygame pendant la lecture de la vidéo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.video_finished = True
                    break

            # Synchroniser la vitesse de lecture avec le framerate de la vidéo
            clock.tick(fps)

            # Vérification si la musique est terminée (pour synchronisation avec la vidéo)
            if not pygame.mixer.music.get_busy():
                self.video_finished = True
                break

        # Libérer les ressources vidéo
        self.video_capture.release()

        # Reprendre la musique de fond une fois la vidéo terminée
        self.game.sound_manager.play_background_music()

        self.stop_video()

    def stop_video(self):
        # Arrêter la lecture de la vidéo et du son
        if self.video_capture is not None:
            self.video_capture.release()
        pygame.mixer.music.stop()
        self.video_finished = True
        self.game.sound_manager.play_background_music()
        self.game.event_manager.kage_stop = False
