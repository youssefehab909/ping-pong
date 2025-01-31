from pygame import *
from random import randint
from time import time as timer

width = 700
height = 500
lost = 0
score = 0
lives = 3
rel_time = False
num_fire = 0



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x,size_y, player_speed):
        super().__init__()
        self.player_image = player_image
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

    def transfer(self, x, y):
        window.blit(self.image, (x, y ))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        # left
        if keys[K_LEFT] and self.rect.x > 0 :
            self.rect.x -= self.speed
        # right
        if keys[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed

    def fire(self):
        # create bullet 
        bullet = Bullet("bullet.png", self.rect.centerx - 8 , self.rect.top, 15, 20, 15)
        # add bullet to the group of bullets 
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        # move from top to button
        self.rect.y += self.speed
        global lost
        # check if reaching the button
        if self.rect.y >= (height - 20): 
            # reset y and x
            self.rect.y = 0
            self.rect.x = randint(0, width - 80)
            if self.player_image == "ufo.png":
                lost += 1


class Bullet(GameSprite):
    def update(self):
        # move from bottom to top 
        self.rect.y -= self.speed

        # check if reach the top
        if self.rect.y <= 0:
            self.kill()


window = display.set_mode((width, height))
display.set_caption("Shooter")

# background
background = transform.scale(image.load("galaxy.jpg"), (width, height))

# bullets group
bullets = sprite.Group()

# sprites
player = Player("rocket.png", 350, 400, 50, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monsters.add(Enemy("ufo.png", randint(0, width - 80), 0, 60, 40, randint(1, 5)))

asteroids = sprite.Group()
for i in range(2):
    asteroids.add(Enemy("asteroid.png", randint(0, width - 80), 0, 60, 40, randint(1, 5)))

# music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound('fire.ogg')

# font
font.init()
style = font.SysFont("Arial", 36)
style2 = font.SysFont("Arial", 70)

text_lost = style.render("Missed:"+ str(lost), 1 ,(255, 255, 255))
text_score = style.render("Score:"+ str(score), 1 ,(255, 255, 255))
win = style2.render("You win", True, (10, 255, 10))
lose = style2.render("You lose", True, (255, 10, 10))

life_text = style2.render(str(lives) , True, (255, 255, 255))

# clock
fps = 60
clock = time.Clock()

# game loop
game = True
finish = False
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
            # check fire state
                if num_fire < 5 and rel_time == False:
                    # sound
                    fire.play()
                    # bullet
                    player.fire()
                    num_fire += 1
                     
            # check reload state
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
            




    if not finish:
        window.blit(background, (0,0))

        player.update()
        player.reset()
        
        monsters.draw(window)
        monsters.update() 

        asteroids.draw(window)
        asteroids.update() 

        bullets.draw(window)
        bullets.update()

        text_lost = style.render("Missed:"+ str(lost), 1 ,(255, 255, 255))
        text_score = style.render("Score:"+ str(score), 1 ,(255, 255, 255))
        life_text = style2.render(str(lives) , True, (255, 255, 255))

        window.blit(text_score, (10, 10))
        window.blit(text_lost, (10, 40))
        window.blit(life_text, (width-50, 10))


        # check reloading state
        if rel_time == True:

            # check remaining time 
            now_time = timer()
            if (now_time - last_time) < 3:
                reloading = style.render("wait...reload", True, (150, 0, 0))
                window.blit(reloading, (260,450))
            else:
                # fire state
                num_fire = 0
                rel_time = False
        # win state
        if score >= 10:
            finish = True
            window.blit(win, (250, 200))


        # checker for collision bullets with monsters 
        monsters_list_bullets = sprite.groupcollide(monsters, bullets, True, True)
        for m in monsters_list_bullets:
            score += 1
            monsters.add(Enemy("ufo.png", randint(0, width - 80), 0, 60, 40, randint(1, 5)))

        # collision enemy with player
        monsters_list = sprite.spritecollide(player, monsters, True)
        asteroids_list = sprite.spritecollide(player, asteroids, True)
        # not empty == collision
        if monsters_list or asteroids_list:
            lives -= 1

        if lives <= 0:
            finish = True
            window.blit(lose, (300, 200))

        # miss 3 enemies
        if lost >= 3:
            finish = True
            window.blit(lose, (250, 200))

        # win state

    display.update()
    clock.tick(fps)
    time.delay(50)