class Setting:
    def __init__(self):
        self.bg_color = (20, 5, 30)
        self.screen_width = 1200
        self.screen_heigh = 800

        # bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 165, 0)
        self.bullet_allowed = 4

        # alien
        self.fleet_drop = 10

        self.ship_limit = 1

        self.speedup_scale = 1.1

        self.initialize_dynamic()

    def initialize_dynamic(self):
        self.alien_speed = 0.5
        self.bullet_speed = 2
        self.speed = 1.5
        self.fleet_direction = 1
        self.alien_point = 5

    def increase_speed(self):
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.speed *= self.speedup_scale
        self.alien_point *= 2

