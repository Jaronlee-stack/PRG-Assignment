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
        for i in map_file:
            map = ""
            for j in i:
                if j !='\n':
                    map+=j
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
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['load'] = 0
    player['pickaxe_lvl'] = 1
    player['portal'] = (0,0)
    player['capacity'] = 10
    
    print("Pleased to meet you, {}. Welcome to Sundrop Town!".format(player['name']))
    clear_fog(fog, player)
    return
    
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


# This function shows the information for the player
def show_information(player): #rephrase
    print()
    print("----- Player Information -----")
    print("Name: {}".format(player['name']))

    if 'portal' in player:
        print("Portal position: {}".format(player['portal']))

    else:
        print("Portal position: (?,?)")
    pickaxe_lvl = player['pickaxe_lvl']
    pickaxe_stats = ['copper', 'silver', 'gold'][pickaxe_lvl - 1]
    print(f"Pickaxe level: {pickaxe_lvl} ({pickaxe_stats})")
    print("------------------------------")
    print(f"Load: {player['load']} / {player['capacity']}")
    print("------------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("------------------------------")
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    with open("save_map.txt","w") as map_saved:
        for row in game_map:
            line ="" #research
            for i in row:
                line+=i
            map_saved.write(line + "\n")
    # save fog
    with open("save_fog.txt", "w") as fog_saved:
        for row in fog:
            line = ""
            for cell in row:
                line += '1' if cell else '0' #change
            fog_saved.write(line + "\n")
    # save player
    with open("save_player.txt", "w") as file: 
        for key in player:
            value = player[key]
            file.write(f"{key}:{value}\n")
    print("Game saved.")
    return
        
# This function loads the game
def load_game(game_map, fog, player): 
    # load map
    with open("save_map.txt", "r") as file:
        game_map[:] = [list(line.strip()) for line in file] #change
    # load fog
    with open("save_fog.txt", "r") as file:
        fog[:] = [[cell == '1' for cell in line.strip()] for line in file]
    # load player
    with open("save_player.txt", "r") as file:
        player.clear() #flag
        for line in file:
            key, value = line.strip().split(":", 1)
            if key in ['x', 'y', 'copper', 'silver', 'gold', 'GP', 'day', 'steps', 'turns', 'capacity', 'load', 'pickaxe_level']:
                player[key] = int(value)
            elif key == 'portal':
                x, y = value.strip("()").split(",")
                player[key] = (int(x), int(y))
            else:
                player[key] = value
    global MAP_WIDTH, MAP_HEIGHT
    MAP_WIDTH = len(game_map[0])
    MAP_HEIGHT = len(game_map)

    print("Game loaded successfully!")
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print("Day {}".format(player['day']))
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

def sell_ore(player): # (New) Sells mined minerals for GP and checks if player meets win condition
    sales_data = []
    for ore in minerals:
        qty = player[ore]
        if qty > 0:
            low_price, high_price = prices[ore]
            real_price = randint(low_price,high_price)
            earned = qty * real_price
            player['GP'] += earned
            print("You sell {} {} ore for {} GP".format(qty,ore,earned))
            sales_data.append((qty, ore, earned))
            player[ore] = 0

    
    print(f"You now have {player['GP']} GP!")
    won =player['GP'] >= WIN_GP
    if won:
        print("-------------------------------------------------------------")
        print(f"Woo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
        print("You now have enough to retire and play video games every day.")
        print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!")
        print("-------------------------------------------------------------")
        save_high_score(player)
    return sales_data, won
    
def shop_menu(player): # (New) Displays shop options for pickaxe and backpack upgrades

    while True:
        print()
        print("----------------------- Shop Menu -------------------------")
        # Pickaxe upgrade options
        if player['pickaxe_lvl'] == 1:
            print("(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP")
        elif player['pickaxe_lvl'] == 2:
            print("(P)ickaxe upgrade to Level 3 to mine gold ore for 150 GP")
        else:
            print("Pickaxe is already at max level (Level 3).")
        # Backpack upgrade
        cost = player['capacity'] * 2
        print(f"(B)ackpack upgrade to carry {player['capacity'] + 2} items for {cost} GP")
        print("(L)eave shop")
        print("-----------------------------------------------------------")
        print(f"Your GP: {player['GP']}")
        print("-----------------------------------------------------------")

        choice = input("Your choice? ").strip().upper()

        if choice == 'P':
            pickaxe_lvl = player['pickaxe_lvl']
            if pickaxe_lvl < 3:
                upgrade_cost = pickaxe_price[pickaxe_lvl-1]
                if player['GP'] < upgrade_cost:
                    print("Not enough GP for picaxe upgrade")
                
                else:
                    player['GP'] -= upgrade_cost
                    player['pickaxe_lvl'] += 1
                    print(f"Pickaxe upgraded to level {player['pickaxe_lvl']}!") #change
            else:
                print("Your pickaxe is already at max level!")
        elif choice == 'B':
            if player['GP'] >= cost:
                player['GP'] -= cost
                player['capacity'] += 2
                print(f"Congratulations! You can now carry {player['capacity']} items.")
                print("Not enough GP for backpack upgrade.")

        elif choice == 'L':
            print("Bye! See you again!")
            break

        else:
            print("Invalid choice. Please try again.")

def move_player(direction, game_map, fog, player): # (New) Moves player, handles mining, fog clearing, and portal use
    direction_map = {'W': (0, -1), 'S': (0, 1), 'A': (-1, 0), 'D': (1, 0)}
    if direction in direction_map:
        px, py = direction_map[direction]
    else:
        px, py = (0, 0)

    new_x = player['x'] + px
    new_y = player['y'] + py
    if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
        print("You can't go that way.")
        return
    if player['load'] >= player['capacity']:
            tile = game_map[new_y][new_x]
            if tile in mineral_names:  # trying to mine
                print("You can't carry anymore, so you can't go that way")
                return
    tile = game_map[new_y][new_x]

    if tile in mineral_names:
        if player['load'] >= player['capacity']:
            print("You can't carry any more, so you can't go that way.")
            player['turns'] =0 
            return
        required_level = {'C': 1, 'S': 2, 'G': 3}[tile]
        if int(player['pickaxe_lvl']) < required_level:
            print(f"Your pickaxe isn't strong enough to mine {mineral_names[tile]}.")
            return
        max_pieces = {'C': 5, 'S': 3, 'G': 2}[tile]
        mined = randint(1, max_pieces)
        space_left = player['capacity'] - player['load']
        ores_mined = min(mined, space_left)
        player[mineral_names[tile]] += ores_mined
        player['load'] += ores_mined
        print(f"You mined {mined} piece(s) of {mineral_names[tile]}.")
        if ores_mined < mined:
            print(f"...but you can only carry {ores_mined} more piece(s)!")
        game_map[new_y][new_x] = ' '
    elif tile == 'T':
        print("You stepped on the town portal. Returning to town...")
        portal(game_map, fog, player)
        return

    player['x'], player['y'] = new_x, new_y
    clear_fog(fog, player)

def portal(game_map, fog, player): # (New) Moves player, handles mining, fog clearing, and portal use
    player['portal'] = (player['y'], player['x'])
    print("You place your portal stone here and zap back to town.")
    sales_data, won = sell_ore(player)

    
    won = player['GP'] >= WIN_GP
    player['day'] += 1
    player['turns'] = TURNS_PER_DAY
    player['load'] = 0
    player['x'], player['y'] = 0, 0
    clear_fog(fog, player)
    if won:
        game_state = 'main'

def mine_menu(game_map, fog, player): # (New) Handles mining gameplay loop, user movement, and in-mine actions

    # Teleport to previous day's location
    if 'portal' in player:
        portal_location = player['portal']
        if portal_location != (0, 0):
            print(f"Teleporting to previous location at {portal_location}")
            player['y'], player['x'] = portal_location
            clear_fog(fog, player)
    if player['turns'] == TURNS_PER_DAY:
        print("\n---------------------------------------------------")
        print(f"{'DAY ' + str(player['day']):^51}")
        print("---------------------------------------------------")
    while player['turns'] > 0:
        print()

        print(f"DAY {player['day']}")
        draw_view(game_map, fog, player)
        print(f"Turns left: {player['turns']}     Load: {player['load']} / {player['capacity']}     Steps: {player['steps']}")
        print("(WASD) to move")
        print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")
        action = input("Action? ").upper()
        print("-------------------------------------------------------------")

        if action in ['W', 'A', 'S', 'D']:
            move_player(action, game_map, fog, player)
            player['steps'] += 1
            player['turns'] -= 1
        elif action == 'M':
            draw_map(game_map, fog, player)
        elif action == 'I':
            show_information(player)
        elif action == 'P':
            return portal(game_map, fog, player) or 'town'
        elif action == 'Q':
            print("Returning to main menu...")
            return 'main'
        else:
            print("Invalid input.")

    print("You are exhausted.")
    return portal(game_map, fog, player) or 'town'

def save_high_score(player):
    # Read existing scores
    scores = []

    with open("high_scores.txt", "r") as f:
        for line in f:
            name, days, steps = line.strip().split(":")
            scores.append((name, int(days), int(steps)))


    # Add new score
    scores.append((player['name'], player['day'], player['steps']))

    # Sort by fewest days, then fewest steps
    scores.sort(key=lambda s: (s[1], s[2]))

    # Keep top 10
    scores = scores[:10]

    # Save back
    with open("high_scores.txt", "w") as f:
        for name, days, steps in scores:
            f.write(f"{name}:{days}:{steps}\n")

def show_high_scores():
    print("===== HIGH SCORES =====")
    try:
        with open("high_scores.txt", "r") as f:
            for i, line in enumerate(f, 1):
                name, days, steps = line.strip().split(":")
                print(f"{i}. {name} - {days} day(s), {steps} step(s)")
    except FileNotFoundError:
        print("No high scores yet!")
    print("========================")
    print()
#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
while True:
    if game_state == 'main':
        show_main_menu()
        choice = input("Your choice? ").strip().upper()
        if choice.upper() == 'N':
            initialize_game(game_map, fog, player)
            game_state = 'town' 

        elif choice.upper() == 'L':
            load_game(game_map, fog, player)
            game_state = 'town'
            choice = input("Your choice? ").strip().upper()
        elif choice.upper() == 'Q':
            print("Thanks for playing Sundrop Caves! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    elif game_state == 'town':
        show_town_menu()
        choice = input("Your choice? ").upper()
        if choice.upper() == 'B':
            game_state = 'shop'
        elif choice.upper() == 'I':
            show_information(player)
        elif choice.upper() == 'M':
            draw_map(game_map, fog, player)
        elif choice.upper() == 'E':
            if 'portal' in player:
                player['x'], player['y'] = player['portal']
            else:
                player['x'], player['y'] = (0, 0)
            game_state = 'mine'
        elif choice.upper() == 'V':
            save_game(game_map, fog, player)
        elif choice.upper() == 'Q':
            game_state = 'main'
        else:
            print("Invalid choice. Please try again.")
    elif game_state == 'shop':
        shop_menu(player)
        game_state = 'town'
    elif game_state == 'mine':
        game_state = mine_menu(game_map, fog, player)
    
    
