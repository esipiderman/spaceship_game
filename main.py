import pygame
import sys
import time
from settings import Setting
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class Game:
    def __init__(self):
        pygame.init()
        self.game_active = False
        self.setting = Setting()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.play_button = Button(self, "play")
        self.setting.screen_heigh = self.screen.get_rect().height
        self.setting.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")

        # make bullet
        self.bullets = pygame.sprite.Group()

        # make ship
        self.ship = Ship(self)

        # make aliens
        self.aliens = pygame.sprite.Group()
        self.create_fleet()

        self.stats = GameStats(self)
        self.scoreboard = ScoreBoard(self)

    def create_fleet(self):
        alien = Alien(self)
        screen_width = self.setting.screen_width
        screen_height = self.setting.screen_heigh

        alien_width = alien.rect.width
        alien_height = alien.rect.height

        ship_height = self.ship.rect.height

        available_space_x = screen_width - alien_width
        number_alien = int(available_space_x // (1.5*alien_width))

        available_space_y = screen_height - ship_height
        number_rows = int(available_space_y / (2*alien_height))

        for row_number in range(number_rows):
            for alien_number in range(number_alien):
                self.create_alien(alien_number, row_number)

    def create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + (1.5 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def run_game(self):
        while True:
            self.check_event()
            if self.game_active:
                self.ship.update()
                self.update_bullet()
                self.update_alien()
            self.update_screen()

    def update_alien(self):
        self.aliens.update()
        self.check_fleet_edge()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        self.check_alien_bottom()

    def ship_hit(self):
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.aliens.empty()
            self.bullets.empty()

            self.create_fleet()
            self.ship.center_ship()
            time.sleep(3)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def check_fleet_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop
        self.setting.fleet_direction *= -1

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.chek_keydown(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self.check_play_button(mouse_position)

    def check_play_button(self, mouse_position):
        button_click = self.play_button.rect.collidepoint(mouse_position)
        if button_click and not self.game_active:
            if self.play_button.rect.collidepoint(mouse_position):
                self.stats.reset_stats()
                self.scoreboard.prep_score()
                self.scoreboard.prep_level()
                self.game_active = True

                self.aliens.empty()
                self.bullets.empty()
                self.create_fleet()
                self.ship.center_ship()

                pygame.mouse.set_visible(False)

    def chek_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self.fire_bullet()

    def check_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def fire_bullet(self):
        if len(self.bullets) <= self.setting.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            # self.stats.score += self.setting.alien_point
            for alien in collision.values():
                self.stats.score += self.setting.alien_point * len(alien)
            self.scoreboard.prep_score()
            self.scoreboard.check_highscore()
            self.scoreboard.prep_level()

        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.setting.increase_speed()

            self.stats.level += 1
            self.scoreboard.prep_level()

    def update_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    ai = Game()
    ai.run_game()
