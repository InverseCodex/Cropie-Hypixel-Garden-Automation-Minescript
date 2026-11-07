
# IMPORT LIBRARIES
import minescript as ms
from time import sleep


### LOBBY CHECKS

# INITIALIZE VARIABLES
TIME_BEFORE_REJOIN = 5 # 5 SECONDS BEFORE REJOINING A LOBBY

def check_location():
    entities = ms.entities()
    entity_count = len(entities)

    if entity_count == 1:
        return 'LIMBO'

    for identifiers in entities:
        if identifiers.name in ('Clerk Seraphine', 'Biblio'):
            return 'HUB'
        elif 'SkyBlock' in identifiers.name:
            return 'LOBBY'

    else:
        return 'GARDEN'


def move_server(location):
    if location == 'LIMBO':
        ms.execute('/lobby')
        sleep(TIME_BEFORE_REJOIN)

    elif location == 'HUB':
        ms.execute('/warp garden')
        return "DONE"

    elif location == 'LOBBY':
        ms.execute('/skyblock')

    return None


def rejoin():
    with ms.EventQueue() as EVENTS:
        EVENTS.register_world_listener()

        while True:
            try:
                current_location = check_location()

                if current_location == 'GARDEN':
                    ms.echo("YOU ARE IN THE GARDEN")
                    return

                move_server(current_location)
                sleep(TIME_BEFORE_REJOIN)
                ms.echo(current_location)

            except Exception:
                # Remain alive while disconnected or transferring.
                sleep(TIME_BEFORE_REJOIN)


rejoin()
