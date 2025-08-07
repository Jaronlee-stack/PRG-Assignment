from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    
    map_list =[]
    # TODO: Add your map loading code here
    with open(filename,'r') as map_file:
        map = ""
        for i in map_file:
            for j in i:
                if j !='\n':
                    map.join(j)
            map_list.append(list(map))
    map_struct.clear()
    map_struct.extend(map_list)

    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    for py in [-1,0,1]:
        for px in [-1,0,1]:
            y = player['y'] + py
            x = player['x'] + px   #change
            if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                fog[y][x] = False
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)
    row = len(game_map)
    col = len(game_map[0])
    fog[:] =[[True for _ in range(col)] for _ in range(row)] #change

    name = input("Greetings, miner!What is your name?")
    # TODO: initialize fog
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['name'] = name
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    
    print("Pleased to meet you, {}. Welcome to Sundrop Town!".format(player['name']))
    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    print("+" + "-" * MAP_WIDTH + "+")
    for y in range(MAP_HEIGHT):
        print("|", end="")
        for x in range(MAP_WIDTH):
            if (y, x) == (player['y'], player['x']):
                print("M", end="")
            elif 'portal' in player and (y, x) == player['portal']: #change
                print("P", end="")
            elif fog[y][x]:
                print("?", end="")
            else:
                print(game_map[y][x], end="")
        print("|")
    print("+" + "-" * MAP_WIDTH + "+")
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player): #change
    print("+---+")
    for py in [-1, 0, 1]:
        print("|", end="")
        for px in [-1, 0, 1]:
            y = player['y'] + py
            x = player['x'] + px
            if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                if (y, x) == (player['y'], player['x']):
                    print("M", end="")
                elif fog[y][x]:
                    print("?", end="")
                else:
                    print(game_map[y][x], end="")
            else:
                print("#", end="")
        print("|")
    print("+---+")
    return

# This function shows the information for the player
def show_information(player):
    print()
    print("----- Player Information -----")
    print("Name:{}".format(player['name']))

    if 'portal' in player:
        print("Portal position: {}".format(player['portal']))

    else:
        print("Portal position: (?,?)")
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
    
    
