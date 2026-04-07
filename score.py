import pygame

class Score(pygame.sprite.Sprite):
    points = {
        "asteroid_small": 50,
        "asteroid_medium": 120,
        "asteroid_large": 300,
    }

    def __init__(self, position, font, font_size, bold=True):
        super().__init__(self.containers)
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.font.set_bold(bold)
        self.score = 0

    def draw(self, screen):
        text_surface = self.font.render(f"Score: {self.score}", True, "white")
        text_rect = text_surface.get_rect(center=(self.position.x, self.position.y))
        screen.blit(text_surface, text_rect)

    def update(self, dt):
        pass

    def increase(self, event):
        self.score += self.points[event]
