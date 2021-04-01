# ブロック崩し
from tkinter import Tk
from tkinter import Canvas
import random


#1m16sでクリアできる
# ゲーム中で使う変数の一覧
blocks = []
block_size = {"x": 75, "y": 30}
ball = {"move_x": 15, "move_y": -15, "x": 350, "y": 250, "w": 10}
ball_bound = 1
bar = {"x": 0, "w": 100}
is_gameover = False
point = 0
hit_i = -1




# ウィンドウの作成
win = Tk()
cv = Canvas(win, width = 600, height = 600)
cv.pack()


# ゲームの初期化
def init_game():
    global is_gameover, point, hit_i
    is_gameover = False

    ball["move_x"] = 15
    ball["move_y"] = -15
    ball["x"] = 350
    ball["y"] = 250
    bar["x"] = 0
    
    point = 0
    hit_i = -1

    # ブロックを配置する
    for iy in range(0, 5):
        for ix in range(0, 8):
            color = "black"
            if (iy + ix) % 2 == 1: color = "gray"
            x1 = ix * block_size["x"]
            x2 = x1 + block_size["x"]
            y1 = iy * block_size["y"]
            y2 = y1 + block_size["y"]
            blocks.append([x1, y1, x2, y2, color])
    win.title("START")


# 物体を描画する
def draw_objects():
    cv.delete('all') # 既存の描画を破棄
    cv.create_rectangle(0, 0, 600, 600, fill="white")
    # ブロックを一つずつ描画
    for i in blocks:
        x1, y1, x2, y2, c = i
        cv.create_rectangle(x1, y1, x2, y2, fill=c)
    # ボールを描画
    #create_ovalで左上(x1, y1）、右下（x2, y2)のサイズの楕円を描画
    cv.create_oval(
    ball["x"] - ball["w"], ball["y"] - ball["w"],
    ball["x"] + ball["w"], ball["y"] + ball["w"],
    fill="gray")
    # バーを描画
    cv.create_rectangle(bar["x"], 590, bar["x"] + bar["w"], 600, fill="black")


# ボールの移動
def move_ball():
    global is_gameover, point, hit_i

    if is_gameover: return

    # 仮の変数に移動後の値を記録
    bx = ball["x"] + ball["move_x"]
    by = ball["y"] + ball["move_y"]

    # 上左右の壁に当たった
    if bx < 0 or bx > 600: ball["move_x"] *= -1
    if by < 0: ball["move_y"] *= -1

    # プレイヤーの操作するバーに当たった？
    if by > 590 and (bar["x"] <= bx <= (bar["x"] + bar["w"])):
        ball["move_y"] *= -1 * ball_bound
        by = 580
    
    # ボールがブロックに当たった
    for i, w in enumerate(blocks):
        x1, y1, x2, y2, c = w
        #改善の余地あり
        w3 = ball["w"] / 3
        if (x1-w3 <= bx <= x2+w3) and (y1-w3 <= by <= y2+w3):
            hit_i = i
            break

    if hit_i >= 0:
        #ブロックの消去
        del blocks[hit_i]

        #反射をどのようにするか
        ball["move_y"] *= -1
        point += 10
        win.title("GAME SCORE = " + str(point))
        hit_i = -1

    # ゲームオーバー
    if by >= 600:
        win.title("Game Over!! score=" + str(point))
        is_gameover = True
        blocks.clear()

    if point >= 400:
        win.title("Game Clear!! score=" + str(point))
        is_gameover = True

    # 移動内容を反映
    if 0 <= bx <= 600: ball["x"] = bx
    if 0 <= by <= 600: ball["y"] = by

    #自動化
    if by >= 0 and ball["move_x"] > 0:
        bar["x"] = bx - 50
    elif by >= 0 and ball["move_x"] < 0:
        bar["x"] = bx - 50


# ゲームループ
def game_loop():
    draw_objects()
    move_ball()
    #after()は、50ms秒後に関数を呼び出す
    win.after(50, game_loop)


if __name__ == "__main__":

    # ゲームのメイン処理
    init_game()
    game_loop()
    win.mainloop() 


