# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:10:23 2018

@author: Administrator
"""

import pygame
from pygame.sprite import Sprite 
import random

class Pill(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen 
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.image = pygame.image.load('image/pill.bmp')
        self.rect = self.image.get_rect()
       
        self.rect.centerx = random.randint(50,1000)
        self.rect.top = -70
        self.y = float(self.rect.y)
        self.apperence = True
        
    
    def update(self):
        self.y += self.ai_settings.pill_speed_factor
        self.rect.y = self.y
        
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        
    def back(self):
        self.rect.centerx = random.randint(50,1000)
        self.y = - random.randint(1000,5000)
        self.rect.y = self.y
   
        