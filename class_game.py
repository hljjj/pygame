import pygame
import random
from pygame.sprite import Sprite #精灵模块

class Ship():
    def __init__(self,screen,game_settings):
        '''初始化飞船并设置参数'''
        self.screen = screen #传递的screen必须是一个surface实例
        self.root_image = pygame.image.load(game_settings.ship_path)  #创建了一个pygame.surface实例
        self.image =pygame.transform.smoothscale(self.root_image,(game_settings.ship_width,
                                                                  game_settings.ship_height)) #修改飞船大小
        self.rect = self.image.get_rect()  #rect是矩形rectangle的缩写,get_rect是surface实例的方法,能获取实例的属性rect
        self.screen_rect = screen.get_rect()  #这里是获取屏幕的属性rect,属性rect是一个矩形对象
        self.rect.centerx = self.screen_rect.centerx #把飞船放到屏幕底部中央
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False  #设置移动标志
        self.moving_left = False
        self.speed = game_settings.ship_speed
        self.x = float(self.rect.centerx)

    def update(self):
        if self.moving_right == True and self.rect.right < self.screen_rect.right: #右边未触底
            self.x += self.speed
            self.rect.centerx = self.x
        elif self.moving_left == True and self.rect.left > self.screen_rect.left: #左边未触底,需要注意pygame的坐标规则
            self.x -= self.speed
            self.rect.centerx = self.x

    def blitme(self):  #blit是块传送
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image,self.rect)

class Actor():
    '''传一张头像作为游戏角色'''
    def __init__(self,screen):
        self.screen = screen
        self.root_image = pygame.image.load('images/24.bmp')
        self.image = pygame.transform.smoothscale(self.root_image,(85,99))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.right = self.screen_rect.right

    def blitme(self):
        '''在指定位置绘制图形'''
        self.screen.blit(self.image,self.rect)


class Bullet(Sprite): #继承精灵类可将矩形所有元素编组并同时操作编组元素方便移动
    '''飞船发射的子弹类'''
    def __init__(self,game_settings,screen,ship):
        '''在飞船所处位置创建一个子弹对象'''
        super(Bullet, self).__init__() #继承sprite类
        self.screen = screen
        #直接导入子弹图像设定缩放比例
        self.root_image = pygame.image.load(game_settings.bullet_path)
        self.image = pygame.transform.smoothscale(self.root_image,
                                                  (game_settings.bullet_width, #注意比例是一个元组
                                                  game_settings.bullet_height))
        self.rect = self.image.get_rect() #根据image创建矩形rect,这一步必不可少
        self.rect.centerx = ship.rect.centerx #子弹中心x与ship一致
        self.rect.bottom = ship.rect.top  #子弹从ship的顶部发出
        self.speed = game_settings.bullet_speed
        self.y = float(self.rect.y) #为了储存浮点数

    def update(self):
        '''向上移动子弹'''
        self.y -= self.speed
        self.rect.y = self.y  #通过修改y坐标向上移动

    def blitme(self):
        '''在屏幕上绘制子弹'''
        self.screen.blit(self.image,self.rect)  #将绘制改为传输

class Alien(Sprite):
    '''外星人类'''
    def __init__(self,game_settings,screen): #需要传递的参数,settings,screen
        super(Alien, self).__init__()
        self.screen = screen  #把screen储存起来
        self.root_image = pygame.image.load(game_settings.alien_path)
        self.image = pygame.transform.smoothscale(self.root_image, #渲染为合适大小
                                                  (game_settings.alien_width,
                                                   game_settings.alien_height))
        self.rect = self.image.get_rect()  #创建rect实例
        self.screen_rect = self.screen.get_rect()
        self.rect.bottom = self.screen_rect.top #从屏幕顶部出来
        self.rect.left = random.randint(0,game_settings.screen_width-game_settings.alien_width+1) #横坐标随机
        self.speed = game_settings.alien_speed
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image,self.rect)

class Button():
    '''创建按钮类'''
    def __init__(self,screen,game_settings,msg):
        self.screen = screen
        self.settings = game_settings
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(0,0,game_settings.button_width,
                                game_settings.button_height) #设置按钮的rect对象
        self.rect.centerx = self.screen_rect.centerx
        self.present_msg(msg)  #不是很明白这个属性的意义,直接调用方法和作为属性有什么区别?

    def present_msg(self,msg):
        '''将msg渲染为图像'''
        #self.settings.font是一个paygame.font.Font实例,这里是从settings获取的
        self.msg_image = self.settings.font.render(msg,  #要转换的文本
                                          True,  #开启反锯齿功能,文本边缘更平滑
                                          self.settings.text_color, #文本颜色
                                          self.settings.button_color #背景颜色,default透明
                                          ) #文字图像
        self.msg_image_rect = self.msg_image.get_rect()  #文字矩形
        self.msg_image_rect.center = self.rect.center #字体居中

    def draw_button(self):
        '''将button绘制到屏幕上'''
        self.screen.fill(self.settings.button_color,self.rect)  #先绘制按钮
        self.screen.blit(self.msg_image,self.msg_image_rect) #把文字图像传输到文字矩形上