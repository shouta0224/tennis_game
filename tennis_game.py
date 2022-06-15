import tkinter
import tkinter.messagebox
import pygame
import sys
import random
import winsound

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)

idx = 0
m_x = 0
m_y = 0
r_y = 700
b_x = 0
b_y = 0
r_s_x = 100
r_s_y = 10
b_s = 15
b_muki = 0
b_hayasa = 5
b_hayasa_s = 5
old_fnt = ("Times New Roman", 24)
mb = 0
lu_k = 1800 #1800
lu_d = 3
muki_x_r = 0
muki_y_r = 0
r = 0
score = 0
level = 0
diffculty = 1
full_s = 0
time = 0
jama_x = 0
jama_y = 0
jama_m = 0

debug = 0 # デバッグモード=1

def mouse_move(e):
    global m_x
    m_x = e.x #マウスの座標を変数に代入する

def r_btn():
    global idx
    idx = 0

def main():
    global b_x, b_y, b_muki, idx, mb, muki_x_r, muki_y_r, r, score, diffculty, level, full_s, time, jama_x, jama_y, jama_m, b_hayasa
    pygame.init()
    pygame.display.set_caption("Tennis Game")
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    font_b = pygame.font.Font(None, 100)
    try:
        font_s_j = pygame.font.Font("font/Corporate-Logo-Rounded.ttf", 50)
    except:
        tkinter.messagebox.showerror("エラー", "フォントファイルがありません。")
        pygame.quit()
        sys.exit()
    tmr = 0
    try:
        title = pygame.image.load("png/title.png")
    except:
        tkinter.messagebox.showerror("エラー", "画像ファイルがありません。")
        pygame.quit()
        sys.exit()
    try:
        pygame.mixer.music.load("bgm/bgm.ogg")
        r_se = pygame.mixer.Sound("se/racket.ogg")
        k_se = pygame.mixer.Sound("se/kabe.ogg")
        l_se = pygame.mixer.Sound("se/level_up.ogg")
        o_se = pygame.mixer.Sound("se/game_over.ogg")
    except:
        tkinter.messagebox.showerror("エラー", "オーディオ機器が接続されていないか、音声ファイルがありません。")
        pygame.quit()
        sys.exit()
    while True:
        tmr = tmr + 1
        K = 0
        J = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if full_s == 0:
                        screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                        full_s = 1
                    else:
                        screen =pygame.display.set_mode((1280, 720))
                        full_s = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    K = 1
                if event.key == pygame.K_j:
                    J = 1
        m_x, m_y = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()

        if idx == 0: #title
            screen.fill(GREEN)
            screen.blit(title, [250,10])
            st = font_s_j.render("easy:0 normal:1 hard:2", True, BLACK)
            screen.blit(st, [330, 500])
            if key[pygame.K_0] == 1:
                diffculty = 0
                idx = 1
            elif key[pygame.K_1] == 1:
                diffculty = 1
                idx = 1
            elif key[pygame.K_2] == 1:
                diffculty = 2
                idx = 1
        elif idx == 1: #reset
            b_x = random.randint(0, 1280)
            b_y = 0
            b_muki = random.randint(0, 3)
            mb = 0
            tmr = 0
            score = 0
            level = 1
            if diffculty == 0:
                b_hayasa = 5
                lu_d = 2
                r_s_x = 100
            elif diffculty == 1:
                b_hayasa = 15
                lu_d = 5
                r_s_x = 100
            elif diffculty == 2:
                b_hayasa = 20
                lu_d = 8
                r_s_x = 100
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)
            l_se.play()
            idx = 2
        elif idx == 2: #play
            screen.fill(WHITE)
            
            pygame.draw.rect(screen, RED, [m_x-r_s_x, r_y, r_s_x*2, r_s_y*2])
            pygame.draw.circle(screen, GREEN, [b_x, b_y], b_s)
            if diffculty >= 1 or (diffculty == 0 and level >= 2):
                pygame.draw.rect(screen, RED, [jama_x-r_s_x, jama_y, r_s_x*2, r_s_y*2])
            score_h = font_s_j.render("タイム:"+str(int(tmr/60))+"　点数:"+str(score)+"　レベル:"+str(level), True, BLACK)
            screen.blit(score_h, [10, 10])

            if debug == 1:
                if K == 1:
                    level = level + 1
                elif J == 1:
                    level = level - 1
            
            if b_muki == 0: #右下
                b_x = b_x + b_hayasa + muki_x_r
                b_y = b_y + b_hayasa + muki_y_r
                if b_x >= 1280:
                    b_muki = 1
                    b_x = 1280
                    k_se.play()
                    if level >= 2 and diffculty >= 1:
                        r = random.randint(0, 2)
                        if r == 1:
                            muki_x_r = random.randint(-3, 3)
                        elif r == 2:
                            muki_y_r = random.randint(-3, 3)
                if b_y >= 720:
                    #b_muki= 2
                    #b_y = 720
                    idx = 3
                if b_y >= r_y-r_s_y:
                    if b_x >= m_x-r_s_x and b_x <= m_x+r_s_x-180:
                        b_muki= 3
                        b_y = r_y-r_s_y
                        score = score + 1
                        if level >= 2 and diffculty >= 1:
                            r = random.randint(0, 2)
                            if r == 1:
                                muki_x_r = random.randint(-3, 3)
                            elif r == 2:
                                muki_y_r = random.randint(-3, 3)
                        r_se.play()
                    if b_x >= m_x+r_s_x-180 and b_x <= m_x+r_s_x:
                        b_muki= 2
                        b_y = r_y-r_s_y
                        score = score + 1
                        if level >= 2 and diffculty >= 1:
                            r = random.randint(0, 2)
                            if r == 1:
                                muki_x_r = random.randint(-3, 3)
                            elif r == 2:
                                muki_y_r = random.randint(-3, 3)
                        r_se.play()
                if diffculty >= 1 or (diffculty == 0 and level >= 2):
                    if b_y >= jama_y - r_s_y and b_y <= jama_y + r_s_y:
                        if b_x >= jama_x-r_s_x and b_x <= jama_x+r_s_x-180:
                            b_muki= 3
                            b_y = jama_y-r_s_y
                            if level >= 2 and diffculty >= 1:
                                r = random.randint(0, 2)
                                if r == 1:
                                    muki_x_r = random.randint(-3, 3)
                                elif r == 2:
                                    muki_y_r = random.randint(-3, 3)
                            r_se.play()
                        if b_x >= jama_x+r_s_x-180 and b_x <= jama_x+r_s_x:
                            b_muki= 2
                            b_y = jama_y-r_s_y
                            if level >= 2 and diffculty >= 1:
                                r = random.randint(0, 2)
                                if r == 1:
                                    muki_x_r = random.randint(-3, 3)
                                elif r == 2:
                                    muki_y_r = random.randint(-3, 3)
                            r_se.play()
                        
            elif b_muki == 1:
                b_x = b_x - b_hayasa - muki_x_r
                b_y = b_y + b_hayasa + muki_y_r
                if b_x <= 0:
                    b_muki = 0
                    b_x = 0
                    k_se.play()
                    if level >= 2 and diffculty >= 1:
                        r = random.randint(0, 2)
                        if r == 1:
                            muki_x_r = random.randint(-3, 3)
                        elif r == 2:
                            muki_y_r = random.randint(-3, 3)
                if b_y >= 720:
                    #b_muki= 3
                    #b_y = 720
                    idx = 3
                if b_y >= r_y-r_s_y:
                    if b_x >= m_x-r_s_x+180 and b_x <= m_x+r_s_x:
                        b_muki= 2
                        b_y = r_y-r_s_y
                        score = score + 1
                        if level >= 2 and diffculty >= 1:
                            r = random.randint(0, 2)
                            if r == 1:
                                muki_x_r = random.randint(-3, 3)
                            elif r == 2:
                                muki_y_r = random.randint(-3, 3)
                        r_se.play()
                    if b_x <= m_x-r_s_x+180 and b_x >= m_x-r_s_x:
                        b_muki= 3
                        b_y = r_y-r_s_y
                        score = score + 1
                        if level >= 2 and diffculty >= 1:
                            r = random.randint(0, 2)
                            if r == 1:
                                muki_x_r = random.randint(-3, 3)
                            elif r == 2:
                                muki_y_r = random.randint(-3, 3)
                        r_se.play()
                if diffculty >= 1 or (diffculty == 0 and level >= 2):
                    if b_y >= jama_y - r_s_y and b_y <= jama_y + r_s_y:
                        if b_x >= jama_x-r_s_x+180 and b_x <= jama_x+r_s_x:
                            b_muki= 2
                            b_y = jama_y-r_s_y
                            if level >= 2 and diffculty >= 1:
                                r = random.randint(0, 2)
                                if r == 1:
                                    muki_x_r = random.randint(-3, 3)
                                elif r == 2:
                                    muki_y_r = random.randint(-3, 3)
                            r_se.play()
                        if b_x <= jama_x-r_s_x+180 and b_x >= jama_x-r_s_x:
                            b_muki= 3
                            b_y = jama_y-r_s_y
                            if level >= 2 and diffculty >= 1:
                                r = random.randint(0, 2)
                                if r == 1:
                                    muki_x_r = random.randint(-3, 3)
                                elif r == 2:
                                    muki_y_r = random.randint(-3, 3)
                            r_se.play()
            elif b_muki == 2: #右上
                b_x = b_x + b_hayasa + muki_x_r
                b_y = b_y - b_hayasa - muki_y_r
                if b_x >= 1280:
                    b_muki = 3
                    b_x = 1280
                    k_se.play()
                    if level >= 2 and diffculty >= 1:
                        r = random.randint(0, 2)
                        if r == 1:
                            muki_x_r = random.randint(-3, 3)
                        elif r == 2:
                            muki_y_r = random.randint(-3, 3)
                if b_y <= 0:
                    b_muki= 0
                    b_y = 0
                    k_se.play()
                    if level >= 2 and diffculty >= 1:
                        r = random.randint(0, 2)
                        if r == 1:
                            muki_x_r = random.randint(-3, 3)
                        elif r == 2:
                            muki_y_r = random.randint(-3, 3)
                if diffculty >= 1 or (diffculty == 0 and level >= 2):
                    if b_y <= jama_y + r_s_y and b_y >= jama_y - r_s_y: #邪魔者の処理
                        if b_x >= jama_x - r_s_x and b_x <= jama_x - r_s_x + 20: #角
                            b_muki = 1
                            b_y = jama_y + r_s_y
                            if level >= 2 and diffculty >= 1:
                                r = random.randint(0, 2)
                                if r == 1:
                                    muki_x_r = random.randint(-3, 3)
                                elif r == 2:
                                    muki_y_r = random.randint(-3, 3)
                            r_se.play()
                        if b_x >= jama_x - r_s_x + 20 and b_x <= jama_x + r_s_x: #面
                            b_muki = 0
                            b_y = jama_y + r_s_y
                            if level >= 2 and diffculty >= 1:
                                r = random.randint(0, 2)
                                if r == 1:
                                    muki_x_r = random.randint(-3, 3)
                                elif r == 2:
                                    muki_y_r = random.randint(-3, 3)
                            r_se.play()
            elif b_muki == 3:
                b_x = b_x - b_hayasa - muki_x_r
                b_y = b_y - b_hayasa - muki_y_r
                if b_x <= 0:
                    b_muki = 2
                    b_x = 0
                    k_se.play()
                    if level >= 2 and diffculty >= 1:
                        r = random.randint(0, 2)
                        if r == 1:
                            muki_x_r = random.randint(-3, 3)
                        elif r == 2:
                            muki_y_r = random.randint(-3, 3)
                if b_y <= 0:
                    b_muki= 1
                    b_y = 0
                    k_se.play()
                    if level >= 2 and diffculty >= 1:
                        r = random.randint(0, 2)
                        if r == 1:
                            muki_x_r = random.randint(-3, 3)
                        elif r == 2:
                            muki_y_r = random.randint(-3, 3)
                if diffculty >= 1 or (diffculty == 0 and level >= 2):
                    if b_y <= jama_y + r_s_y and b_y >= jama_y - r_s_y: #邪魔者の処理
                        if b_x >= jama_x - r_s_x and b_x <= jama_x - r_s_x + 20: #角
                            b_muki = 0
                            b_y = jama_y + r_s_y
                            if level >= 2 and diffculty >= 1:
                                r = random.randint(0, 2)
                                if r == 1:
                                    muki_x_r = random.randint(-3, 3)
                                elif r == 2:
                                    muki_y_r = random.randint(-3, 3)
                            r_se.play()
                        if b_x >= jama_x - r_s_x + 20 and b_x <= jama_x + r_s_x: #面
                            b_muki = 1
                            b_y = jama_y + r_s_y
                            if level >= 2 and diffculty >= 1:
                                r = random.randint(0, 2)
                                if r == 1:
                                    muki_x_r = random.randint(-3, 3)
                                elif r == 2:
                                    muki_y_r = random.randint(-3, 3)
                            r_se.play()
            if tmr % lu_k == 0 and tmr != 0:
                lu = font_s_j.render("スピードアップ！", True, BLACK)
                screen.blit(lu, [1000, 10])
                level = level + 1
                l_se.play()
#                b_hayasa = b_hayasa + lu_d

            b_hayasa = b_hayasa_s + (lu_d * level)
            if tmr ==5184000:
                l_se.play()
                idx = 4

            if jama_m == 0:
                jama_x = jama_x - 10
                if jama_x <= 0:
                    jama_m = 1
                    jama_y = random.randint(10, 400)
            else:
                jama_x = jama_x + 10
                if jama_x >= 1280:
                    jama_m = 0
                    jama_y = random.randint(10, 400)
        elif idx == 3: #gameover
            pygame.mixer.music.stop()
            screen.fill(BLACK)
            go = font_b.render("GAME OVER", True, WHITE)
            re = font_s_j.render("Rキーを押して戻る", True, WHITE)
            score_h = font_s_j.render("タイム:"+str(time)+"　点数:"+str(score)+"　レベル:"+str(level), True, WHITE)
            screen.blit(score_h, [10, 10])
            screen.blit(go, [430, 360])
            screen.blit(re, [480, 500])
            if mb == 0:
                o_se.play()
                mb = 1
                time = int(tmr / 60)
#                tkinter.messagebox.showinfo("ゲームオーバー", str(round(tmr/60))+"秒でゲームオーバー")
            
            if key[pygame.K_r] == 1:
                idx = 0
        elif idx == 4: #
            screen.fill(BLACK)
            go = font_b.render("!?!?!?!?!?", True, WHITE)
            re = font_s_j.render("Rキーを押して戻る", True, WHITE)
            screen.blit(go, [430, 360])
            screen.blit(re, [480, 500])
            if mb == 0:
                mb = 1
                tkinter.messagebox.showinfo("!?!?!?!?", "24時間")
            
            if key[pygame.K_r] == 1:
                idx = 0
        
        pygame.display.update()
        clock.tick(60)
        

if __name__ == '__main__':
    main()
