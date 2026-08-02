from pygame import *
from random import randint, choice

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image_path = player_image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__(player_image, player_x, player_y, size_x, size_y, 0)

class Bullet(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
        self.direction = direction   
    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__(player_image, player_x, player_y, size_x, size_y, 0)
        self.direction = 'up'  # Начальное направление движения
        self.direction1 = 'right'

    def patrol(self):
        """Метод для перемещения врагов вертикально"""
        if self.direction == 'up':  # Двигаемся вверх
            self.rect.y -= 1
            if self.rect.y <= 273:  # Если достигли верха
                self.direction = 'down'
                self.image_path = 'bottom1.png'
                self.image = transform.scale(image.load(self.image_path), (50, 50))
        elif self.direction == 'down':  # Двигаемся вниз
            self.rect.y += 1
            if self.rect.y >= 470:  # Если дошли до низа
                self.direction = 'up'
                self.image_path = 'up1.png'
                self.image = transform.scale(image.load(self.image_path), (50, 50))

    def patrol_horizontal(self):
        """Метод для перемещения врагов горизонтально"""
        if self.direction1 == 'right':  # Двигаемся направо
            self.rect.x += 1
            if self.rect.x >= 407:  # Если достигли правого края
                self.direction1 = 'left'
                self.image_path = 'left1.png'
                self.image = transform.scale(image.load(self.image_path), (50, 50))
        elif self.direction1 == 'left':  # Двигаемся налево
            self.rect.x -= 1
            if self.rect.x <= 148:  # Если дошли до левого края
                self.direction1 = 'right'  # Здесь должна меняться именно direction1!
                self.image_path = 'right1.png'
                self.image = transform.scale(image.load(self.image_path), (50, 50))

bg = image.load('Pole.jpg')
win_screen = image.load('ФОН12333.jpg') 
lose_screen = image.load('Фон123.png')
mixer.init()
mixer.music.load('ss.mp3')
sound1 = mixer.Sound('crash-2.mp3')
sound2 = mixer.Sound('fail-sound.mp3')
death = mixer.Sound('death.mp3')
keys_state = {K_a: False, K_d: False, K_w: False, K_s: False}
wall = GameSprite('Веном.png', 414, 346, 30, 120, 0)
wall1 = GameSprite('Веном1.png', 299, 346, 115, 27, 0)
wall2 = GameSprite('Веном1.png', 200, 439, 215, 27, 0)
wall3 = GameSprite('Веном.png', 200, 249, 30, 190, 0)
wall4 = GameSprite('Веном1.png', 230, 249, 267, 27, 0)
wall5 = GameSprite('Веном.png', 497, 249, 30, 301, 0)
wall6 = GameSprite('Веном1.png', 148, 523, 349, 27, 0)
wall7 = GameSprite('Веном.png', 118, 390, 30, 160, 0)
wall8 = GameSprite('Веном1.png', 0, 390, 118, 27, 0)
wall9 = GameSprite('Веном1.png', 0, 310, 201, 25, 0)
wall10 = GameSprite('Finish.png', 0, 335, 18, 55, 0)
screen_width = 700
screen_height = 600
window = display.set_mode((screen_width, screen_height))
display.set_caption('Simple shooter')
player = Player('up.png', 360, 378, 50, 50)
enemy1 = Enemy('up1.png', 444, 470, 50, 50)
enemy2 = Enemy('right1.png', 148, 470, 50, 50)
all_bullets = sprite.Group()
enemies_group = sprite.Group()
enemies_group.add(enemy1)
enemies_group.add(enemy2)
walls = sprite.Group()
walls.add(wall,wall1,wall2,wall3,wall4,wall5,wall6,wall7,wall8,wall9)
wll = sprite.Group()
wll.add(wall10)
last_spawn_time = 0 
spawn_interval = 500
ss = 800
run = True
game_over1 = False
game_over = False
FPS = time.Clock()
total_kills = 0
max_kills_needed = 21
mixer.music.play(-1)
while run:
    current_time = time.get_ticks()  
    window.blit(bg, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            if player.image_path == 'up.png':
                bullet_x = player.rect.centerx - (45 // 2)
                new_bullet = Bullet('Bulup.png', int(bullet_x), player.rect.top, 45, 45, 7, 'up')
                all_bullets.add(new_bullet)
                sound1.play()
            elif player.image_path == 'bottom.png':
                bullet_x = player.rect.centerx - (45 // 2)
                new_bullet = Bullet('Buldown.png', int(bullet_x), player.rect.bottom, 45, 45, 7, 'down')
                all_bullets.add(new_bullet)
                sound1.play()
            elif player.image_path == 'left.png':
                bullet_y = player.rect.centery - (45 // 2)
                new_bullet = Bullet('Bulleft.png', player.rect.left, int(bullet_y), 45, 45, 7, 'left')
                all_bullets.add(new_bullet)
                sound1.play()
            elif player.image_path == 'right.png':
                bullet_y = player.rect.centery - (45 // 2)
                new_bullet = Bullet('Bulright.png', player.rect.right, int(bullet_y), 45, 45, 7, 'right')
                all_bullets.add(new_bullet)
                sound1.play()
        
    keys_pressed = key.get_pressed()
    if not game_over:
        if keys_pressed[K_a]:
            player.image_path = 'left.png'
            player.image = transform.scale(image.load('left.png'), (50, 50))
            player.rect.x -= 1
            if sprite.spritecollide(player, walls, False):
                player.rect.x += 1
        elif keys_pressed[K_d]:
            player.image_path = 'right.png'
            player.image = transform.scale(image.load('right.png'), (50, 50))
            player.rect.x += 1
            if sprite.spritecollide(player, walls, False):
                player.rect.x -= 1
        elif keys_pressed[K_w]:
            player.image_path = 'up.png'
            player.image = transform.scale(image.load('up.png'), (50, 50))
            player.rect.y -= 1
            if sprite.spritecollide(player, walls, False):
                player.rect.y += 1
        elif keys_pressed[K_s]:
            player.image_path = 'bottom.png'
            player.image = transform.scale(image.load('bottom.png'), (50, 50))
            player.rect.y += 1
            if sprite.spritecollide(player, walls, False):
                player.rect.y -= 1
                
        # Обработка столкновения пуль с врагами
        hit_list = sprite.groupcollide(enemies_group, all_bullets, True, True)
        total_kills += len(hit_list)
            
        # Проверяем поражение
        if sprite.spritecollide(player, enemies_group, False):  
            game_over1 = True
            game_over = True
            
        # Проверяем победу
        if sprite.spritecollide(player, wll, False):
            game_over = True
            
        # Движение врагов и обновление экрана
        enemy1.patrol()
        enemy2.patrol_horizontal()
        window.fill((0, 0, 0))  
        window.blit(bg, (0, 0))
        if not game_over:
            all_bullets.update()
            enemies_group.update()
            all_bullets.draw(window)
            enemies_group.draw(window)
            player.reset()
            for w in walls.sprites():
                w.reset()
            for ww in wll.sprites():
                ww.reset()
            for wall_sprite in walls.sprites():
                bullets_hit_wall = sprite.spritecollide(wall_sprite, all_bullets, True)
            if sprite.groupcollide(enemies_group, all_bullets, False,True):
                death.play()
        else:
            mixer.music.stop()
            if game_over1:
                window.blit(lose_screen, (0, 0))
                sound2.play()
            else:
                window.blit(win_screen, (0, 0))
                mixer.music.load('won-game.mp3')
                mixer.music.play(-1)
        FPS.tick(60)
        display.flip()
quit()