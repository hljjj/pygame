import pygame
from pygame.sprite import Group  # 进行编组管理

import game_functions as gf
from settings import Settings
from class_game import Ship, Actor, Button, ScoreBoard, HighScore
from game_stats import Stats


def run_game():
    stats = Stats()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))  # 创建屏幕
    pygame.display.set_caption('外星人入侵')  # 游戏标题
    ship = Ship(screen, game_settings)  # 创建飞船
    actor = Actor(screen)  # 添加背景人物
    bullets = Group()  # 创建编组用于存储子弹,必须是在主循环外创建,循环内创建会导致游戏卡顿
    aliens = Group()  # 编组管理外星人
    play_button = Button(screen, game_settings, 'PLAY')  # 创建button
    score_board = ScoreBoard(screen, stats, game_settings)  # 创建计分板
    high_score = HighScore(screen, game_settings)  # 创建最高分记录板
    while True:  # 永远循环
        gf.check_event(game_settings, screen, ship, bullets, aliens, stats, play_button)  # 监听输入
        gf.check_time(game_settings, screen, aliens, stats)  # 计时器,定时创建alien
        gf.check_ship_alien(game_settings, ship, bullets, aliens, stats, high_score)  # 检查飞船碰撞
        ship.update()  # 更新飞船位置
        gf.check_bullets(bullets, aliens, stats, score_board, game_settings)  # 更新子弹,检测碰撞,计分
        gf.update_aliens(aliens)  # 更新外星人位置
        gf.update_screen(game_settings, screen, ship, actor, bullets,
                         aliens, play_button, stats, score_board, high_score)  # 更新屏幕


run_game()   # 运行游戏
