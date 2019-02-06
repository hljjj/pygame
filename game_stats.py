import csv


class Stats():
    def __init__(self):
        self.game_activate = False  # 默认游戏启动设置为false
        self.score = 0  # 玩家得分
        self.score_point = 1  # 一个外星人得分
        self.level = 1  # 初始等级
        self.score_level = 10  # 等级分数跨度,1级n*1分,2级n*2分
        self.last_time = 0  # 计时器

    def reset_stats(self):
        '''重置游戏统计信息'''
        self.score = 0
        self.game_activate = False
        self.level = 1


def high_score(score):
    '''输出分数返回最高分'''
    path = 'game_stats.csv'
    with open(path, 'r') as f:  # 只读模式打开
        reader = csv.reader(f)  # 阅读器对象不能直接判断是否为空,而且只有r模式可以读取内容
        read_list = []
        for row in reader:  # 读取全部内容到列表
            read_list.append(row)
    with open(path, 'a') as f:
        writer = csv.writer(f)
        data = []
        for row in read_list[1:]:  # 切片,首行是字段
            try:
                data.append(row[0])  # 读取最高分
            except IndexError:  # 有可能存在空白
                pass
        if int(max(data)) <= score:  # 比已有分数都高才写入
            writer.writerow([score, ])

