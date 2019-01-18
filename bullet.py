import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position#此處隨飛機的位置變化
        self.speed = 12#子彈速度略快於飛機速度
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)#取得子彈的邊緣(非透明部份)

    def move(self):
        self.rect.top -= self.speed#一直往上即可

        if self.rect.top < 0:
            self.active = False#清掉該子彈
            
    def reset(self, position):
        self.rect.left, self.rect.top = position[0]-5, position[1]-5#此處隨飛機的位置變化
        self.active = True

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position#此處隨飛機的位置變化
        self.speed = 12#子彈速度略快於飛機速度
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)#取得子彈的邊緣(非透明部份)

    def move(self):
        self.rect.top -= self.speed#一直往上即可

        if self.rect.top < 0:
            self.active = False#清掉該子彈
            
    def reset(self, position):
        self.rect.left, self.rect.top = position[0]-5, position[1]-5#此處隨飛機的位置變化
        self.active = True  


        
