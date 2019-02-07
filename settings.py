import pygame


class Settings():
    '''储存alien_game的所有设置'''
    def __init__(self):
        '''初始化游戏设置'''
        self.screen_width = 800
        self.screen_height = 600
        self.f_color = (255, 250, 250)  # 白色,屏幕填充颜色
        # 设置飞船参数
        self.ship_speed = 0.5
        self.ship_width = 40
        self.ship_height = 80
        self.ship_limit = 3  # 限制3次沉船机会
        # 设置子弹参数
        self.bullet_speed = 0.1  # 子弹每次循环移动1个位置
        self.bullet_width = 10  # 子弹矩形的大小
        self.bullet_height = 20
        self.bullet_limit = 20  # 同屏bullet限制
        # 设置外星人参数
        self.alien_speed = 0.05
        self.alien_width = 40
        self.alien_height = 40
        self.alien_built_speed = 2  # 每1秒创建一个外星人
        self.alien_limit = 10  # 限制外星人数量
        # 设置按钮参数
        self.button_width = 200
        self.button_height = 100
        self.button_color = (255, 255, 0)  # 黄色,按钮填充颜色
        self.text_color = (11, 6, 36)  # 黑色,字体颜色
        pygame.init()
        self.font = pygame.font.SysFont(None, 48)  # 字体设置,需要pygame.init()初始化设置才能生效
        # 设置计分板参数
        self.score_width = 100
        self.score_height = 30
        self.score_color = (243, 244, 36)  # 暗黄色
        self.score_font = pygame.font.SysFont(None, 20)  # 计分板字体设置
        self.high_score_font = pygame.font.SysFont(None, 30)  # 最高分字体设置
        # 设置图片,声音路径
        self.ship_path = 'images/ship.bmp'
        self.bullet_path = 'images/bullet.bmp'
        self.alien_path = 'images/alien.bmp'
        self.collide_sound = 'sound/Bomb.mp3'
        # 设置难度变化率
        self.speed_up = 1.2  # 速度将以120%的比例上升

    def reset(self):
        '''将可变参数重置为初始值'''
        self.ship_speed = 0.5
        self.ship_limit = 3
        self.alien_speed = 0.05
        self.bullet_speed = 0.1  # 暂时不设置变化
        self.alien_built_speed = 2  # alien创建速度
        self.alien_limit = 6  # 同屏alien数量

    def level_up(self):
        '''难度升级'''
        if self.ship_speed < 1:  # ship速度上限
            self.ship_speed *= self.speed_up  # ship移动距离增加
        self.alien_speed *= self.speed_up  # alien速度提升
        self.alien_built_speed /= self.speed_up  # 创建速度加快,应该不是很明显
        self.alien_limit *= self.speed_up  # 同屏alien上限增加

