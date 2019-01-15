import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('images/planeB.png').convert_alpha()
        self.image2 = pygame.image.load('images/planeB_2.png').convert_alpha()

        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("images/planeB_die_1.png").convert_alpha(),\
            pygame.image.load("images/planeB_die_2.png").convert_alpha(),\
            pygame.image.load("images/planeB_die_3.png").convert_alpha(),\
            pygame.image.load("images/planeB_die_4.png").convert_alpha()\

        ])

        
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2

        self.active = True#未陣亡
        self.mask = pygame.mask.from_surface(self.image1)#非透明部份檢測        

        self.rect.left, self.rect.top = \
                        randint(0,self.width - self.rect.width),\
                        randint(-5*self.height ,0)
        
    def move(self):#敵人只往下衝
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.active = True#復活
        self.rect.left, self.rect.top = \
                randint(0,self.width - self.rect.width),\
                randint(-5*self.height ,0)


class MidEnemy(pygame.sprite.Sprite):
    #敵機生命值
    enegy = 8
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('images/planeC.png').convert_alpha()
        self.image2 = pygame.image.load('images/planeC_2.png').convert_alpha()

        #中彈特效
        self.image_hit = pygame.image.load("images/planeC_die_1.png").convert_alpha()

        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("images/planeC_die_1.png").convert_alpha(),\
            pygame.image.load("images/planeC_die_2.png").convert_alpha(),\
            pygame.image.load("images/planeC_die_3.png").convert_alpha(),\
            pygame.image.load("images/planeC_die_4.png").convert_alpha()\

        ])

        
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        
        self.active = True#未陣亡
        self.mask = pygame.mask.from_surface(self.image1)#非透明部份檢測

        self.enegy = MidEnemy.enegy
        
        self.rect.left, self.rect.top = \
                        randint(0,self.width - self.rect.width),\
                        randint(-10*self.height ,-self.height)

        self.hit = False
        
    def move(self):#敵人只往下衝
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.active = True#復活
        self.enegy = MidEnemy.enegy
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width),\
            randint(-10*self.height ,-self.height)



class BigEnemy(pygame.sprite.Sprite):
    #敵機生命值
    enegy = 20
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('images/planeE.png').convert_alpha()
        self.image2 = pygame.image.load('images/planeE_2.png').convert_alpha()

        #中彈特效
        self.image_hit = pygame.image.load("images/planeE_die_1.png").convert_alpha()

        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("images/planeE_die_1.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_2.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_1.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_2.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_1.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_2.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_3.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_2.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_3.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_4.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_4.png").convert_alpha(),\
            pygame.image.load("images/planeE_die_4.png").convert_alpha()
        ])

        
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1

        self.active = True#未陣亡
        self.mask = pygame.mask.from_surface(self.image1)#非透明部份檢測

        self.enegy = BigEnemy.enegy

        self.rect.left, self.rect.top = \
                        randint(0,self.width - self.rect.width),\
                        randint(-10*self.height ,-5*self.height)

        self.hit = False
        
    def move(self):#敵人只往下衝
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):

        self.active = True#復活
        self.enegy = BigEnemy.enegy
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width),\
            randint(-10*self.height ,-5*self.height)
