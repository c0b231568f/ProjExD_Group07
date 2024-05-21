import math
import os
import random
import sys
import time
import pygame as pg
from pygame.sprite import Group

WIDTH, HEIGHT = 1200, 900

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    画面内判定 : 中のときTrue
    """
    yoko, tate = True, True
    if obj_rct.right < 0 or WIDTH < obj_rct.left:
        yoko = False
    if obj_rct.bottom < 0 or HEIGHT < obj_rct.top:
        tate = False
    return yoko, tate


class Hero:
    """
    主人公に関するクラス
    """
    spd = 1.0
    delta = {
        pg.K_UP: (0, -5*spd),
        pg.K_RIGHT: (5*spd, 0),
        pg.K_DOWN: (0, 5*spd),
        pg.K_LEFT: (-5*spd, 0),
    }
    img0 = pg.transform.rotozoom(pg.image.load("fig/hero0.png"), 0, 1.0)
    img = pg.transform.flip(img0, True, False)
    imgs = {
        (+5*spd, 0): img0,  # 右
        (+5*spd, -5*spd): img0,  # 右上
        (0, -5*spd): img0,  # 上
        (-5*spd, -5*spd): img,  # 左上
        (-5*spd, 0): img,  # 左
        (-5*spd, +5*spd): img,   # 左下
        (0, +5*spd): img,  # 下
        (+5*spd, +5*spd): img0,  # 右下
    }

    def __init__(self, xy: tuple[int, int]):
        """
        Surfaceつくる
        """
        self.img0 = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy

    def update(self, key_lst: list[bool], spd: float, screen: pg.Surface):
        """
        移動させる
        """
        sum_mv = [0, 0]
        self.spd = spd
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs[tuple(sum_mv)]
        screen.blit(self.img, self.rct)


    def mvd(self, key_lst: [bool], spd: float) -> tuple[int, int]:
        """
        総移動距離
        """
        ttl_mv = [0, 0]
        seld.spd = spd
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                ttl_mv[0] += mv[0]
                ttl_mv[1] += mv[1]
        return ttl_mv


def main():
    tmr = 0
    spd = 1.0
    clock = pg.time.Clock()
    pg.display.set_caption("roguelike")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    hero = Hero((WIDTH/2, HEIGHT/2))

    while True:
        pass

    key_lst = pg.key.get_pressed()
    hero.update(key_lst, spd, screen)
    total_moved = hero.mvd(key_lst, spd)
    pg.display.update()
    clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
