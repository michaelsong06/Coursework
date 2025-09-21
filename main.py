#imports
import pygame, sys
from pygame.locals import *
import json
from sprites import *
from config import *

# Initialise pygame and basic pygame variables
pygame.init()
clock = pygame.time.Clock()

# Create window
pygame.display.set_caption("NEA")

class GameState():

    def __init__(self):

        self.state = "main_menu"

        self.difficulty = "easy"
        self.mode = "timed"
        self.theme = theme_options[0]

        self.controls = "WASD"

        self.timer = 0
        self.score_count = 0
        self.coins = 0
        self.died = False

        pygame.mixer.music.play(-1)

    def main_menu(self):
        
        # Get save.json for coins
        with open("save.json", "r") as read_save:
            save = json.load(read_save)

        while True:
            pygame.display.update()
            # bg colour
            WINDOW.blit(menubg, (0,0))

            # Player and gun
            player_menu_icon = WINDOW.blit(player_menu_img, (int(window_width*0.2), int(window_height*0.4)))
            WINDOW.blit(pygame.transform.rotate(gun_img, -20), (player_menu_icon.centerx - player_menu_icon.width/1.3, player_menu_icon.centery - player_menu_icon.height/2.2))

            # Piggy bank
            piggy_icon = WINDOW.blit(piggy_img, (int(window_width*0.05), int(window_height*0.7)))
            coins_text = smallfont.render(str(save["coins"]), True, BLACK)
            WINDOW.blit(coins_text, (piggy_icon.centerx, piggy_icon.centery - coins_text.get_height()/2))

            # title
            title_card = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.1), int(window_width*0.4), int(window_height*0.15)))
            title_text = mediumfont.render("SHOOTER GAME", True, BLACK)
            WINDOW.blit(title_text, (title_card.centerx - title_text.get_width()/2, title_card.centery - title_text.get_height()/2))

            # play button
            play_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.6), int(window_height*0.35), int(window_width*0.2), int(window_height*0.15)))
            play_text = smallfont.render("PLAY", True, BLACK)
            WINDOW.blit(play_text, (play_button.centerx - play_text.get_width()/2, play_button.centery - play_text.get_height()/2))

            # settings button
            options_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.6), int(window_height*0.55), int(window_width*0.2), int(window_height*0.15)))
            options_text = smallfont.render("OPTIONS", True, BLACK)
            WINDOW.blit(options_text, (options_button.centerx - options_text.get_width()/2, options_button.centery - options_text.get_height()/2))

            # quit button
            quit_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.6), int(window_height*0.75), int(window_width*0.2), int(window_height*0.15)))
            quit_text = smallfont.render("QUIT", True, BLACK)
            WINDOW.blit(quit_text, (quit_button.centerx - quit_text.get_width()/2, quit_button.centery - quit_text.get_height()/2))

            # Checking for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Checking for cursor coordinates
                cursor = pygame.mouse.get_pos()

                # Checking for clicks on each button and changing the state accordingly
                if play_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "dif_mode_menu"
                        return
                if options_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "options"
                        return
                if quit_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "quit"
                        return
            
            clock.tick(FPS)

    def options(self):

        while True:
            pygame.display.update()

            # bg colour
            WINDOW.blit(menubg, (0,0))

            # title
            options_card = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.1), int(window_width*0.4), int(window_height*0.15)))
            options_text = mediumfont.render("OPTIONS", True, BLACK)
            WINDOW.blit(options_text, (options_card.centerx - options_text.get_width()/2, options_card.centery - options_text.get_height()/2))

            # shop
            shop_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.4), int(window_height*0.35), int(window_width*0.2), int(window_height*0.15)))
            shop_text = smallfont.render("SHOP", True, BLACK)
            WINDOW.blit(shop_text, (shop_button.centerx - shop_text.get_width()/2, shop_button.centery - shop_text.get_height()/2))

            # HTP
            htp_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.55), int(window_width*0.175), int(window_height*0.15)))
            htp_text = smallfont.render("HOW TO PLAY", True, BLACK)
            WINDOW.blit(htp_text, (htp_button.centerx - htp_text.get_width()/2, htp_button.centery - htp_text.get_height()/2))

            # Controls
            controls_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.525), int(window_height*0.55), int(window_width*0.175), int(window_height*0.15)))
            controls_instruction = tinyfont.render("CONTROL SETTINGS (click to toggle)", True, BLACK)
            WINDOW.blit(controls_instruction, ((controls_button.centerx - controls_instruction.get_width()/2, controls_button.top + controls_button.height/5)))
            controls_text = smallfont.render(self.controls, True, BLACK)
            WINDOW.blit(controls_text, (controls_button.centerx - controls_text.get_width()/2, controls_button.centery))

            # back
            back_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.4), int(window_height*0.75), int(window_width*0.2), int(window_height*0.15)))
            back_text = smallfont.render("BACK", True, BLACK)
            WINDOW.blit(back_text, (back_button.centerx - back_text.get_width()/2, back_button.centery - back_text.get_height()/2))

            # Checking for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Checking for cursor coordinates
                cursor = pygame.mouse.get_pos()

                # Checking for clicks on each button and changing the state accordingly
                if shop_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "shop"
                        return
                if htp_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "htp"
                        return
                if controls_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        if self.controls == "WASD":
                            self.controls = "arrows"
                        elif self.controls == "arrows":
                            self.controls = "WASD"
                if back_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "main_menu"
                        return
            
            clock.tick(FPS)

    def shop(self):

        while True:
            pygame.display.update()

            # bg colour
            WINDOW.blit(menubg, (0,0))

            # title
            shop_card = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.1), int(window_width*0.4), int(window_height*0.15)))
            shop_text = mediumfont.render("SHOP", True, BLACK)
            WINDOW.blit(shop_text, (shop_card.centerx - shop_text.get_width()/2, shop_card.centery - shop_text.get_height()/2))

            # sorry, nothing here yet
            sorry_text = mediumfont.render("Sorry, nothing in the shop yet...", True, BLACK)
            WINDOW.blit(sorry_text, (window_width/2 - sorry_text.get_width()/2, window_width/2 - sorry_text.get_width()/2))

            # back
            back_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.4), int(window_height*0.75), int(window_width*0.2), int(window_height*0.15)))
            back_text = smallfont.render("BACK", True, BLACK)
            WINDOW.blit(back_text, (back_button.centerx - back_text.get_width()/2, back_button.centery - back_text.get_height()/2))

            # Checking for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Checking for cursor coordinates
                cursor = pygame.mouse.get_pos()

                # Checking for clicks on each button and changing the state accordingly
                if back_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "options"
                        return
            
            clock.tick(FPS)

    def htp(self):

        current_page = 0

        while True:
            pygame.display.update()

            # bg colour
            WINDOW.blit(menubg, (0,0))

            # title
            htp_card = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.1), int(window_width*0.4), int(window_height*0.15)))
            htp_text = mediumfont.render("HOW TO PLAY", True, BLACK)
            WINDOW.blit(htp_text, (htp_card.centerx - htp_text.get_width()/2, htp_card.centery - htp_text.get_height()/2))

            # themes
            pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.3), int(window_width*0.4), int(window_height*0.4)))
            WINDOW.blit(htp_pages[current_page], (int(window_width*0.3125), int(window_height*0.325)))

            # arrows
            left_button = pygame.draw.polygon(WINDOW, WHITE, [[int(window_width*0.275), int(window_height*0.45)], 
                                                              [int(window_width*0.25), int(window_height*0.5)], 
                                                              [int(window_width*0.275), int(window_height*0.55)]])
            right_button = pygame.draw.polygon(WINDOW, WHITE, [[int(window_width*0.725), int(window_height*0.45)], 
                                                               [int(window_width*0.725), int(window_height*0.55)], 
                                                               [int(window_width*0.75), int(window_height*0.5)]])

            # back
            back_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.4), int(window_height*0.75), int(window_width*0.2), int(window_height*0.15)))
            back_text = smallfont.render("BACK", True, BLACK)
            WINDOW.blit(back_text, (back_button.centerx - back_text.get_width()/2, back_button.centery - back_text.get_height()/2))

            # Checking for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Checking for cursor coordinates
                cursor = pygame.mouse.get_pos()

                # Checking for clicks on each button and changing the state accordingly
                if left_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        if current_page != 0:
                            current_page -= 1
                        else:
                            current_page = htp_page_num - 1
                if right_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        if current_page != htp_page_num - 1:
                            current_page += 1
                        else:
                            current_page = 0
                if back_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "options"
                        return
            
            clock.tick(FPS)

    
    def dif_mode_menu(self):

        # Load save data
        with open("save.json", "r") as save_file:
            save = json.load(save_file)

        while True:
            pygame.display.update()

            # bg colour
            WINDOW.blit(menubg, (0,0))
            
            # title
            select_dif_mode_card = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.1), int(window_width*0.4), int(window_height*0.2)))
            select_dif_text = mediumfont.render("SELECT DIFFICULTY", True, BLACK)
            WINDOW.blit(select_dif_text, (select_dif_mode_card.centerx - select_dif_text.get_width()/2, select_dif_mode_card.centery - select_dif_text.get_height()/1.1))
            and_mode_text = mediumfont.render("AND GAME MODE", True, BLACK)
            WINDOW.blit(and_mode_text, (select_dif_mode_card.centerx - and_mode_text.get_width()/2, select_dif_mode_card.centery - and_mode_text.get_height()/20))

            # easy difficulty
            if self.difficulty == "easy":
                easy_button = pygame.draw.rect(WINDOW, GREEN, (int(window_width*0.325), int(window_height*0.35), int(window_width*0.1), int(window_height*0.15)))
            else:
                easy_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.325), int(window_height*0.35), int(window_width*0.1), int(window_height*0.15)))
            easy_text = smallfont.render("EASY", True, BLACK)
            WINDOW.blit(easy_text, (easy_button.centerx - easy_text.get_width()/2, easy_button.centery - easy_text.get_height()/2))
            # normal difficulty
            if self.difficulty == "normal":
                normal_button = pygame.draw.rect(WINDOW, GREEN, (int(window_width*0.45), int(window_height*0.35), int(window_width*0.1), int(window_height*0.15)))
            else:
                normal_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.45), int(window_height*0.35), int(window_width*0.1), int(window_height*0.15)))
            normal_text = smallfont.render("NORMAL", True, BLACK)
            WINDOW.blit(normal_text, (normal_button.centerx - normal_text.get_width()/2, normal_button.centery - normal_text.get_height()/2))
            # hard difficulty
            if self.difficulty == "hard":
                hard_button = pygame.draw.rect(WINDOW, GREEN, (int(window_width*0.575), int(window_height*0.35), int(window_width*0.1), int(window_height*0.15)))
            else:
                hard_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.575), int(window_height*0.35), int(window_width*0.1), int(window_height*0.15)))
            hard_text = smallfont.render("HARD", True, BLACK)
            WINDOW.blit(hard_text, (hard_button.centerx - hard_text.get_width()/2, hard_button.centery - hard_text.get_height()/2))

            # timed mode
            if self.mode == "timed":
                timed_button = pygame.draw.rect(WINDOW, GREEN, (int(window_width*0.325), int(window_height*0.55), int(window_width*0.1), int(window_height*0.15)))
            else:
                timed_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.325), int(window_height*0.55), int(window_width*0.1), int(window_height*0.15)))
            timed_text = smallfont.render("TIMED", True, BLACK)
            WINDOW.blit(timed_text, (timed_button.centerx - timed_text.get_width()/2, timed_button.top + int(timed_button.height*0.15)))
            high_score_text = tinyfont.render("High Score", True, BLACK)
            WINDOW.blit(high_score_text, (timed_button.centerx - high_score_text.get_width()/2, timed_button.top + int(timed_button.height*0.45)))
            high_score_value = smallfont.render(str(save["high-score"]), True, BLACK)
            WINDOW.blit(high_score_value, (timed_button.centerx - high_score_value.get_width()/2, timed_button.top + int(timed_button.height*0.6)))
            # scored mode
            if self.mode == "scored":
                scored_button = pygame.draw.rect(WINDOW, GREEN, (int(window_width*0.45), int(window_height*0.55), int(window_width*0.1), int(window_height*0.15)))
            else:
                scored_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.45), int(window_height*0.55), int(window_width*0.1), int(window_height*0.15)))
            scored_text = smallfont.render("SCORED", True, BLACK)
            WINDOW.blit(scored_text, (scored_button.centerx - scored_text.get_width()/2, scored_button.top + int(scored_button.height*0.15)))
            best_time_text = tinyfont.render("Best Time", True, BLACK)
            WINDOW.blit(best_time_text, (scored_button.centerx - best_time_text.get_width()/2, scored_button.top + int(scored_button.height*0.45)))
            if save["best-time"] is not None:
                best_time_value = smallfont.render(str(save["best-time"]) + "s", True, BLACK)
            else:
                best_time_value = smallfont.render("- - s", True, BLACK)
            WINDOW.blit(best_time_value, (scored_button.centerx - best_time_value.get_width()/2, scored_button.top + int(scored_button.height*0.6)))
            # endless mode
            if self.mode == "endless":
                endless_button = pygame.draw.rect(WINDOW, GREEN, (int(window_width*0.575), int(window_height*0.55), int(window_width*0.1), int(window_height*0.15)))
            else:
                endless_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.575), int(window_height*0.55), int(window_width*0.1), int(window_height*0.15)))
            endless_text = smallfont.render("ENDLESS", True, BLACK)
            WINDOW.blit(endless_text, (endless_button.centerx - endless_text.get_width()/2, endless_button.top + int(endless_button.height*0.15)))
            endless_high_score_text = tinyfont.render("High Score", True, BLACK)
            endless_high_score_text_blit = WINDOW.blit(endless_high_score_text, (endless_button.left + int(endless_button.width*0.1), endless_button.top + int(endless_button.height*0.45)))
            endless_longest_time_text = tinyfont.render("Longest Time", True, BLACK)
            endless_longest_time_text_blit = WINDOW.blit(endless_longest_time_text, (endless_button.left + int(endless_button.width*0.5), endless_button.top + int(endless_button.height*0.45)))
            endless_high_score_value = smallfont.render(str(save["endless"]["high-score"]), True, BLACK)
            WINDOW.blit(endless_high_score_value, (endless_high_score_text_blit.centerx - endless_high_score_value.get_width()/2, endless_button.top + int(endless_button.height*0.6)))
            endless_longest_time_value = smallfont.render(str(save["endless"]["best-time"]) + "s", True, BLACK)
            WINDOW.blit(endless_longest_time_value, (endless_longest_time_text_blit.centerx - endless_longest_time_value.get_width()/2, endless_button.top + int(endless_button.height*0.6)))

            # back
            back_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.75), int(window_width*0.125), int(window_height*0.15)))
            back_text = mediumfont.render("BACK", True, BLACK)
            WINDOW.blit(back_text, (back_button.centerx - back_text.get_width()/2, back_button.centery - back_text.get_height()/2))
            # continue
            continue_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.45), int(window_height*0.75), int(window_width*0.25), int(window_height*0.15)))
            continue_text = mediumfont.render("CONTINUE", True, BLACK)
            WINDOW.blit(continue_text, (continue_button.centerx - continue_text.get_width()/2, continue_button.centery - continue_text.get_height()/2))

            # Checking for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Checking for cursor coordinates
                cursor = pygame.mouse.get_pos()

                # Checking for clicks on each button and changing the settings accordingly
                if easy_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.difficulty = "easy"
                if normal_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.difficulty = "normal"
                if hard_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.difficulty = "hard"
                if timed_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.mode = "timed"
                if scored_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.mode = "scored"
                if endless_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.mode = "endless"
                if back_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "main_menu"
                        return
                if continue_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "theme_menu"
                        return
            
            clock.tick(FPS)

    def theme_menu(self):
        
        num_themes = len(theme_options)
        theme_index = 0
        
        while True:
            pygame.display.update()
            # bg colour
            WINDOW.blit(menubg, (0,0))

            # title
            select_world_card = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.1), int(window_width*0.4), int(window_height*0.15)))
            select_world_text = mediumfont.render("SELECT WORLD", True, BLACK)
            WINDOW.blit(select_world_text, (select_world_card.centerx - select_world_text.get_width()/2, select_world_card.centery - select_world_text.get_height()/2))
            # themes
            world_frame = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.3), int(window_width*0.4), int(window_height*0.4)))
            WINDOW.blit(theme_options[theme_index]["banner"], (int(window_width*0.325), int(window_height*0.35)))
            world_text = smallfont.render(theme_options[theme_index]["name"], True, BLACK)
            WINDOW.blit(world_text, (world_frame.centerx - world_text.get_width()/2, world_frame.top + int(world_frame.height*0.125/2) - world_text.get_height()/2))
            # arrows
            left_button = pygame.draw.polygon(WINDOW, WHITE, [[int(window_width*0.275), int(window_height*0.45)], 
                                                              [int(window_width*0.25), int(window_height*0.5)], 
                                                              [int(window_width*0.275), int(window_height*0.55)]])
            right_button = pygame.draw.polygon(WINDOW, WHITE, [[int(window_width*0.725), int(window_height*0.45)], 
                                                               [int(window_width*0.725), int(window_height*0.55)], 
                                                               [int(window_width*0.75), int(window_height*0.5)]])
            
            # back
            back_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.75), int(window_width*0.125), int(window_height*0.15)))
            back_text = mediumfont.render("BACK", True, BLACK)
            WINDOW.blit(back_text, (back_button.centerx - back_text.get_width()/2, back_button.centery - back_text.get_height()/2))
            # continue
            continue_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.45), int(window_height*0.75), int(window_width*0.25), int(window_height*0.15)))
            continue_text = mediumfont.render("CONTINUE", True, BLACK)
            WINDOW.blit(continue_text, (continue_button.centerx - continue_text.get_width()/2, continue_button.centery - continue_text.get_height()/2))

            # Checking for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Checking for cursor coordinates
                cursor = pygame.mouse.get_pos()

                # Checking for clicks on each button and changing the state accordingly
                if left_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        if theme_index != 0:
                            theme_index -= 1
                        else:
                            theme_index = num_themes - 1
                if right_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        if theme_index != num_themes - 1:
                            theme_index += 1
                        else:
                            theme_index = 0
                if back_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "dif_mode_menu"
                        return
                if continue_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        lets_roll_sound.play()
                        self.state = "main_game"
                        self.theme = theme_options[theme_index]
                        return
            
            clock.tick(FPS)

    def main_game(self):

        # Play bg music
        pygame.mixer.music.stop()
        self.theme["music"].play(-1)
        
        # Difficulty settings
        powerup_chance_freq = settings[self.difficulty]["powerup"]["chance-freq"]
        powerup_lifetime = settings[self.difficulty]["powerup"]["lifetime"]
        powerup_duration = settings[self.difficulty]["powerup"]["duration"]
        powerup_health_boost = settings[self.difficulty]["powerup"]["health-boost"]
        powerup_speed_multiplier = settings[self.difficulty]["powerup"]["speed-mult"]
        powerup_poison_damage = settings[self.difficulty]["powerup"]["poison-damage"]
        # Player attributes
        player_max_health = settings[self.difficulty]["player"]["max-health"]
        player_health = player_max_health
        player_speed = settings[self.difficulty]["player"]["speed"]
        player_proj_speed = settings[self.difficulty]["player"]["proj-speed"]
        player_proj_damage = settings[self.difficulty]["player"]["proj-damage"]
        # Enemy attributes
        basic_enemy_health = settings[self.difficulty]["enemy"]["basic"]["max-health"]
        basic_enemy_speed = settings[self.difficulty]["enemy"]["basic"]["speed"]
        basic_enemy_damage = settings[self.difficulty]["enemy"]["basic"]["damage"]
        shooter_enemy_health = settings[self.difficulty]["enemy"]["shooter"]["max-health"]
        shooter_enemy_speed = settings[self.difficulty]["enemy"]["shooter"]["speed"]
        shooter_enemy_damage = settings[self.difficulty]["enemy"]["shooter"]["damage"]
        shooter_enemy_proj_freq = settings[self.difficulty]["enemy"]["shooter"]["proj-freq"]
        shooter_enemy_proj_speed = settings[self.difficulty]["enemy"]["shooter"]["proj-speed"]
        shooter_enemy_proj_damage = settings[self.difficulty]["enemy"]["shooter"]["proj-damage"]

        # Images controlled by the selected theme
        mapimg = self.theme["map"]
        enemy_sprite = self.theme["enemies"]["basic"]
        shooter_sprite = self.theme["enemies"]["shooter"]

        player_footsteps = self.theme["footsteps"]
        footsteps = pygame.mixer.Channel(5)

        # Instantiate basic objects needed for game and create lists for arrays of objects
        player = Player(player_health, player_speed, powerup_speed_multiplier)
        enemies = []
        projectiles = []
        powerups = []
        powerups_status = {id: {"active": False, "timer": 0} for id in powerup_icons.keys() if id != "health"}
        coins = []

        # Initialize timer, score count and coin count to 0
        self.timer = 0
        self.score_count = 0
        self.coins = 0

        # Player not dead yet
        self.died = False

        # Camera scroll controls where the objects in the scene move depending on the direction the player moves in, since the camera follows the player
        camera_scroll = [0,0]

        # Initialize frame count for timer
        frames = 0

        # Initialize as unpaused
        paused = False

        # Main loop
        while True:
            pygame.display.update()

            # When the game isn't paused, run the main game code
            if not paused:
                
                # Make cursor invisible so we can blit the crosshair image instead
                pygame.mouse.set_visible(False)

                # Background image controlled by camera scroll, placement determined by background size and window size to ensure player spawns in the middle of the map
                WINDOW.fill(RED)
                WINDOW.blit(mapimg, (-(map_width - window_width)/2 - camera_scroll[0], -(map_height - window_height)/2 - camera_scroll[1]))

                # Checking for events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    # If player presses escape, pause the game
                    if event.type == pygame.KEYUP:
                        if event.key == K_ESCAPE:
                            paused = True

                    # Checking for cursor coordinates
                    cursor_x, cursor_y = pygame.mouse.get_pos()
                    # Checking if the player clicked mouse
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            # If so, append a projectile object to the list
                            projectiles.append(PlayerProjectile(cursor_x, cursor_y, speed=player_proj_speed, damage=player_proj_damage, sprite_img=RED))
                            gun_sound.play()

                # Checking for any keys pressed
                keys = pygame.key.get_pressed()

                #---------------------------------------------PLAYER/CONTROLS---------------------------------------------#

                # If any main controls are pressed, alter the camera scroll so the environment can move accordingly (in an inverted fashion)
                if (keys[pygame.K_a] and self.controls == "WASD") or (keys[pygame.K_LEFT] and self.controls == "arrows"):
                    if camera_scroll[0] > -player.get_borders()["x"]:
                        camera_scroll[0] -= player.get_speed()
                        # Also decide the direction the sprite surface is facing
                        player.set_orientation("left")
                        player.set_moving_x(True)
                    else:
                        player.set_moving_x(False)
                if (keys[pygame.K_d] and self.controls == "WASD") or (keys[pygame.K_RIGHT] and self.controls == "arrows"):
                    if camera_scroll[0] < player.get_borders()["x"]:
                        camera_scroll[0] += player.get_speed()
                        player.set_orientation("right")
                        player.set_moving_x(True)
                    else:
                        player.set_moving_x(False)
                if (keys[pygame.K_w] and self.controls == "WASD") or (keys[pygame.K_UP] and self.controls == "arrows"):
                    if camera_scroll[1] > -player.get_borders()["y"]:
                        camera_scroll[1] -= player.get_speed()
                        player.set_moving_y(True)
                    else:
                        player.set_moving_y(False)
                if (keys[pygame.K_s] and self.controls == "WASD") or (keys[pygame.K_DOWN] and self.controls == "arrows"):
                    if camera_scroll[1] < player.get_borders()["y"]:
                        camera_scroll[1] += player.get_speed()
                        player.set_moving_y(True)
                    else:
                        player.set_moving_y(False)
                
                # If the player isn't pressing any controls, the player is not moving
                if self.controls == "WASD":
                    if not(keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
                        player.set_moving_x(False)
                        player.set_moving_y(False)
                    else:
                        if not footsteps.get_busy():
                            footsteps.play(player_footsteps)
                elif self.controls == "arrows":
                    if not(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                        player.set_moving_x(False)
                        player.set_moving_y(False)

            
                # Run the main methods for all the main objects in the game
                player.main(WINDOW)
                player.hitbox(WINDOW)

                # If the health goes below 0, game over
                if player.get_health() <= 0:
                    print("YOU DIED")
                    self.state = "game_over"
                    self.died = True
                    pygame.mouse.set_visible(True)
                    return
                
                #---------------------------------------------ENEMIES---------------------------------------------#
                
                # Every {enemy_wave_period} seconds, spawn some random number of enemies, with a random number of basic and shooter enemies
                if self.timer % enemy_wave_period == 1 and len(enemies) < 1000:
                    if random.randint(0, enemy_num_chance) == 0:
                        if random.randint(0,1) == 0:
                            enemies.append(BasicEnemy(speed=basic_enemy_speed, health=basic_enemy_health, damage=basic_enemy_damage, damage_speed=enemy_damage_speed, sprite_img=enemy_sprite))
                        else:
                            enemies.append(ShooterEnemy(speed=shooter_enemy_speed, health=shooter_enemy_health, damage=shooter_enemy_damage, damage_speed=enemy_damage_speed, projectile_freq=shooter_enemy_proj_freq, sprite_img=shooter_sprite))

                if keys[pygame.K_m]:
                    enemies.append(BasicEnemy(speed=basic_enemy_speed, health=basic_enemy_health, damage=basic_enemy_damage, damage_speed=enemy_damage_speed, sprite_img=enemy_sprite))
                if keys[pygame.K_n]:
                    enemies.append(ShooterEnemy(speed=shooter_enemy_speed, health=shooter_enemy_health, damage=shooter_enemy_damage, damage_speed=enemy_damage_speed, projectile_freq=shooter_enemy_proj_freq, sprite_img=shooter_sprite))


                for enemy in enemies:
                    # If enemy health goes down to 0, add score to player's score count, delete the enemy, and drop coins
                    if enemy.get_health() <= 0:
                        enemy_death_sound.play()
                        self.score_count += settings[self.difficulty]["enemy"][enemy.identify()]["score"]
                        # Let each coin have some random variation to their spawnings so they don't all overlap each other
                        for i in range(coin_num):
                            coin_x = int(enemy.get_xy("x", camera_scroll) + camera_scroll[0])
                            coin_x = random.randint(coin_x - coin_spawn_range, coin_x + coin_spawn_range)
                            coin_y = int(enemy.get_xy("y", camera_scroll) + camera_scroll[1])
                            coin_y = random.randint(coin_y - coin_spawn_range, coin_y + coin_spawn_range)
                            coins.append(Coin(coin_x, coin_y, coin_img))
                        enemies.remove(enemy)
                    
                    # If any enemy collides with the player's hitbox, the player takes damage at a delayed interval
                    if enemy.hitbox(WINDOW, camera_scroll).colliderect(player.hitbox(WINDOW)):
                        
                        if enemy.get_damage_delay_timer() == 0:
                            if player.get_poison_status() == True:
                                enemy.set_health(enemy.get_health() - powerup_poison_damage)
                                enemy_damaged_sound.play()
                            else:
                                if player.get_shield_status() == False:
                                    player_damaged_sound.play()
                                    player.set_health(player.get_health() - enemy.get_damage())
                                
                        enemy.set_damage_delay_timer(enemy.get_damage_delay_timer() + 1)

                        if enemy.get_damage_delay_timer() >= FPS * enemy.get_damage_speed():
                            enemy.set_damage_delay_timer(0)
                    else:
                        enemy.set_damage_delay_timer(0)

                    enemy.main(WINDOW, camera_scroll)
                    
                    # If a shooter enemy's shooting cooldown runs out, fire another shot at the player
                    if enemy.identify() == "shooter":
                        if enemy.get_projectile_cooldown() == 0 and enemy.get_frozen_status() == False:
                            projectiles.append(EnemyProjectile(speed=shooter_enemy_proj_speed, damage=shooter_enemy_proj_damage, origin_x=enemy.get_xy("x", camera_scroll), origin_y=enemy.get_xy("y", camera_scroll), sprite_img=BLACK))
                        enemy.set_projectile_cooldown(enemy.get_projectile_cooldown() + 1)
                        if enemy.get_projectile_cooldown() >= FPS * enemy.get_projectile_freq():
                            enemy.set_projectile_cooldown(0)
                    
                #---------------------------------------------PROJECTILES---------------------------------------------# 

                for projectile in projectiles:
                    
                    projectile.main(WINDOW, keys, self.controls, player.get_speed(), player.get_moving("x"), player.get_moving("y"))

                    projectile_removed = False
                    # If any projectile hits an enemy's hitbox, remove both that enemy and that projectile from their corresponding lists
                    if projectile.identify() != "enemy":
                        for enemy in enemies:
                            if enemy.hitbox(WINDOW, camera_scroll).collidepoint(projectile.get_xy("x"), projectile.get_xy("y")):
                                enemy.set_health(enemy.get_health() - projectile.get_damage())
                                enemy_damaged_sound.play()
                                projectiles.remove(projectile)
                                projectile_removed = True
                                break
                    # But if it hits a player hitbox, deal damage to the player
                    else:
                        if player.hitbox(WINDOW).collidepoint(projectile.get_xy("x"), projectile.get_xy("y")):
                            if player.get_shield_status() == False:
                                player_damaged_sound.play()
                                player.set_health(player.get_health() - projectile.get_damage())
                            projectiles.remove(projectile)
                            projectile_removed = True
                
                    # Checks if the projectiles have gone out of range and delete them if so, to save memory
                    if ((projectile.get_xy("x") < -projectile.get_despawn_range()) or 
                        (projectile.get_xy("y") < -projectile.get_despawn_range()) or 
                        (projectile.get_xy("x") > window_width + projectile.get_despawn_range()) or 
                        (projectile.get_xy("y") > window_height + projectile.get_despawn_range())) and projectile_removed == False:
                        projectiles.remove(projectile)
                

                #---------------------------------------------POWERUPS/COINS--------------------------------------------#

                # Blit the freeze powerup overlay on the screen, and if the freeze runs out, play the unfreeze sound effect 1 second before
                if powerups_status["freeze"]["active"]:
                    WINDOW.blit(freeze_overlay, (0,0))
                if powerups_status["freeze"]["timer"] == powerup_duration*FPS - FPS:
                    unfreeze_sound.play()

                # If powerup is active, blit the shield to the screen
                if powerups_status["shield"]["active"]:
                    WINDOW.blit(shield_bubble, (int(window_width*0.5) - shield_bubble.get_width()/2, int(window_height*0.5) - shield_bubble.get_height()/2))
                # Start to play the unshield sound 1 second before it runs out, and stop the shield background sound right before it runs out
                if powerups_status["shield"]["timer"] == powerup_duration*FPS - FPS:
                    unshield_sound.play()
                if powerups_status["shield"]["timer"] == powerup_duration*FPS - 1:
                    shield_sound.stop()

                # At a random chance every frame, spawn a powerup
                if random.randint(1, FPS*powerup_chance_freq) == 1:
                    powerup_choice = Powerup(random.choice(list(powerup_icons.keys())))
                    powerups.append(powerup_choice)

                # Run the main for the existing powerups on the map
                for powerup in powerups:
                    powerup.main(WINDOW, camera_scroll, powerup_lifetime)
                    powerup.set_timer(powerup.get_timer() + 1)
                    # If the lifetime of the powerup runs out, remove it
                    if powerup.get_timer() >= FPS * powerup_lifetime:
                        powerups.remove(powerup)

                    # If the player collides with the powerup, remove it and make it active
                    if powerup.hitbox(WINDOW, camera_scroll).colliderect(player.hitbox(WINDOW)):
                        powerups.remove(powerup)
                        if powerup.identify() != "health":
                            powerups_status[powerup.identify()]["active"] = True
                            powerups_status[powerup.identify()]["timer"] = 0

                            if powerup.identify() == "speed":
                                speed_sound.play()
                            if powerup.identify() == "freeze":
                                freeze_sound.play()
                            if powerup.identify() == "shield":
                                shield_sound.stop()
                                shield_sound.play(-1, fade_ms=1000)
                            if powerup.identify() == "poison":
                                poison_sound.play()
                        else:
                            powerup.health(player, powerup_health_boost)
                            health_sound.play()
                
                # Display the active powerups as icons in the corner
                active_powerups = ActivePowerups(powerups_status)
                active_powerups.main(WINDOW, powerup_duration)
                active_powerups.activate_powerups(player, enemies)

                # Run the main for all existing coins on the map
                for coin in coins:
                    coin.main(WINDOW, camera_scroll)
                    # If player collides with coin, increment coin count
                    if coin.hitbox(WINDOW, camera_scroll).colliderect(player.hitbox(WINDOW)):
                        coin_sound.play()
                        coins.remove(coin)
                        self.coins += 1

                #---------------------------------------------GAME SETTINGS---------------------------------------------#

                # Timer
                frames += 1
                if frames % FPS == 0:
                    self.timer += 1
                    frames = 0

                # Displaying the timer, adding a number of 0s to the start to make it 3 digits
                time_card = pygame.draw.rect(WINDOW, GRAY, (int(window_width*0.9), 0, int(window_width*0.1), int(window_height*0.1)))
                pygame.draw.rect(WINDOW, BLACK, (int(window_width*0.9) - UI_border, -UI_border, int(window_width*0.1) + 2*UI_border, int(window_height*0.1) + 2*UI_border), UI_border)
                time_display = str(self.timer)
                if len(time_display) < 4:
                    zeros = (3 - len(time_display)) % 3
                    for i in range(zeros):
                        time_display = "0" + time_display
                time_blit = mediumfont.render(time_display, True, BLACK)
                WINDOW.blit(time_blit, (time_card.centerx - time_blit.get_width()/2, time_card.centery - time_blit.get_height()/2))

                # Display how many enemies are currently on the map
                enemy_count_card = pygame.draw.rect(WINDOW, GRAY, (int(window_width*0.35), 0, int(window_width*0.3), int(window_height*0.1)))
                pygame.draw.rect(WINDOW, BLACK, (int(window_width*0.35) - UI_border, -UI_border, int(window_width*0.3) + 2*UI_border, int(window_height*0.1) + 2*UI_border), UI_border)
                enemy_count_display = mediumfont.render("Enemies: " + str(len(enemies)), True, BLACK)
                WINDOW.blit(enemy_count_display, (enemy_count_card.centerx - enemy_count_display.get_width()/2, enemy_count_card.centery - enemy_count_display.get_height()/2))

                # Display Score
                score_card = pygame.draw.rect(WINDOW, GRAY, (int(window_width*0.85), int(window_height*0.8), int(window_width*0.15), int(window_height*0.2)))
                pygame.draw.rect(WINDOW, BLACK, (int(window_width*0.85) - UI_border, int(window_height*0.8) - UI_border, int(window_width*0.15) + 2*UI_border, int(window_height*0.2) + 2*UI_border), UI_border)
                score_display = largefont.render(str(self.score_count), True, BLACK)
                WINDOW.blit(score_display, (score_card.centerx - score_display.get_width()/2, score_card.top + int(score_card.height*0.3)))
                score_text = smallfont.render("SCORE", True, BLACK)
                WINDOW.blit(score_text, (score_card.centerx - score_text.get_width()/2, score_card.top + int(score_card.height*0.1)))

                # Displaying coin count
                coin_card = pygame.draw.rect(WINDOW, GRAY, (0, int(window_height*0.8), int(window_width*0.15), int(window_height*0.2)))
                pygame.draw.rect(WINDOW, BLACK, (-UI_border, int(window_height*0.8) - UI_border, int(window_width*0.15) + 2*UI_border, int(window_height*0.2) + 2*UI_border), UI_border)
                coin_count = largefont.render(str(self.coins), True, BLACK)
                WINDOW.blit(coin_count, (coin_card.centerx - coin_count.get_width()/2, coin_card.top + int(coin_card.height*0.3)))
                coin_text = smallfont.render("COINS", True, BLACK)
                WINDOW.blit(coin_text, (coin_card.centerx - coin_text.get_width()/2, coin_card.top + int(coin_card.height*0.1)))

                # Winning the game
                if self.mode == "timed":
                    if self.timer >= time_limit:
                        self.state = "game_over"
                        pygame.mouse.set_visible(True)
                        return
                elif self.mode == "scored":
                    if self.score_count >= score_goal:
                        self.state = "game_over"
                        pygame.mouse.set_visible(True)
                        return
                
                # Show cursor
                cursor_x, cursor_y = pygame.mouse.get_pos()
                WINDOW.blit(cursor_img, (cursor_x - cursor_img.get_width()/2, cursor_y - cursor_img.get_height()/2))

            # If player paused the game by pressing ESC
            else:
                
                pygame.mouse.set_visible(True)

                translucent = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
                translucent.fill((0,0,0,1))
                WINDOW.blit(translucent, (0,0))

                # Pause menu card
                pause_menu = pygame.draw.rect(WINDOW, BLACK, (int(window_width*0.35), int(window_height*0.3), int(window_width*0.3), int(window_height*0.4)))
                pause_title_card = pygame.draw.rect(WINDOW, WHITE, (int(pause_menu.left + pause_menu.width*0.1), int(pause_menu.top + pause_menu.height*0.1), int(pause_menu.width*0.8), int(pause_menu.height*0.3)))
                pause_text = mediumfont.render("PAUSED", True, BLACK)
                WINDOW.blit(pause_text, (pause_title_card.centerx - pause_text.get_width()/2, pause_title_card.centery - pause_text.get_height()/2))

                # Continue button
                cont_button = pygame.draw.rect(WINDOW, WHITE, (int(pause_menu.left + pause_menu.width*0.2), int(pause_menu.top + pause_menu.height*0.45), int(pause_menu.width*0.6), int(pause_menu.height*0.2)))
                cont_text = smallfont.render("CONTINUE GAME", True, BLACK)
                WINDOW.blit(cont_text, (cont_button.centerx - cont_text.get_width()/2, cont_button.centery - cont_text.get_height()/2))

                # Quit button
                quit_button = pygame.draw.rect(WINDOW, WHITE, (int(pause_menu.left + pause_menu.width*0.2), int(pause_menu.top + pause_menu.height*0.7), int(pause_menu.width*0.6), int(pause_menu.height*0.2)))
                quit_text = smallfont.render("QUIT GAME", True, BLACK)
                quit_text_disclaimer = tinyfont.render("Current game data will be lost!", True, BLACK)
                WINDOW.blit(quit_text, (quit_button.centerx - quit_text.get_width()/2, quit_button.centery - quit_text.get_height()/1.5))
                WINDOW.blit(quit_text_disclaimer, (quit_button.centerx - quit_text_disclaimer.get_width()/2, quit_button.centery + quit_text_disclaimer.get_height()/3))

                # Checking for events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    # Checking for cursor coordinates
                    cursor = pygame.mouse.get_pos()

                    # If player presses escape, unpause the game
                    if event.type == pygame.KEYUP:
                        if event.key == K_ESCAPE:
                            paused = False
                    
                    # Checking for clicks on each button and changing the state accordingly
                    if quit_button.collidepoint(cursor):
                        if event.type == MOUSEBUTTONDOWN:
                            pygame.mixer.stop()
                            guncock_sound.play()
                            pygame.mixer.music.play(-1)
                            self.state = "main_menu"
                            return
                    if cont_button.collidepoint(cursor):
                        if event.type == MOUSEBUTTONDOWN:
                            guncock_sound.play()
                            paused = False

            clock.tick(FPS)

    def game_over(self):

        new_high_score = False
        new_best_time = False

        pygame.mixer.stop()
        if self.died:
            lose_sound.play()
        else:
            win_sound.play()
        pygame.mixer.music.play(-1)
        
        # Updating high scores and best times if applicable
        if not self.died or self.mode == "endless":
            with open("save.json", "r") as update_save:
                update_data = json.load(update_save)
                # If mode is timed, update high score if high enough
                if self.mode == "timed":
                    if self.score_count > update_data["high-score"]:
                        update_data["high-score"] = self.score_count
                        new_high_score = True
                # If mode is scored, update best time if lower or not set yet
                elif self.mode == "scored":
                    if update_data["best-time"] is not None:
                        if self.timer < update_data["best-time"]:
                            update_data["best-time"] = self.timer
                            new_best_time = True
                    else:
                        update_data["best-time"] = self.timer
                        new_best_time = True
                # If mode is endless, update score or time if higher (extra section in json file)
                elif self.mode == "endless":
                    update_endless = [False, False]
                    if self.score_count > update_data["endless"]["high-score"]:
                        update_data["endless"]["high-score"] = self.score_count
                        new_high_score = True
                    if self.timer > update_data["endless"]["best-time"]:
                        update_data["endless"]["best-time"] = self.timer
                        new_best_time = True
            # dump this updated data into json
            with open("save.json", "w") as update_save:
                update_save.write(json.dumps(update_data))
        
        with open("save.json", "r") as update_save:
            save = json.load(update_save)
            save["coins"] += self.coins
        with open("save.json", "w") as add_coins:
            add_coins.write(json.dumps(save))

        while True:
            pygame.display.update()

            # bg colour
            WINDOW.blit(menubg, (0,0))

            # title
            title_card = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.3), int(window_height*0.1), int(window_width*0.4), int(window_height*0.15)))
            title_text = mediumfont.render(self.mode.upper() + " MODE", True, BLACK)
            WINDOW.blit(title_text, (title_card.centerx - title_text.get_width()/2, title_card.centery - title_text.get_height()/2))

            
            # Image of player either dead or holding a trophy
            if self.died:
                WINDOW.blit(player_dead_img, (int(window_width*0.2), int(window_height*0.4)))
                WINDOW.blit(largefont.render("YOU DIED", True, RED), (int(window_width*0.55), int(window_height*0.35)))
            else:
                player_menu_icon = WINDOW.blit(player_menu_img, (int(window_width*0.2), int(window_height*0.4)))
                WINDOW.blit(pygame.transform.rotate(trophy_img, (-30)), (player_menu_icon.centerx, player_menu_icon.centery))
                WINDOW.blit(largefont.render("YOU LIVED", True, GREEN), (int(window_width*0.54), int(window_height*0.35)))

            # Score/time from this game
            if new_high_score:
                WINDOW.blit(smallfont.render("New High Score!", True, RED), (int(window_width*0.55), int(window_height*0.5)))
            score_text = WINDOW.blit(mediumfont.render("Score", True, BLACK), (int(window_width*0.55), int(window_height*0.525)))
            score_display = mediumfont.render(str(self.score_count), True, BLACK)
            WINDOW.blit(score_display, (score_text.centerx - score_display.get_width()/2, int(window_height*0.61)))
            if new_best_time:
                WINDOW.blit(smallfont.render("New Best Time!", True, RED), (int(window_width*0.71), int(window_height*0.5)))
            time_text = WINDOW.blit(mediumfont.render("Time", True, BLACK), (int(window_width*0.72), int(window_height*0.525)))
            time_display = mediumfont.render(str(self.timer) + "s", True, BLACK)
            WINDOW.blit(time_display, (time_text.centerx - time_display.get_width()/2, int(window_height*0.61)))
            
            # Piggy bank
            piggy_icon = WINDOW.blit(piggy_img, (int(window_width*0.05), int(window_height*0.7)))
            coins_text = smallfont.render(str(save["coins"]), True, BLACK)
            WINDOW.blit(coins_text, (piggy_icon.centerx, piggy_icon.centery - coins_text.get_height()/2))
            earned_coins_text = mediumfont.render("+" + str(self.coins), True, BLACK)
            WINDOW.blit(earned_coins_text, (piggy_icon.centerx - earned_coins_text.get_width()/2, piggy_icon.top - earned_coins_text.get_height()))

            # Back to menu button
            menu_button = pygame.draw.rect(WINDOW, WHITE, (int(window_width*0.55), int(window_height*0.75), int(window_width*0.25), int(window_height*0.15)))
            menu_text = smallfont.render("BACK TO MAIN MENU", True, BLACK)
            WINDOW.blit(menu_text, (menu_button.centerx - menu_text.get_width()/2, menu_button.centery - menu_text.get_height()/2))

            # Checking for events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Checking for cursor coordinates
                cursor = pygame.mouse.get_pos()

                # Checking for clicks on each button and changing the state accordingly
                if menu_button.collidepoint(cursor):
                    if event.type == MOUSEBUTTONDOWN:
                        guncock_sound.play()
                        self.state = "main_menu"
                        return
            
            clock.tick(FPS)

    def run(self):
        
        match self.state:
            case "main_menu":
                self.main_menu()
            case "options":
                self.options()
            case "shop":
                self.shop()
            case "htp":
                self.htp()
            case "dif_mode_menu":
                self.dif_mode_menu()
            case "theme_menu":
                self.theme_menu()
            case "main_game":
                self.main_game()
            case "game_over":
                self.game_over()
            case "quit":
                pygame.quit()
                sys.exit()

game = GameState()
while True:
    game.run()

    