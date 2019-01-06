import pygame
import sys
import traceback
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height= 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飛機大戰")

background = pygame.image.load('images/Faux_Space.png')


#載入遊戲音樂
bgm_volume = 0.2
sound_volume = 0.2
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
enemy_flying_sound.set_volume(sound_volume)
enemy_down_sound = pygame.mixer.Sound('sounds/enemy_down.wav')
enemy_down_sound.set_volume(sound_volume)
me_down_sound = pygame.mixer.Sound('sounds/me_down.wav')
me_down_sound.set_volume(sound_volume)



def main():
    pygame.init()
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background,(0,0))

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







