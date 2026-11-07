# Cropie-Hypixel-Garden-Automation
Cropie is a Python-based automation tool for Hypixel SkyBlock's Garden, built with Minescript and Pyjinn to automate crop farming and pest hunting.


# REQUIREMENTS:
## Before, downloading the script. Check if you have the following up-to-date.
1. Minescript 5.0 for Fabric (Recommended) - https://modrinth.com/mod/minescript/versions
2. Minecraft 26.3+ 
3. Fabric API (Recommended but if you have a different one, it's okay) - 

# HOW TO USE
## After making sure each requirements are already met do the following in order.
1. Locate your minescript folder in your current profile folder. (It's located usually at ...\profiles\minecraft-26.3\minescript)
2. Replace your minescript folder with the minescript folder from here and apply.
3. If you have existing scripts that you wanted to use, just drag the files into the folder instead of replacing it.
4. To execute the script, type '\main' when playing Hypixel SkyBlock works in the lobby, the hub, and your island.

# FEATURES
## GARDEN AUTOMATION
- HANDLES FARMING CROPS, AND HUNTNG PESTS AUTOMATICALLY.

## EVACUATION, LIMBO, AND KICK PROTECTION
- AUTO DETECTS WHEN A PLAYER GETS KICK BACK INTO THE HUB, OR LOBBY AND AUTOMATICALLY TRAVEL BACK TO THE GARDEN AND RESUME ITSELF

## INCOMING FEATURES
- MORE CUSTOMIZABLE OPTIONS AND A FRIENDLY HUD TO MANAGE THE SCRIPT
- BETTER PATHFINDING AND PEST HUNTING
- FORAGING, COMBAT, FISHING, AND MANY MORE SKILL GRINDING AUTOMATION INCOMING
- BETTER MACRO-CHECK DETECTION
- MORE SOPHISTICATED GARDENING TASK SUCH AS AUTO COMPLETE VISITOR AND AUTO STORE/ AUTO SELL INVENTORY

# KNOWN BUGS
- CURRENT VERSION CANNOT RELIABLY HUNT PESTS WHEN A GREENHOUSE IS PRESENT (WORKING ON IMPLEMENTING A PROPER PATHFINDING ALGORITHM)
- CURRENTLY WORKS ONLY ON S-SHAPED FARM
  
# FIRST RUN CHECKLIST
1. Open 'main.py' first and update the following variables:
- YAW_DURING_FARMING = The yaw of your player character during farming
- PITCH_DURING_FARMING = The pitch of your player character during farming
- STARTING_DIRECTION = The first direction in which you start moving when farming
- HORIZONTAL_BOUNDS = This is a 2 element list where it points towards the left and right bounds of your movement during farming
- VERTICAL_BOUNDS = This is a 2 element list where it points towards the up and down bounds of your movement during farming
