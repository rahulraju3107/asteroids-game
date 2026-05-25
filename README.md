# Asteroids

A classic Asteroids arcade game built with Python and Pygame. Navigate your ship through an asteroid field, shoot to survive, and rack up the highest score you can.

## Features

- Player-controlled ship with rotation and forward/reverse thrust
- Asteroids that split into smaller, faster fragments when shot
- Score system with bonus points for smaller asteroids
- 3 lives with brief invincibility on respawn
- Increasing difficulty as time progresses
- Particle effects on asteroid destruction
- Screen wrapping for seamless movement
- Game over screen with restart support

## Controls

| Key | Action |
|-----|--------|
| W | Thrust forward |
| S | Thrust backward |
| A | Rotate left |
| D | Rotate right |
| Space | Shoot |
| Enter | Restart (game over screen) |
| ESC | Quit (game over screen) |

## Setup

Requires Python 3.11+ and [uv](https://github.com/astral-sh/uv).

```bash
uv sync
uv run main.py
```
