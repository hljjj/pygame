import sys
import pygame

from time import sleep

from class_game import Bullet, Alien, ScoreBoard
from game_stats import high_score as hs


def check_event(game_settings, screen, ship, bullets, aliens, stats, play_button):  # 为了移动飞船,需要传递参数
    '''事件管理函数,响应鼠标和键盘输入'''
    for event in pygame.event.get():  # 监视键盘和鼠标操作
        if event.type == pygame.QUIT:  # 捕捉到退出
            sys.exit()  # 调用sys模块退出
        elif event.type == pygame.KEYDOWN:  # 捕捉键盘输入
            check_keydown(event, game_settings, screen, ship, bullets, aliens, stats)
        elif event.type == pygame.KEYUP:  # 按键弹起
            check_keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 捕捉鼠标点击
            mouse_x, mouse_y = pygame.mouse.get_pos()  # 获取鼠标点击坐标
            check_mouse(mouse_x, mouse_y, stats, play_button, game_settings, ship)


def bullet_fire(game_settings, screen, ship, bullets):
    if len(bullets) < game_settings.bullet_limit:  # 限制子弹数量
        new_bullet = Bullet(game_settings, screen, ship)  # 创建新子弹
        bullets.add(new_bullet)  # 把新子弹添加到编组


def check_time(game_settings, screen, aliens, stats):  # 计算时间间隔作为计时器
    if stats.game_activate is True:
        current_time = pygame.time.get_ticks()  # 获取当前经过时间,以毫秒计
        if current_time-stats.last_time > 1000*game_settings.alien_built_speed:  # 设置每n秒自动生成一个alien
            alien_built(game_settings, screen, aliens)
            stats.last_time = current_time  # 把当前时间赋给last_time


def alien_built(game_settings, screen, aliens):
    if len(aliens) < game_settings.alien_limit:  # 限制外星人个数
        new_alien = Alien(game_settings, screen)
        aliens.add(new_alien)


def ship_hit(game_settings, ship, bullets, aliens, stats, high_score):
    '''alien到达了底部的时候的操作'''
    sleep(3)  # 暂停,单位是s
    game_settings.ship_limit -= 1  # 失去一艘船
    bullets.empty()  # 清空子弹
    aliens.empty()   # 清空外星人
    ship.rect.centerx = ship.screen_rect.centerx  # 飞船重新居中
    if game_settings.ship_limit <= 0:  # 飞船耗尽,游戏结束
        score = stats.score
        hs(score)   # 输出分数
        high_score.update()   # 更新最高分
        high_score.pre_msg()
        stats.reset_stats()  # 重置分数,等级,标记
        game_settings.reset()  # 重置游戏难度


def check_ship_alien(game_settings, ship, bullets, aliens, stats, high_score):
    '''检测是否有alien到达了底部'''
    for alien in aliens.sprites():
        if alien.rect.bottom >= game_settings.screen_height:  # 发生触底
            ship_hit(game_settings, ship, bullets, aliens, stats, high_score)


def check_keydown(event, game_settings, screen, ship, bullets, aliens,stats):
    if stats.game_activate is True:
        if event.key == pygame.K_RIGHT:  # 读取键入的属性,捕捉到右箭头
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # 捕捉左键
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:  # 捕捉空格键
            bullet_fire(game_settings, screen, ship, bullets)
        elif event.key == pygame.K_a:  # 设置一个让外星人生成的条件
            alien_built(game_settings, screen, aliens)
        if event.key == pygame.K_q or pygame.K_ESCAPE:  # 捕捉退出键
            sys.exit()
    else:
        if event.key == pygame.K_q or pygame.K_ESCAPE:  # 捕捉退出键
            sys.exit()


def check_keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_mouse(mouse_x, mouse_y, stats, play_button, game_settings, ship):
    if play_button.rect.collidepoint(mouse_x, mouse_y):  # 点对面碰撞
        stats.game_activate = True
        game_settings.reset()
        ship.rect.centerx = ship.screen_rect.centerx
        pygame.init()


def check_bullets(bullets, aliens, stats, score_board, game_settings):
    bullets.update()
    # 碰撞检测
    collides = pygame.sprite.groupcollide(bullets,  # 作为子弹的编组
                                          aliens,  # 作为子弹目标的编组
                                          True,    # 删除发生碰撞的子弹
                                          True     # 删除发生碰撞的目标
                                          )
    if collides:    # 计分
        sound_bomb(game_settings)
        for alien in collides.values():
            stats.score += len(alien)*stats.score_point
    score_board.present_msg()  # 更新计分板
    if stats.score >= stats.score_level*stats.level:
        stats.level += 1  # 升一级
        game_settings.level_up()  # 难度升级
    for bullet in bullets.copy():  # 删除超出屏幕的子弹
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def update_aliens(aliens):
    aliens.update()  # 有触底检测,不需要删除过线alien


def update_screen(game_settings, screen, ship, actor, bullets, aliens, play_button, stats, score_board, high_score):
    '''屏幕管理函数,自动更新屏幕'''
    screen.fill(game_settings.f_color)
    actor.blitme()
    ship.blitme()  # 绘制飞船
    bullets.draw(screen)  # 也可以用bullets.sprites()返回一个列表,用for遍历调用blitme函数
    aliens.draw(screen)    # 和for一样的作用
    if stats.game_activate is False:
        play_button.draw_button()  # 当游戏未启动时才画按钮
        high_score.draw()  # 画最高分记录
    else:
        score_board.draw()  # 显示计分板
    pygame.display.flip()   # 用新的屏幕取代旧屏幕,需要注意层级


def sound_bomb(game_settings):
    '''播放爆炸音效'''
    pygame.mixer.music.load(game_settings.collide_sound)
    pygame.mixer.music.play()