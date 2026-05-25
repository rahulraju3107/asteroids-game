import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 24)

    running = True
    while running:
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        Asteroid.containers = (asteroids, updatable, drawable)
        Shot.containers = (shots, updatable, drawable)
        Player.containers = (updatable, drawable)
        AsteroidField.containers = (updatable,)

        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField()

        score = 0
        dt = 0
        game_over = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = "restart"
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            if not running:
                break
            if game_over == "restart":
                break

            if not game_over:
                updatable.update(dt)

                for asteroid in asteroids:
                    if player.invincibility_timer <= 0 and asteroid.collision(player):
                        player.lives -= 1
                        if player.lives > 0:
                            player.respawn()
                        else:
                            game_over = True
                            break

                    for shot in shots:
                        if asteroid.collision(shot):
                            shot.kill()
                            score += asteroid.get_score()
                            asteroid.split()
                            break

            screen.fill((0, 0, 0))

            if game_over:
                game_over_text = font.render("GAME OVER", True, (255, 255, 255))
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                restart_text = font.render("ENTER to restart / ESC to quit", True, (150, 150, 150))
                screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30)))
                screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)))
                screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 45)))
            else:
                for d in drawable:
                    d.draw(screen)
                score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
                lives_surface = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
                screen.blit(score_surface, (10, 10))
                screen.blit(lives_surface, (10, 45))

            pygame.display.flip()
            dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
