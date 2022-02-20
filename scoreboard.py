import pygame

class ScoreBoard:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.setting = game.setting
        self.stats = game.stats

        self.text_color = (170, 170, 170)
        self.font = pygame.font.SysFont(None, 46)

        self.prep_score()
        self.prep_highscore()
        self.prep_level()

    def prep_score(self):
        score_str = str(f"Score:{self.stats.score}")
        self.score_image = self.font.render(score_str, True, self.text_color, self.setting.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top + 20

    def prep_highscore(self):
        score_str = str(f"HighScore:{self.stats.high_score}")
        self.highscore_image = self.font.render(score_str, True, self.text_color, self.setting.bg_color)
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = self.screen_rect.top +20

    def prep_level(self):
        leve_str = str(f"Level:{self.stats.level}")
        self.level_image = self.font.render(leve_str, True, self.text_color, self.setting.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 20
        self.level_rect.top = self.screen_rect.top + 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highscore_image, self.highscore_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def check_highscore(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_highscore()
