import pygame
import sys
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import Score
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_POSITION, SCORE_FONT, SCORE_FONT_SIZE
from logger import log_state, log_event

def resolve_asteroid_collision(a, b):
    delta = b.position - a.position
    distance = delta.length()

    if distance == 0:
        delta = pygame.Vector2(1, 0)
        distance = 1

    min_distance = a.radius + b.radius
    if distance >= min_distance:
        return

    normal = delta / distance
    tangent = pygame.Vector2(-normal.y, normal.x)

    # Separate overlapping asteroids first
    overlap = min_distance - distance
    a.position -= normal * (overlap / 2)
    b.position += normal * (overlap / 2)

    # Mass based on area
    m1 = a.radius ** 2
    m2 = b.radius ** 2

    v1n = a.velocity.dot(normal)
    v1t = a.velocity.dot(tangent)
    v2n = b.velocity.dot(normal)
    v2t = b.velocity.dot(tangent)

    # 1D elastic collision along the normal
    v1n_after = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
    v2n_after = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

    a.velocity = tangent * v1t + normal * v1n_after
    b.velocity = tangent * v2t + normal * v2n_after

def handle_asteroid_collisions(asteroids, cell_size = 120):
    grid = {}
    asteroid_list = list(asteroids)

    for asteroid in asteroid_list:
        cell_x = int(asteroid.position.x // cell_size)
        cell_y = int(asteroid.position.y // cell_size)
        key = (cell_x, cell_y)

        if key not in grid:
            grid[key] = []
        grid[key].append(asteroid)

    checked = set()

    for (cell_x, cell_y), cell_asteroids in grid.items():
        neighbors = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                neighbor_key = (cell_x + dx, cell_y + dy)
                if neighbor_key in grid:
                    neighbors.extend(grid[neighbor_key])

        for a in cell_asteroids:
            for b in neighbors:
                if a is b:
                    continue

                pair = tuple(sorted((id(a), id(b))))
                if pair in checked:
                    continue
                checked.add(pair)

                if a.collides_with(b):
                    resolve_asteroid_collision(a, b)

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
        handle_asteroid_collisions(asteroids)
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
