# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:26:14 2018

@author: Administrator
"""

class GameStats():
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        
        a = open('high_score.txt')
        b = a.read()
        self.high_score = int(b)
    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1