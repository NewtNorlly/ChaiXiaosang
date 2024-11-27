"""
以下代码由 柴桑 编写
这是一个小游戏程序,名为"恐龙快跑(黄州府)"
鼓励各位HGer拿去玩.
欢迎各位程序员大佬关注我的小仓库!
"""

import os
import pygame
import random

# 初始化 Pygame
pygame.init()

# 屏幕大小
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("恐龙快跑（黄州府）")

# 颜色定义
BLUE = (135, 206, 250)  # 天空蓝
BLACK = (0, 0, 0)

# 时钟和字体
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# 恐龙类
class Dinosaur:
    def __init__(self):
        self.image = pygame.image.load(r"C:\Users\NewtN\Pictures\Camera Roll\小恐龙-removebg-preview (1).png")  # 恐龙图片路径
        self.image = pygame.transform.scale(self.image, (60, 90))  # 调整大小
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 80
        self.is_jumping = False
        self.jump_speed = 20  # 增大初始跳跃速度，跳得更高
        self.gravity = 1  # 重力
        self.velocity = 0  # 速度
        self.is_space_pressed = False  # 空格键是否按下

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -self.jump_speed  # 设置跳跃初速度
            self.is_space_pressed = True  # 记录空格键按下状态

    def update(self):
        if self.is_jumping:
            # 空格按住时增加跳跃速度
            if self.is_space_pressed:
                self.velocity = max(self.velocity, -self.jump_speed)  # 限制最大向上速度

            self.rect.y += self.velocity  # 更新位置
            self.velocity += self.gravity  # 重力影响

            if self.rect.y >= HEIGHT - 80:  # 恢复地面位置
                self.rect.y = HEIGHT - 80
                self.is_jumping = False
                self.velocity = 0  # 结束跳跃时，速度为零

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 障碍物类
class Obstacle:
    def __init__(self, x, y, speed, image_path):
        self.image = pygame.image.load(image_path)  # 加载障碍物图片
        self.image = pygame.transform.scale(self.image, (30, 50))  # 调整障碍物大小
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 云朵类
class Cloud:
    def __init__(self):
        self.image = pygame.image.load(r"C:\Users\NewtN\Pictures\Camera Roll\云朵-removebg-preview.png")  # 云朵图片路径
        self.image = pygame.transform.scale(self.image, (100, 60))  # 调整云朵大小
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 300)  # 随机生成在屏幕外
        self.rect.y = random.randint(50, 150)  # 云朵高度随机
        self.speed = random.randint(1, 3)  # 云朵滚动速度

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:  # 如果滚出屏幕，重新生成云朵
            self.rect.x = random.randint(WIDTH, WIDTH + 300)
            self.rect.y = random.randint(50, 150)
            self.speed = random.randint(1, 3)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 路灯类
class StreetLamp:
    def __init__(self, x, y):
        try:
            self.image = pygame.image.load(r"C:\Users\NewtN\Pictures\Camera Roll\路灯-removebg-preview.png")  # 路灯图片路径
            self.image = pygame.transform.scale(self.image, (120, 240))  # 调整路灯大小
        except pygame.error as e:
            print("Error loading streetlamp image:", e)
            self.image = None
        self.rect = self.image.get_rect() if self.image else None
        self.rect.x = x
        self.rect.y = HEIGHT - 240  # 调整路灯高度，确保整个路灯都露出来
        self.speed = 2  # 路灯的移动速度

    def update(self):
        if self.rect:
            self.rect.x -= self.speed
            if self.rect.right < 0:  # 如果路灯滚出屏幕，重新生成
                self.rect.x = WIDTH + random.randint(50, 300)  # 随机右侧出现
                self.rect.y = HEIGHT - 240  # 保持在新的高位置

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)

# 加载背景图片
background_image = pygame.image.load(r"C:\Users\NewtN\Pictures\Camera Roll\HG.png")  # 替换为你的背景图片路径
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # 缩放到屏幕大小

# 主游戏函数
def main():
    run = True
    dinosaur = Dinosaur()
    obstacles = []
    clouds = [Cloud() for _ in range(3)]  # 生成多个云朵
    street_lamps = [StreetLamp(WIDTH + 100, HEIGHT - 100) for _ in range(3)]  # 将路灯放置在地面位置
    spawn_timer = 0
    score = 0
    min_obstacle_distance = 200  # 设置障碍物之间的最小间距

    obstacle_image_path = r"C:\Users\NewtN\Pictures\Camera Roll\刺猬-removebg-preview.png"  # 替换为你的障碍物图片路径

    last_obstacle_speed = random.randint(5, 10)  # 初始障碍物速度

    while run:
        # 先填充蓝色背景
        screen.fill(BLUE)
        # 绘制背景图片
        screen.blit(background_image, (0, 0))

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dinosaur.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    dinosaur.is_space_pressed = False  # 空格键松开

        # 更新和绘制云朵
        for cloud in clouds:
            cloud.update()
            cloud.draw(screen)

        # 更新和绘制路灯
        for street_lamp in street_lamps:
            street_lamp.update()
            street_lamp.draw(screen)

        # 更新和绘制恐龙
        dinosaur.update()
        dinosaur.draw(screen)

        # 障碍物生成
        if spawn_timer <= 0:
            x = WIDTH
            if obstacles:
                last_obstacle = obstacles[-1]
                # 保证障碍物之间的距离大于最小间距
                while x - last_obstacle.rect.right < min_obstacle_distance:
                    x = random.randint(WIDTH, WIDTH + 300)  # 调整位置，避免间距过小

            # 设置新障碍物的速度为一个小于等于上一个障碍物速度的随机值
            new_speed = random.randint(5, min(last_obstacle_speed, 12))

            obstacle = Obstacle(x, HEIGHT - 50, new_speed, obstacle_image_path)
            obstacles.append(obstacle)
            last_obstacle_speed = new_speed  # 更新上一个障碍物的速度
            spawn_timer = random.randint(50, 100)
        else:
            spawn_timer -= 1

        # 更新和绘制障碍物
        for obstacle in list(obstacles):
            obstacle.update()
            obstacle.draw(screen)
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
                score += 1
            if dinosaur.rect.colliderect(obstacle.rect):
                run = False  # 游戏结束

        # 显示分数
        score_text = font.render(f"Run,run,run: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # 控制游戏帧率
        clock.tick(60)

    # 游戏结束后显示分数
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    pygame.time.wait(2000)  # 显示游戏结束画面2秒钟

    pygame.quit()

if __name__ == "__main__":
    main()
