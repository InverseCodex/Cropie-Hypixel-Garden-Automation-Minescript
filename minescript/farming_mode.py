import minescript as ms
import time
import java
import movement
import lobby_check
### INITIALIZE VARIABLES
pest_hunt = False
POLLING_TIME = 0.5

### INITIALIZE EXTERNAL SCRIPT
HUD_SCRIPT = java.import_pyjinn_script("getPest.pyj")
get_pest = HUD_SCRIPT.get("getPest")

### FARMING BOUNDS
x_bounds = [-143.700, 48.700] # HORIZONTAL BOUNDS
z_bounds = [-139.300, -55.300] # VERTICAL BOUNDS

### UPDATE INFOS FUNCTION 
def update_pest(): # GETS HUD INFO, RETURNS PESTS INFO, IF RETURNED NONE, GARDEN IS CLEAR
    pest_info = get_pest() # RUN THE FUNCTION FROM THE PYJINN SCRIPT TO EXTRACT TAB HUD INFO
    target_plot = ""
    # GET THE INFO FOR THE AMOUNT OF ALIVE PESTS AND INFESTED PLOT
    
    alive = int(pest_info['ALIVE'])
    
    if alive > 0: # IF A PLOT IS INFESTED
        infested_plots = pest_info['PLOTS']
        target_plot = infested_plots[0]
        return alive, infested_plots, target_plot
    
    ## NO MORE PESTS
    return None

def check_player_position():
    return ms.player_position() # CHECK CURRENT POSITION

def change_direction(current_direction):
    
    if current_direction == 'left':
        current_direction = 'right'
    else: 
        current_direction = 'left'
    
    return current_direction

def move_to_direction(current_direction):
    if current_direction == 'left':
        ms.player_press_right(False)
        ms.player_press_left(True)
    
    elif current_direction == 'right':
        ms.player_press_left(False)
        ms.player_press_right(True)


### START FARMING
def main_farm(target_yaw,target_pitch,starting_direction,horizontal_bounds,vertical_bounds):
    
    ### PHASE 1
    
    # CHECK CURRENT LOBBY IF YOU'RE STILL IN GARDEN
    if lobby_check.check_location() != 'GARDEN':
        lobby_check.rejoin()
        
    ### INITIAL CHECKS
    ms.echo('INITIALIZE FARMING') # CONFIRM IF COMMAND GOT THROUGH
    
    ### INITIALIZE FARMING 
    movement.reset_position()
    time.sleep(1.5)
    
    # PREPARE INITIAL STATE OF PLAYER BEFORE FARMING
    ms.player_inventory_select_slot(0) # 0-INDEXED HOTBAR KEY
    current_direction = starting_direction.lower() # STARTING DIRECTION OF YOUR LINE
    
    ms.echo('PASSED THE INITIAL STEPS','\n')
    ### START MAIN LOOP
    
    while True:
        ### PHASE 2
        
        if lobby_check.check_location() != 'GARDEN':
                movement.stop_movements()
                lobby_check.rejoin()
        
        # PRESS THE NORMAL BUTTONS
        ms.player_press_forward(True)
        ms.player_press_attack(True)
        
        # RETRIEVE PLAYER INFOS
        x,y,z = ms.player_position() # CONSTANTLY UPDATE PLAYER POSITION
        yaw, pitch = ms.player_orientation() # CONSTANTLY UPDATE PLAYER ORIENTATION
        
        # LOGIC TO RE-ALIGN CROSSHAIR TO CROPS
        ## IMPROVE
        movement.set_orientation(target_yaw,target_pitch) 
        
        # STARTS THE MOVEMENT
        move_to_direction(current_direction) # START MOVING TO CURRENT DIRECTION
        time.sleep(0.5)

        # GET PLAYER VELOCITY
        player_velocity_x, player_velocity_z = movement.get_velocity() # UPDATE X AND Z VELOCITY
        
        ### STATE CONDITIONS PER DIRECTION
        
        # DURING LEFT DIRECTION
        if current_direction == 'left':
            # REACHES THE LEFT BOUNDARY BUT NOT AT THE END
            if player_velocity_x == 0: 
                current_direction = change_direction(current_direction) # CHANGE DIRECTION
            
            # REACHES THE END OF THE FARM
            elif x >= horizontal_bounds[1] - 0.500 and z >= vertical_bounds[1] - 0.500:  
                movement.reset_position() # RESET POSITION AGAIN
                current_direction = starting_direction.lower()
                time.sleep(0.5) # DELAY BEFORE NEXT CYCLE
            
            # WHEN MOVING FORWARD, WAIT TILL YOU HIT A WALL
            while player_velocity_z > 0:
                time.sleep(POLLING_TIME)
                # GET PLAYER VELOCITY IN THE Z AXIS
                _,player_velocity_z = movement.get_velocity()
            
            
            move_to_direction(current_direction)           
                
        
        #DURING RIGHT DIRECTION
        elif current_direction == 'right':
            
            if player_velocity_x == 0:
                current_direction = change_direction(current_direction)
                
            while player_velocity_z > 0:
                time.sleep(POLLING_TIME)
                # GET PLAYER VELOCITY IN THE Z AXIS
                _,player_velocity_z = movement.get_velocity()  
            
            move_to_direction(current_direction)                 
        
        
        # PEST CHECK
        
        if lobby_check.check_location() != 'GARDEN':
                movement.stop_movements()
                lobby_check.rejoin()
                
        pest_status = update_pest()
        
        if pest_status != None:
            alive, _, _= pest_status
            # CHECK IF ALIVE > 4
            
            if alive >= 4:
                ms.echo("PEST THRESHOLD REACHED")
                time.sleep(1)
                ms.echo("ENTERING PEST HUNTING MODE")
                ms.player_press_left(False)
                ms.player_press_forward(False)
                ms.player_press_right(False)
                ms.player_press_attack(False)
                time.sleep(1)
                pest_hunt = True
                ms.execute(r'\pest_hunting_mode') # START PEST 
                return "HUNT"
                
        # CHECK IF PLAYER IS OUT OF BOUNDS
        if (x < x_bounds[0] - 2 or x > x_bounds[1] + 2) or (z < z_bounds[0] - 2 or z > z_bounds[1] + 2):
            ms.echo("PLAYER OUT OF BOUNDS, RESTARTING SCRIPT")
            ms.execute(r'\main')
            return None
        
