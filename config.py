import pygame, sys
from pygame.locals import *
import os

pygame.init()

FPS = 60

# Screen Resolution
aspect_ratio = [16,9]
pixel_factor = 100
window_width, window_height = aspect_ratio[0] * pixel_factor, aspect_ratio[1] * pixel_factor

WINDOW = pygame.display.set_mode((window_width, window_height))

map_width, map_height = 4000,4000

# Fonts
pygame.font.init()
tinyfont = pygame.font.SysFont("Arial", int(pixel_factor/8))
smallfont = pygame.font.SysFont("Arial", int(pixel_factor/4))
mediumfont = pygame.font.SysFont("Arial", int(pixel_factor/1.5))
largefont = pygame.font.SysFont("Arial", int(pixel_factor))

# Colours
BLACK, WHITE = (0,0,0), (255,255,255)
GRAY = (100,100,130)
RED, GREEN, BLUE = (255,0,0), (0,255,0), (0,0,255)

# Music and Sounds
pygame.mixer.init()
lobby_music = pygame.mixer.music.load("assets/lobby_music.wav")
pygame.mixer.music.set_volume(0.3)

gun_sound = pygame.mixer.Sound("assets/gunshot.wav")
guncock_sound = pygame.mixer.Sound("assets/guncock.wav")
lets_roll_sound = pygame.mixer.Sound("assets/lets_roll.wav")
player_damaged_sound = pygame.mixer.Sound("assets/player_damaged_sound.wav")
enemy_damaged_sound = pygame.mixer.Sound("assets/enemy_damaged_sound.wav")
enemy_death_sound = pygame.mixer.Sound("assets/enemy_dead.wav")
win_sound = pygame.mixer.Sound("assets/game_lived.wav")
lose_sound = pygame.mixer.Sound("assets/game_died.wav")
health_sound = pygame.mixer.Sound("assets/health.wav")
speed_sound = pygame.mixer.Sound("assets/speed.wav")
shield_sound = pygame.mixer.Sound("assets/shield.wav")
unshield_sound = pygame.mixer.Sound("assets/unshield.wav")
freeze_sound = pygame.mixer.Sound("assets/freeze.wav")
unfreeze_sound = pygame.mixer.Sound("assets/unfreeze.wav")
poison_sound = pygame.mixer.Sound("assets/poison.wav")
coin_sound = pygame.mixer.Sound("assets/coin.wav")

menubg = pygame.transform.scale(pygame.image.load("assets/menubg.jpg"), (window_width, window_height))

UI_border = int(window_width/200)

enemy_size = int(window_width/24)

health_bar_length = int(window_width/20)
health_bar_height = int(window_width/80)
health_bar_border = int(health_bar_length/15)

time_limit = 120
score_goal = 200

htp_page_num = 14
htp_pages = []
for i in range(htp_page_num):
    htp_pages.append(pygame.transform.scale(pygame.image.load("assets/htp" + str(i + 1) + ".png").convert(), (int(window_width*0.375), int((window_height*0.35)))))

# 0: Grassland
# 1: Desert
# 2: City
# 3: Volcano
theme_options = {
    0: {
        "name": "GRASSLAND",
        "banner": pygame.transform.scale(pygame.image.load("assets/grassland_banner.jpg").convert(), (int(window_width*0.35), int((window_height*0.3)))),
        "map": pygame.transform.scale(pygame.image.load("assets/grassland_map.png").convert(), (map_width, map_height)),
        "enemies": {
            "basic": pygame.transform.scale(pygame.image.load("assets/enemy_sprite.png").convert_alpha(), (enemy_size, enemy_size)),
            "shooter": pygame.transform.scale(pygame.image.load("assets/shooter_enemy_sprite.png").convert_alpha(), (enemy_size, enemy_size))
        },
        "music": pygame.mixer.Sound("assets/grassland_bg.wav"),
        "footsteps": pygame.mixer.Sound("assets/footsteps_grass.wav")
    },
    1: {
        "name": "DESERT",
        "banner": pygame.transform.scale(pygame.image.load("assets/desert_banner.jpg").convert(), (int(window_width*0.35), int((window_height*0.3)))),
        "map": pygame.transform.scale(pygame.image.load("assets/desert_map.png").convert(), (map_width, map_height)),
        "enemies": {
            "basic": pygame.transform.scale(pygame.image.load("assets/enemy_sprite_desert.png").convert_alpha(), (enemy_size, enemy_size)),
            "shooter": pygame.transform.scale(pygame.image.load("assets/shooter_enemy_sprite_desert.png").convert_alpha(), (enemy_size, enemy_size))
        },
        "music": pygame.mixer.Sound("assets/desert_bg.wav"),
        "footsteps": pygame.mixer.Sound("assets/footsteps_grass.wav")
    },
    2: {
        "name": "CITY",
        "banner": pygame.transform.scale(pygame.image.load("assets/city_banner.jpg").convert(), (int(window_width*0.35), int((window_height*0.3)))),
        "map": pygame.transform.scale(pygame.image.load("assets/city_map.png").convert(), (map_width, map_height)),
        "enemies": {
            "basic": pygame.transform.scale(pygame.image.load("assets/enemy_sprite.png").convert_alpha(), (enemy_size, enemy_size)),
            "shooter": pygame.transform.scale(pygame.image.load("assets/shooter_enemy_sprite.png").convert_alpha(), (enemy_size, enemy_size))
        },
        "music": pygame.mixer.Sound("assets/grassland_bg.wav"),
        "footsteps": pygame.mixer.Sound("assets/footsteps_rock.wav")
    },
    3: {
        "name": "LAVA",
        "banner": pygame.transform.scale(pygame.image.load("assets/volcano_banner.png").convert(), (int(window_width*0.35), int((window_height*0.3)))),
        "map": pygame.transform.scale(pygame.image.load("assets/volcano_map.png").convert(), (map_width, map_height)),
        "enemies": {
            "basic": pygame.transform.scale(pygame.image.load("assets/enemy_sprite.png").convert_alpha(), (enemy_size, enemy_size)),
            "shooter": pygame.transform.scale(pygame.image.load("assets/shooter_enemy_sprite.png").convert_alpha(), (enemy_size, enemy_size))
        },
        "music": pygame.mixer.Sound("assets/volcano_bg.wav"),
        "footsteps": pygame.mixer.Sound("assets/footsteps_volcano.wav")
    }
}

# Player images
player_walk_images = [pygame.transform.scale(pygame.image.load("assets/player_sprite.png").convert_alpha(), (int(window_width/20), int(window_width/20))),
                      pygame.transform.scale(pygame.image.load("assets/player_sprite2.png").convert_alpha(), (int(window_width/20), int(window_width/20)))]
player_img_damaged = pygame.transform.scale(pygame.image.load("assets/player_sprite_damaged.png").convert_alpha(), (player_walk_images[0].get_width(), player_walk_images[0].get_height()))
player_img_poison = pygame.transform.scale(pygame.image.load("assets/player_sprite_poison.png").convert_alpha(), (player_walk_images[0].get_width(), player_walk_images[0].get_height()))
player_menu_img = pygame.transform.scale(player_walk_images[0], (int(window_width/4), int(window_width/4)))
player_dead_img = pygame.transform.scale(pygame.image.load("assets/player_dead.png").convert_alpha(), (int(window_width/4), int(window_width/4)))

# Menu images
gun_img = pygame.transform.scale(pygame.image.load("assets/gun.png").convert_alpha(), (int(window_width/3),int((window_width/3)/1.5)))
trophy_img = pygame.transform.scale(pygame.image.load("assets/trophy.png").convert_alpha(),(int(window_width/8),int(window_width/8)))
piggy_img = pygame.transform.scale(pygame.image.load("assets/piggybank.png").convert_alpha(), (int(window_width/8), int(window_width/12)))

# Coin images and settings
coin_img = pygame.transform.scale(pygame.image.load("assets/coin.png").convert_alpha(), (int(window_width/30), int(window_width/30)))
coin_num = 2
coin_spawn_range = 50

cursor_img = pygame.transform.scale(pygame.image.load("assets/cursor.png").convert_alpha(), (int(window_width/50), int(window_width/50)))

# Enemy AI coordinate offset timer
reset_offset_timer = 0.5
enemy_damage_speed = 0.5
enemy_wave_period = 6
enemy_num_chance = 8 # the higher the number, the smaller the number of enemies spawned

# Center of screen for player
centre_x = int(window_width / 2)
centre_y = int(window_height / 2)

# Display hitboxes for debugging
HITBOXES = False

# Icons for powerups
powerup_icons = {"health": pygame.image.load("assets/powerup_health.png").convert_alpha(),
                 "speed": pygame.image.load("assets/powerup_speed.png").convert_alpha(),
                 "shield": pygame.image.load("assets/powerup_shield.png").convert_alpha(),
                 "poison": pygame.image.load("assets/powerup_poison.png").convert_alpha(),
                 "freeze": pygame.image.load("assets/powerup_freeze.png").convert_alpha()}
powerup_size = int(window_width/25)
active_powerup_size = int(window_width/15)

shield_bubble = pygame.transform.scale(pygame.image.load("assets/shield_bubble.png").convert_alpha(), (int(window_width/8), int(window_width/8)))
freeze_overlay = pygame.transform.scale(pygame.image.load("assets/freeze_overlay.png").convert_alpha(), (window_width, window_height))

projectile_size = int(window_width/250)

settings = {
    "easy": {
        "player": {
            "max-health": 200,
            "speed": 10,
            "proj-speed": 30,
            "proj-damage": 10
        },
        "powerup": {
            "chance-freq": 2,
            "lifetime": 50,
            "duration": 10,
            "health-boost": 50,
            "speed-mult": 1.5,
            "poison-damage": 10
        },
        "enemy": {
            "basic": {
                "max-health": 50,
                "speed": 1,
                "damage": 10,
                "score": 5
            },
            "shooter": {
                "max-health": 80,
                "speed": 1,
                "damage": 10,
                "proj-freq": 5,
                "proj-speed": 5,
                "proj-damage": 10,
                "score": 10
            }
        }
    },
    "normal": {
        "player": {
            "max-health": 150,
            "speed": 10,
            "proj-speed": 30,
            "proj-damage": 10
        },
        "powerup": {
            "chance-freq": 4,
            "lifetime": 30,
            "duration": 10,
            "health-boost": 50,
            "speed-mult": 1.5,
            "poison-damage": 10
        },
        "enemy": {
            "basic": {
                "max-health": 100,
                "speed": 1,
                "damage": 10,
                "score": 10
            },
            "shooter": {
                "max-health": 150,
                "speed": 1,
                "damage": 10,
                "proj-freq": 5,
                "proj-speed": 5,
                "proj-damage": 20,
                "score": 20
            }
        }
    },
    "hard": {
        "player": {
            "max-health": 100,
            "speed": 10,
            "proj-speed": 30,
            "proj-damage": 10
        },
        "powerup": {
            "chance-freq": 6,
            "lifetime": 20,
            "duration": 10,
            "health-boost": 50,
            "speed-mult": 1.5,
            "poison-damage": 10
        },
        "enemy": {
            "basic": {
                "max-health": 150,
                "speed": 1,
                "damage": 20,
                "score": 20
            },
            "shooter": {
                "max-health": 200,
                "speed": 1,
                "damage": 20,
                "proj-freq": 5,
                "proj-speed": 5,
                "proj-damage": 20,
                "score": 30
            }
        }
    }
}

