import pygame 
import random
from actor import Player, Enemy, Bullet, Baby, Destroyer
from pygame.locals import *
from pygame import mixer


# configuraciones
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675

PLAYABLE_WIDTH = 1200
PLAYABLE_HEIGHT = 675


class App:
    def __init__(self, screen_width, screen_height, bg_color=(0, 0, 0)):
        self.width = screen_width
        self.height = screen_height
        self.bg_color = bg_color
    
        pygame.init()
        pygame.display.set_caption('Do Not Rage Quit (pre-alpha) ')

        self.font = pygame.font.Font('clase_9/assets/fonts/IceCreamPartySolid.ttf', 30)
        self.score = 0
        self.level = 1
        self.minutes = 0
        self.seconds = 0
        self.difficulty = 1000
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.background_image = pygame.image.load("clase_9/assets/images/bg1.jpg").convert()
        self.is_running = False

        # self.sprites es para renderizar
        self.sprites = pygame.sprite.Group()
        # self.enemies es para detectar colisiones
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.buffed_enemies = pygame.sprite.Group()

        self.ADD_ENEMY_EVENT = pygame.USEREVENT + 1
        self.TIME_EVENT = pygame.USEREVENT + 1

        self.player: Player = None
        self.clock = pygame.time.Clock()

        mixer.init()
        mixer.music.load('clase_9/assets/music/tokyo_drift.wav')
        mixer.music.play()

    def show_score(self, x, y):
        score = self.font.render("Kills: " + str(self.score), True, (0,0,0), (255,255,255))
        self.screen.blit(score, (x, y))
        time = self.font.render("Time: " + str(self.minutes) + ":" + str(self.seconds), True, (0,0,0), (255,255,255))
        self.screen.blit(time, (x + 150, y))
        pre_alpha = self.font.render("by Dr Sorro" , True, (0,0,0), (255,255,255))
        self.screen.blit(pre_alpha, (1050, y))

    def show_game_over(self):
       pass


    def add_player(self, player):
        self.player = player
        self.sprites.add(player)
    
    def add_enemy(self, enemy):
        self.enemies.add(enemy)
        self.sprites.add(enemy)
    
    def add_buffed_enemy(self, buffed_enemy):
        self.buffed_enemies.add(buffed_enemy)
        self.sprites.add(buffed_enemy)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        self.sprites.add(bullet)

    def hit_border(self, sprite, value_callback1, value_callback2, TOPLIMIT, BOTTOMLIMIT, coordinate):
        if sprite.rect[coordinate] + (sprite.width + sprite.height) > TOPLIMIT: 
                sprite.callback(value_callback1)
        if sprite.rect[coordinate] < BOTTOMLIMIT:  
                sprite.callback(value_callback2)

    def update(self, keys):
        self.player.update(keys)
        # sprite group
        self.enemies.update()
        self.buffed_enemies.update()
        self.bullets.update()
        self.screen.blit(self.background_image, [0, 30])
            #self.screen.fill(self.bg_color)
        # dibujar todos los sprites
        for sprite in self.sprites:
            self.screen.blit(sprite.surf, sprite.rect)
        # detectar colisiones entre el player y enemies
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.player.kill()
            self.is_running = False
        if pygame.sprite.spritecollideany(self.player, self.buffed_enemies):
            self.player.kill()
            self.is_running = False
        if pygame.sprite.groupcollide(self.bullets, self.enemies, True, True):
            self.score += 1
        bc = pygame.sprite.groupcollide(self.bullets, self.buffed_enemies, True, True)
        if bc:
            self.score += 2
        
        
        
        pygame.display.flip()
        # para mantener 30 frames por segundo
        self.clock.tick(20)

    def run(self):
        pygame.time.set_timer(self.TIME_EVENT, 1000)
    
        self.is_running = True
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                
                if event.type == self.TIME_EVENT:
                    if self.seconds == 59:
                        self.seconds = 0
                        self.minutes += 1
                    else:
                        self.seconds += 1
                    
                if event.type == self.ADD_ENEMY_EVENT:
                    if self.score < 30:
                        self.add_enemy(Baby()) 
                    if 100 > self.score > 15:
                        self.add_enemy(Enemy())
                    if self.score > 30:
                        self.add_buffed_enemy(Destroyer())
                    
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == K_1:
                        self.add_bullet(Bullet((self.player.rect[0] + self.player.rect[2]/2, self.player.rect[1] + self.player.rect[2]/2)))
            # if self.player.rect[1] + self.player.height  * 2 > SCREEN_HEIGHT :
            #     self.player.block_path(1)
            # if self.player.rect[1] < 40:  
            #     self.player.block_path(0)
            # if self.player.rect[0] + self.player.width * 2 > SCREEN_WIDTH : 
            #     self.player.block_path(3)
            # if self.player.rect[0] < 0:  
            #     self.player.block_path(2)

            self.hit_border(self.player, 1, 0, SCREEN_HEIGHT, 40, 1)
            self.hit_border(self.player, 3, 2, SCREEN_WIDTH, 0, 0)

            if 10 > self.score > 0:
                self.level = 2
                
            if 20 > self.score > 10:
                self.level = 3
                
            if 30 > self.score > 20:
                self.level = 4
                
            if 40 > self.score > 30:
                self.level = 5
                
            
            

            keys = pygame.key.get_pressed()
            self.show_score(0,0)
           
            # if keys[K_1]:
            #     self.add_bullet(Bullet((self.player.rect[0], self.player.rect[1])))
            self.update(keys)

        pygame.quit()


if __name__ == "__main__":
    app = App(SCREEN_WIDTH, SCREEN_HEIGHT)
    app.add_player(Player())
    app.run()
    