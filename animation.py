import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, size=(320, 320)):
        super().__init__()
        self.sprite_name = sprite_name
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load(f'assets/{sprite_name}.png'), self.size)
        self.current_image = 0
        self.animations = self.load_animation_images(sprite_name)
        self.images = self.animations
        self.animation = False

    def start_animation(self):
        self.animation = True

    def animate(self, loop = False):
        if self.animation:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
                if loop == False:
                    # desactiver l'animation
                    self.animation = False
        
        self.image = self.images[self.current_image]

    def load_animation_images(self, sprite_name):
        images = []
        path = f"assets/{sprite_name}/"

        for num in range(1, 24):
            image_path = f"{path}{sprite_name}{num}.png"
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, self.size)
            images.append(image)
        
        return images

    @staticmethod
    def load_animations():
        return {
            'mummy': AnimateSprite.load_animation_images('mummy'),
            'alien': AnimateSprite.load_animation_images('alien')
        }  