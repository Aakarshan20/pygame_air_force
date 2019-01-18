import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply

from pygame.locals import *
from random import *

bg_size = width, height= 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飛機大戰")

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

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


def inc_speed(target, inc):#加速
    for each in target:
        each.speed += inc
        
    

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
    bullet_sound.set_volume(sound_volume*0.5)
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

    #生成普通子彈
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4#宏定義

    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))#飛機中上位置傳給子彈

    #生成超級子彈
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8#宏定義

    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-21, me.rect.centery)))#左翼
        bullet2.append(bullet.Bullet2((me.rect.centerx+22, me.rect.centery)))#右翼

    clock = pygame.time.Clock()

    #中彈圖像索引
    e1_destory_index = 0
    e2_destory_index = 0
    e3_destory_index = 0
    me_destory_index = 0

    #統計用戶得分
    score =0
    score_font = pygame.font.Font('font/msjhbd.ttf',36)#引入微軟正黑 大小36


    #用於阻止重覆打開記錄文件
    recorded = False
    
    #標誌是否暫停遊戲
    paused = False

    #用於切換圖片
    switch_image = True
    #暫停圖(正常)
    pause_nor_image = pygame.image.load('images/pause_normal.png').convert_alpha()
    #暫停圖(hover)
    pause_pressed_image = pygame.image.load('images/pause_hover.png').convert_alpha()
    #開始圖(正常)
    start_nor_image = pygame.image.load('images/play_normal.png').convert_alpha()
    #開始圖(hover)
    start_pressed_image = pygame.image.load('images/play_hover.png').convert_alpha()

    #圖片大小都一樣所以取得其中一個的矩型即可
    paused_rect = pause_nor_image.get_rect()
    paused_rect.top, paused_rect.left = 10, (width-paused_rect.width -10)
    pause_image = pause_nor_image#預設為第一張圖

    #設置難度級別
    level =1
    
    #設置全屏炸彈
    bomb_image = pygame.image.load('images/nuclear_icon_small.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    #bomb_rect.left, bomb_rect.top = 10, height - bomb_rect.height-10
    bomb_font =  pygame.font.Font('font/msjhbd.ttf',48)#引入微軟正黑 大小48
    bomb_num = 3
    
    #每30秒發一次補給包
    bullet_supply = supply.Bullet_Supply(bg_size)    
    bomb_supply = supply.Bomb_Supply(bg_size)
    #全屏炸彈定時器
    SUPPLY_TIME = USEREVENT#自定義事件
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)#30*1000ms
    #pygame.time.set_timer(SUPPLY_TIME, 5 * 1000)#5*1000ms

    
    #超級子彈的定時器
    DOUBLE_BULLET_TIME = USEREVENT+1

    #標誌是否使用超級子彈
    is_double_bullet = False

    #復活後無敵時間的計時器
    INVINCIBLE_TIME = USEREVENT+2


    #我方生命數
    life_image = pygame.image.load('images/life.png')
    life_rect = life_image.get_rect()
    life_num = 1    

    #game over畫面
    gameover_font =pygame.font.Font('font/msjhbd.ttf',36)#引入微軟正黑 大小36
    again_image = pygame.image.load('images/restart.png').convert_alpha()
    again_rect = again_image.get_rect()

    gameover_image = pygame.image.load('images/quit.png').convert_alpha()
    gameover_rect = gameover_image.get_rect()
    
    
    
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
                        bullet_sound.set_volume(sound_volume*0.5)
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
                        bullet_sound.set_volume(sound_volume*0.5)
                        bomb_sound.set_volume(sound_volume)
                        supply_sound.set_volume(sound_volume)
                        get_bomb_sound.set_volume(sound_volume)
                        get_bullet_sound.set_volume(sound_volume)
                        upgrade_sound.set_volume(sound_volume)
                        enemy_flying_sound.set_volume(sound_volume)
                        enemy_down_sound.set_volume(sound_volume)
                        me_down_sound.set_volume(sound_volume)
                        me_down_sound.set_volume(me_sound_volume)
                #if event.key ==K_SPACE:
                    #bullet_sound.play()
                #if event.key ==K_RALT:
                if event.key ==K_SPACE:
                    if bomb_num:#查看炸彈是否有庫存
                        bomb_num -=1
                        bomb_sound.play()
                        for each in enemies:#循環每個敵人
                            if each.rect.bottom >0:
                                each.active = False#改為陣亡
                                

                

            if event.type == MOUSEBUTTONDOWN:
                #按下鼠標左鍵 且在暫停圖內
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused #直接取反改狀態
                    if paused:
                        #暫停背景音樂與其他音效
                        pygame.time.set_timer(SUPPLY_TIME, 0)#取消自定義事件
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30*1000)#取消自定義事件
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            if event.type == MOUSEMOTION:#修改hover樣式
                if paused_rect.collidepoint(event.pos):
                    #如果是暫停狀態下 更換暫停的圖片 反之 更換開始的圖片
                    if paused:
                        pause_image = start_pressed_image
                    else:
                        pause_image = pause_pressed_image
                else:#鼠標不在pause圖片的區域中
                    if paused:
                        pause_image = start_nor_image
                    else:
                        pause_image = pause_nor_image
            
            if event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):#隨機二選一
                    bomb_supply.reset()
                    #bullet_supply.reset()
                else:
                    bullet_supply.reset()
            
            if event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible= False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)
                
                

        #根據用戶的得分增加難度
        if level ==1 and score > 5000:
            level =2
            upgrade_sound.play()#難度提升的音效
            #增加3小型 2中型 1大型敵機
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)

            #提速
            inc_speed(small_enemies, 1)

        elif level ==2 and score > 30000:
            level =3
            upgrade_sound.play()#難度提升的音效
            #增加5小型 3中型 2大型敵機
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            #提速
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level ==3 and score > 600000:
            level =4
            upgrade_sound.play()#難度提升的音效
            #增加5小型 3中型 2大型敵機
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            #提速
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        elif level ==5 and score > 1000000:
            level =5
            upgrade_sound.play()#難度提升的音效
            #增加5小型 3中型 2大型敵機
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            #提速
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)
            
        screen.blit(background,(0,0))           
                    
        if life_num and not paused:#有餘命且沒按暫停才進行主流程
            
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
            

            #檢查是否有出現補給
            #繪製全屏炸彈補給與檢查玩家是否獲得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    #代表獲得補給(發生碰撞)
                    get_bomb_sound.play()
                    if bomb_num <3: #炸彈最多3個
                        bomb_num +=1
                    bomb_supply.active=False#取得後就消除該補給
            
            #繪製雙重子彈補給與檢查玩家是否獲得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    #代表獲得補給(發生碰撞)
                    get_bullet_sound.play()
                    #發射超級子彈
                    is_double_bullet = True
                    
                    #18秒後呼叫DOUBLE_BULLET_TIME事件 關閉雙重子彈
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18*1000)
                    bullet_supply.active=False#取得後就消除該補給
            
            
            
            #發射子彈(10幀一次)
            if not (delay % 10):
                bullet_sound.play()
                bullets = []
                #檢查是否為超級子彈
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-21, me.rect.centery))#左翼
                    bullets[bullet2_index+1].reset((me.rect.centerx+22, me.rect.centery))#右翼
                    bullet2_index = (bullet2_index +2 ) % BULLET2_NUM#八顆
                    
                else:
                    bullets = bullet1
                    
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index +1 ) % BULLET1_NUM#四顆
                

            #檢查子彈是否與敵機發生碰撞
            #for b in bullets:
            for b in bullets:
                if b.active:#活的子彈才要檢查
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:#有東西 代表有碰到敵機
                        b.active = False#清除子彈
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:#如果是中/大型敵機 擊中先扣血
                                e.hit = True#中彈屬性
                                e.enegy -=1
                                if e.enegy == 0 :#血量見底
                                    e.active = False#清除
                            else:
                                e.active = False#清除敵機
                        

            #繪製大型飛機
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:#中彈
                        #繪製被打到的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else: 
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    #畫血條(底色)
                    pygame.draw.line(screen, WHITE, \
                                     (each.rect.left, each.rect.top-5), \
                                     (each.rect.right, each.rect.top-5),2)#圖像上方5pixel處 寬度2pixel
                    #當生命>20% 畫綠色 否則紅色
                    enegy_remain = each.enegy / enemy.BigEnemy.enegy
                    if enegy_remain > 0.2:
                        enegy_color = GREEN
                    else:
                        enegy_color = RED
                    pygame.draw.line(screen, enegy_color,\
                                     (each.rect.left, each.rect.top-5), \
                                     #左邊起算加上寬度(總長度)乘以血量的比例
                                     (each.rect.left + each.rect.width*enegy_remain, \
                                      each.rect.top-5),2)#圖像上方5pixel處 寬度2pixel
                    
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
                            score += 10000
                            each.reset()
                            
                    

            #繪製中型飛機
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:#中彈
                        #繪製被打到的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else: 
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    #畫血條(底色)
                    pygame.draw.line(screen, WHITE, \
                                     (each.rect.left, each.rect.top-5), \
                                     (each.rect.right, each.rect.top-5),2)#圖像上方5pixel處 寬度2pixel
                    #當生命>20% 畫綠色 否則紅色
                    enegy_remain = each.enegy / enemy.MidEnemy.enegy
                    if enegy_remain > 0.2:
                        enegy_color = GREEN
                    else:
                        enegy_color = RED
                    pygame.draw.line(screen, enegy_color,\
                                     (each.rect.left, each.rect.top-5), \
                                     #左邊起算加上寬度(總長度)乘以血量的比例
                                     (each.rect.left + each.rect.width*enegy_remain, \
                                      each.rect.top-5),2)#圖像上方5pixel處 寬度2pixel
                else:
                    #陣亡
                    enemy_down_sound.play()
                    if not (delay %5):
                        if e1_destory_index == 0:
                            enemy_down_sound.play()
                        screen.blit(each.destory_images[e2_destory_index], each.rect)
                        e2_destory_index = (e2_destory_index +1)%4
                        if e2_destory_index == 0:
                            score += 5000
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
                            score += 1000
                            each.reset()

            #檢測我方飛機是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, \
                                                       pygame.sprite.collide_mask)

            if enemies_down and not me.invincible:#我方被撞 且重生無敵時間已過
                me.active = False
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
                        life_num -=1
                        me.reset()
                        #調用重生計時器
                        pygame.time.set_timer(INVINCIBLE_TIME, 3*1000)#3000ms
                        #print("Game over")
                        #running = False
            
            #繪製全屏炸彈數量
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height-10-bomb_rect.height))
            screen.blit(bomb_text, (20+bomb_rect.width, height-5-text_rect.height))

            #繪製飛機生命值
            if life_num :
                for i in range(life_num):
                    screen.blit(life_image, \
                                (width -10 - (i+1) * life_rect.width, \
                                height -10 - life_rect.height))        
            #繪製得分: 將string渲染成surface對象 True=抗鋸齒 WHITE字體前景色
            score_text = score_font.render("Score: %s" % str(score), True, WHITE)

            screen.blit(score_text, (10,30))

        #繪製遊戲結束畫面
        elif life_num == 0:#不能用else 因為會連按暫停都給你結束
            #背景音樂停止
            pygame.mixer.music.stop()

            #停止全部音效
            pygame.mixer.stop()

            #停止發放補給
            pygame.time.set_timer(SUPPLY_TIME, 0)

            #如果還沒開過文件
            if not recorded:
                recorded = True#設為開過檔案

                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))

                
                
            #繪製結束介面
            screen.blit(background,(0,0))  
            record_score_text = score_font.render("Best :%d" % record_score, True ,WHITE)
            screen.blit(record_score_text, (50,50))
            #screen.blit(background,(0,0))  #---
            gameover_text1 = gameover_font.render("Your Score " , True , WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                      (width - gameover_text1_rect.width)//2,height //3

            screen.blit(gameover_text1, gameover_text1_rect)
            #screen.blit(background,(0,0))  #---
            gameover_text2 = gameover_font.render(str(score), True ,WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                      (width - gameover_text2_rect.width)//2, \
                                      gameover_text1_rect.bottom +10

            screen.blit(gameover_text2, gameover_text2_rect)
            #screen.blit(background,(0,0))  #----
            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            #screen.blit(background,(0,0))  #---

            #檢測用戶鼠標操作
            #如果是左鍵
            if pygame.mouse.get_pressed()[0]:
                # 獲取滑鼠座標
                pos = pygame.mouse.get_pos()
                #如果用戶點擊"重新開始"
                if again_rect.left < pos[0] < again_rect.right and \
                    again_rect.top < pos[1] < again_rect.bottom:
                    #調用main() 重新開始遊戲
                    main()
                #如果用戶點擊"結束"    
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                    gameover_rect.top < pos[1] < gameover_rect.bottom:
                    #結束遊戲
                    pygame.quit()
                    sys.exit()
                    

                                    
            #running = False
            
            
        

        #繪製暫停按紐
        screen.blit(pause_image,paused_rect)
            
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








