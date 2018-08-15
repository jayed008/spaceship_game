  # -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:52:59 2018

@author: Administrator
"""

#import sys
import pygame
from settings import Settings
from ship import Ship
#from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button 
from scoreboard import Scoreboard  
from pill import Pill

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion") 
    play_button = Button(screen, 'Play')
    stats = GameStats(ai_settings)
    sb = Scoreboard(screen, ai_settings, stats)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    pills = Pill(ai_settings, screen)
    gf.creat_fleet(ai_settings, screen, aliens)
    while True:
        gf.check_events(stats, play_button, aliens, bullets, 
                      ship, ai_settings, screen, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb)
            gf.update_aliens(ai_settings, aliens, ship, bullets, stats, screen, sb, pills)
            if pills.apperence:
                gf.update_pills(pills, ship, ai_settings, screen)
        gf.update_screen(ai_settings,stats,sb,screen,ship,bullets,
                         aliens,play_button, pills)  
        
run_game()
