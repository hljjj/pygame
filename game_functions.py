import sys
import pygame

from time import sleep

from class_game import Bullet,Alien

def bullet_fire(game_settings,screen,ship,bullets):
    new_bullet = Bullet(game_settings, screen, ship)  # 创建新子弹
    bullets.add(new_bullet)  # 把新子弹添加到编组

def alien_built(game_settings,screen,aliens):
    if len(aliens) < game_settings.alien_limit:  #限制外星人个数
        new_alien = Alien(game_settings,screen)
        aliens.add(new_alien)

def ship_hit(game_settings,ship,bullets,aliens,stats):
    '''alien到达了底部的时候的操作'''
    sleep(3) #暂停,单位是s
    game_settings.ship_limit -= 1 #失去一条命
    bullets.empty()  #清空子弹
    aliens.empty()   #清空外星人
    ship.rect.centerx = ship.screen_rect.centerx #飞船重新居中
    pygame.init()  #需要重置计时器不然外星人生成会混乱
    if game_settings.ship_limit <= 0:  # 飞船耗尽,游戏结束
        stats.game_activate = False

def check_ship_alien(game_settings,ship,bullets,aliens,stats):
    '''检测是否有alien到达了底部'''
    for alien in aliens.sprites():
        if alien.rect.bottom >= game_settings.screen_height: #发生触底
            ship_hit(game_settings,ship,bullets,aliens,stats)

def check_keydown(event,game_settings,screen,ship,bullets,aliens):
    if event.key == pygame.K_RIGHT:  # 读取键入的属性,捕捉到右箭头
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:  # 捕捉左键
        ship.moving_left = True
    elif event.key == pygame.K_SPACE: #捕捉空格键
        bullet_fire(game_settings,screen,ship,bullets)
    elif event.key == pygame.K_a: #设置一个让外星人生成的条件
        alien_built(game_settings,screen,aliens)
    elif event.key == pygame.K_q or pygame.K_ESCAPE: #捕捉退出键
        sys.exit()

def check_keyup(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_event(game_settings,screen,ship,bullets,aliens,stats,play_button):  #为了移动飞船,需要传递参数
    '''事件管理函数,响应鼠标和键盘输入'''
    for event in pygame.event.get():  # 监视键盘和鼠标操作
        if event.type == pygame.QUIT:  # 捕捉到退出
            sys.exit()  # 调用sys模块退出
        elif event.type == pygame.KEYDOWN: #捕捉键盘输入
            check_keydown(event,game_settings,screen,ship,bullets,aliens)
        elif event.type == pygame.KEYUP: #按键弹起
            check_keyup(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN: #捕捉鼠标点击
            mouse_x,mouse_y = pygame.mouse.get_pos() #获取鼠标点击坐标
            check_mouse(mouse_x,mouse_y,stats,play_button,game_settings,ship)

def check_mouse(mouse_x,mouse_y,stats,play_button,game_settings,ship):
    if play_button.rect.collidepoint(mouse_x,mouse_y): #点对面碰撞
        stats.game_activate = True
        game_settings.ship_limit = 3
        ship.rect.centerx = ship.screen_rect.centerx
        pygame.init()

def update_screen(game_settings,screen,ship,actor,bullets,aliens,play_button,stats):
    '''屏幕管理函数,自动更新屏幕'''
    screen.fill(game_settings.f_color)
    actor.blitme()
    ship.blitme()  # 绘制飞船
    for bullet in bullets.sprites():  #注意不要漏了s,这个函数会返回一个list
        bullet.blitme()    #对编组内每个元素调用draw方法重画子弹
    aliens.draw(screen)    #和for一样的作用
    if stats.game_activate == False:
        play_button.draw_button()  #当游戏未启动时才画按钮
    pygame.display.flip()  # 用新的屏幕取代旧屏幕,需要注意层级

def update_bullets(bullets,aliens):
    bullets.update()
    #碰撞检测
    collide_dict = pygame.sprite.groupcollide(bullets,#作为子弹的编组
                                       aliens, #作为子弹目标的编组
                                       True,   #删除发生碰撞的子弹
                                       True    #删除发生碰撞的目标
                                       )
    for bullet in bullets.copy():  # 删除超出屏幕的子弹
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def update_aliens(aliens):
    aliens.update()  #有触底检测,不需要删除过线alien
