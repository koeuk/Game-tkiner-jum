# =============================================================================
#  Adventure of Prince — a Tkinter side-scrolling platformer
# =============================================================================
#  Sections:
#    1. Imports
#    2. Config / constants
#    3. Window & canvas setup
#    4. Game state
#    5. Assets (images)
#    6. Sound
#    7. Level data
#    8. Rendering helpers (spawn / load_level)
#    9. Screens (home, slides, level picker, intro, story)
#   10. Collision helpers
#   11. Physics & input (gravity, jump, move)
#   12. Win / game-over / score
#   13. Event bindings
#   14. Main
# =============================================================================

# --- 1. IMPORTS --------------------------------------------------------------
import math
import random
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer

# --- 2. CONFIG / CONSTANTS ---------------------------------------------------
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 740
GRAVITY_FORCE = 9
JUMP_FORCE = 25
SPEED = 5
TIMED_LOOP = 10

COIN_SCORE = 4
WATER_SCORE = 7
FIRE_SCORE = 10
DOOR_UNLOCK_SCORE = 20      # score needed to pass through level 1's door
MAX_LIVES = 3               # hearts the player starts each level with

# Monster patrol
MONSTER_SPEED_BY_LEVEL = {0: 2, 1: 3, 2: 4}   # px per tick, tougher each level
MONSTER_SPEED = 2                              # fallback speed
MONSTER_RANGE = 70          # px the monster wanders each side of its spawn
MONSTER_TICK = 30           # ms between patrol steps

# HUD colour palette
HUD_BG = "#141821"
HUD_ACCENT = "#f5c542"
HUD_HEART = "#ff4d4d"
HUD_HEART_LOST = "#5a2a2a"
HUD_FONT = "DejaVu Sans"

# Drawn-background palettes, one per level. sky_top/sky_bot are the gradient
# endpoints (RGB); hill_far/hill_near are the two parallax silhouette layers.
SCENE = {
    0: {"sky_top": (14, 26, 58), "sky_bot": (4, 6, 16),
        "hill_far": "#0e1c30", "hill_near": "#060d18", "moon": "#f2f3e6"},
    1: {"sky_top": (34, 18, 54), "sky_bot": (8, 4, 16),
        "hill_far": "#1c1030", "hill_near": "#0d0618", "moon": "#efe6f5"},
    2: {"sky_top": (46, 16, 24), "sky_bot": (12, 4, 6),
        "hill_far": "#301016", "hill_near": "#180608", "moon": "#f5e6d6"},
}

# --- 3. WINDOW & CANVAS SETUP ------------------------------------------------
root = tk.Tk()
root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
root.title('Advanture OF Prince')

canvas = tk.Canvas(root)

scrollbar_bottom = tk.Scrollbar(root, orient='horizontal', command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar_bottom.set)
scrollbar_bottom.place(relx=0, rely=1, relwidth=1, anchor='sw')

# --- 4. GAME STATE -----------------------------------------------------------
score = 0
lives = MAX_LIVES
current_level = 0
keyPressed = []

# ids / handles created at runtime
player_id = None
score_id = None
heart_ids = []
monsters = []               # [{"id", "dir", "min_x", "max_x"}, ...]
stars = []                  # [{"id", "dim"}, ...] twinkling star field
parallax = []               # [{"ids": [id, id], "speed": float}, ...] hill layers
gravity_after_id = None
scroll_after_id = None       # drives the animated background (parallax + twinkle)
monster_after_id = None

# --- 5. ASSETS (IMAGES) ------------------------------------------------------
# Screens
game_start = tk.PhotoImage(file='image/bg.png')
game_over = tk.PhotoImage(file='image/Gameover.png')
game_win = tk.PhotoImage(file='image/Gamewin.png')
game_introduction = tk.PhotoImage(file='image/introduction-of-game.png')
game_story = tk.PhotoImage(file='image/story.png')

# UI / buttons
button_help = tk.PhotoImage(file='image/help.png')
button_play = tk.PhotoImage(file='image/start-play.png')
button_exist = tk.PhotoImage(file='image/exist.png')
button_exists = tk.PhotoImage(file='image/button_exist.png')
button_level = tk.PhotoImage(file='image/button_level.png')
story_list = tk.PhotoImage(file='image/story-list.png')
play_again = tk.PhotoImage(file='image/playAgain.png')
retry = tk.PhotoImage(file='image/Retry.png')
back_to_game = tk.PhotoImage(file='image/back.png')

# Level picker / backgrounds
all_level_bg = tk.PhotoImage(file="image/all-levels.png")
level1_list = tk.PhotoImage(file='image/level1-list.png')
level2_list = tk.PhotoImage(file='image/level2-list.png')
level3_list = tk.PhotoImage(file='image/level3-list.png')
level1_bg = tk.PhotoImage(file='image/level1.png')
level2 = tk.PhotoImage(file='image/level2.png')
level3 = tk.PhotoImage(file='image/level3.png')

# Story slides
slide1 = tk.PhotoImage(file='image/slide1.png')
slide2 = tk.PhotoImage(file='image/slide2.png')
slide3 = tk.PhotoImage(file='image/slide3.png')

# Sprites
hero = tk.PhotoImage(file='image/Ranger.png')
flower = tk.PhotoImage(file='image/flower.png')
queen = tk.PhotoImage(file='image/queen.png')
coin = tk.PhotoImage(file='image/coin.png')
water = tk.PhotoImage(file='image/water.png')
boom = tk.PhotoImage(file='image/boom.png')
door = tk.PhotoImage(file='image/door.png')
door2 = tk.PhotoImage(file='image/door2.png')
long_wall = tk.PhotoImage(file='image/long-wall.png')
fire = tk.PhotoImage(file='image/fire.png')

# Monster: the source art faces LEFT. Keep the original for left-walking and a
# horizontally-mirrored copy for right-walking so it faces where it moves.
_monster_src = Image.open('image/monster.png')
monster = ImageTk.PhotoImage(_monster_src)                                   # faces left
monster_right = ImageTk.PhotoImage(_monster_src.transpose(Image.FLIP_LEFT_RIGHT))  # faces right

# --- 6. SOUND ----------------------------------------------------------------
# NOTE: if you launch the game as root you will hear nothing — a root process
# can't reach your user's PulseAudio/PipeWire session. Run it as your normal
# user. On a machine with no sound device at all the game runs silently.
try:
    mixer.init()
    _audio_ok = True
except Exception as e:
    _audio_ok = False
    print("Audio disabled (no sound device):", e)

# Sound file paths
SND_START = 'sound/open.mp3'
SND_JUMP = 'sound/jump.mp3'
SND_COIN = 'sound/coin.mp3'
SND_WATER = 'sound/water.mp3'
SND_FIRE = 'sound/fire.mp3'
SND_BOOM = 'sound/boom.mp3'
SND_MONSTER = 'sound/monster.mp3'
SND_DOOR = 'sound/into door.mp3'
SND_WIN = 'sound/meet-queen.mp3'
SND_LOSE = 'sound/Game-Over.mp3'

def play_sound(path, loops=0):
    """Play a sound / music track on the shared music stream (no-op if audio
    is off). loops=0 plays once; loops=-1 loops forever.

    Each call replaces the currently-playing track — this is the game's
    original behaviour and the sounds are tuned for it.
    """
    if not _audio_ok:
        return
    try:
        mixer.music.load(path)
        mixer.music.play(loops)
    except Exception as e:
        print("Could not play sound", path, ":", e)

# --- 7. LEVEL DATA -----------------------------------------------------------
# Each level is described declaratively. A "group" is a batch of identical
# sprites sharing an image, a collision tag, and an anchor:
#   {"img": <PhotoImage>, "tag": <str|None>, "anchor": NW|CENTER, "pos": [(x, y), ...]}
# Sprites with tag=None are decorative (no collision).
LEVELS = {
    0: {
        "bg": level1_bg,
        "player": (30, 50),
        "groups": [
            {"img": door, "tag": "DOOR", "anchor": NW, "pos": [(1290, 30)]},
            {"img": long_wall, "tag": "PLATFORM", "anchor": NW, "pos": [
                (500, 500), (30, 530), (750, 600), (250, 450), (380, 330),
                (560, 200), (680, 380), (810, 250), (950, 135), (1100, 380),
                (920, 490), (1225, 100)]},
            {"img": water, "tag": "WATER", "anchor": NW, "pos": [(80, 480)]},
            {"img": coin, "tag": "COIN", "anchor": NW, "pos": [
                (100, 480), (720, 330), (620, 150)]},
            {"img": water, "tag": "WATER", "anchor": CENTER, "pos": [
                (500, 300), (550, 470), (1000, 460), (340, 420), (1040, 110)]},
            {"img": boom, "tag": "BOOM", "anchor": CENTER, "pos": [(610, 485)]},
            {"img": fire, "tag": "FIRE", "anchor": CENTER, "pos": [
                (440, 310), (800, 360)]},
            {"img": monster, "tag": "MONSTER", "anchor": CENTER, "pos": [
                (820, 560), (1200, 340)]},
            {"img": flower, "tag": None, "anchor": CENTER, "pos": [
                (900, 580), (570, 180), (1373, 70), (1110, 360)]},
        ],
    },
    1: {
        "bg": level2,
        "player": (30, 50),
        "groups": [
            {"img": long_wall, "tag": "PLATFORM", "anchor": NW, "pos": [
                (0, 600), (60, 600), (200, 500), (300, 400), (320, 400),
                (120, 300), (220, 200), (400, 300), (500, 200), (600, 100),
                (670, 100), (400, 625), (500, 550), (500, 575), (500, 600),
                (500, 625), (600, 450), (700, 350), (800, 250), (900, 150),
                (850, 350), (950, 625), (1050, 550), (1050, 575), (1050, 600),
                (1200, 600), (1050, 625), (1250, 450)]},
            {"img": flower, "tag": None, "anchor": CENTER, "pos": [
                (1260, 430), (650, 520), (830, 83), (210, 480)]},
            {"img": door2, "tag": "DOOR2", "anchor": NW, "pos": [(1335, 405)]},
            {"img": water, "tag": "WATER", "anchor": NW, "pos": [
                (1150, 480), (700, 280), (180, 230), (450, 230), (500, 480)]},
            {"img": fire, "tag": "FIRE", "anchor": NW, "pos": [
                (220, 245), (270, 150), (700, 50), (850, 190), (300, 440)]},
            {"img": boom, "tag": "BOOM", "anchor": NW, "pos": [
                (700, 420), (390, 370), (600, 170)]},
            {"img": monster, "tag": "MONSTER", "anchor": NW, "pos": [
                (800, 260), (1250, 520)]},
            {"img": coin, "tag": "COIN", "anchor": NW, "pos": [
                (600, 50), (640, 50), (500, 250), (1000, 100), (960, 100),
                (1100, 490)]},
        ],
    },
    2: {
        "bg": level3,
        "player": (100, 200),
        "groups": [
            {"img": long_wall, "tag": "PLATFORM", "anchor": NW, "pos": [
                (40, 630), (600, 330), (400, 430), (200, 530), (800, 230),
                (850, 230), (770, 70), (1000, 130), (1050, 130), (330, 230),
                (550, 130), (400, 630), (700, 550), (900, 450), (550, 630),
                (1110, 350), (1250, 530), (1250, 700), (950, 620), (1250, 230),
                (1300, 130), (120, 130)]},
            {"img": flower, "tag": None, "anchor": CENTER, "pos": [
                (500, 400), (740, 310), (700, 610), (980, 200), (920, 50)]},
            {"img": queen, "tag": "QUEEN", "anchor": NW, "pos": [(1350, 56)]},
            {"img": monster, "tag": "MONSTER", "anchor": NW, "pos": [
                (90, 40), (1020, 540)]},
            {"img": water, "tag": "WATER", "anchor": NW, "pos": [
                (250, 460), (660, 63), (800, 7), (700, 265), (350, 160),
                (1330, 460)]},
            {"img": coin, "tag": "COIN", "anchor": NW, "pos": [
                (300, 480), (1000, 400), (420, 180), (250, 80), (600, 580),
                (820, 500), (1000, 80), (500, 600)]},
            {"img": fire, "tag": "FIRE", "anchor": NW, "pos": [
                (500, 600), (1250, 480), (900, 180)]},
            {"img": boom, "tag": "BOOM", "anchor": NW, "pos": [
                (650, 300), (770, 520), (1350, 200)]},
        ],
    },
}

# --- 8. RENDERING HELPERS ----------------------------------------------------
def spawn(image, positions, tag=None, anchor=CENTER):
    """Draw the same sprite at every (x, y) in positions."""
    for x, y in positions:
        canvas.create_image(x, y, image=image, tags=tag, anchor=anchor)

def round_rect(x1, y1, x2, y2, r=16, **kwargs):
    """Draw a rounded rectangle (used for HUD / menu panels)."""
    pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
           x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
           x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
    return canvas.create_polygon(pts, smooth=True, **kwargs)

def _hex(rgb):
    return "#%02x%02x%02x" % rgb

def _lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def _hill_points(x_off, baseline, amp, humps, w):
    """Rolling-hill silhouette whose left and right edges match, so two copies
    tile seamlessly when scrolled."""
    steps = 48
    pts = []
    for i in range(steps + 1):
        x = x_off + w * i / steps
        y = baseline - amp * (0.5 - 0.5 * math.cos(2 * math.pi * humps * i / steps))
        pts += [x, y]
    pts += [x_off + w, SCREEN_HEIGHT, x_off, SCREEN_HEIGHT]
    return pts

def _add_parallax(baseline, amp, humps, color, speed):
    """Two tiled hill polygons that scroll at `speed` px/tick."""
    a = canvas.create_polygon(_hill_points(0, baseline, amp, humps, SCREEN_WIDTH),
                              fill=color, outline=color, smooth=True, tags="BG")
    b = canvas.create_polygon(_hill_points(SCREEN_WIDTH, baseline, amp, humps, SCREEN_WIDTH),
                              fill=color, outline=color, smooth=True, tags="BG")
    parallax.append({"ids": [a, b], "speed": speed})

def build_scene(level):
    """Draw the whole animated background: gradient sky, stars, moon, hills."""
    global stars, parallax
    stars = []
    parallax = []
    pal = SCENE.get(level, SCENE[0])

    # Gradient sky (horizontal bands from sky_top down to sky_bot)
    bands = 74
    for i in range(bands):
        col = _hex(_lerp(pal["sky_top"], pal["sky_bot"], i / (bands - 1)))
        y0 = SCREEN_HEIGHT * i // bands
        y1 = SCREEN_HEIGHT * (i + 1) // bands + 1
        canvas.create_rectangle(0, y0, SCREEN_WIDTH, y1, fill=col, outline=col, tags="BG")

    # Star field (upper portion of the sky)
    for _ in range(70):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(8, 430)
        r = random.choice([1, 1, 1, 2])
        sid = canvas.create_oval(x - r, y - r, x + r, y + r,
                                 fill="#ffffff", outline="", tags="BG")
        stars.append({"id": sid, "dim": "#7f8db0"})

    # Moon with a soft glow (concentric discs, dark → light)
    mx, my, mr = 1160, 120, 54
    for gr, gcol in ((mr + 34, _hex(_lerp(pal["sky_top"], (255, 255, 255), 0.15))),
                     (mr + 16, _hex(_lerp(pal["sky_top"], (255, 255, 255), 0.30)))):
        canvas.create_oval(mx - gr, my - gr, mx + gr, my + gr,
                           fill=gcol, outline="", tags="BG")
    canvas.create_oval(mx - mr, my - mr, mx + mr, my + mr,
                       fill=pal["moon"], outline="", tags="BG")

    # Two parallax hill layers (far = slower/smaller, near = faster/taller)
    _add_parallax(560, 45, 3, pal["hill_far"], 0.4)
    _add_parallax(655, 85, 2, pal["hill_near"], 0.9)

def animate_background():
    """Scroll the parallax hills and twinkle a few stars each tick."""
    global scroll_after_id
    for layer in parallax:
        for pid in layer["ids"]:
            canvas.move(pid, -layer["speed"], 0)
            if canvas.coords(pid)[0] <= -SCREEN_WIDTH:
                canvas.move(pid, 2 * SCREEN_WIDTH, 0)
    if stars:
        for s in random.sample(stars, k=min(6, len(stars))):
            bright = random.random() > 0.4
            canvas.itemconfigure(s["id"], fill="#ffffff" if bright else s["dim"])
    scroll_after_id = canvas.after(30, animate_background)

def stop_loops():
    """Cancel the gravity / scroll / monster loops so they don't stack up."""
    global gravity_after_id, scroll_after_id, monster_after_id
    if gravity_after_id is not None:
        root.after_cancel(gravity_after_id)
        gravity_after_id = None
    if scroll_after_id is not None:
        canvas.after_cancel(scroll_after_id)
        scroll_after_id = None
    if monster_after_id is not None:
        root.after_cancel(monster_after_id)
        monster_after_id = None

def load_level(level):
    """Build and start a level from its declarative LEVELS entry."""
    global player_id, score_id, current_level, score, lives, monsters
    stop_loops()
    canvas.delete("all")

    data = LEVELS[level]
    score = 0
    lives = MAX_LIVES
    current_level = level
    monsters = []

    # Drawn, animated background (gradient sky + stars + moon + parallax hills)
    build_scene(level)
    animate_background()

    # Back-to-menu button
    canvas.create_image(20, 20, image=button_exist, anchor="nw", tags="backhome")

    # All sprites for the level
    for g in data["groups"]:
        spawn(g["img"], g["pos"], g["tag"], g["anchor"])

    # Register every monster so it can patrol back and forth
    for mid in canvas.find_withtag("MONSTER"):
        mx = canvas.coords(mid)[0]
        monsters.append({
            "id": mid,
            "dir": 1,
            "min_x": max(0, mx - MONSTER_RANGE),
            "max_x": min(SCREEN_WIDTH - monster.width(), mx + MONSTER_RANGE),
        })
        canvas.itemconfigure(mid, image=monster_right)   # starts walking right

    # Player, floor and score readout
    px, py = data["player"]
    player_id = canvas.create_image(px, py, image=hero, anchor=NW)
    canvas.create_rectangle(0, 730, SCREEN_WIDTH, SCREEN_HEIGHT, fill="black", tags="PLATFORM")
    draw_hud()
    update_score()
    update_lives()

    gravity()
    animate_monsters()

# --- 9. SCREENS --------------------------------------------------------------
def home():
    play_sound(SND_START)   # opening sound, plays once
    canvas.create_image(1, 0, image=game_start, anchor='nw')
    canvas.create_image(500, 500, image=story_list, tags="story")
    canvas.create_image(700, 500, image=button_play, tags="startgame")
    canvas.create_image(900, 500, image=button_help, tags="help")
    # controls hint strip near the bottom
    round_rect(390, 650, 1010, 702, r=22, fill="#0d1017", stipple="gray50",
               outline=HUD_ACCENT, width=2)
    canvas.create_text(
        700, 676,
        text="←  →  Move      Space  Jump      Save the Queen",
        fill="white", font=(HUD_FONT, 15, "bold"))

def startGame(event=None):
    stop_loops()
    canvas.delete('all')
    showSlid1()

def showSlid1():
    canvas.create_image(1, 0, image=slide1, anchor='nw')
    canvas.after(1000, showSlid2)

def showSlid2():
    canvas.create_image(1, 0, image=slide2, anchor='nw')
    canvas.after(1000, showSlid3)

def showSlid3():
    canvas.create_image(1, 0, image=slide3, anchor='nw')
    canvas.create_text(700, 420, text="Loading...", font=('sansarif', 28, 'bold'), fill='white')
    canvas.after(2000, alllevels)

def alllevels(event=None):
    stop_loops()
    canvas.delete("all")
    canvas.create_image(1, 0, image=all_level_bg, anchor="nw")
    canvas.create_image(200, 250, image=level1_list, anchor="nw", tags="level1-")
    canvas.create_image(565, 250, image=level2_list, anchor="nw", tags="level2-")
    canvas.create_image(950, 250, image=level3_list, anchor="nw", tags="level3-")
    canvas.create_image(20, 20, image=button_exist, anchor="nw", tags="backhome")

def level01(event=None):
    load_level(0)

def level02(event=None):
    load_level(1)

def level03(event=None):
    load_level(2)

def introdution(event=None):
    stop_loops()
    canvas.delete("all")
    canvas.create_image(1, 0, image=game_introduction, anchor='nw')
    canvas.create_image(20, 20, image=button_exist, anchor="nw", tags="backhome")

def story(event=None):
    stop_loops()
    canvas.delete("all")
    canvas.create_image(1, 0, image=game_story, anchor='nw')
    canvas.create_image(20, 20, image=button_exist, anchor="nw", tags="backhome")

def back(event=None):
    stop_loops()
    canvas.delete("all")
    home()

# --- 10. COLLISION HELPERS ---------------------------------------------------
def check_movement(dx=0, dy=0, checkGround=False):
    """Return True if the player can move by (dx, dy) without leaving the
    screen or hitting a PLATFORM.

    Collision uses the player's full bounding box, inset slightly (INSET) so
    the platform the hero is resting on doesn't read as a wall — otherwise the
    hero snags on platform edges and gets stuck.
    """
    INSET = 3
    x, y = canvas.coords(player_id)
    w, h = hero.width(), hero.height()

    # Horizontal screen bounds
    if x + dx < 0 or x + w + dx > SCREEN_WIDTH:
        return False

    if checkGround:
        # Thin strip just below the feet, across the body width:
        # "is there ground to stand on / can I fall by dy?"
        x1, y1 = x + INSET, y + h
        x2, y2 = x + w - INSET, y + h + dy
    else:
        # Full body box after the proposed move, inset on every side so the
        # floor underfoot / a wall we're flush against don't false-block.
        x1, y1 = x + dx + INSET, y + dy + INSET
        x2, y2 = x + w + dx - INSET, y + h + dy - INSET

    overlap = canvas.find_overlapping(x1, y1, x2, y2)
    for platform in canvas.find_withtag("PLATFORM"):
        if platform in overlap:
            return False
    return True

def touching(tag):
    """Return the id of the first item with `tag` overlapping the player, else 0."""
    x, y = canvas.coords(player_id)
    overlap = canvas.find_overlapping(x, y, x + hero.width(), y + hero.height())
    for item in canvas.find_withtag(tag):
        if item in overlap:
            return item
    return 0

# --- 11. PHYSICS & INPUT -----------------------------------------------------
def gravity():
    global gravity_after_id
    if check_movement(0, GRAVITY_FORCE, True):
        canvas.move(player_id, 0, GRAVITY_FORCE)
    gravity_after_id = root.after(TIMED_LOOP, gravity)

def animate_monsters():
    """Walk each monster back and forth, and end the game if one catches the
    player (even while the player is standing still)."""
    global monster_after_id
    speed = MONSTER_SPEED_BY_LEVEL.get(current_level, MONSTER_SPEED)
    for m in monsters:
        canvas.move(m["id"], m["dir"] * speed, 0)
        x = canvas.coords(m["id"])[0]
        if x <= m["min_x"] or x >= m["max_x"]:
            m["dir"] *= -1
            canvas.itemconfigure(m["id"],
                                 image=monster_right if m["dir"] > 0 else monster)

    # A patrolling monster can bump into a stationary player
    if monsters and touching("MONSTER") > 0:
        play_sound(SND_MONSTER)
        gameOver()
        return

    monster_after_id = root.after(MONSTER_TICK, animate_monsters)

def jump(force):
    if force > 0:
        if check_movement(0, -force):
            canvas.move(player_id, 0, -force)
            root.after(TIMED_LOOP, jump, force - 1)

def start_move(event):
    if event.keysym not in keyPressed:
        keyPressed.append(event.keysym)
        if len(keyPressed) == 1:
            move()

def stop_move(event):
    if event.keysym in keyPressed:
        keyPressed.remove(event.keysym)

def move():
    global score, lives
    if keyPressed == []:
        return

    x = 0
    if "Left" in keyPressed:
        x -= SPEED
    elif "Right" in keyPressed:
        x += SPEED
    elif "space" in keyPressed and not check_movement(0, GRAVITY_FORCE, True):
        jump(JUMP_FORCE)
        play_sound(SND_JUMP)
    if check_movement(x):
        canvas.move(player_id, x, 0)
    root.after(TIMED_LOOP, move)

    # --- Interactions -------------------------------------------------------
    get_water = touching("WATER")
    if get_water > 0:
        play_sound(SND_WATER)
        canvas.delete(get_water)
        score += WATER_SCORE
        score += COIN_SCORE
        update_score()

    get_coin = touching("COIN")
    if get_coin > 0:
        play_sound(SND_COIN)
        canvas.delete(get_coin)
        score += COIN_SCORE
        update_score()

    get_fire = touching("FIRE")
    if get_fire > 0:
        play_sound(SND_FIRE)
        canvas.delete(get_fire)
        score -= FIRE_SCORE
        lives -= 1
        update_lives()
        update_score()
        if lives <= 0 or score < 0:
            gameOver()

    if touching("BOOM") > 0:
        play_sound(SND_BOOM)
        gameOver()

    if touching("MONSTER") > 0:
        play_sound(SND_MONSTER)
        gameOver()

    if touching("QUEEN") > 0:
        gameWin()

    get_door1 = touching("DOOR")
    if get_door1 > 0 and score > DOOR_UNLOCK_SCORE:
        play_sound(SND_DOOR)
        canvas.delete(get_door1)
        level02()

    if touching("DOOR2") > 0:
        play_sound(SND_DOOR)
        level03()

# --- 12. WIN / GAME-OVER / SCORE ---------------------------------------------
def draw_hud():
    """Draw the in-game HUD panel: level badge + coin score readout + hearts."""
    global score_id, heart_ids
    round_rect(500, 8, 900, 58, r=16, fill=HUD_BG, stipple="gray50",
               outline=HUD_ACCENT, width=2, tags="HUD")
    # level badge
    round_rect(514, 18, 620, 48, r=12, fill=HUD_ACCENT, tags="HUD")
    canvas.create_text(567, 33, text=f"LEVEL {current_level + 1}", fill="#1a1206",
                       font=(HUD_FONT, 13, "bold"), tags="HUD")
    # coin icon
    canvas.create_oval(640, 21, 664, 45, fill=HUD_ACCENT, outline="#c8961e",
                       width=2, tags="HUD")
    canvas.create_text(652, 33, text="$", fill="#8a6d1a",
                       font=(HUD_FONT, 13, "bold"), tags="HUD")
    # score value
    score_id = canvas.create_text(676, 33, text="0", anchor="w", fill="white",
                                  font=(HUD_FONT, 20, "bold"), tags="HUD")
    # hearts
    heart_ids = []
    for i in range(MAX_LIVES):
        hid = canvas.create_text(802 + i * 32, 32, text="♥",
                                 fill=HUD_HEART, font=(HUD_FONT, 22), tags="HUD")
        heart_ids.append(hid)

def update_score():
    canvas.itemconfigure(score_id, text=str(score))

def update_lives():
    for i, hid in enumerate(heart_ids):
        full = i < lives
        canvas.itemconfigure(hid, text="♥" if full else "♡",
                             fill=HUD_HEART if full else HUD_HEART_LOST)

# tag used by the retry / play-again button for each level
_RETRY_TAG = {0: "level1-", 1: "level2-", 2: "level3-"}

def gameOver():
    global score
    stop_loops()
    canvas.delete('all')
    play_sound(SND_LOSE)
    score = 0
    canvas.create_image(1, 0, image=game_over, anchor='nw')
    canvas.create_image(600, 350, image=retry, anchor='nw', tags=_RETRY_TAG[current_level])
    canvas.create_image(600, 450, image=back_to_game, anchor='nw', tags='backhome')

def gameWin():
    stop_loops()
    canvas.delete('all')
    play_sound(SND_WIN)
    canvas.create_image(1, 0, image=game_win, anchor='nw')
    canvas.create_image(600, 350, image=play_again, anchor='nw', tags=_RETRY_TAG[current_level])
    canvas.create_image(600, 450, image=button_level, anchor='nw', tags='button_level')
    canvas.create_image(600, 500, image=button_exists, anchor='nw', tags='backhome')

# --- 13. EVENT BINDINGS ------------------------------------------------------
canvas.tag_bind("help", "<Button-1>", introdution)
canvas.tag_bind("story", "<Button-1>", story)
canvas.tag_bind("backhome", "<Button-1>", back)
canvas.tag_bind("button_level", "<Button-1>", alllevels)
canvas.tag_bind("startgame", "<Button-1>", startGame)
canvas.tag_bind("level1-", "<Button-1>", level01)
canvas.tag_bind("level2-", "<Button-1>", level02)
canvas.tag_bind("level3-", "<Button-1>", level03)

# Hand cursor on every clickable button
CLICKABLE_TAGS = ("help", "story", "backhome", "button_level",
                  "startgame", "level1-", "level2-", "level3-")

def _hand_cursor(event):
    canvas.config(cursor="hand2")

def _default_cursor(event):
    canvas.config(cursor="")

for _tag in CLICKABLE_TAGS:
    canvas.tag_bind(_tag, "<Enter>", _hand_cursor)
    canvas.tag_bind(_tag, "<Leave>", _default_cursor)

root.bind("<Key>", start_move)
root.bind("<KeyRelease>", stop_move)

# --- 14. MAIN ----------------------------------------------------------------
canvas.pack(expand=True, fill='both')
home()
root.mainloop()
