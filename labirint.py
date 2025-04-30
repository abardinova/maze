# Разработай свою игру в этом файле!
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, pictare, w, h, x, y):
        super().__init__()
        self.image=transform.scale(image.load(pictare),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self,  pictare, w, h, x, y, x_speed, y_speed):
        super().__init__(pictare, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        if (self.rect.x <= 620 and self.x_speed > 0) or (self.rect.x >= 0 and self.x_speed < 0):
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barries, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.right, p.rect.right) 
        if (self.rect.y <= 410 and self.y_speed > 0) or (self.rect.y >= 0 and self.y_speed < 0):    
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barries, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)        
    def fire(self):
        bullet = Bullet('bullet.png', 20, 15, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)
class Emeny(GameSprite): 
    def __init__(self,  pictare, w, h, x, y, speed):
        super().__init__(pictare, w, h, x, y)
        self.speed = speed
        self.direction = "left"
    def update(self):
            if self.rect.x <= 470:
                self.direction = "right"
            if self.rect.x >= 700 - 85:
                self.direction = "left"
            if self.direction == "left":
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed  
class Bullet(GameSprite): 
    def __init__(self,  pictare, w, h, x, y, speed):
        super().__init__(pictare, w, h, x, y)
        self.speed = speed
    def update(self):  
        self.rect.x += self.speed
        if self.rect.x > 700 :
            self.kill()



window = display.set_mode((700, 500))
display.set_caption('Первая игра!')
back = (250, 192, 203)
w1 = GameSprite('paint.webp', 80, 100,400,250)
w2 = GameSprite('paint.webp', 270, 100, 50, 400)
player = Player('hero.png', 80, 80, 5, 100, 0, 0)
final = GameSprite('pac1.webp', 80, 80, 620, 420)
monsters = sprite.Group()
monster = Emeny('pac2.png', 80, 80, 620, 180, 7)
monsters.add = monster
barries = sprite.Group()
barries.add(w1)
barries.add(w2)
bullets = sprite.Group()
speed = 10
run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
           if e.key == K_LEFT:
               player.x_speed = -speed
           elif e.key == K_RIGHT:
               player.x_speed = speed
           elif e.key == K_UP:
               player.y_speed = -speed
           elif e.key == K_DOWN:
               player.y_speed = speed
           elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
           if e.key == K_LEFT:
               player.x_speed = 0
           elif e.key == K_RIGHT:
               player.x_speed = 0
           elif e.key == K_UP:
               player.y_speed = 0
           elif e.key == K_DOWN:
               player.y_speed = 0
    if finish != True:
        window.fill(back)
        player.update()
        monster.update()
        bullets.update()

        barries.draw(window)
        bullets.draw(window)

        player.reset()        
        final.reset()
        monster.reset()

        sprite.groupcollide(bullets, barries, True, False)
        sprite.groupcollide(bullets, barries, True, True)
        if sprite.collide_rect(player, final):
            finish = True
            img = transform.scale(image.load('win.png'), (400,400))
            window.blit(img,(150,50))
        if sprite.collide_rect(player, monster):
            finish = True
            img = transform.scale(image.load('lose.jpg'), (400,400))
            window.blit(img,(150,50))
    display.update()