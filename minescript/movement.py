import minescript as ms
from time import sleep
import math

### INITIALIZE VARIABLES
PLOT_CENTERS = {
    0: (0, 0),
    1: (0, -96),
    2: (-96, 0),
    3: (96, 0),
    4: (0, 96),
    5: (-96, -96),
    6: (96, -96),
    7: (-96, 96),
    8: (96, 96),
    9: (0, -192),
    10: (-192, 0),
    11: (192, 0),
    12: (0, 192),
    13: (-96, -192),
    14: (96, -192),
    15: (-192, -96),
    16: (192, -96),
    17: (-192, 96),
    18: (192, 96),
    19: (-96, 192),
    20: (96, 192),
    21: (-192, -192),
    22: (192, -192),
    23: (-192, 192),
    24: (192, 192),
}


### AIMING
def target(tx, ty, tz): # l
    X, Y, Z = ms.player_position()
    YAW, PITCH = ms.player_orientation()

    # CALCULATE THE X,Y,Z DISTANCE RELATIVE TO TARGET
    DX = tx - X
    DY = ty - (Y + 1.62)
    DZ = tz - Z
    
    # CALCULATE THE HORIZONTAL MAGNITUDE OF THE DISTANCE RELATIVE TO TARGET
    HORIZONTAL = math.hypot(DX, DZ)


    # CALCULATE THE YAW AND PITCH RELATIVE TO THE TARGET 
    TARGET_YAW = math.degrees(math.atan2(-DX, DZ))
    TARGET_PITCH = -math.degrees(math.atan2(DY, HORIZONTAL))

    # NORMALIZE THE YAW TO FIND THE NEAREST YAW ROTATION
    YAW_DIFF = (TARGET_YAW - YAW + 180) % 360 - 180
    PITCH_DIFF = TARGET_PITCH - PITCH

    # MAKE THE ROTATION NOT INSTANTANEOUS
    STEPS = 30 #THE BIGGER THE STEPS IS, THE SLOWER THE CAMERA MOVEMENT

    for i in range(1, STEPS + 1):
        PROGRESS = i / STEPS # A SLOW PROGRESS TO 1.00 EACH ITERATION

        ms.player_set_orientation(
            YAW + YAW_DIFF * PROGRESS,
            PITCH + PITCH_DIFF * PROGRESS
        )

        sleep(0.001)
    
def toggle_fly():
    ms.player_press_jump(True)
    sleep(0.05)
    ms.player_press_jump(False)
    sleep(0.05)
    ms.player_press_jump(True)
    sleep(0.05)
    ms.player_press_jump(False)
    
def toggle_descent(TOGGLE):
    STATE = True
    
    if not TOGGLE:
        STATE = False
    
    ms.player_press_sneak(STATE)

def toggle_ascent(TOGGLE):
    STATE = True
    
    if not TOGGLE:
        STATE = False
    
    ms.player_press_jump(STATE)

def check_distance(X_CURRENT, Z_CURRENT, X_DESTINATION, Z_DESTINATION):
    X_COORDINATE = X_DESTINATION - X_CURRENT
    Z_COORDINATE = Z_DESTINATION - Z_CURRENT
    
    return math.hypot(X_COORDINATE, Z_COORDINATE)

def reset_position():
    ms.execute('/warp garden')
    sleep(0.5)
    ms.player_press_sneak(True)
    sleep(0.5)
    ms.player_press_sneak(False)
    sleep(0.5)
    

def set_orientation(YAW_TARGET, PITCH_TARGET):
    YAW, PITCH = ms.player_orientation()

    STEPS = 30

    # FIND SHORTEST ANGULAR DISTANCE
    YAW_DIFFERENCE = (YAW_TARGET - YAW + 180) % 360 - 180
    PITCH_DIFFERENCE = PITCH_TARGET - PITCH

    for i in range(1, STEPS + 1):
        PROGRESS = i / STEPS

        ms.player_set_orientation(
            YAW + YAW_DIFFERENCE * PROGRESS,
            PITCH + PITCH_DIFFERENCE * PROGRESS
        )

        sleep(0.02)
        
def get_velocity():
    player_info = ms.entities(limit=1, max_distance=1)
    for stats in player_info:
        player_velocity_x, player_velocity_z = stats.velocity[0], stats.velocity[2] 
    
    return player_velocity_x,player_velocity_z

def stop_movements():
    ms.player_press_forward(False)
    ms.player_press_left(False)
    ms.player_press_right(False)
    ms.player_press_attack(False)
    ms.player_press_use(False)