## MAIN LOOP ###

### INITIALIZE THE FARMING LOOP

import minescript as ms
import time
from queue import Empty
from farming_mode import main_farm
from timeout import catch_break
import threading

FARMING_TIME_IN_MINUTES = 180
BREAK_TIME_MINUTES = 2

## INITIALIZE VARIABLES
YAW_DURING_FARMING = 0.0
PITCH_DURING_FARMING = -57
STARTING_DIRECTION = "left"  ## EITHER 'left' OR 'right'
HORIZONTAL_BOUNDS = [-143.700, 48.700] ## CHANGE THIS TO THE ACTUAL BOUNDS OF YOUR HORIZONTAL DIRECTION (FROM START TO FINISH)  
VERTICAL_BOUNDS = [-139.300, -55.300] ## CHANGE THIS TO THE ACTUAL BOUNDS OF YOUR VERTICAL DIRECTION (FRON START TO FINISH)

def start_main():
    # Create two threads
    THREAD_1 = threading.Thread(target=catch_break, args = (FARMING_TIME_IN_MINUTES, BREAK_TIME_MINUTES))
    THREAD_2 = threading.Thread(target=main_farm, args = (YAW_DURING_FARMING,PITCH_DURING_FARMING,STARTING_DIRECTION,HORIZONTAL_BOUNDS,VERTICAL_BOUNDS))
    
    # Start both threads
    THREAD_1.start()
    THREAD_2.start()

    # Wait until both threads finish
    THREAD_1.join()
    THREAD_2.join()

    
start_main()