import math
import os
import random
import sys
import time
import pygame as pg
from pygame.sprite import Group

WIDTH, HEIGHT = 1200, 900
NUM_OF_ENEMYS = 10

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    
    yoko, tate = True, True
    if obj_rct.right < 0 or WIDTH < obj_rct.left:
        yoko = False
    if obj_rct.bottom < 0 or HEIGHT < obj_rct.top:
        tate = False
    return yoko, tate

def calc_orientation(org: pg.Rect, dst: pg.Rect) -> tuple[float, float]:
    x_diff, y_diff = dst.centerx - org.centerx, dst.centery - org.centery
    norm = math.sqrt(x_diff ** 2 + y_diff ** 2)
    return x_diff / norm, y_diff / norm

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pg.transform.rotozoom(pg.image.load("fig/character_monster_skeleton_02.png"), 0, 0.1)
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.vx, self.vy = +5, +5

    def update(self, screen: pg.Surface):
        
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


def main():
    tmr = 0
    clock = pg.time.Clock()
    pg.display.set_caption("roguelike")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.transform.rotozoom(pg.image.load(f"fig/maptile_sogen_02.png"), 0, 2.5)
    emys = pg.sprite.Group()
    #enemys = [Enemy((255, 0, 0), 10) for i in range(NUM_OF_ENEMYS)]

    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 
        screen.blit(bg_img, [0, 0])

        if tmr % 200 ==0:
            emys.add(Enemy())
        emys.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
