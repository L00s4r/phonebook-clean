from pygame import *
from random import randint
import time as t
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.im=player_image
        self.size_x=size_x
        self.size_y=size_y
        self.image=transform.scale(image.load(player_image), (size_x, size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class plr(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed,hp):
        self.hp = hp
        self.im=player_image
        self.size_x=size_x
        self.size_y=size_y
        self.image=transform.scale(image.load(player_image), (size_x, size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def jump(self):
        global space_power
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE] and space_power >= 1:
            self.rect.y -= 70
            space_power -= 99999999999999999999999999999999999999999999999999999999999999999999999999999999
    def upd(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys_pressed[K_d]and self.rect.x<s-self.size_x:
            self.rect.x += self.speed
    def player_collide(self):
           self.rect.y -= 1
    def lose_hp(self):
        self.hp -= 50
bg_image1 = image.load('Звёздное небо.png')
Meteorit = image.load('Метеорит.png')
Roket = image.load('Ракета.png')
Direction = image.load('Стрела.png')
background123 = image.load('Гф.png')
background1234 = image.load('Гф1.png')
background12345 = image.load('Гф2.png')
Heart = image.load('Heart.png')
Skull = image.load('Чeреп.png')
bg = (255,255,255)
lose = 0
s = 700
d = 600
window = display.set_mode((s, d))
display.set_caption('Побег к0л06кA')
background = (65,105,225)
run=True
run1=True
run2=False
run3=False
run4=False
run123=False
font.init()
ff = font.Font(None,35)
loses = ff.render(str(lose), True, (249,249,249))
start1 = ff.render('Нажмите SPACE для запуска', True, (255,255,255))
start2 = ff.render('Выберите уровень', True, (210,180,140))
finish = ff.render('Вы проиграли! Нажмите SPACE для перезапуска', True, (255,10,10))
viygrish = ff.render('Вы выиграли! Нажмите SPACE для перехода на второй уровень!', True, (23,255,23))
viygrish2 = ff.render('Поздравляю! Вы прошли игру! Нажмите SPACE для окончания игры!', True, (23,255,23))
player = plr('шар.png',35,-5,50,50,3.5,100)
platform1 = GameSprite('Платформа.png',0,90,398,35,0)
platform2 = GameSprite('Платформа.png',300,250,400,35,0)
platform3 = GameSprite('Платформа.png',0,425,380,35,0)
platform4 = GameSprite('Платформа.png',306,550,300,35,0)
platform9 = GameSprite('Платформа.png',459,0,38,34,0)
platform10 = GameSprite('Платформа.png',-5,325,105,34,0)
platform11 = GameSprite('Платформа.png',-5,99,188,34,0)
platform12 = GameSprite('Платформа.png',256,178,115,34,0)
platform13 = GameSprite('Платформа.png',570,199,115,34,0)
platform14 = GameSprite('Платформа.png',-5,269,167,34,0)
platform15 = GameSprite('Платформа.png',247,328,115,34,0)
platform16 = GameSprite('Платформа.png',515,305,115,34,0)
platform17 = GameSprite('Платформа.png',247,515,115,34,0)
platform18 = GameSprite('Платформа.png',514,468,115,34,0)
ship1 = GameSprite('шип.png',354,60,40,30,0)
ship2 = GameSprite('шип.png',295,231,40,23,0)
ship3 = GameSprite('шип.png',332,395,40,30,0)
ship4 = GameSprite('шип.png',168,60,40,30,0)
ship5 = GameSprite('шип.png',193,60,40,30,0)
ship6 = GameSprite('шип1.png',460,33,36,30,0)
ship7 = GameSprite('шип.png',-5,60,40,30,0)
ship8 = GameSprite('шип.png',659,220,40,30,0)
ship9 = GameSprite('шип1.png',253,120,40,27,0)
ship10 = GameSprite('шип.png',304,231,40,23,0)
ship11 = GameSprite('шип.png',489,220,40,30,0)
ship12 = GameSprite('шип.png',467,220,40,30,0)
ship13 = GameSprite('шип1.png',268,120,40,27,0)
ship14 = GameSprite('шип.png',-5,405,40,20,0)
ship15 = GameSprite('шип.png',21,405,40,20,0)
ship16 = GameSprite('шип.png',47,405,40,20,0)
ship17 = GameSprite('шип.png',73,405,40,20,0)
ship18 = GameSprite('шип.png',99,405,40,20,0)
ship19 = GameSprite('шип.png',125,405,40,20,0)
ship20 = GameSprite('шип.png',151,405,40,20,0)
ship21 = GameSprite('шип.png',177,405,40,20,0)
ship22 = GameSprite('шип.png',203,405,40,20,0)
ship24 = GameSprite('шип2.png',248,257,53,25,0)
ship25 = GameSprite('шип3.png',145,73,37,25,0)
ship26 = GameSprite('шип4.png',94,131,37,30,0)
ship27 = GameSprite('шип4.png',113,133,31,24,0)
ship28 = GameSprite('шип3.png',254,142,43,36,0)
ship29 = GameSprite('шип3.png',291,142,43,36,0)
ship30 = GameSprite('шип3.png',328,142,43,36,0)
ship31 = GameSprite('шип3.png',567,163,43,36,0)
ship32 = GameSprite('шип4.png',642,232,43,36,0)
ship33 = GameSprite('шип3.png',126,244,37,25,0)
ship34 = GameSprite('шип6.png',161,271,53,29,0)
ship35 = GameSprite('шип5.png',194,330,53,32,0)
ship36 = GameSprite('шип3.png',515,275,37,32,0)
ship37 = GameSprite('шип3.png',593,275,37,30,0)
ship38 = GameSprite('шип3.png',593,438,37,30,0)
ship39 = GameSprite('шип6.png',361,515,51,34,0)
olatf=sprite.Group()
olatf.add(platform1)
olatf.add(platform2)
olatf.add(platform3)
olatf.add(platform10)
asd=sprite.Group()
asd.add(ship1)
asd.add(ship2)
asd.add(ship3)
asd.add(ship4)
asd.add(ship5)
asd.add(ship6)
asd.add(ship7)
asd.add(ship8)
asd.add(ship9)
asd.add(ship10)
asd.add(ship11)
asd.add(ship12)
asd.add(ship13)
asd.add(ship14)
asd.add(ship15)
asd.add(ship16)
asd.add(ship17)
asd.add(ship18)
asd.add(ship19)
asd.add(ship20)
asd.add(ship21)
asd.add(ship22)
asd.add(ship24)
asdd = sprite.Group()
asdd.add(platform11)
asdd.add(platform12)
asdd.add(platform13)
asdd.add(platform14)
asdd.add(platform15)
asdd.add(platform16)
asdd.add(platform18)
oh = sprite.Group()
oh.add(platform4)
oh1 = sprite.Group()
oh1.add(platform17)
asddd=sprite.Group()
asddd.add(ship25)
asddd.add(ship26)
asddd.add(ship27)
asddd.add(ship28)
asddd.add(ship29)
asddd.add(ship30)
asddd.add(ship31)
asddd.add(ship32)
asddd.add(ship33)
asddd.add(ship34)
asddd.add(ship35)
asddd.add(ship36)
asddd.add(ship37)
asddd.add(ship38)
asddd.add(ship39)
oh.add(platform4)
hpp = ff.render(str(player.hp), True, (10,255,10))
fps = time.Clock()
space_power=0
zanovo=False
while run:
    for e in event.get():
        if e.type == QUIT:
            run=False
    while run1:
        window.blit(background123,(0,0))
        window.blit(start1,(160,450))
        keys_pressed = key.get_pressed()
        for e in event.get():
            if e.type == QUIT:
                run = False
                run1=False
        if keys_pressed[K_SPACE]:
            run1=False
            run3=True
        fps.tick(100)
        display.update()
        while run3:
            window.blit(bg_image1,(0,0))
            window.blit(hpp,(620,10))
            window.blit(Heart,(575,0))
            window.blit(loses,(623,50))
            window.blit(Skull,(582,37))
            for e in event.get():
                if e.type == QUIT:
                    run=False
                    run3=False
            player.reset()
            player.upd()
            platform1.reset()
            platform2.reset()
            platform3.reset()
            platform4.reset()
            platform9.reset()
            platform10.reset()
            ship1.reset()
            ship2.reset()
            ship3.reset()
            ship4.reset()
            ship5.reset()
            ship6.reset()
            ship7.reset()
            ship8.reset()
            ship9.reset()
            ship10.reset()
            ship11.reset()
            ship12.reset()
            ship13.reset()
            ship14.reset()
            ship15.reset()
            ship16.reset()
            ship17.reset()
            ship18.reset()
            ship19.reset()
            ship20.reset()
            ship21.reset()
            ship22.reset()
            ship24.reset()
            if sprite.spritecollide(player, olatf, False):
                player.player_collide()
                space_power = 20
                player.jump()
            if sprite.spritecollide(player, oh, False):
                player.player_collide()
                window.fill(background)
                window.blit(background1234,(0,0))
                keys_pressed = key.get_pressed()
                if keys_pressed[K_SPACE]:
                    run4=True
                    run3=False
                    player = plr('шар.png',35,-5,50,50,3.5,100)
            if sprite.spritecollide(player,asd,False):
                player.hp -= 50
                if player.hp <= 50:
                    hpp = ff.render(str(player.hp), True, (255,10,10))
                    player.rect.y -= 50
                if player.hp <= 0:
                    player = plr('шар.png',35,-5,50,50,3.5,100)
                    hpp = ff.render(str(player.hp), True, (10,255,10))
                    lose+=1
                    loses = ff.render(str(lose), True, (249,249,249))
            player.rect.y += 1
            fps.tick(200)
            display.update()
        while run4:
            window.blit(bg_image1,(0,0))
            window.blit(Meteorit,(299,-5))
            window.blit(Roket,(542,360))
            window.blit(Direction,(276,395))
            window.blit(hpp,(620,10))
            window.blit(Heart,(575,0))
            for e in event.get():
                if e.type == QUIT:
                    run=False
                    run4=False
            player.reset()
            player.upd()
            platform11.reset()
            platform12.reset()
            platform13.reset()
            platform14.reset()
            platform15.reset()
            platform16.reset()
            platform17.reset()
            platform18.reset()
            ship25.reset()
            ship26.reset()
            ship27.reset()
            ship28.reset()
            ship29.reset()
            ship30.reset()
            ship31.reset()
            ship32.reset()
            ship33.reset()
            ship34.reset()
            ship35.reset()
            ship36.reset()
            ship37.reset()
            ship38.reset()
            ship39.reset()
            if sprite.spritecollide(player, asdd, False):
                player.player_collide()
                space_power = 20
                player.jump()
            if sprite.spritecollide(player,asddd,False):
                player.hp -= 50
                hpp = ff.render(str(player.hp), True, (255,10,10))
                if player.hp <= 50:
                    player.rect.y -= 50
                if player.hp <= 0:
                    player = plr('шар.png',35,-5,50,50,3.5,100)
                    hpp = ff.render(str(player.hp), True, (10,255,10))
            if sprite.spritecollide(player, oh1, False):
                player.player_collide()
                window.fill(bg)
                window.blit(background12345,(0,0))
                keys_pressed = key.get_pressed()
                if keys_pressed[K_SPACE]:
                    run=False
                    run4=False
            player.rect.y += 1
            fps.tick(200)
            display.update()