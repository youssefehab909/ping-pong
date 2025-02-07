from pygame import *
from random import randint


width = 700
height = 500
speed_x = 5
speed_y = 5

blue = (200, 255, 255)
window = display.set_mode((width,height))
display.set_caption("Ping pong game")

window.fill(blue)


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

class Player(GameSprite):
    def update1(self):
        keys = key.get_pressed()
        # left
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        # right
        if keys[K_DOWN] and self.rect.y < height - 150:
            self.rect.y += self.speed

    def update2 (self):
        keys = key.get_pressed()
        # left
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        # right
        if keys[K_s] and self.rect.y < height - 150:
            self.rect.y += self.speed


class Ball(GameSprite):
    def update(self):
        global speed_y,speed_x, player1, player2

        self.rect.x += speed_x
        self.rect.y += speed_y

        #TODO: change direction = mutiply by -1
        #collision with up and down
        if self.rect.y < 0 or self.rect.y > height-50:
            speed_y*= -1
        #collision with paddels
        if sprite.collide_rect(player1, self) or sprite.collide_rect(player2, self):
            speed_x *= -1

player1 = Player("paddel.png",650 ,150, 50, 150, 10)
player2 = Player("paddel.png",5 ,150, 50, 150, 10)

ball = Ball("ball.png", 300, 250, 50, 50,5)

# music
# mixer.init()
# mixer.music.load("space.ogg")
# mixer.music.play()

# font
font.init()
style = font.SysFont("Arial", 36)
style2 = font.SysFont("Arial", 70)

win1 = style.render("PLAYER 1 WINS",True, (0,0,0))
win2 = style.render("PLAYER 2 WINS",True, (0,0,0))

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

       

    if not finish:
        window.fill(blue)
        player1.update1()
        player2.update2()

        player1.reset()
        player2.reset()

        ball.update()
        ball.reset()

        #player1 winning state
        if ball.rect.x < 0:
            window.blit(win1,(320,200))
            finish = True

        if ball.rect.x > 700:
            window.blit(win2,(320,200))
            finish = True
        #player2 winning state
    display.update()
    clock.tick(fps)
