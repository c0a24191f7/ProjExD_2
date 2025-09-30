import os
import random
import sys
import time
import pygame as pg

# Pygameの初期化
pg.init()

# 画面サイズの定義
WIDTH, HEIGHT = 1100, 650

# 移動量辞書の定義
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

# ディレクトリの変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#---
## 演習課題の関数定義

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    # 泣いているこうかとん画像をロード
    gameover_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    gameover_rct = gameover_img.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    
    # フォントの設定と「Game Over」文字の描画
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    
    # 画面を黒くするSurfaceを作成し、透明度を設定
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(190)
    blackout.fill((0, 0, 0))

    # 画面に描画
    screen.blit(blackout, (0, 0))
    screen.blit(gameover_img, gameover_rct)
    screen.blit(text, text_rct)
    pg.display.update()
    time.sleep(5)  # 5秒間待機

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

#---
## メインゲームループ

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    #爆弾の拡大・加速機能 
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    
    vx, vy = +5, +5
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # こうかとんの移動
        kk_rct.move_ip(sum_mv)
        yoko, tate = check_bound(kk_rct)
        if not yoko:
            kk_rct.move_ip(-sum_mv[0], 0)
        if not tate:
            kk_rct.move_ip(0, -sum_mv[1])

        # 爆弾の拡大と加速
        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        bb_rct.move_ip(avx, avy)
        
        # 画面外判定
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
            
        # 画面に描画
        screen.blit(bg_img, (0, 0))
        screen.blit(kk_img, kk_rct)
        
        # 拡大した爆弾画像をblitする
        bb_img = bb_imgs[idx]
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)

#---
## プログラムの実行

if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()