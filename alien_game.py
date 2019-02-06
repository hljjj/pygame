import pygame
from pygame.sprite import Group #对子弹进行编组管理

from settings import Settings
from class_game import Ship,Actor,Button
from game_functions import check_event,update_screen,update_bullets,update_aliens,alien_built,check_ship_alien
from game_stats import Stats

def run_game():
    stats = Stats()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height)) #创建屏幕
    pygame.display.set_caption('外星人入侵')  #游戏标题
    ship = Ship(screen,game_settings) #创建飞船
    actor = Actor(screen)  #添加背景人物
    bullets = Group()  #创建编组用于存储子弹,必须是在主循环外创建,循环内创建会导致游戏卡顿
    aliens = Group()  #编组管理外星人
    play_button = Button(screen,game_settings,'PLAY') #创建button
    last_time = 0 #创建计时器
    while True: #永远循环
        check_event(game_settings,screen,ship,bullets,aliens,stats,play_button)  #监听输入
        if stats.game_activate == True:
            current_time = pygame.time.get_ticks()  #获取当前经过时间,以毫秒计
            if current_time-last_time > 1000*game_settings.alien_built_speed:  #设置每n秒自动生成一个alien
                alien_built(game_settings,screen,aliens)
                last_time = current_time  #把当前时间赋给last_time
        check_ship_alien(game_settings,ship,bullets,aliens,stats)
        ship.update()  #更新位置
        update_bullets(bullets,aliens) #更新子弹
        update_aliens(aliens) #更新外星人位置
        update_screen(game_settings,screen,ship,actor,bullets,aliens,play_button,stats) #更新屏幕


run_game()   #运行游戏
