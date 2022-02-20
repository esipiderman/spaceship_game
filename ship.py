import pygame

class Ship:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.speed = game.setting.speed

        # load image
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        # ship moving
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.speed
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
