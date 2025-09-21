import pygame, sys
from pygame.locals import *
import math
import random
from config import *


class Player():
    
    def __init__(self, health, speed, powerup_speed_multiplier):
        # Coordinates for centre of screen for position of player
        self.x = centre_x - (player_walk_images[0].get_width() / 2)
        self.y = centre_y  - (player_walk_images[0].get_height() / 2)

        # Pixel distances set for how far the player can walk (up to the edge of the map)
        self.border_x = (map_width / 2) - (player_walk_images[0].get_width() / 2)
        self.border_y = (map_height / 2) - (player_walk_images[0].get_height() / 2)

        # Animation variables: animation_frames decides how fast the animation is i.e. how many frames of game should pass for one frame of animation
        self.animation_count = 0
        self.animation_frames = 8

        # Get state of the player for display purposes
        self.orientation = "right"
        self.moving_x = False
        self.moving_y = False

        self.health = health
        self.max_health = health
        self.speed = speed
        self.original_speed = speed
        self.powerup_speed_multiplier = powerup_speed_multiplier

        self.shield = False
        self.poison = False
    
    def get_borders(self):
        return {"x":self.border_x, "y":self.border_y}

    def get_speed(self):
        return self.speed
    
    def get_health(self):
        return self.health
    def set_health(self, new_health):
        self.health = new_health
    
    def get_orientation(self):
        return self.orientation
    def set_orientation(self, new_orientation):
        self.orientation = new_orientation
    
    def get_moving(self, axis):
        if axis == "x":
            return self.moving_x
        elif axis == "y":
            return self.moving_y

    def set_moving_x(self, new_moving_x):
        self.moving_x = new_moving_x
    def set_moving_y(self, new_moving_y):
        self.moving_y = new_moving_y

    def get_xy(self, axis):
        if axis == "x":
            return self.x
        elif axis == "y":
            return self.y


    def main(self, WINDOW):
        
        # Loops back round after animation count has reached the end to prevent index error
        if self.animation_count + 1 >= 2*self.animation_frames:
            self.animation_count = 0
        self.animation_count += 1

        # Checks orientation of player and flips the sprite horizontally accordingly
        if self.orientation == "right":
            # If the player is moving the sprite, play the animation at the speed decided
            if self.moving_x or self.moving_y:
                WINDOW.blit(player_walk_images[self.animation_count//self.animation_frames], (self.x, self.y))
            # Otherwise, just play the first frame to make it look like they are still
            else:
                WINDOW.blit(player_walk_images[0], (self.x, self.y))
        # Same for left
        elif self.orientation == "left":
            if self.moving_x or self.moving_y:
                WINDOW.blit(pygame.transform.flip(player_walk_images[self.animation_count//self.animation_frames], True, False), (self.x, self.y))
            else:
                WINDOW.blit(pygame.transform.flip(player_walk_images[0], True, False), (self.x, self.y))
        
        # If poison effect on, run poison overlay
        if self.poison:
            self.show_poison(WINDOW)

        # health bar coordinates
        self.health_bar_x = centre_x - int(health_bar_length/2)
        self.health_bar_y = self.y - health_bar_height - 2*health_bar_border
        # drawing on health bar, calculating length depending on proportion between max health and current health
        health_bar_circle = pygame.draw.circle(WINDOW, BLACK, (self.health_bar_x, self.health_bar_y + int(health_bar_height/2)), int(health_bar_height*0.8))
        self.health_px = int((self.health/self.max_health) * (health_bar_length - int(health_bar_circle.width/2)))
        pygame.draw.rect(WINDOW, BLACK, (self.health_bar_x, self.health_bar_y, health_bar_length, health_bar_height))
        pygame.draw.rect(WINDOW, GREEN, (self.health_bar_x + int(health_bar_circle.width/2), self.health_bar_y, self.health_px, health_bar_height))
        pygame.draw.rect(WINDOW, BLACK, (self.health_bar_x, self.health_bar_y, health_bar_length, health_bar_height), health_bar_border)
        # health bar text to display numerical health value
        health_text = tinyfont.render(str(self.health), True, WHITE)
        WINDOW.blit(health_text, (health_bar_circle.centerx - health_text.get_width()/2, health_bar_circle.centery - health_text.get_height()/2))
    
    def hitbox(self, WINDOW):
        if HITBOXES:
            pygame.draw.rect(WINDOW, (255,0,0), (self.x, self.y, player_walk_images[0].get_width(), player_walk_images[1].get_height()), 1)
        
        return pygame.Rect(self.x, self.y, player_walk_images[0].get_width(), player_walk_images[1].get_height())

    def show_poison(self, WINDOW):
        if self.orientation == "left":
            WINDOW.blit(pygame.transform.flip(player_img_poison, True, False), (self.x, self.y))
        elif self.orientation == "right":
            WINDOW.blit(player_img_poison, (self.x, self.y))

    
    def speed_on(self):
        self.speed = int(self.original_speed * self.powerup_speed_multiplier)
    def speed_off(self):
        self.speed = self.original_speed

    def get_shield_status(self):
        return self.shield
    def shield_on(self):
        self.shield = True
    def shield_off(self):
        self.shield = False

    def get_poison_status(self):
        return self.poison
    def poison_on(self):
        self.poison = True
    def poison_off(self):
        self.poison = False


class BasicEnemy():

    def __init__(self, speed, health, damage, damage_speed, sprite_img):
        
        # Pass in the image of the sprite, since there will be multiple enemy types so each will need its own sprite image
        self.sprite_img = sprite_img
        
        # Border attributes to ensure enemies don't leave the map
        self.border_x = int(map_width / 2) - (int(self.sprite_img.get_width() / 2))
        self.border_y = int(map_height / 2) - (int(self.sprite_img.get_height() / 2))

        # Initialise a random position on the map to spawn the enemy
        self.x = random.randint(centre_x - self.border_x, centre_x + self.border_x)
        self.y = random.randint(centre_y - self.border_y, centre_y + self.border_y)

        # Basic attributes for enemy
        self.speed = speed
        self.health = health
        self.max_health = health
        self.damage = damage
        self.damage_speed = damage_speed
        self.damage_delay_timer = 0

        # Offset attributes to give the enemy a strafing ability (preventing enemies all piling on top of each other)
        self.reset_offset = 0
        self.offset_x = random.randint(-300, 300)
        self.offset_y = random.randint(-300, 300)

        self.frozen = False


    def main(self, WINDOW, camera_scroll):
        
        if self.reset_offset == 0:
            self.offset_x = random.randint(-300, 300)
            self.offset_y = random.randint(-300, 300)
            self.reset_offset = random.randint(int(FPS*reset_offset_timer), int(FPS*reset_offset_timer + FPS))
        else:
            self.reset_offset -= 1

        self.direction = None

        # If frozen effect is false, let the enemies move
        if self.frozen == False:
            if self.x < centre_x + self.offset_x + camera_scroll[0] and self.x < centre_x + self.border_x:
                self.x += self.speed
            elif self.x > centre_x + self.offset_x + camera_scroll[0] and self.x > centre_x - self.border_x:
                self.x -= self.speed
            if self.y < centre_y + self.offset_y + camera_scroll[1] and self.y < centre_y + self.border_y:
                self.y += self.speed
            elif self.y > centre_y + self.offset_y + camera_scroll[1] and self.y > centre_y - self.border_y:
                self.y -= self.speed
                
        
        WINDOW.blit(self.sprite_img, (self.x - camera_scroll[0] - (self.sprite_img.get_width() / 2), self.y - camera_scroll[1] - (self.sprite_img.get_height() / 2)))

        # health bar coordinates
        self.health_bar_x = self.x - camera_scroll[0] - int(health_bar_length/2)
        self.health_bar_y = self.y - camera_scroll[1] - (self.sprite_img.get_height()/2) - health_bar_height - 2*health_bar_border
        # drawing on health bar, calculating length depending on proportion between max health and current health
        health_bar_circle = pygame.draw.circle(WINDOW, BLACK, (self.health_bar_x, self.health_bar_y + int(health_bar_height/2)), int(health_bar_height*0.8))
        self.health_px = int((self.health/self.max_health) * (health_bar_length - int(health_bar_circle.width/2)))
        pygame.draw.rect(WINDOW, BLACK, (self.health_bar_x, self.health_bar_y, health_bar_length, health_bar_height))
        pygame.draw.rect(WINDOW, RED, (self.health_bar_x + int(health_bar_circle.width/2), self.health_bar_y, self.health_px, health_bar_height))
        pygame.draw.rect(WINDOW, BLACK, (self.health_bar_x, self.health_bar_y, health_bar_length, health_bar_height), health_bar_border)
        # health bar text to display numerical health value
        health_text = tinyfont.render(str(self.health), True, WHITE)
        WINDOW.blit(health_text, (health_bar_circle.centerx - health_text.get_width()/2, health_bar_circle.centery - health_text.get_height()/2))
    
    def hitbox(self, WINDOW, camera_scroll):
        
        if HITBOXES:
            pygame.draw.rect(WINDOW, (255,0,0), (self.x - camera_scroll[0] - (self.sprite_img.get_width() / 2), 
                                                self.y - camera_scroll[1] - (self.sprite_img.get_height() / 2), 
                                                self.sprite_img.get_width(), self.sprite_img.get_height()), 1)
        
        return pygame.Rect(self.x - camera_scroll[0] - (self.sprite_img.get_width() / 2), self.y - camera_scroll[1] - (self.sprite_img.get_height() / 2), self.sprite_img.get_width(), self.sprite_img.get_height())

    def identify(self):
        return "basic"
    
    def get_health(self):
        return self.health
    def set_health(self, new_health):
        self.health = new_health

    def set_damage_delay_timer(self, new_damage_delay_timer):
        self.damage_delay_timer = new_damage_delay_timer
    def get_damage_delay_timer(self):
        return self.damage_delay_timer
    
    def get_damage(self):
        return self.damage
    
    def get_damage_speed(self):
        return self.damage_speed

    def get_xy(self, axis, camera_scroll):
        if axis == "x":
            return self.x - camera_scroll[0] - (self.sprite_img.get_width() / 2)
        elif axis == "y":
            return self.y - camera_scroll[1] - (self.sprite_img.get_height() / 2)

    def get_sprite_img(self):
        return self.sprite_img
    
    def get_frozen_status(self):
        if self.frozen == True:
            return True
        else:
            return False

    def freeze_on(self):
        self.frozen = True
    def freeze_off(self):
        self.frozen = False


class ShooterEnemy(BasicEnemy):

    def __init__(self, speed, health, damage, damage_speed, projectile_freq, sprite_img):
        super().__init__(speed, health, damage, damage_speed, sprite_img)

        self.projectile_freq = projectile_freq
        self.projectile_cooldown = projectile_freq
    
    def get_projectile_freq(self):
        return self.projectile_freq
    
    def get_projectile_cooldown(self):
        return self.projectile_cooldown
    def set_projectile_cooldown(self, new_projectile_cooldown):
        self.projectile_cooldown = new_projectile_cooldown
    
    def identify(self):
        return "shooter"


class PlayerProjectile():

    def __init__(self, cursor_x, cursor_y, speed, damage, sprite_img):

        self.speed = speed
        self.damage = damage
        self.despawn_range = 500

        self.sprite_img = sprite_img

        self.x = centre_x
        self.y = centre_y
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        self.dxdy = self.calc_trajectory()
        
    
    def calc_trajectory(self):
        self.angle = math.atan2(self.y - self.cursor_y, self.x - self.cursor_x)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        return [self.dx, self.dy]
    

    def main(self, WINDOW, projectilekey, controls, player_speed, is_moving_x, is_moving_y):
        
        self.x -= int(self.dxdy[0])
        self.y -= int(self.dxdy[1])

        if is_moving_x:
            if (projectilekey[pygame.K_a] and controls == "WASD") or (projectilekey[pygame.K_LEFT] and controls == "arrows"):
                self.x += player_speed
            if (projectilekey[pygame.K_d] and controls == "WASD") or (projectilekey[pygame.K_RIGHT] and controls == "arrows"):
                self.x -= player_speed
        if is_moving_y:
            if (projectilekey[pygame.K_w] and controls == "WASD") or (projectilekey[pygame.K_UP] and controls == "arrows"):
                self.y += player_speed
            if (projectilekey[pygame.K_s] and controls == "WASD") or (projectilekey[pygame.K_DOWN] and controls == "arrows"):
                self.y -= player_speed

        pygame.draw.circle(WINDOW, self.sprite_img, (self.x, self.y), projectile_size)
    
    def get_damage(self):
        return self.damage
    
    def get_xy(self, axis):
        if axis == "x":
            return self.x
        elif axis == "y":
            return self.y
    
    def get_despawn_range(self):
        return self.despawn_range

    def identify(self):
        return "player"


class EnemyProjectile(PlayerProjectile):
    
    def __init__(self, speed, damage, origin_x, origin_y, sprite_img):
        super().__init__(0, 0, speed, damage, sprite_img)
        self.despawn_range = 500

        self.x = origin_x
        self.y = origin_y

        self.dxdy = self.calc_trajectory()

    def calc_trajectory(self):
        self.angle = math.atan2(self.y - centre_y, self.x - centre_x)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        return [self.dx, self.dy]

    def identify(self):
        return "enemy"
    

class Powerup():
    
    def __init__(self, powerup_id):
        # Powerup ID determines which powerup this powerup object is and picks out the relevant icon for it
        self.powerup_id = powerup_id
        self.sprite_icon = powerup_icons[powerup_id]
        self.sprite_icon = pygame.transform.scale(self.sprite_icon, (powerup_size, powerup_size))

        self.border_x = int((map_width / 2)) - int((powerup_size / 2))
        self.border_y = int((map_height / 2)) - int((powerup_size / 2))
        self.x = random.randint(centre_x - self.border_x, centre_x + self.border_x)
        self.y = random.randint(centre_y - self.border_y, centre_y + self.border_y)

        # Timer to control when to despawn
        self.timer = 0
    
    def main(self, WINDOW, camera_scroll, powerup_lifetime):
        # Allow it to flash right before it disappears, like a fading effect almost
        if (self.timer > FPS*(powerup_lifetime - 1) and self.timer < int(FPS*(powerup_lifetime - 0.5)) or 
            self.timer > FPS*(powerup_lifetime - 2) and self.timer < int(FPS*(powerup_lifetime - 1.5)) or 
            self.timer > FPS*(powerup_lifetime - 3) and self.timer < int(FPS*(powerup_lifetime - 2.5))):
            return

        WINDOW.blit(self.sprite_icon, (self.x - camera_scroll[0] - (powerup_size/2), self.y - camera_scroll[1] - (powerup_size/2)))
        
    def hitbox(self, WINDOW, camera_scroll):
        if HITBOXES:
            pygame.draw.rect(WINDOW, (255,0,0), (self.x - camera_scroll[0] - (powerup_size/2), 
                                                self.y - camera_scroll[1] - (powerup_size/2), 
                                                powerup_size, powerup_size), 1)
        
        return pygame.Rect(self.x - camera_scroll[0] - (powerup_size/2), self.y - camera_scroll[1] - (powerup_size/2), powerup_size, powerup_size)

    def identify(self):
        return self.powerup_id
    
    def get_timer(self):
        return self.timer
    def set_timer(self, new_time):
        self.timer = new_time

    # Health is a special powerup since it does not get applied over a period of time, it is just straight away used up when collected, so this method is in this class instead
    def health(self, player, powerup_health_boost):
        player.health += powerup_health_boost
        if player.health > player.max_health:
            player.health = player.max_health


class ActivePowerups():
    def __init__(self, active_powerups):
        self.active_powerups = active_powerups
    
    def main(self, WINDOW, powerup_duration):
        # Number of active powerups for active icon formatting
        self.num_active_powerups = 0
        for powerup in self.active_powerups:
            if self.active_powerups[powerup]["active"]:
                self.display_icon(WINDOW, powerup, self.num_active_powerups, self.active_powerups[powerup]["timer"], powerup_duration)
                self.num_active_powerups += 1
                # Timer for powerups incrementing
                self.active_powerups[powerup]["timer"] += 1
                if self.active_powerups[powerup]["timer"] >= FPS*powerup_duration:
                    self.active_powerups[powerup]["active"] = 0
                    self.active_powerups[powerup]["timer"] = 0
        
    def activate_powerups(self, player, enemies):
        # Speed powerup
        if self.active_powerups["speed"]["active"]:
            player.speed_on()
        else:
            player.speed_off()
        # Shield powerup
        if self.active_powerups["shield"]["active"]:
            player.shield_on()
        else:
            player.shield_off()
        # Poison powerup
        if self.active_powerups["poison"]["active"]:
            player.poison_on()
        else:
            player.poison_off()
        # Freeze powerup
        if self.active_powerups["freeze"]["active"]:
            for enemy in enemies:
                enemy.freeze_on()
        else:
            for enemy in enemies:
                enemy.freeze_off()

    def display_icon(self, WINDOW, powerup_id, num_active_powerups, timer, powerup_duration):
        # Display all active powerups as large icons in the corner, along with how long it has left
        active_powerup_icon = pygame.transform.scale(powerup_icons[powerup_id], (active_powerup_size, active_powerup_size))
        active_powerup_blit = WINDOW.blit(active_powerup_icon, (int(window_width*0.01) + (num_active_powerups*(active_powerup_size+20)), int(window_width*0.01)))
        timer_display = smallfont.render(str(int(((FPS*powerup_duration - timer)/FPS) + 1)), True, (0,0,0))
        timer_card = pygame.draw.rect(WINDOW, GRAY, (active_powerup_blit.centerx - active_powerup_blit.width/4, active_powerup_blit.bottom + int(window_width*0.01), active_powerup_blit.width/2, timer_display.get_height()))
        pygame.draw.rect(WINDOW, BLACK, (timer_card.left - int(UI_border/2), timer_card.top - int(UI_border/2), timer_card.width + int(UI_border/2)*2, timer_card.height + int(UI_border/2)*2), int(UI_border/2))
        WINDOW.blit(timer_display, (timer_card.centerx - timer_display.get_width()/2, timer_card.centery - timer_display.get_height()/2))


class Coin():
    def __init__(self, x, y, set_coin_img):
        self.x = x
        self.y = y
        self.coin_img = set_coin_img
    
    def main(self, WINDOW, camera_scroll):
        WINDOW.blit(self.coin_img, (self.x - camera_scroll[0], self.y - camera_scroll[1]))

    def hitbox(self, WINDOW, camera_scroll):
        if HITBOXES:
            pygame.draw.rect(WINDOW, (255,0,0), (self.x - camera_scroll[0] - (self.coin_img.get_width() / 2), 
                                                self.y - camera_scroll[1] - (self.coin_img.get_height() / 2), 
                                                self.coin_img.get_width(), self.coin_img.get_height()), 1)
        
        return pygame.Rect(self.x - camera_scroll[0] - (self.coin_img.get_width() / 2), self.y - camera_scroll[1] - (self.coin_img.get_height() / 2), self.coin_img.get_width(), self.coin_img.get_height())