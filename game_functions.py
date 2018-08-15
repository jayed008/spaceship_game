# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:15:05 2018

@author: Administrator
"""

import sys
import pygame
from bullet import Bullet
from alien import Alien
from ship import Ship
from time import sleep
import random


def check_keydown_events(event, ai_settings, screen, ship, bullets, sb):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        with open('high_score.txt', 'w') as f:
            f.write(str(sb.stats.high_score))
        f.close()
        sys.exit()
        
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_events(stats, play_button, aliens, bullets, 
                      ship, ai_settings, screen, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('high_score.txt', 'w') as f:
                f.write(str(sb.stats.high_score))
            f.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.K_SPACE:
            check_keydown_events(event, ai_settings, screen, ship, bullets, sb)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens,
                              bullets, ship, ai_settings, screen, sb)
            
def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, 
                      ship, ai_settings, screen, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        sb.perp_score()
        sb.perp_high_score()
        sb.perp_level()
        sb.perp_ships()
        aliens.empty()
        bullets.empty()
        creat_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        pygame.mouse.set_visible(False)
                

def update_screen(ai_settings, stats, sb, screen, ship, bullets, aliens, 
                  play_button, pills):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
#    alien.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pills.blitme()
    pygame.display.flip()
    
def creat_fleet(ai_settings, screen, aliens):
    alien = Alien(ai_settings, screen) 
    number_aliens_x  = get_number_aliens(alien, ai_settings)
    number_rows = get_number_rows(alien, ai_settings, screen)
    for row_number in range(int(number_rows / 2)):
        for aliens_number in range(int(number_aliens_x / 2)):
            creat_aliens(aliens_number, row_number, ai_settings, screen, 
                         aliens)
        
def get_number_aliens(alien, ai_settings):
    alien_width = alien.rect.width
    avalible_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = avalible_x/(2*alien_width)
    return number_aliens_x

def get_number_rows(alien, ai_settings, screen):
    alien_height = alien.rect.height
    ship = Ship(ai_settings, screen)
    ship_height = ship.rect.height
    avalible_y = ai_settings.screen_height - 3*alien_height - ship_height
    number_rows = int(avalible_y/(2*alien_height))
    return number_rows

    
def creat_aliens(alien_number, row_number, ai_settings, screen, aliens):
    
        alien = Alien(ai_settings, screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 4 * alien_width * alien_number + 2 * alien_width * random.uniform(0.00001,1)
        alien.rect.x = alien.x 
        alien.rect.y = 2 * alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)
    
   
   
def update_bullets(bullets, aliens, ai_settings, screen, ships, stats,
                   sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, bullets, aliens, stats,
                                  sb)
            
def check_bullet_alien_collisions(ai_settings, screen, bullets, aliens, stats, 
                                  sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.perp_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.perp_level()
        creat_fleet(ai_settings, screen, aliens)
            
def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) <= ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(stats, aliens, bullets, ai_settings, screen, ship, sb, pills):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.perp_ships()
        aliens.empty()
        bullets.empty()
        creat_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        sleep(0.5)
        pills.back()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb, pills):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(stats, aliens, bullets, ai_settings, screen, ship, sb, pills)
            break
        
def update_aliens(ai_settings, aliens, ship, bullets, stats, screen, sb, pills):
    check_fleet_edges(ai_settings, aliens)
    aliens.update() 
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, aliens, bullets, ai_settings, screen, ship, sb, pills)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb, pills)
    

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.perp_high_score()

def update_pills(pills, ship, ai_settings, screen):
    pills.update()
    check_ship_eat(ship, pills, ai_settings)
    check_pills_bottom(screen, pills)
        
def check_ship_eat(ship, pills, ai_settings):
    if check_collision(ship, pills):
        ai_settings.change_bullet()
        pills.back()
def check_collision(a, b):
    if a.rect.x <= b.rect.x <= a.rect.x + a.rect.width or \
    a.rect.x <= b.rect.x + b.rect.width <= a.rect.x + a.rect.width:
        if a.rect.y <= b.rect.y <= a.rect.y + a.rect.height or \
        a.rect.y <= b.rect.y + b.rect.height <= a.rect.y + a.rect.height:
            return True
    else:
        return False

def check_pills_bottom(screen, pills):
    screen_rect = screen.get_rect()
    if pills.rect.bottom >= screen_rect.bottom:
        pills.back()
        