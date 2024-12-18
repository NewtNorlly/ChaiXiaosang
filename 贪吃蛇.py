import pygame
import time
import random

# 初始化pygame
pygame.init()

# 设置游戏窗口
width = 600
height = 400
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("贪吃蛇游戏")

# 颜色定义
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 设置蛇的初始参数
snake_block = 10
snake_speed = 15

# 设置时钟
clock = pygame.time.Clock()

# 字体
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


# 显示分数
def Your_score(score):
    value = score_font.render("得分: " + str(score), True, black)
    game_window.blit(value, [0, 0])


# 画蛇
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_window, green, [x[0], x[1], snake_block, snake_block])


# 显示消息
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_window.blit(mesg, [width / 6, height / 3])


# 主游戏循环
def gameLoop():
    game_over = False
    game_close = False

    # 蛇初始位置
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    # 蛇的身体，初始化蛇为一个方块
    snake_List = []
    Length_of_snake = 1

    # 食物位置
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # 游戏主循环
    while not game_over:

        while game_close:
            game_window.fill(blue)
            message("游戏结束! 按Q退出 或 C重新开始", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 蛇是否碰到墙壁
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        game_window.fill(blue)

        # 画食物
        pygame.draw.rect(game_window, yellow, [foodx, foody, snake_block, snake_block])

        # 更新蛇的位置
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        # 控制蛇的长度，保持蛇头位置，删除尾部
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检查蛇是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 画蛇
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        # 更新显示
        pygame.display.update()

        # 吃到食物
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # 控制游戏速度
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
