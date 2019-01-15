import pygame
import sys
import traceback
import myplane
#import bullet
import enemy
#import supply

from pygame.locals import *
from random import *

bg_size = width, height= 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飛機大戰")

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
        
def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.MidEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def main():
    pygame.init()
    pygame.mixer.init()

    

    

    background = pygame.image.load('images/Faux_Space.png')
    
    #載入遊戲音樂
    bgm_volume = 0.2
    sound_volume = 0.1
    me_sound_volume = 0.01
    pygame.mixer.music.load('sounds/game_music.wav')
    pygame.mixer.music.set_volume(bgm_volume)

    bullet_sound = pygame.mixer.Sound('sounds/bullet.wav')
    bullet_sound.set_volume(sound_volume)
    bomb_sound = pygame.mixer.Sound('sounds/use_bomb.wav')
    bomb_sound.set_volume(sound_volume)
    supply_sound = pygame.mixer.Sound('sounds/supply.wav')
    supply_sound.set_volume(sound_volume)
    get_bomb_sound = pygame.mixer.Sound('sounds/get_bomb.wav')
    get_bomb_sound.set_volume(sound_volume)
    get_bullet_sound = pygame.mixer.Sound('sounds/get_bullet.wav')
    get_bullet_sound.set_volume(sound_volume)
    upgrade_sound = pygame.mixer.Sound('sounds/upgrade.wav')
    upgrade_sound.set_volume(sound_volume)
    enemy_flying_sound = pygame.mixer.Sound('sounds/enemy_flying.wav')
    enemy_flying_sound.set_volume(0.2)
    enemy_down_sound = pygame.mixer.Sound('sounds/enemy_down.wav')
    enemy_down_sound.set_volume(sound_volume)
    me_down_sound = pygame.mixer.Sound('sounds/me_down.wav')
    me_down_sound.set_volume(me_sound_volume)


    pygame.mixer.music.play(-1)
    #生成我方飛機
    me = myplane.MyPlane(bg_size)

    #生成敵方飛機
    enemies = pygame.sprite.Group()

    #生成敵方小飛機
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    #生成敵方中飛機
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    

    #生成敵方大飛機
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)


    clock = pygame.time.Clock()

    #中彈圖像索引
    e1_destory_index = 0
    e2_destory_index = 0
    e3_destory_index = 0
    me_destory_index = 0
    

    #用於切換圖片
    switch_image = True

    #用於延遲
    delay = 100
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_KP_MINUS:
                    if bgm_volume > 0:
                        bgm_volume -=0.01
                        pygame.mixer.music.set_volume(bgm_volume)
                    if sound_volume > 0:
                        sound_volume -=0.01
                        me_sound_volume -=0.01
                        bullet_sound.set_volume(sound_volume)
                        bomb_sound.set_volume(sound_volume)
                        supply_sound.set_volume(sound_volume)
                        get_bomb_sound.set_volume(sound_volume)
                        get_bullet_sound.set_volume(sound_volume)
                        upgrade_sound.set_volume(sound_volume)
                        enemy_flying_sound.set_volume(sound_volume)
                        enemy_down_sound.set_volume(sound_volume)
                        me_down_sound.set_volume(me_sound_volume)
                    
                if event.key == K_KP_PLUS:
                    if bgm_volume < 0.5:
                        bgm_volume +=0.01
                        pygame.mixer.music.set_volume(bgm_volume)
                    if sound_volume < 0.5:
                        sound_volume +=0.01
                        me_sound_volume +=0.01
                        bullet_sound.set_volume(sound_volume)
                        bomb_sound.set_volume(sound_volume)
                        supply_sound.set_volume(sound_volume)
                        get_bomb_sound.set_volume(sound_volume)
                        get_bullet_sound.set_volume(sound_volume)
                        upgrade_sound.set_volume(sound_volume)
                        enemy_flying_sound.set_volume(sound_volume)
                        enemy_down_sound.set_volume(sound_volume)
                        me_down_sound.set_volume(sound_volume)
                        me_down_sound.set_volume(me_sound_volume)
                if event.key ==K_SPACE:
                    bullet_sound.play()
                if event.key ==K_RALT:
                    bomb_sound.play()
        #檢測用戶的鍵盤操作
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()

        screen.blit(background,(0,0))

        #繪製大型飛機
        for each in big_enemies:
            if each.active:
                each.move()
                if switch_image:
                    screen.blit(each.image1, each.rect)
                else:
                    screen.blit(each.image2, each.rect)

                #大型機音效
                if each.rect.bottom == -50:
                    enemy_flying_sound.play(-1)

            else:
                #陣亡
                enemy_down_sound.play()
                if not (delay %5):
                    if e1_destory_index == 0:
                        enemy_down_sound.play()
                    screen.blit(each.destory_images[e3_destory_index], each.rect)
                    e3_destory_index = (e3_destory_index +1)%12
                    if e3_destory_index == 0:
                        enemy_flying_sound.stop()
                        each.reset()
                    
                

        #繪製中型飛機
        for each in mid_enemies:
            if each.active:
                each.move()
                if switch_image:
                    screen.blit(each.image1, each.rect)
                else:
                    screen.blit(each.image2, each.rect)
            else:
                #陣亡
                enemy_down_sound.play()
                if not (delay %5):
                    if e1_destory_index == 0:
                        enemy_down_sound.play()
                    screen.blit(each.destory_images[e2_destory_index], each.rect)
                    e2_destory_index = (e2_destory_index +1)%4
                    if e2_destory_index == 0:
                        each.reset()

        #繪製小型飛機
        for each in small_enemies:
            if each.active:
                each.move()
                if switch_image:
                    screen.blit(each.image1, each.rect)
                else:
                    screen.blit(each.image2, each.rect)
            else:
                #陣亡
                
                if not (delay %5):
                    if e1_destory_index == 0:
                        enemy_down_sound.play()
                    screen.blit(each.destory_images[e1_destory_index], each.rect)
                    e1_destory_index = (e1_destory_index +1)%4
                    if e1_destory_index == 0:
                        each.reset()

        #檢測我方飛機是否被撞
        enemies_down = pygame.sprite.spritecollide(me, enemies, False, \
                                                   pygame.sprite.collide_mask)

        if enemies_down:#我方已掛
            #me.active = False
            for e in enemies_down:
                e.active = False#敵方也順便爆炸
            
        
        #繪製我方飛機
        if me.active:#存活
            if switch_image:
                screen.blit(me.image1, me.rect)
            else:
                screen.blit(me.image2, me.rect)

        else:
            #陣亡
            if not (delay %5):
                if e1_destory_index == 0:
                        enemy_down_sound.play()
                screen.blit(me.destory_images[me_destory_index], me.rect)
                me_destory_index = (me_destory_index +1)%4
                if me_destory_index == 0:
                    #me.reset()
                    print("Game over")
                    running = False
            
        if not (delay%5):#切換
            switch_image = not switch_image
            
        delay -=1
        if not delay:
            delay = 100
        
        pygame.display.flip()

        clock.tick(60)#60幀per second

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()








