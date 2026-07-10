#============================ IMPORTS ============================
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
import time
# from random import randrange
import random
# ---------------------------------------------------------------------------
#=> CONSTANT
# ---------------------------------------------------------------------------

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 740
GRAVITY_FORCE = 9
JUMP_FORCE = 25
SPEED = 5
TIMED_LOOP = 10

#=> Global
# ---------------------------------------------------------------------------
score=0
hight_score=0
keyPressed = []
coin_score=4
water_score=7
fire_score=10
current_level=0
gravity_after_id=None
scroll_after_id=None



# ---------------------------------------------------------------------------
root = tk.Tk()
root.geometry(str(SCREEN_WIDTH)+"x"+str(SCREEN_HEIGHT))
root.title('Advanture OF Prince')
canvas = tk.Canvas(root)

# ---------------------------------------------------------------------------
#=> VARIABLES
# ---------------------------------------------------------------------------
game_start=tk.PhotoImage(file='image/bg.png')
game_over=tk.PhotoImage(file='image/Gameover.png')
game_win=tk.PhotoImage(file='image/Gamewin.png')
game_introduction=tk.PhotoImage(file='image/introduction-of-game.png')
game_story=tk.PhotoImage(file='image/story.png')

all_levels=tk.PhotoImage(file='image/all-level.png')
button_help=tk.PhotoImage(file='image/help.png')
button_play=tk.PhotoImage(file='image/start-play.png')
button_exist=tk.PhotoImage(file='image/exist.png')
level1_list=tk.PhotoImage(file='image/level1-list.png',)
level2_list=tk.PhotoImage(file='image/level2-list.png')
level3_list=tk.PhotoImage(file='image/level3-list.png')
level1_bg=tk.PhotoImage(file='image/level1.png')
level2=tk.PhotoImage(file='image/level2.png')
level3=tk.PhotoImage(file='image/level3.png')
story_list=tk.PhotoImage(file='image/story-list.png')
slide1=tk.PhotoImage(file='image/slide1.png')
slide2=tk.PhotoImage(file='image/slide2.png')
slide3=tk.PhotoImage(file='image/slide3.png')


hero=tk.PhotoImage(file='image/Ranger.png')
flower=tk.PhotoImage(file='image/flower.png')
queen=tk.PhotoImage(file='image/queen.png')
coin=tk.PhotoImage(file='image/coin.png')
water=tk.PhotoImage(file='image/water.png')
boom=tk.PhotoImage(file='image/boom.png')
door=tk.PhotoImage(file='image/door.png')
door2=tk.PhotoImage(file='image/door2.png')
long_wall=tk.PhotoImage(file='image/long-wall.png')
monster=tk.PhotoImage(file='image/monster.png')
fire=tk.PhotoImage(file='image/fire.png')
all_level_bg= PhotoImage(file="image/all-levels.png")
score_id = canvas.create_text(600, 15, text="Score:", font=("bold", 15))
button_exists= PhotoImage(file="image/button_exist.png")
button_level=tk.PhotoImage(file='image/button_level.png')
play_again=tk.PhotoImage(file='image/playAgain.png')
retry=tk.PhotoImage(file='image/Retry.png')
back_to_game=tk.PhotoImage(file='image/back.png')


 # ==================  PLAYER ===============
player_id=canvas.create_image(20,50, image = hero)

 # ==================  SCROLL ===============
scrollbar_bottom = tk.Scrollbar(root, orient='horizontal', command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar_bottom.set)
scrollbar_bottom.place(relx=0, rely=1, relwidth=1, anchor='sw')

def stop_loops():
    # Cancel any running gravity / scroll loop so they don't stack up
    # every time a new screen or level is shown.
    global gravity_after_id, scroll_after_id
    if gravity_after_id is not None:
        root.after_cancel(gravity_after_id)
        gravity_after_id = None
    if scroll_after_id is not None:
        canvas.after_cancel(scroll_after_id)
        scroll_after_id = None

def scroll_background():
    global scroll_after_id
    canvas.move(background1,-1,0)
    canvas.move(background2,-1,0)
    if canvas.coords(background1)[0]<-SCREEN_WIDTH:
        canvas.coords(background1,SCREEN_WIDTH,0)
    elif canvas.coords(background2)[0]<-SCREEN_WIDTH:
        canvas.coords(background2,SCREEN_WIDTH,0)
    scroll_after_id = canvas.after(5,scroll_background)

background1 = canvas.create_image(1, 0, image= level1_bg, anchor="nw")
background2 = canvas.create_image(SCREEN_WIDTH, 0, image= level1_bg , anchor="nw")

#=========================== ALL LEVELS =======================
def alllevels(event=None):
    stop_loops()
    canvas.delete("all")
    canvas.create_image(1,0, image = all_level_bg, anchor = "nw")
    # ______________________________LEVEL1_____________________________________
    canvas.create_image(200,250, image = level1_list, anchor = "nw", tags="level1-")
    # ______________________________LEVEL2_______________________________________
    canvas.create_image(565,250, image = level2_list, anchor = "nw", tags="level2-")
    # ______________________________LEVEL3_______________________________________
    canvas.create_image(950,250, image = level3_list, anchor = "nw", tags="level3-")
    canvas.create_image(20,20, image =button_exist, anchor = "nw",tags="backhome")
#===========================LEVEL1 =======================
def level01(event=None):
    global player_id, score_id, background1, background2, current_level, score
    stop_loops()
    canvas.delete("all")
    canvas.create_image(1, 0, image= level1_bg, anchor="nw")
    score = 0
    current_level = 0
    background1 = canvas.create_image(1, 0, image= level1_bg, anchor="nw")
    background2 = canvas.create_image(SCREEN_WIDTH, 0, image= level1_bg , anchor="nw")
    scroll_background()
    # canvas.create_image(0,0,image=level1_bg, anchor='nw')
    canvas.create_image(20,20, image =button_exist, anchor = "nw",tags="backhome")
# ==================  DOOR  ===============
    canvas.create_image(1290,30, image=door , tags="DOOR", anchor=NW)
# ==================  LONG STONE IMAGE ===============
    canvas.create_image(500,500, image = long_wall , tags="PLATFORM", anchor=NW)
    canvas.create_image(30,530, image = long_wall , tags="PLATFORM", anchor=NW)
    canvas.create_image(750,600, image = long_wall , tags="PLATFORM", anchor=NW)
    canvas.create_image(250,450, image = long_wall ,tags="PLATFORM", anchor=NW)
    canvas.create_image(380,330, image = long_wall ,tags="PLATFORM", anchor=NW)
    canvas.create_image(560,200, image = long_wall ,tags="PLATFORM", anchor=NW)
    canvas.create_image(680,380, image = long_wall ,tags="PLATFORM", anchor=NW)
    canvas.create_image(810,250, image = long_wall ,tags="PLATFORM", anchor=NW)
    canvas.create_image(950,135, image = long_wall ,tags="PLATFORM", anchor=NW)
    canvas.create_image(1100,380, image = long_wall ,tags="PLATFORM", anchor=NW)
    canvas.create_image(920,490, image = long_wall ,tags="PLATFORM", anchor=NW)
    canvas.create_image(1225,100, image = long_wall ,tags="PLATFORM", anchor=NW)
    # ================== COIN IMAGE ======================
    canvas.create_image(80, 480, image = water , tags = "WATER", anchor=NW)
    canvas.create_image(100, 480, image = coin , tags = "COIN", anchor=NW)
    canvas.create_image(720, 330, image = coin , tags = "COIN", anchor=NW)
    canvas.create_image(620, 150, image = coin , tags = "COIN", anchor=NW)
    # ==================  WATER IMAGE ===============
    canvas.create_image(500,300, image=water, tags="WATER")
    canvas.create_image(550,470, image=water, tags="WATER")
    canvas.create_image(1000,460, image=water, tags="WATER")
    canvas.create_image(340,420, image=water, tags="WATER")
    canvas.create_image(1040,110, image=water, tags="WATER")
    # ================== BOOM IMAGE =================
    canvas.create_image(610,485, image=boom, tags="BOOM")
    # ================== FIRE IMAGE =================
    canvas.create_image(440,310, image=fire,tags="FIRE")
    canvas.create_image(800,360, image=fire,tags="FIRE")
    # ==================  PLAYER ===============
    player_id = canvas.create_image(30,50, image = hero, anchor=NW)
    # ==================  MONSTER IMAGE ===============
    canvas.create_image(820,560, image=monster, tags="MONSTER")
    canvas.create_image(1200,340, image=monster, tags="MONSTER")
    # ================== FLOWER IMAGE ==================
    canvas.create_image(900,580, image=flower)
    canvas.create_image(570,180, image=flower)
    canvas.create_image(1373,70, image=flower)
    canvas.create_image(1110,360, image=flower)
    canvas.create_rectangle(0,730,SCREEN_WIDTH,SCREEN_HEIGHT,fill="black",tags="PLATFORM")
    score_id = canvas.create_text(1300, 15, text="Score:", font=("bold", 15), fill='white')
    gravity()
# =======================> LEVEL_2 <==========================
def level02(event=None):
    global player_id, score_id, background1, background2, current_level, score
    stop_loops()
    canvas.delete("all")
    canvas.create_image(1, 0, image= level2, anchor="nw")
    score = 0
    current_level = 1
    background1 = canvas.create_image(1, 0, image= level2, anchor="nw")
    background2 = canvas.create_image(SCREEN_WIDTH, 0, image= level2 , anchor="nw")
    scroll_background()
    canvas.create_image(20,20, image =button_exist, anchor = "nw",tags="backhome")

    # ============= long_wall =================
    canvas.create_image(0,600, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(60,600, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(200,500, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(300,400, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(320,400, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(120,300, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(220,200, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(400,300, image = long_wall , tags="PLATFORM", anchor=NW)
    canvas.create_image(500, 200, image= long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(600, 100, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(670, 100, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(400, 625, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(500, 550, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(500, 575, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(500, 600, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(500, 625, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(600,450, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(700, 350, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(800, 250, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(900, 150,image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(850, 350, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(950, 625, image=long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(1050, 550, image= long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(1050, 575, image= long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(1050, 600, image= long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(1200, 600, image= long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(1050, 625, image= long_wall, tags='PLATFORM', anchor=NW)
    canvas.create_image(1250, 450, image=long_wall,  tags='PLATFORM', anchor=NW)
    # =============== flower ===================
    canvas.create_image(1260, 430, image = flower)
    canvas.create_image(650, 520, image = flower)
    canvas.create_image(830, 83, image = flower)
    canvas.create_image(210, 480, image = flower)
    # =============== DOOR ====================
    canvas.create_image(1335,405, image=door2 , tags="DOOR2", anchor=NW)
    # =============== WATER ===================
    canvas.create_image(1150, 480, image= water, tags='WATER', anchor=NW)
    canvas.create_image(700, 280, image= water, tags='WATER', anchor=NW)
    canvas.create_image(180, 230, image= water, tags='WATER', anchor=NW)
    canvas.create_image(450, 230, image= water, tags='WATER', anchor=NW)
    canvas.create_image(500, 480, image= water, tags='WATER', anchor=NW)
    # =============== FIRE ===================
    canvas.create_image(220, 245, image=fire, tags ='FIRE', anchor=NW)
    canvas.create_image(270, 150, image=fire, tags ='FIRE', anchor=NW)
    canvas.create_image(700, 50, image=fire, tags ='FIRE', anchor=NW)
    canvas.create_image(850, 190, image=fire, tags ='FIRE', anchor=NW)
    canvas.create_image(300, 440, image=fire, tags ='FIRE', anchor=NW)
    # =============== BOOM ===================
    canvas.create_image(700, 420, image=boom, tags='BOOM', anchor=NW)
    canvas.create_image(390, 370, image=boom, tags='BOOM', anchor=NW)
    canvas.create_image(600, 170, image=boom, tags='BOOM', anchor=NW)
    # =============== MONSTER ===================
    canvas.create_image(800, 260, image=monster, tags='MONSTER', anchor=NW)
    canvas.create_image(1250, 520, image=monster, tags='MONSTER', anchor=NW)
    # =============== COIN ===================
    canvas.create_image(600, 50, image=coin, tags='COIN', anchor=NW)
    canvas.create_image(640, 50, image=coin, tags='COIN', anchor=NW)
    canvas.create_image(500, 250, image=coin, tags='COIN', anchor=NW)
    canvas.create_image(1000, 100, image=coin, tags='COIN', anchor=NW)
    canvas.create_image(960, 100, image=coin, tags='COIN', anchor=NW)
    canvas.create_image(1100, 490, image=coin, tags='COIN', anchor=NW)
    #   =============== PLAYER ===================
    player_id = canvas.create_image(30,50, image = hero, anchor=NW)
    canvas.create_rectangle(0,730,SCREEN_WIDTH,SCREEN_HEIGHT,fill="black",tags="PLATFORM")
    #   =============== PLAYER ===================
    score_id = canvas.create_text(1300, 15, text="Score:", font=("bold", 15), fill='white')
    gravity()
    #=========================== LEVEL3 =======================
def level03(event=None):
    global player_id, score_id, background1, background2, current_level, score
    stop_loops()
    canvas.delete("all")
    score = 0
    current_level = 2
    background1 = canvas.create_image(1, 0, image= level3, anchor="nw")
    background2 = canvas.create_image(SCREEN_WIDTH, 0, image= level3 , anchor="nw")
    scroll_background()
    canvas.create_image(20,20, image =button_exist, anchor = "nw",tags="backhome")
# ========================== WHITE STONE IMAGE ================

    canvas.create_image(40, 630, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(600, 330, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(400, 430, image = long_wall,  tags = "PLATFORM", anchor=NW)
    canvas.create_image(200, 530, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(800, 230, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(850, 230, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(770, 70, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(1000, 130, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(1050, 130, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(330, 230, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(550, 130, image =long_wall, tags = "PLATFORM", anchor=NW)
    
    canvas.create_image(400, 630, image =long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(700, 550, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(900, 450, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(550, 630, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(1110, 350, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(1250, 530, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(1250, 700, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(950, 620, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(1250, 230, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(1300, 130, image = long_wall, tags = "PLATFORM", anchor=NW)
    canvas.create_image(120, 130, image = long_wall, tags = "PLATFORM", anchor=NW)
# =========================== FLOWER ===========================
    canvas.create_image(500, 400, image = flower)
    canvas.create_image(740, 310, image = flower)
    canvas.create_image(700, 610, image = flower)
    canvas.create_image(980, 200, image = flower)
    canvas.create_image(920, 50, image = flower)
# ========================= PRINCESS ===========================
    canvas.create_image(1350,56, image = queen, tags = "QUEEN", anchor=NW)
# =========================== MONSTER ============================
    canvas.create_image(90, 40, image = monster, tags = "MONSTER", anchor=NW)
    canvas.create_image(1020, 540, image = monster, tags = "MONSTER", anchor=NW)
# =========================== WATER IMAGE ========================
    canvas.create_image(250,460, image = water, tags = 'WATER', anchor=NW)
    canvas.create_image(660,63, image = water, tags = 'WATER', anchor=NW)
    canvas.create_image(800,7, image = water, tags = 'WATER', anchor=NW)
    canvas.create_image(700,265, image = water, tags = 'WATER', anchor=NW)
    canvas.create_image(350,160, image = water, tags = 'WATER', anchor=NW)
    canvas.create_image(1330,460, image = water, tags = 'WATER', anchor=NW)
# =========================== COIN IMAGE =========================
    canvas.create_image(300,480, image = coin, tags = "COIN", anchor=NW)
    canvas.create_image(1000,400, image = coin, tags = "COIN", anchor=NW)
    canvas.create_image(420,180, image = coin, tags = "COIN", anchor=NW)
    canvas.create_image(250,80, image = coin, tags = "COIN", anchor=NW)
    canvas.create_image(600,580, image = coin, tags = "COIN", anchor=NW)
    canvas.create_image(820,500, image = coin, tags = "COIN", anchor=NW)
    canvas.create_image(1000,80, image = coin, tags = "COIN", anchor=NW)
    canvas.create_image(500,600, image = coin, tags = "COIN", anchor=NW)
# =========================== FIRE IMAGE =========================
    canvas.create_image(500,600, image = fire, tags = "FIRE", anchor=NW)
    canvas.create_image(1250,480, image = fire, tags = "FIRE", anchor=NW)
    canvas.create_image(900, 180, image = fire, tags = "FIRE", anchor=NW)
# =========================== BOOM IMAGE =========================
    canvas.create_image(650,300, image = boom, tags = "BOOM", anchor=NW)
    canvas.create_image(770,520, image = boom, tags = "BOOM", anchor=NW)
    canvas.create_image(1350,200, image = boom, tags = "BOOM", anchor=NW)
# =========================== PLAYER IMAGE =========================
    canvas.create_rectangle(0,730,SCREEN_WIDTH,SCREEN_HEIGHT,fill="black",tags="PLATFORM")
    player_id=canvas.create_image(100,200, image = hero, anchor=NW)
    score_id = canvas.create_text(1300, 15, text="Score:", font=("bold", 15), fill='white')
    gravity()
# ---------------------------------------------------------------------------

# ==============> Indroduction <==================
def introdution(event):
    stop_loops()
    canvas.delete("all")
    canvas.create_image(1, 0, image=game_introduction, anchor = 'nw')
    canvas.create_image(20,20, image =button_exist, anchor = "nw",tags="backhome")
# ==============> Story <==================
def story(event):
    stop_loops()
    canvas.delete("all")
    canvas.create_image(1, 0, image=game_story, anchor = 'nw')
    canvas.create_image(20,20, image =button_exist, anchor = "nw",tags="backhome")
# ---------------------------------------------------------------------------
def back(event):
    stop_loops()
    canvas.delete("all")
    home()
#=> CREATE GAME SHOW
# ---------------------------------------------------------------------------
def home():
    Start_Sound()
    canvas.create_image(1, 0, image=game_start, anchor='nw')
    canvas.create_image(500,500,image=story_list, tags="story")
    canvas.create_image(700,500, image=button_play, tags="startgame")
    canvas.create_image(900,500,image=button_help, tags="help")
    # winsound.PlaySound("sound/open.mp3",winsound.SND_FILENAME | winsound.SND_ASYNC)

####### START GAME ######3
def startGame(event):
    stop_loops()
    canvas.delete('all')
    showSlid1()
    # winsound .PlaySound("Audioes\space-war.wav",winsound.SND_FILENAME | winsound.SND_ASYNC)
def showSlid1():
    canvas.create_image(1,0,image=slide1,anchor='nw')
    canvas.after(1000,showSlid2)
def showSlid2():
    canvas.create_image(1,0,image=slide2, anchor='nw')
    canvas.after(1000,showSlid3)
def showSlid3():
    canvas.create_image(1,0,image=slide3, anchor='nw')
    canvas.create_text(700,420,text="Loading...",font=('sansarif',28,'bold'),fill='white')
    canvas.after(2000,alllevels)
# ___________________Check_move(player)___________________________________
def check_movement(dx=0, dy=0, checkGround=False):
    coord = canvas.coords(player_id)
    platforms = canvas.find_withtag("PLATFORM")
    if coord[0] + dx < 0 or coord[0]+hero.width() + dx > SCREEN_WIDTH:
        return False
    if checkGround:
        overlap = canvas.find_overlapping(coord[0]+hero.width(), coord[1], coord[0]+ hero.width() , coord[1]+hero.height() + dy)
    else:
        overlap = canvas.find_overlapping(coord[0]+dx, coord[1]+dy, coord[0]+dx, coord[1]+ hero.width())
    for platform in platforms:
        if platform in overlap:
            return False
    return True
# ==============> WHEN GET COIN <==================
def check_movement_coin():
    coord = canvas.coords(player_id)
    coin = canvas.find_withtag("COIN")
    overlap = canvas.find_overlapping(coord[0], coord[1], coord[0] + hero.width(),coord[1] + hero.height())
    for co in coin:
        if co in overlap:
            return co
    return 0
# ==============> WHEN GET WATER <==================
def check_movement_water():
    coord = canvas.coords(player_id)
    water = canvas.find_withtag("WATER")
    overlap = canvas.find_overlapping(coord[0], coord[1], coord[0] + hero.width(),coord[1] + hero.height())
    for wat in water:
        if wat in overlap:
            return wat
    return 0
# ==============> WHEN GET FIRE <==================
def check_movement_fire():
    coord = canvas.coords(player_id)
    fire = canvas.find_withtag("FIRE")
    overlap = canvas.find_overlapping(coord[0], coord[1], coord[0] + hero.width(),coord[1] + hero.height())
    for fi in fire:
        if fi in overlap:
            return fi
    return 0
# ==============> WHEN GET BOOM <==================
def check_movement_boom():
    coord = canvas.coords(player_id)
    boom = canvas.find_withtag("BOOM")
    overlap = canvas.find_overlapping(coord[0], coord[1], coord[0] + hero.width(),coord[1] + hero.height())
    for bo in boom:
        if bo in overlap:
            return bo
    return 0
# ==============> WHEN GET BOOM <==================
def check_movement_monster():
    coord = canvas.coords(player_id)
    monster = canvas.find_withtag("MONSTER")
    overlap = canvas.find_overlapping(coord[0], coord[1], coord[0] + hero.width(),coord[1] + hero.height())
    for mon in monster:
        if mon in overlap:
            return mon
    return 0
# ==============> WHEN GET DOOR <==================
def check_movement_door1():
    coord = canvas.coords(player_id)
    door = canvas.find_withtag("DOOR")
    overlap = canvas.find_overlapping(coord[0], coord[1], coord[0] + hero.width(),coord[1] + hero.height())
    for do in door:
        if do in overlap:
            return do
    return 0
def check_movement_door2():
    coord = canvas.coords(player_id)
    door = canvas.find_withtag("DOOR2")
    overlap = canvas.find_overlapping(coord[0], coord[1], coord[0] + hero.width(),coord[1] + hero.height())
    for do in door:
        if do in overlap:
            return do
    return 0
# ==============> WHEN MEET QUEEN <==================
def check_movement_queen():
    coord = canvas.coords(player_id)
    queen = canvas.find_withtag("QUEEN")
    overlap = canvas.find_overlapping(coord[0], coord[1], coord[0] + hero.width(),coord[1] + hero.height())
    for qe in queen:
        if qe in overlap:
            return qe
    return 0
# ==============> WHEN JUMP <==================

def jump(force):
    if force > 0:
        if check_movement(0, -force):
            canvas.move(player_id, 0, -force)
            root.after(TIMED_LOOP, jump, force-1)
def start_move(event):
    if event.keysym not in keyPressed:
        keyPressed.append(event.keysym)
        if len(keyPressed) == 1:
            move()
def move():
    global score,water_score,coin_score,fire_score
    if not keyPressed == []:
        x = 0
        if "Left" in keyPressed:
            x -= SPEED
        elif "Right" in keyPressed:
            x += SPEED
        elif "space" in keyPressed and not check_movement(0, GRAVITY_FORCE, True):
            jump(JUMP_FORCE)
            Jump_sound()
        if check_movement(x):
            canvas.move(player_id, x, 0)
        root.after(TIMED_LOOP, move)
        get_coin = check_movement_coin()
        get_water = check_movement_water()
        get_fire = check_movement_fire()
        get_boom = check_movement_boom()
        get_monster = check_movement_monster()
        get_door1 = check_movement_door1()
        get_door2 = check_movement_door2()
        get_queen = check_movement_queen()

# ==============> WHEN WATER <==================
        if get_water > 0:
            coord = canvas.coords(get_water)
            Water_sound()
            canvas.delete(get_water)
            # canvas.create_image(coord[0], coord[1], image=skin)
            score += water_score
            score += coin_score
            update_score()
# ==============> WHEN COIN <==================    
        if get_coin > 0:
            coord = canvas.coords(get_coin)
            Coin_Sound()
            canvas.delete(get_coin)
            score += coin_score
            update_score()
# ==============> WHEN FIRE <==================
        if get_fire > 0:
            Fire_Sound()
            canvas.delete(get_fire)
            score -= fire_score
            if score < 0:
                gameOver()
            update_score()
# ==============> WHEN BOOM <==================            
        if get_boom > 0:
            coord = canvas.coords(get_boom)
            Boom_Sound()
            canvas.delete(get_boom)
            gameOver()
# ==============> WHEN MONSTER <==================    
        if get_monster > 0:
            coord = canvas.coords(get_monster)
            monster_sound()
            canvas.delete(get_monster)
            gameOver()
# ==============> WHEN QUEEN <==================    
        if get_queen > 0:
            canvas.delete(get_queen)
            gameWin()
# ==============> WHEN DOOR1 <==================
        if get_door1 > 0:
            if score > 20:
                door_sound()
                canvas.delete(get_door1)
                level02()
# ==============> WHEN DOOR2 <==================
        if get_door2 > 0:
            door_sound()
            canvas.delete(get_door2)
            level03()
# ==============>GRAVITY <==================        
def gravity():
    global gravity_after_id
    if check_movement(0, GRAVITY_FORCE, True):
        canvas.move(player_id, 0, GRAVITY_FORCE)
    gravity_after_id = root.after(TIMED_LOOP, gravity)
def stop_move(event):
    global keyPressed
    if event.keysym in keyPressed:
        keyPressed.remove(event.keysym)

# =========================== SOUND =========================
def Lose_Sound():
    mixer.init() 
    mixer.music.load('sound/Game-Over.mp3') 
    mixer.music.play()

def Start_Sound():
    mixer.init() 
    mixer.music.load('sound/open.mp3') 
    mixer.music.play()

def Boom_Sound():
    mixer.init() 
    mixer.music.load('sound/boom.mp3') 
    mixer.music.play()

def Coin_Sound():
    mixer.init() 
    mixer.music.load('sound/coin.mp3') 
    mixer.music.play()
    
def Jump_sound():
    mixer.init() 
    mixer.music.load('sound/jump.mp3') 
    mixer.music.play()

def Water_sound():
    mixer.init() 
    mixer.music.load('sound/water.mp3') 
    mixer.music.play()

def door_sound():
    mixer.init() 
    mixer.music.load('sound/into door.mp3') 
    mixer.music.play()

def monster_sound():
    mixer.init() 
    mixer.music.load('sound/monster.mp3') 
    mixer.music.play()
    

def Win_sound():
    mixer.init() 
    mixer.music.load('sound/meet-queen.mp3') 
    mixer.music.play()

def Fire_Sound():
    mixer.init() 
    mixer.music.load('sound/fire.mp3') 
    mixer.music.play()
# ==============> GAMEOVER <==================

# ==============> GAMEOVER <==================
def gameOver():
    global score
    stop_loops()
    canvas.delete('all')
    Lose_Sound()
    score=0
    canvas.create_image(1, 0, image=game_over, anchor = 'nw')
    if current_level == 0:
        canvas.create_image(600, 350, image=retry, anchor = 'nw',tags='level1-')
    elif current_level == 1:
        canvas.create_image(600, 350, image=retry, anchor = 'nw',tags='level2-')
    elif current_level == 2:
        canvas.create_image(600, 350, image=retry, anchor = 'nw',tags='level3-')
    canvas.create_image(600, 450, image=back_to_game, anchor = 'nw', tags='backhome')

# ==============> GAMEOVER <==================
def gameWin():
    stop_loops()
    canvas.delete('all')
    Win_sound()
    canvas.create_image(1, 0, image=game_win, anchor = 'nw')
    if current_level == 0:
        canvas.create_image(600, 350, image=play_again, anchor = 'nw',tags='level1-')
    elif current_level == 1:
        canvas.create_image(600, 350, image=play_again, anchor = 'nw',tags='level2-')
    elif current_level == 2:
        canvas.create_image(600, 350, image=play_again, anchor = 'nw',tags='level3-')
    canvas.create_image(600, 450, image=button_level, anchor = 'nw',tags='button_level')
    canvas.create_image(600, 500, image=button_exists, anchor = 'nw',tags='backhome')

# ==============> UPDATE SCORE <==================
def update_score():
    canvas.itemconfigure(score_id, text="Score: " + str(score))

#=> ALLOW WINDOWS KEYS AND TAGES BIND
# ---------------------------------------------------------------------------
canvas.tag_bind("help","<Button-1>",introdution )
canvas.tag_bind("story","<Button-1>", story)
canvas.tag_bind("backhome","<Button-1>", back)
canvas.tag_bind("button_level","<Button-1>", alllevels)
canvas.tag_bind("startgame","<Button-1>", startGame )
canvas.tag_bind("level1-","<Button-1>", level01 )
canvas.tag_bind("level2-","<Button-1>", level02 )
canvas.tag_bind("level3-","<Button-1>", level03 )
root.bind("<Key>", start_move)
root.bind("<KeyRelease>", stop_move)
# canvas.tag_bind("RETRY","<Button-1>", Retry )
#=> MAIN ROOT
# ---------------------------------------------------------------------------
canvas.pack(expand=True, fill='both')
home()
root.mainloop()

