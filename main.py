import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from highscores import load_scores, update_scores


def draw_title_screen(screen, font, title_font, player_name, difficulty_index, selected_row):
    screen.fill((0, 0, 0))

    title = title_font.render("A S T E R O I D S", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, 120)))

    cx = SCREEN_WIDTH / 2
    base_y = 250
    spacing = 50

    rows = [
        f"Name: {player_name}",
        f"Difficulty:  < {DIFFICULTY_OPTIONS[difficulty_index]} >",
        "Start Game",
        "High Scores",
        "Exit",
    ]

    # blinking cursor for name input
    if selected_row == 0:
        blink = pygame.time.get_ticks() // 500 % 2
        rows[0] = f"Name: {player_name}{'_' if blink else ' '}"

    for i, text in enumerate(rows):
        color = (255, 255, 255) if i == selected_row else (150, 150, 150)
        prefix = "> " if i == selected_row else "  "
        surface = font.render(prefix + text, True, color)
        screen.blit(surface, surface.get_rect(center=(cx, base_y + i * spacing)))


def draw_highscores_screen(screen, font, title_font, scores):
    screen.fill((0, 0, 0))

    title = title_font.render("HIGH SCORES", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, 120)))

    if not scores:
        empty = font.render("No scores yet.", True, (150, 150, 150))
        screen.blit(empty, empty.get_rect(center=(SCREEN_WIDTH / 2, 300)))
    else:
        header = font.render("  #  Name        Score   Date", True, (150, 150, 150))
        screen.blit(header, header.get_rect(center=(SCREEN_WIDTH / 2, 220)))

        for i, entry in enumerate(scores[:10]):
            line = f" {i + 1:>2}  {entry['name']:<10}  {entry['score']:<7} {entry['date']}"
            surface = font.render(line, True, (255, 255, 255))
            screen.blit(surface, surface.get_rect(center=(SCREEN_WIDTH / 2, 260 + i * 30)))

    back = font.render("ESC to go back", True, (150, 150, 150))
    screen.blit(back, back.get_rect(center=(SCREEN_WIDTH / 2, 600)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 24)
    title_font = pygame.font.SysFont("monospace", 48)

    running = True
    player_name = ""
    difficulty_index = 1

    while running:
        # --- TITLE SCREEN ---
        selected_row = 0
        viewing_highscores = False
        start_game = False

        while running and not start_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if event.type != pygame.KEYDOWN:
                    continue

                if viewing_highscores:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        viewing_highscores = False
                    continue

                if event.key == pygame.K_UP:
                    selected_row = max(0, selected_row - 1)
                elif event.key == pygame.K_DOWN:
                    selected_row = min(4, selected_row + 1)
                elif event.key == pygame.K_RETURN:
                    if selected_row == 0:
                        selected_row = 1
                    elif selected_row == 1:
                        selected_row = 2
                    elif selected_row == 2:
                        if player_name.strip():
                            start_game = True
                    elif selected_row == 3:
                        viewing_highscores = True
                    elif selected_row == 4:
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif selected_row == 0:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode and len(player_name) < 10:
                        if event.unicode.isalnum() or event.unicode == " ":
                            player_name += event.unicode
                elif selected_row == 1:
                    if event.key == pygame.K_LEFT:
                        difficulty_index = max(0, difficulty_index - 1)
                    elif event.key == pygame.K_RIGHT:
                        difficulty_index = min(2, difficulty_index + 1)

            if not running:
                break

            if viewing_highscores:
                draw_highscores_screen(screen, font, title_font, load_scores())
            else:
                draw_title_screen(screen, font, title_font, player_name, difficulty_index, selected_row)

            pygame.display.flip()
            clock.tick(60)

        if not running:
            break

        # --- GAME SESSION ---
        diff_name = DIFFICULTY_OPTIONS[difficulty_index]
        diff = DIFFICULTY_SETTINGS[diff_name]

        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        Asteroid.containers = (asteroids, updatable, drawable)
        Shot.containers = (shots, updatable, drawable)
        Player.containers = (updatable, drawable)
        AsteroidField.containers = (updatable,)

        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField(diff["spawn_rate_mult"], diff["speed_mult"])

        score = 0
        dt = 0
        game_over = False
        score_saved = False
        saved_scores = []
        player_rank = 0

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

            if game_over and not score_saved:
                saved_scores = update_scores(player_name, score)
                for i, entry in enumerate(saved_scores):
                    if entry["name"].lower() == player_name.lower():
                        player_rank = i + 1
                        break
                score_saved = True

            screen.fill((0, 0, 0))

            if game_over:
                y = SCREEN_HEIGHT / 2 - 80

                game_over_text = font.render("GAME OVER", True, (255, 255, 255))
                screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH / 2, y)))

                score_text = font.render(f"Score: {score}  (Rank #{player_rank})", True, (255, 255, 255))
                screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH / 2, y + 40)))

                divider = font.render("--- Top 5 ---", True, (150, 150, 150))
                screen.blit(divider, divider.get_rect(center=(SCREEN_WIDTH / 2, y + 90)))

                for i, entry in enumerate(saved_scores[:5]):
                    color = (255, 255, 255) if entry["name"].lower() == player_name.lower() else (150, 150, 150)
                    line = f"{i + 1}. {entry['name']:<10} {entry['score']}"
                    surface = font.render(line, True, color)
                    screen.blit(surface, surface.get_rect(center=(SCREEN_WIDTH / 2, y + 120 + i * 28)))

                restart_text = font.render("ENTER for title / ESC to quit", True, (150, 150, 150))
                screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH / 2, y + 290)))
            else:
                for d in drawable:
                    d.draw(screen)
                score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
                lives_surface = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
                diff_surface = font.render(diff_name, True, (150, 150, 150))
                screen.blit(score_surface, (10, 10))
                screen.blit(lives_surface, (10, 45))
                screen.blit(diff_surface, (SCREEN_WIDTH - diff_surface.get_width() - 10, 10))

            pygame.display.flip()
            dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
