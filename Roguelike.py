import math
import os
import random
import sys
import time
import pygame as pg
from pygame.sprite import Group


WIDTH, HEIGHT = 1200, 900
FIELDRANGE = 1200


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def calc_orientation(org: pg.Rect, dst: pg.Rect) -> tuple[float, float]:
    """
    オブジェクト同士のベクトル計算メソッド
    引数: org: pg.Rect, dst: pg.Rect (orgからみたdstのベクトルを計算)
    戻り値: orgからみたdstのx方向の距離, orgからみたdstのy方向の距離
    """
    x_diff, y_diff = dst.centerx - org.centerx, dst.centery - org.centery
    norm = math.sqrt(x_diff ** 2 + y_diff ** 2)
    return x_diff / norm, y_diff / norm


def over_field(obj_rct: pg.Rect) -> bool:
    """
    オブジェクトがフィールド外にいったらTrueを返す関数
    引数：pg.Rect
    戻り値：T/F
    """
    if obj_rct.left < 0 - FIELDRANGE or \
        WIDTH + FIELDRANGE < obj_rct.right or \
        obj_rct.top < 0 - FIELDRANGE or \
        HEIGHT + FIELDRANGE < obj_rct.bottom:
        return True
    return False


class Weapon(pg.sprite.Sprite):
    """
    Heroクラスをベースに武器にまつわるクラス
    引数：Heroクラス
    """
    def __init__(self, hero):
        super().__init__()

    def update():
        pass

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
        pg.K_UP: (0, -1),
        pg.K_RIGHT: (1, 0),
        pg.K_DOWN: (0, 1),
        pg.K_LEFT: (-1, 0),
    }
    
    img0 = pg.transform.rotozoom(pg.image.load("fig/hero0.png"), 0, 0.15)
    img = pg.transform.flip(img0, True, False)

    imgs = {
        (+1, 0): img0,  # 右
        (+1, -1): img0,  # 右上
        (0, -1): img0,  # 上
        (-1, -1): img,  # 左上
        (-1, 0): img,  # 左
        (-1, +1): img,   # 左下
        (0, +1): img,  # 下
        (+1, +1): img0,  # 右下
    }

    def __init__(self, xy: tuple[int, int]):
        """
        Surfaceつくる
        """
        self.spd = __class__.spd
        self.img0 = self.imgs[(+1, 0)]
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
                sum_mv[0] += mv[0]*spd
                sum_mv[1] += mv[1]*spd
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if any(sum_mv): # sum_mv両方0の時のみFalse
            self.img = __class__.imgs[tuple([_/abs(_) if _ != 0 else 0 for _ in sum_mv])] # __class__.imgsのkeyの値に整形
        screen.blit(self.img, self.rct)


    def mvd(self, key_lst: list[bool], spd: float) -> tuple[int, int]:
        """
        総移動距離
        """
        ttl_mv = [0, 0]
        self.spd = spd
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                ttl_mv[0] += mv[0]
                ttl_mv[1] += mv[1]
        return ttl_mv


def main():
    """
    main関数
    """
    tmr = 0
    spd = 10.0
    hp = 100
    clock = pg.time.Clock()
    pg.display.set_caption("roguelike")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"fig/maptile_sogen_02.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH/30, HEIGHT/30))
    hero = Hero((WIDTH/2, HEIGHT/2))

    while True:
        # hero = Hero()
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        total_dist = hero.mvd(key_lst, spd)# hero.mvd() # hero.mvdメソッドは、他のメンバーが作る予定（戻り値x, yのタプル）
        for i in range(90):
            for j in range(90):
                screen.blit(bg_img, [-WIDTH + i*WIDTH/30 + (total_dist[0]%(WIDTH/30)), -HEIGHT + j*HEIGHT/30+ (total_dist[1]%(HEIGHT/30))])


        hero.update(key_lst, spd, screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
