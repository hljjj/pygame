import pygame

class Settings():
    '''储存alien_game的所有设置'''
    def __init__(self):
        '''初始化游戏设置'''
        self.screen_width = 800
        self.screen_height = 600
        self.f_color = (255,250,250) #白色,屏幕填充颜色
        #设置飞船参数
        self.ship_speed = 0.5
        self.ship_width = 60
        self.ship_height = 120
        self.ship_limit = 3 #限制3次沉船机会
        #设置子弹参数
        self.bullet_speed = 0.1 #子弹每次循环移动1个位置
        self.bullet_width = 20 #子弹矩形的大小
        self.bullet_height = 40
        #设置外星人参数
        self.alien_speed = 0.1
        self.alien_width = 60
        self.alien_height = 60
        self.alien_built_speed = 2 #每2秒创建一个外星人
        self.alien_limit = 10 #限制外星人数量
        #设置按钮参数
        self.button_width = 200
        self.button_height = 100
        self.button_color = (255,255,0)  #黄色,按钮填充颜色
        self.text_color = (11,6,36) #黑色,字体颜色
        pygame.init()
        self.font = pygame.font.SysFont(None,48)  #字体设置,需要pygame.init()初始化设置才能生效
        #设置图片路径
        self.ship_path = 'images/ship.bmp'
        self.bullet_path = 'images/bullet.bmp'
        self.alien_path = 'images/alien.bmp'

