from PIL import Image

# 图片文件路径列表
image_paths = [
    '恐龙快跑素材库/HG2.0.png',
    '恐龙快跑素材库/中式柱子1.jpg',
    '恐龙快跑素材库/安国寺-removebg-preview.png',
    '恐龙快跑素材库/中式柱子2.jpg',
    '恐龙快跑素材库/HG3.0-removebg-preview.png',
    '恐龙快跑素材库/中式柱子3.jpg',
    '恐龙快跑素材库/遗爱湖建筑群-removebg-preview.png',
    '恐龙快跑素材库/中式柱子4.jpg',
    '恐龙快跑素材库/长江大桥-removebg-preview.png',
    '恐龙快跑素材库/中式柱子5.jpg',
    '恐龙快跑素材库/陈潭秋故居-removebg-preview.png',
    '恐龙快跑素材库/中式柱子6.jpg',
    '恐龙快跑素材库/壁纸-removebg-preview.png',
    '恐龙快跑素材库/中式柱子7.jpg',
    '恐龙快跑素材库/湖北省博物馆-removebg-preview.png',
    '恐龙快跑素材库/中式柱子8.jpg',
    '恐龙快跑素材库/黄州师范学院-removebg-preview.png',
    '恐龙快跑素材库/中式柱子9.jpg',
    '恐龙快跑素材库/黄州文庙-removebg-preview.png',
    '恐龙快跑素材库/中式柱子10.jpg',
    '恐龙快跑素材库/栖霞楼-removebg-preview.png',
    '恐龙快跑素材库/中式柱子11.jpg',
    '恐龙快跑素材库/青云塔-removebg-preview.png'
]

# 游戏屏幕高度
screen_height = 400

# 打开所有图片并计算总宽度
images = [Image.open(path) for path in image_paths]
total_width = sum(int(img.width * (screen_height / img.height)) for img in images)

# 创建一个新的空白图像，高度为屏幕高度
background = Image.new('RGBA', (total_width, screen_height))

# 将每张图片粘贴到背景上
current_x = 0
for image in images:
    # 计算新的尺寸，保持宽高比
    new_width = int(image.width * (screen_height / image.height))
    resized_image = image.resize((new_width, screen_height), Image.LANCZOS)
    background.paste(resized_image, (current_x, 0))
    current_x += new_width

# 保存合成后的背景图像
background.save('恐龙快跑素材库/combined_buildings_aligned.png')

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
        self.image = pygame.image.load('恐龙快跑素材库/小恐龙-removebg-preview.png')
        self.image = pygame.transform.scale(self.image, (60, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 80
        self.is_jumping = False
        self.jump_speed = 20
        self.gravity = 1
        self.velocity = 0
        self.is_space_pressed = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -self.jump_speed
            self.is_space_pressed = True

    def update(self):
        if self.is_jumping:
            if self.is_space_pressed:
                self.velocity = max(self.velocity, -self.jump_speed)
            self.rect.y += self.velocity
            self.velocity += self.gravity
            if self.rect.y >= HEIGHT - 80:
                self.rect.y = HEIGHT - 80
                self.is_jumping = False
                self.velocity = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 障碍物类
class Obstacle:
    def __init__(self, x, y, speed, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 建筑物类
class Building:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = self.width

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 主游戏函数
def main():
    run = True
    dinosaur = Dinosaur()
    obstacles = []
    building_image_path = '恐龙快跑素材库/combined_buildings_aligned.png'
    building = Building(building_image_path, 0, HEIGHT - 400)
    spawn_timer = 0
    score = 0
    min_obstacle_distance = 200
    obstacle_image_path = '恐龙快跑素材库/刺猬-removebg-preview.png'
    last_obstacle_speed = random.randint(5, 10)

    while run:
        screen.fill(BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dinosaur.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    dinosaur.is_space_pressed = False

        building.update()
        building.draw(screen)

        dinosaur.update()
        dinosaur.draw(screen)

        if spawn_timer <= 0:
            x = WIDTH
            if obstacles:
                last_obstacle = obstacles[-1]
                while x - last_obstacle.rect.right < min_obstacle_distance:
                    x = random.randint(WIDTH, WIDTH + 300)
            new_speed = random.randint(5, min(last_obstacle_speed, 12))
            obstacle = Obstacle(x, HEIGHT - 50, new_speed, obstacle_image_path)
            obstacles.append(obstacle)
            spawn_timer = random.randint(50, 100)
        spawn_timer -= 1

        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw(screen)
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
                score += 1
            if dinosaur.rect.colliderect(obstacle.rect):
                run = False

        score_text = font.render(f"Run,run,run: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()