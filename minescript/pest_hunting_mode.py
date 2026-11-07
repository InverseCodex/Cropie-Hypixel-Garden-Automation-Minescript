### IMPORT LIBRARIES
import math
import minescript as ms
import java
import time
import lobby_check
import movement

### INITIALIZE EXTERNAL SCRIPT
HUD_SCRIPT = java.import_pyjinn_script("getPest.pyj")
get_pest = HUD_SCRIPT.get("getPest")

### INITIALIZE STATIC INFO
POLLING_TIME = 0.05
CHASE_COUNT = 5
# PEST TYPES
COMMON = {
    "entity.minecraft.bat",
    "entity.minecraft.silverfish"
}

# CORRESPONDS TO THE CENTER COORDINATE OF EACH PLOT NUMBER DO NOT CHANGE ANYTHING HERE
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


### UPDATE INFOS FUNCTION 
def update_pest(): # GETS HUD INFO, RETURNS PESTS INFO, IF RETURNED NONE, GARDEN IS CLEAR
    # IMPROVE
    ## IMPROVE THE ALGORITHM TO PICK THE CLOSEST PLOT INSTEAD OF PICKING THE FIRST INDEX
    
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

def pick_target(current_plot): # RETURNS TARGET UUID OR NONE IF NO PEST DETECTED
    current_plot = int(current_plot) # TURNS STR INTO INT
    entity_info = ms.entities(sort='nearest', limit=512, max_distance=512)
    
    # X AND Z BOUNDS OF CURRENT PLOT
    X_BOUNDS = (PLOT_CENTERS[current_plot][0] - 48, PLOT_CENTERS[current_plot][0] + 48)
    Z_BOUNDS = (PLOT_CENTERS[current_plot][1] - 48, PLOT_CENTERS[current_plot][1] + 48)
    
    # PICK A TARGET AND STORE THE UUID
    for entity in entity_info:
        tx,ty,tz = entity.position
        if entity.type in COMMON and (tx > X_BOUNDS[0] and tx < X_BOUNDS[1]) and (tz > Z_BOUNDS[0] and tz < Z_BOUNDS[1]): # MAKE SURE THE NEAREST PEST IS INSIDE THE PLOT
            ms.echo('CURRENT TARGET IS AT: ',tx,ty,tz, '\n')
            return entity.uuid
        
    ## NO PEST DETECTED NEARBY
    return None

def update_target_location(uuid): # RETURNS TARGET'S CURRENT LOCATION, IF NONE THEN THE TARGET IS NO LONGER DETECTED
    entity_info = ms.entities()
    
    # FIND THE X,Y,Z COORDINATE OF THE ENTITY WITH THE SPECIFIED UUID
    for entity in entity_info:
        if entity.uuid == uuid:
            tx, ty, tz = entity.position 
            return tx,ty,tz
    
    ## UUID IS NOT DETECTED NEARBY
    return None


### PEST HUNTING MOVEMENTS
def adjust_level(uuid): # GETS LEVEL WITH TARGET, IF IT RETURNS NONE: TARGET IS NO LONGER PRESENT
    target_location = update_target_location(uuid)
    
    if target_location == None:
        #UUID OF THE TARGET IS NO LONGER PRESENT
        return None
    
    x, y, z = ms.player_position()
    tx,ty,tz = target_location
    
    movement.toggle_descent(True) # MOVE DOWN TO Y + 9 OF THE TARGET PEST
    
    while y >= ty + 9: 
        x, y, z = ms.player_position() # CONSTANTLY UPDATE PLAYER'S POSITION
        
    movement.toggle_descent(False)
    return True

def chase_target(uuid): # JUST CHASES TARGET INCREMENTALLY, IF IT RETURNS NONE: TARGET IS NO LONGER PRESENT
    
    target_location = update_target_location(uuid)
    
    if target_location == None:
        #UUID OF THE TARGET IS NO LONGER PRESENT
        return None
    
    # IF TARGET IS STILL ALIVE
    x, y, z = ms.player_position()
    tx,ty,tz = target_location
    
    if y >= ty + 9: # GO TO Y + 9 LEVEL
        adjust_level(uuid) # GO TO Y + 9 LEVEL
    
    # INCREMENTAL MOVEMENT TO TARGET
    movement.target(tx,ty,tz) # LOOK AT TARGET
    ms.player_press_forward(True)
    
    for tries in range(0,CHASE_COUNT): # CONSTANT LOOP TO LOOK AT THE TARGET WHILE MOVING
        target_location = update_target_location(uuid)
        
        if target_location != None:
            tx,ty,tz = target_location
            x, y, z = ms.player_position()
            movement.target(tx,ty,tz)
            
            if movement.check_distance(x,z,tx,tz) <= 3:
                ms.player_press_forward(False)
                
            time.sleep(POLLING_TIME)
            
        else:
            ms.echo("CURRENT TARGET NO LONGER FOUND")
            break 
        
        
    ms.player_press_forward(False) # STOP CHASING
    
    ## CHASE END
    
def patrol_plot(current_plot): # RETURNS TARGET UUID OR NONE IF NO TARGET IS FOUND DURING PATROL
    current_plot = int(current_plot) # TURNS STR INTO INT
    # X AND Z BOUNDS OF CURRENT PLOT
    X_BOUNDS = (PLOT_CENTERS[current_plot][0] - 48, PLOT_CENTERS[current_plot][0] + 48)
    Z_BOUNDS = PLOT_CENTERS[current_plot][1]
    
    # GO TO THE STARTING POSITION
    x,y,z = ms.player_position()
    distance = movement.check_distance(x,z,X_BOUNDS[0], Z_BOUNDS)
    movement.target(X_BOUNDS[0], y, Z_BOUNDS)
    
    while distance > 2:
        x,y,z = ms.player_position()
        distance = movement.check_distance(x,z,X_BOUNDS[0], Z_BOUNDS)
        ms.player_press_forward(True)
    
    # ARRIVED AT THE STARTING POSITION
    ms.player_press_forward(False)
    
    # MOVE CROSSHAIR TO END POSITION
    movement.target(X_BOUNDS[1], y, Z_BOUNDS)
    x,y,z = ms.player_position()
    distance = movement.check_distance(x,z,X_BOUNDS[1], Z_BOUNDS)
    
    while distance > 5:
        x,y,z = ms.player_position()
        movement.target(X_BOUNDS[1], y, Z_BOUNDS)
        distance = movement.check_distance(x,z,X_BOUNDS[1], Z_BOUNDS)
        ms.player_press_forward(True)
        time.sleep(POLLING_TIME)
        target = pick_target(current_plot)
        
        if target != None:
            ms.player_press_forward(False)
            return target
    
    # NO TARGET FOUND DURING PATROL 
    ms.player_press_forward(False)
    return None

### GARDEN GENERAL MOVEMENTS
def move_to_center(current_plot): # MOVES TO THE CENTER OF THE CURRENT TARGET PLOT
    ms.echo('MOVE TO PLOT ',current_plot)
    current_plot = int(current_plot) # TURNS STR INTO INT
    # INITIALIZE THE X,Z COORDINATES OF THE PLOT'S CENTER AND THE PLAYER'S
    x_center, z_center =  PLOT_CENTERS[current_plot][0], PLOT_CENTERS[current_plot][1] 
    x,y,z = ms.player_position()
    
    distance = movement.check_distance(x,z,x_center,z_center)
    
    # MOVE TOWARDS THE CENTER
    movement.target(x_center,y,z_center)
    ms.player_press_forward(True)
    
    while distance > 6:
        x,y,z = ms.player_position()
        movement.target(x_center,y,z_center)
        distance = movement.check_distance(x,z,x_center,z_center)
        time.sleep(POLLING_TIME)
    
    ms.player_press_forward(False) # ARRIVED AT THE CENTER
    
def plot_fly(): # MOVES BACK TO Y = 100 AT THE CENTER OF THE CURRENT PLOT
    # FLY TO Y = 100 AGAIN
    x,y,z = ms.player_position()
    movement.toggle_ascent(True)
    
    while y < 100:
        x,y,z = ms.player_position()
    
    # DONE REACHING Y = 100
    movement.toggle_ascent(False)


### MAIN LOOP

# INITIALIZE VARIABLES
if lobby_check.check_location() != 'GARDEN':
    ms.echo('YOU ARE NOT IN THE GARDEN')
    movement.stop_movements()
    lobby_check.rejoin()
                
pest_status = update_pest()

## SPECIAL CONDITION: IF FOR SOME REASON THIS SCRIPT RUNS BUT GARDEN IS NOT INFESTED
if not pest_status:
    ms.echo("PLOT IS NOT INFESTED", '\n')
    alive = 0

## OFFICIALLY BEGIN THE PEST HUNT MODE
else: 
    if lobby_check.check_location() != 'GARDEN':
        movement.stop_movements()
        lobby_check.rejoin()
        
    # UPDATE VARIABLE VALUES
    alive, infested_plots, target_plot = update_pest()
    ms.echo(alive, infested_plots, target_plot)
    current_alive, current_plot = alive, target_plot
    is_leveled = False

    # BREAK FARMING AND STARTING PEST HUNTING
    movement.reset_position()
    time.sleep(2)
    
    # START PICKING A PLOT
    movement.toggle_fly() 
    ms.echo("CURRENT TARGET: ",current_plot)
    plot_fly() # INITIALIZE POSITION AT Y=100 OF CURRENT PLOT
    move_to_center(current_plot) # GO TO CENTER
    
    # SWITCH TO VACUUM
    ms.player_inventory_select_slot(1) # 0-INDEXED HOTBAR KEY

    

    
while alive > 0:
    # CHECK CURRENT LOBBY IF YOU'RE STILL IN GARDEN
    if lobby_check.check_location() != 'GARDEN':
        movement.stop_movements()
        lobby_check.rejoin()
        continue
        
    # CHECK IF A TARGET IS NEARBY
    current_alive = alive
    current_target = pick_target(current_plot)
    
    ## NONE DETECTED
    if current_target == None: # IF NO PESTS CAN BE DETECTED NEARBY
        
        # CHECK FIRST IF CURRENT PLOT STILL INFESTED
        pest_status = update_pest()
        
        if pest_status != None: # MAKES SURE THERE'S STILL PESTS
            alive, infested_plots, target_plot = pest_status
            
        else: # NO PESTS
            break
        
        # CHECKS IF THERE ARE PESTS IN THE CURRENT PLOT
        if alive > 0:
            
            if current_plot in infested_plots: # CURRENT PLOT IS STILL INFESTED, ACTIVATE PATROL
                
                while current_target == None: # ACTIVATE PATROL 
                    current_target = patrol_plot(current_plot)
                    
                    # CHECK IF PEST COUNT DROPPED
                    
                    #UPDATE PESTS INFO FIRST
                    
                    if lobby_check.check_location() != 'GARDEN':
                        movement.stop_movements()
                        lobby_check.rejoin()
                                    
                    pest_status = update_pest()
                            
                    if pest_status != None: # MAKES SURE THERE'S STILL PESTS
                        alive, infested_plots, target_plot = pest_status
                        
                    else:
                        break
                    
                    # CHECK IF PEST COUNT WENT DOWN
                    if current_alive > alive:
                        # CHECK IF PLOT STILL INFESTED
                        if current_plot in infested_plots:
                            continue
                        
                        else:
                            break # BREAK THE WHILE LOOP IF CURRENT PLOT NO LONGER INFESTED
                        
            elif alive == 0:
                break
        
            else: # CURRENT PLOT IS NO LONGER INFESTED, MOVE TO NEXT PLOT
                plot_fly() 
                is_leveled = False
                current_plot = target_plot
                move_to_center(current_plot)
            
    
    ## PEST DETECTED
    else: # IF A PEST IS TARGETED
        
        if is_leveled:
            ms.player_press_use(True) # HOLD DOWN RIGHT CLICK
            target_chase = chase_target(current_target) # PICK A TARGET AND CHASE IT
        
        else:
            ms.player_press_use(True) # HOLD DOWN RIGHT CLICK
            is_leveled = adjust_level(current_target) # GO DOWN TO Y + 11
            target_chase = chase_target(current_target) # PICK A TARGET AND CHASE IT
        
    
    #UPDATE PESTS INFO FIRST
    ms.player_press_use(False) # STOPS HOLDING RIGHT CLICK
    if lobby_check.check_location() != 'GARDEN':
        movement.stop_movements()
        lobby_check.rejoin()
                    
    pest_status = update_pest()
            
    if pest_status != None: # MAKES SURE THERE'S STILL PESTS
        alive, infested_plots, target_plot = pest_status
    else:
        break
    
    # CHECK IF PEST COUNT WENT DOWN
    if current_alive > alive and alive > 0:
        
        # CHECK IF PLOT STILL INFESTED
        if current_plot in infested_plots:
            continue
        
        else:
            # MOVE TO NEXT PLOT
            plot_fly()
            current_plot = target_plot # CHANGE TO THE NEXT TARGETED PLOT
            move_to_center(target_plot)
    

### PEST HUNTING DONE
ms.player_press_use(False)
ms.echo("PEST HUNT COMPLETED")
movement.toggle_fly()
time.sleep(2)
ms.execute(r'\main')
    
            
    
    