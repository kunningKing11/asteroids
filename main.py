import pygame
import sys
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import Score
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_POSITION, SCORE_FONT, SCORE_FONT_SIZE
from logger import log_state, log_event


def asteroid_type(asteroid):
    size = asteroid.radius
    for i in range(0, len(asteroid.categories)):
        if (size > asteroid.sizes[i]):
            if (i == (len(asteroid.categories) - 1)):
                return asteroid.categories[(i + 1)]
            else:
                continue
        elif (size == asteroid.sizes[i]):
            return asteroid.categories[(i + 1)]
        else: # asteroid is smaller than current category
            return asteroid.categories[i]

def main():
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Score.containers = (updatable, drawable)

    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    asteroid_field = AsteroidField()

    score = Score(SCORE_POSITION, SCORE_FONT, SCORE_FONT_SIZE)

    clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            for shot in shots:
                if shot.collides_with(asteroid):
                    shot.kill()
                    type = asteroid_type(asteroid)
                    log_event(f"asteroid_shot, type: {type}")
                    score.increase(type)
                    asteroid.split()
        for item in drawable:
            item.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
