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
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：敵Rect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.right < 0 or WIDTH < obj_rct.left:
        yoko = False
    if obj_rct.bottom < 0 or HEIGHT < obj_rct.top:
        tate = False
    return yoko, tate

def calc_orientation(org: pg.Rect, dst: pg.Rect) -> tuple[float, float]:
    x_diff, y_diff = dst.centerx - org.centerx, dst.centery - org.centery
    norm = math.sqrt(x_diff ** 2 + y_diff ** 2)
    if norm != 0:
        return x_diff / norm, y_diff / norm
    else:
        return 0, 0


class Enemy(pg.sprite.Sprite):
    """
    敵に関するクラス
    """
    imgs = [pg.transform.rotozoom(pg.image.load(f"fig/character_monster_{i}.png"), 0, 0.1) for i in range(0,2)]  # 敵の画像をロードする
    def __init__(self, hero:"Hero"):
        super().__init__()
        self.img = random.choice(__class__.imgs)  # 敵をランダムに出る
        self.sct = 10  # 敵のスポーンct
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 敵が出現するときの座標をランダムにする
        #敵が出現する時、攻撃対象のheroの方向を計算
        self.vx, self.vy = calc_orientation(self.rct, hero.rct)  
        #self.vx, self.vy = random.randint(-7, 7), random.randint(-7, 7)  # 敵の横方向、縦方向のベクトル
        self.speed = 7  # 敵の速さの設定

    def update(self,hero:"Hero", screen: pg.Surface):
        """
        敵を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.vx, self.vy = calc_orientation(self.rct, hero.rct)
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.speed*self.vx, self.speed*self.vy)
        screen.blit(self.img, self.rct)

    def cool(self, screen:pg.Surface):
        self.speed = 3
        self.sct = 100
        img = pg.Surface((WIDTH,HEIGHT))
        pg.draw.rect(img, (0, 0, 255), (0, 0, WIDTH, HEIGHT))
        img.set_alpha(60)
        screen.blit(img,[0, 0])
        pg.display.update()
        time.sleep(0.7)

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
    
    img0 = pg.transform.rotozoom(pg.image.load("fig/hero0.png"), 0, 0.1)
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

"""
class Cool(pg.sprite.Sprite):
    #敵を減速し、スポーンctを長くなる

    def __init__(self, screen):
        img = pg.Surface((WIDTH,HEIGHT))
        pg.draw.rect(img, (0, 0, 255), (0, 0, WIDTH, HEIGHT))
        img.set_alpha(60)
        screen.blit(img,[0, 0])
        pg.display.update()
        time.sleep(0.3)
    def update(self, emys: "Enemy", screen):
        for emy in emys:
            emy.speed = 0.5
        img = pg.Surface((WIDTH,HEIGHT))
        pg.draw.rect(img, (0, 0, 255), (0, 0, WIDTH, HEIGHT))
        img.set_alpha(60)
        screen.blit(img,[0, 0])
        pg.display.update()
        emys.sct = 1000
"""
def main():
    tmr = 0
    spd = 10.0
    hp = 100
    clock = pg.time.Clock()
    pg.display.set_caption("roguelike")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.transform.rotozoom(pg.image.load(f"fig/maptile_sogen_02.png"), 0, 2.5)  # 背景の画像を2.5倍してロードする
    emys = pg.sprite.Group()
    hero = Hero((WIDTH/2, HEIGHT/2))
    emy = Enemy(hero)

    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 
            if event.type == pg.KEYDOWN and event.key == pg.K_c: #and score.value >= 20:
                emy.cool(screen)
                #score.value -= 20
        screen.blit(bg_img, [0, 0])

        if tmr % emy.sct == 0:  # 200フレームに1回，敵を出現させる
            emys.add(Enemy(hero))
        total_moved = hero.mvd(key_lst, spd)
        hero.update(key_lst, spd, screen)
        emys.update(hero, screen)
        #Cool.update(emys, screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
