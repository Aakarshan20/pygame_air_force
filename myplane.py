import pygame
import sys
from pygame import *

class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/planeA.png").convert_alpha();
        self.image2 = pygame.image.load("images/planeA_2.png").convert_alpha();                

        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("images/planeA_die_1.png").convert_alpha(),\
            pygame.image.load("images/planeA_die_2.png").convert_alpha(),\
            pygame.image.load("images/planeA_die_3.png").convert_alpha(),\
            pygame.image.load("images/planeA_die_4.png").convert_alpha()\

        ])


        self.rect = self.image1.get_rect()

        
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left , self.rect.top = \
                       (self.width - self.rect.width)//2,\
                       self.height-self.rect.height-60
        self.speed = 10

        self.active = True#未陣亡
        #調用mask.from_surface檢測非透明模塊的邊緣
        self.mask = pygame.mask.from_surface(self.image1)
        
    #定義四個方向的移動
    def moveUp(self):
        if self.rect.top >0:
            self.rect.top -= self.speed
        else:
            self.rect.top =0

    def moveDown(self):
        if self.rect.bottom> self.height -61:
            self.rect.bottom = self.height-60
        else:
            self.rect.top +=self.speed

    def moveLeft(self):
        if self.rect.left <1:
            self.rect.left = 0
        else:
            self.rect.left -=self.speed
        
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right +=self.speed
        else:
            self.rect.right = self.width
