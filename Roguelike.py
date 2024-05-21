import glob
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

print(glob.glob("./fig/*"))

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

class Field(pg.sprite.Sprite):
    """
    アイテムや背景オブジェクトを表示
    """
    images = glob.glob("./fig/*")
    def __init__(self, hero):
        super().__init__()
        self.images = pg.image.load(random.choice(__class__.images))
        self.rect = self.images.get_rect()
        self.rect.center = (random.randint(-WIDTH, WIDTH*2), random.randint(-HEIGHT, HEIGHT*2))
        self.tag = "recover" if self.images == "filename1" else "background"
        self.mvd = hero.mvd()

    def update(self, screen, hero):
        if over_field(self.pos):
            self.kill()
        self.mvd = hero.mvd()-self.mvd
        self.rect.move_ip(self.mvd[0], self.mvd[1])
        screen.blit(self.images, self.rect)


class Score:
    """
    スコアと撃墜数を管理
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.value = 0
        self.def_nums = 0
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, HEIGHT-100

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.value}\nDefeated Enemys: {self.def_nums}", 0, self.color)
        screen.blit(self.image, self.rect)

def main():
    """
    main関数
    """
    tmr = 0
    clock = pg.time.Clock()
    pg.display.set_caption("roguelike")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"fig/maptile_sogen_02.png")
    bg_img = pg.transform.scale(bg_img, (WIDTH/30, HEIGHT/30))
    score = Score()

    while True:
        # hero = Hero()
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        total_dist = (110,110)# hero.mvd() # hero.mvdメソッドは、他のメンバーが作る予定（戻り値 合計移動距離を示すx, yのタプル）
        for i in range(90):
            for j in range(90):
                screen.blit(bg_img, [-WIDTH + i*WIDTH/30 + (total_dist[0]%(WIDTH/30)), -HEIGHT + j*HEIGHT/30+ (total_dist[1]%(HEIGHT/30))])

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
