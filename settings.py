# -*- coding: utf-8 -*-
"""
Created on Mon May 21 14:25:41 2018

@author: Administrator
"""

import random
class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 1000    
        self.fleet_drop_speed = 10
        self.ship_limit = 3
        self.score_scala = 1.5
        
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        self.pill_speed_factor = 1.5
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points= 50
        self.bullet_color = 60, 60, 60
        self.bullet_width = 10
        self.bullet_height = 15
        
    def increase_speed(self):
        self.ship_speed_factor += 0.2
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale 
        self.alien_points = int(self.alien_points * self.score_scala)
        
        
    def change_bullet(self):
        self.bullet_color = random.randint(1,255), random.randint(1,255), random.randint(1,255)
        self.bullet_height += 10