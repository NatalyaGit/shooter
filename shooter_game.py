from pygame import *
from random import randint
from time import time as mytime
#описываем классы
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>10:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<700 -10- self.rect.width:
            self.rect.x+=self.speed

    def fire(self):
        y = self.rect.y
        x = self.rect.centerx
        bullet = Bullet('bullet.png', x-7, y, 15,30,5)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y +=self.speed
        if self.rect.y>500-self.rect.height:
            self.rect.x = randint(5,700-5-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(1,3)
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<0:
            self.kill()



#создай окно игры
window = display.set_mode((700,500))
display.set_caption('Шутер')

#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'), (700,500))
button = GameSprite('button.png',300, 225, 100, 50, 0)



#подключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#подключение шрифтов
font.init()
font1 = font.Font(None, 36)



#создаем спрайты
player = Player('rocket.png', 316,400,68, 100, 5)

enemy_count = 5
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('ufo.png', randint(5, 700-5-70),-50,70, 40, randint(1,3))
    enemyes.add(enemy)

asteroid_count = 3
asteroids = sprite.Group()
for i in range(asteroid_count):
    asteroid = Enemy('asteroid.png', randint(5, 700-5-70),-50,70, 40, randint(1,2))
    asteroids.add(asteroid)


bullets = sprite.Group()

boss = Enemy('ufo.png', randint(5, 700-5-70),-50,210, 120, randint(1,3))

#обработай событие «клик по кнопке "Закрыть окно"»
game = True
finish = True
menu = True
lost = 0
score = 0
text = 0
font_lose = font1.render('Ты проиграл!', 1, (255,255,255))
font_win = font1.render('Ты выиграл!', 1, (255,255,255))
boss_f = 0
boss_l = False

clock = time.Clock()
FPS = 60

while game:
    # проверка нажатия на кнопку "выход"
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_TAB:
                menu = False
                finish = False
                strt_time = mytime()

    if menu == True:
        window.blit(background, (0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False
                strt_time = mytime()
        if text == 1:
            window.blit(font_win, (250,175))
        elif text == 2:
            window.blit(font_lose, (250,175))
        if text!=0:
            font_time = font1.render('Время на уровне: '+str(int(end_time-strt_time)), 1, (255,255,255))
            window.blit(font_time, (250,350))
        lost = 0
        score = 0
        enemyes.empty()
        for i in range(enemy_count):
            enemy = Enemy('ufo.png', randint(5, 700-5-70),-50,70, 40, randint(1,3))
            enemyes.add(enemy)
        asteroids.empty()
        for i in range(asteroid_count):
            asteroid = Enemy('asteroid.png', randint(5, 700-5-70),-50,70, 40, randint(1,2))
            asteroids.add(asteroid)
        bullets.empty()
        



    if finish!=True:
        #рисовка объектов сцены
        window.blit(background, (0,0))
        player.update()
        enemyes.update()
        bullets.update()
        asteroids.update()
        player.reset()
        enemyes.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprite_list1 = sprite.spritecollide(player,enemyes, False)
        sprite_list2 = sprite.spritecollide(player,asteroids, False)
        if len(sprite_list1)>0 or len(sprite_list2)>0 or lost>3:
            text=2
            finish=True
            menu=True
            end_time = mytime()

        sprite_list = sprite.groupcollide(enemyes, bullets, True, True)
        for m in sprite_list:
            score+=1
            enemy = Enemy('ufo.png', randint(5, 700-5-70),-50,70, 40, randint(1,3))
            enemyes.add(enemy)
        if score>9:
            text=1
            finish=True
            menu=True
            end_time = mytime()




        #рисовка текста
        font_lost = font1.render('Пропущено '+str(lost), 1, (255,255,255))
        window.blit(font_lost, (10,50))
        font_score = font1.render('Счет '+str(score), 1, (255,255,255))
        window.blit(font_score, (10,20))

    # обновление окна игры
    display.update()
    clock.tick(FPS)









# from pygame import *

# class GameSprite(sprite.Sprite):
#     def __init__(self, player_image, player_x, player_y, player_speed):
#         super().__init__()
#         self.image = transform.scale(image.load(player_image), (65, 65))    
#         self.speed = player_speed
#         self.rect = self.image.get_rect()
#         self.rect.x = player_x
#         self.rect.y = player_y 
#     def reset(self):
#         window.blit(self.image, (self.rect.x, self.rect.y))

# class Player(GameSprite):
#     def update(self):
#         keys = key.get_pressed()
#         if keys[K_LEFT] and self.rect.x > 15:
#             self.rect.x -= self.speed
#         if keys[K_RIGHT] and self.rect.x < 700 - 80:
#             self.rect.x += self.speed
#         if keys[K_UP] and self.rect.y > 15:
#             self.rect.y -= self.speed
#         if keys[K_DOWN] and self.rect.y < 500 - 80:
#             self.rect.y += self.speed

# class Enemy(GameSprite):
#     def update(self):
#         if self.rect.x <= 470:
#             self.direction = "right"
#         if self.rect.x >= 700 - 85:
#             self.direction = "left"

#         if self.direction == "left":
#             self.rect.x -= self.speed
#         else:
#             self.rect.x += self.speed

# class Wall(sprite.Sprite):
#     def __init__(self, color_1,color_2, color_3, wall_x, wall_y, wall_width, wall_height):
#         super().__init__()
#         self.width = wall_width
#         self.height = wall_height
#         self.image = Surface((self.width, self.height))
#         self.image.fill((color_1, color_2, color_3))
#         self.rect = self.image.get_rect()
#         self.rect.x = wall_x
#         self.rect.y = wall_y
#     def draw_wall(self):
#         window.blit(self.image, (self.rect.x, self.rect.y))

# window = display.set_mode((700, 500))
# display.set_caption("Догонялки")
# background = transform.scale(image.load("background.jpg"), (700, 500))


# clock = time.Clock()
# FPS = 60

# mixer.init()
# mixer.music.load('jungles.ogg')
# mixer.music.play()

# player = Player('hero.png', 30, 30, 5)
# enemy = Enemy('cyborg.png', 200, 200, 5)
# treasure = GameSprite('treasure.png', 300, 300, 5)
# w_1 = Wall(255, 255, 255, 100, 0, 5, 300)

# game = True
# while game:
#     window.blit(background,(0, 0))
#     w_1.draw_wall()
#     player.update()
#     player.reset()
#     enemy.update()
#     enemy.reset()
#     treasure.reset()
#     for e in event.get():
#         if e.type == QUIT:
#             game = False
            
#     clock.tick(FPS)

#     display.update()






# #Создай собственный Шутер!

# from pygame import *
# from random import randint
# from time import time as timer


# class GameSprite(sprite.Sprite):
#     def __init__(self, player_image,player_x, player_y, w,h, player_speed):
#         super().__init__()
#         self.image = transform.scale(image.load(player_image), (w,h))
#         self.speed = player_speed
#         self.rect = self.image.get_rect()
#         self.rect.x = player_x
#         self.rect.y = player_y

#     def reset(self):
#         window.blit(self.image, (self.rect.x,self.rect.y))

# class Player(GameSprite):
#     def update(self):
#         key_pressed = key.get_pressed()
#         if key_pressed[K_LEFT] and self.rect.x>5:
#             self.rect.x -= self.speed
#         if key_pressed[K_RIGHT] and self.rect.x<win_width-75:
#             self.rect.x += self.speed

#     def fire(self):
#         bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 20,30, 15)
#         Bullets.add(bullet)

# class Enemy(GameSprite):
#    #движение врага
#    def update(self):
#        self.rect.y += self.speed
#        global lost
#        #исчезает, если дойдет до края экрана
#        if self.rect.y > win_height:
#            self.rect.x = randint(80, win_width - 80)
#            self.rect.y = 0
#            lost +=1

# class Bullet(GameSprite):
#     def update(self):
#         self.rect.y -=self.speed
#         if self.rect.y < 0:
#             self.kill()

 

# win_width = 700
# win_height = 500
# window = display.set_mode((win_width,win_height))
# display.set_caption('Shooter game')
# background = transform.scale(image.load('galaxy.jpg'), (win_width,win_height)) 

# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
# shut = mixer.Sound('fire.ogg')

# font.init()
# font1 = font.SysFont('Arial', 36)

# clock = time.Clock()
# FPS = 60

# player = Player('rocket.png', win_width/2, win_height-80, 65, 85, 5)

# Bullets = sprite.Group()
# EnemyGroup = sprite.Group()
# enemy_count = 5
# for i in range(enemy_count):
#     enemy1 = Enemy('ufo.png', randint(5,win_width-70),-40, 65, 45,randint(1,2))
#     EnemyGroup.add(enemy1)
# AsteroidGroup = sprite.Group()
# asteroid_count = 3
# for i in range(asteroid_count):
#     asteriod = Enemy('asteroid.png', randint(5,win_width-70),-40, 65, 45,1)
#     AsteroidGroup.add(asteriod)



# game = True
# finish = False
# lost = 0
# score = 0
# num_fire = 0
# rel_time =False
# while game:


#     for e in event.get():
#         if e.type == QUIT:
#             game = False
#         if e.type == KEYDOWN:
#             if e.key == K_SPACE:
#                 if num_fire<5 and rel_time==False:    
#                     num_fire+=1    
#                     player.fire()
#                     shut.play()
#                 if num_fire>=5 and rel_time==False:
#                     rel_time = True
#                     cur_time = timer()

                

    
                

#     if finish == False:     

#         if rel_time:
#             new_time = timer()
#             if new_time-cur_time<2:
#                 text_reload = font1.render('Wait, reload...', True, (255,255,255))
#                 window.blit(text_reload, (250,250))
#             else:
#                 rel_time=False
#                 num_fire=0
#         window.blit(background,(0, 0))
#         player.update()
#         player.reset()
#         EnemyGroup.update()
#         EnemyGroup.draw(window)
#         Bullets.update()
#         Bullets.draw(window)
#         AsteroidGroup.update()
#         AsteroidGroup.draw(window)

#         text_score = font1.render('Счёт: '+str(score), 1, (255,255,255))
#         window.blit(text_score, (10,20))
#         text_lose = font1.render('Пропущено: '+str(lost), 1, (255,255,255))
#         window.blit(text_lose, (10,50))
#     sprite_list = sprite.groupcollide(AsteroidGroup, Bullets, False, True)
#     sprite_list = sprite.groupcollide(EnemyGroup, Bullets, True, True)
#     for mnst in sprite_list:
#         score +=1
#         enemy1 = Enemy('ufo.png', randint(5,win_width-70),-40, 65, 45,randint(1,5))
#         EnemyGroup.add(enemy1)
    
#     if score >=10:
#         finish = True
#         win = font1.render('YOU WIN!', 1, (255,255,255))
#         window.blit(win, (250,250)) 
    # sprite_list = sprite.spritecollide(player, EnemyGroup, False)
    # if lost >3 or len(sprite_list)>0:
    #     finish = True
    #     win = font1.render('YOU LOOSE!', 1, (255,255,255))
    #     window.blit(win, (250,250))

#     display.update()
#     clock.tick(FPS)

