import minescript as ms
import time

def catch_break(FARMING_TIME_IN_MINUTES,BREAK_TIME_MINUTES):
    CURRENT_TIME = FARMING_TIME_IN_MINUTES * 60
    CURRENT_BREAK = BREAK_TIME_MINUTES * 60
    
    # COUNTDOWN TO STOP FARMING
    for seconds in range(CURRENT_TIME):
        time.sleep(1)
    
    # CEASE ALL MOVEMENT
    ms.player_press_forward(False)
    ms.player_press_left(False)
    ms.player_press_right(False)
    ms.player_press_attack(False)
    ms.player_press_use(False)
    
    TARGET_SCRIPT = ["pest_hunting_mode","farming_mode"]

    for JOB in ms.job_info():
        if any(TARGET in ARG for TARGET in TARGET_SCRIPT for ARG in JOB.command):
            if not JOB.self:
                ms.execute(rf"\killjob {JOB.job_id}")
                
    
    # MOVE TO HUB
    ms.execute('/warp hub')
    
    # COUNTDOWN ON BREAK
    for seconds in range(CURRENT_BREAK):
        time.sleep(1)
    
    ms.execute(r'\timeout')
    return
