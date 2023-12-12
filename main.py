import pygame
import os
import sys
import graphics
import characters
import algorithm
import threading
import time
class GameState:
    def __init__(self, file_name):
        self.screen_size_x = 800
        self.screen_size_y = 533
        self.maze_width = 360         #maze 360 x 360px
        self.coordinate_map_x = 380   # tọa độ px đỉnh top-left của maze
        self.coordinate_map_y = 114
        self.getInputMaze(file_name)
        self.princess_direction = "RIGHT"
        self.ghost_direction = []
        for i in range(len(self.ghost_position)):
            self.ghost_direction.append("DOWN")
            
    def getInputMaze(self, name):
        self.maze = []
        self.gate_position = ()
        self.princess_position = ()
        self.ghost_position = []
        with open(os.path.join(maze_path, name),"r") as file:
            for line in file:
                row = []
                for chr in line:
                    if chr != '\n': row.append(chr)
                self.maze.append(row)

        self.maze_size = len(self.maze) // 2                    #maze 6/8/10
        self.cell_width = self.maze_width // self.maze_size     #độ dài px cạnh của 1 ô

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 'S':
                    self.gate_position = (i, j)
                if self.maze[i][j] == 'E':
                    self.princess_position = (i, j)
                if self.maze[i][j] == 'M':
                    self.ghost_position.append([i, j])
                    
    def show_information(self):
        print("Maze: ")
        for i in range(len(self.maze)):
            print(self.maze[i])
        print("Gate position: {}".format(self.gate_position))
        print("Princess position: {} {}".format(self.princess_position, self.princess_direction))
        for i in range(len(self.ghost_position)):
            print("Ghost number {}: {} {}".format(i+1, self.ghost_position[i], self.ghost_direction[i]))

def loadImagePath(size):
    image_path = os.path.join(project_path, "image")
    background_path = os.path.join(image_path, "background.png")
    border_path = os.path.join(image_path, "border.png")
    floor_path = os.path.join(image_path, "map"+str(size)+".png")
    wall_path = os.path.join(image_path, "wall"+str(size)+".png")
    gate_path = os.path.join(image_path, "gate"+str(size)+".png")
    princess_path = os.path.join(image_path, "princess"+str(size)+".png")
    ghost_path = os.path.join(image_path, "ghost"+str(size)+".png")
    ghostattack_path = os.path.join(image_path, "ghostattack"+str(size)+".png")
    signwin_path = os.path.join(image_path, "sign_win.png")
    signlose_path = os.path.join(image_path, "sign_lose.png")
    close_path= os.path.join(image_path, "close.png")
    bt_ai_path = os.path.join(image_path, "bt_aimode.png")
    bt_analyze_path = os.path.join(image_path, "bt_analyze.png")
    bt_restart_path = os.path.join(image_path, "bt_restart.png")
    bt_guide_path = os.path.join(image_path, "bt_guide.png")
    bt_select_map_path = os.path.join(image_path, "bt_select_map.png")
    bt_map_path = os.path.join(image_path, "bt_map.png")
    return background_path, border_path, floor_path, wall_path, gate_path, princess_path, ghost_path, \
        ghostattack_path, signwin_path, signlose_path, close_path, bt_ai_path, bt_analyze_path, bt_restart_path, bt_guide_path\
            , bt_select_map_path, bt_map_path
def calcCoordinate(game, x, y):
    coordinate_x = game.coordinate_map_x + game.cell_width * (y // 2)
    coordinate_y = game.coordinate_map_y + game.cell_width * (x // 2)
    return [coordinate_x, coordinate_y]
def updateEnemyPosition(window, game, background, border, floor, gate, wall, princess, princess_character, ghost_character, list_ghost, ghostattack, new_param):
    if checkPrincessIsKilled(princess_character, ghost_character):
        new_param["isDead"]=True
        new_param["dead_coord"]=(princess["coordinates"][0], princess["coordinates"][1])
        graphics.drawScreen(window, game, background, border, floor, gate,  wall, None, None, ghostattack, new_param)
        return 1
    #---First Move---
    past_position = []
    new_position = []
    for i in range(len(ghost_character)):
        past_position.append([ghost_character[i].getX(), ghost_character[i].getY()])
        ghost_character[i] = ghost_character[i].move(game.maze, princess_character)
        new_position.append([ghost_character[i].getX(), ghost_character[i].getY()])
    graphics.enemyMoveAnimation(past_position, new_position, window, game, background, border, floor, gate, wall, princess, list_ghost, ghostattack, new_param)
    if checkPrincessIsKilled(princess_character, ghost_character):
        new_param["isDead"]=True
        new_param["dead_coord"]=(princess["coordinates"][0], princess["coordinates"][1])
        graphics.drawScreen(window, game, background, border, floor, gate,  wall, None, None, ghostattack, new_param)
        return 1
    ghost_character, list_ghost = updateGhostList(ghost_character, list_ghost)
    
    #---Second Move---
    past_position = []
    new_position = []
    for i in range(len(ghost_character)):
        past_position.append([ghost_character[i].getX(), ghost_character[i].getY()])
        ghost_character[i] = ghost_character[i].move(game.maze, princess_character)
        new_position.append([ghost_character[i].getX(), ghost_character[i].getY()])
    graphics.enemyMoveAnimation(past_position, new_position, window, game, background, border, floor, gate, wall, princess, list_ghost, ghostattack, new_param)
    if checkPrincessIsKilled(princess_character, ghost_character):
        new_param["isDead"]=True
        new_param["dead_coord"]=(princess["coordinates"][0], princess["coordinates"][1])
        graphics.drawScreen(window, game, background, border, floor, gate,  wall, None, None, ghostattack, new_param)
        return 1
    ghost_character, list_ghost = updateGhostList(ghost_character, list_ghost)
    
    x = princess_character.getX()
    y = princess_character.getY()
    if game.maze[x-1][y]=="S" or game.maze[x+1][y]=="S" or game.maze[x][y-1]=="S" or game.maze[x][y+1]=="S":
        return 2
    return 0

def updateEnemyPosition_VS(window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, \
                           princess_character1, princess_character2, ghost_character1, ghost_character2, \
                               list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, player):
    if player==1:
        if checkPrincessIsKilled(princess_character1, ghost_character1):
            new_param1["isDead"]=True
            new_param1["dead_coord"]=(princess1["coordinates"][0], princess1["coordinates"][1])
            graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
            return 1
    else:
        if checkPrincessIsKilled(princess_character2, ghost_character2):
            new_param2["isDead"]=True
            new_param2["dead_coord"]=(princess2["coordinates"][0], princess2["coordinates"][1])
            graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
            return 1
    #---First Move---
    past_position = []
    new_position = []
    if player==1:
        for i in range(len(ghost_character1)):
            past_position.append([ghost_character1[i].getX(), ghost_character1[i].getY()])
            ghost_character1[i] = ghost_character1[i].move(game1.maze, princess_character1)
            new_position.append([ghost_character1[i].getX(), ghost_character1[i].getY()])
        graphics.enemyMoveAnimation_VS(past_position, new_position, window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, player)
        if checkPrincessIsKilled(princess_character1, ghost_character1):
            new_param1["isDead"]=True
            new_param1["dead_coord"]=(princess1["coordinates"][0], princess1["coordinates"][1])
            graphics.enemyMoveAnimation_VS(past_position, new_position, window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, player)
            return 1
        ghost_character1, list_ghost1 = updateGhostList(ghost_character1, list_ghost1)
    else:
        for i in range(len(ghost_character2)):
            past_position.append([ghost_character2[i].getX(), ghost_character2[i].getY()])
            ghost_character2[i] = ghost_character2[i].move(game2.maze, princess_character2)
            new_position.append([ghost_character2[i].getX(), ghost_character2[i].getY()])
        graphics.enemyMoveAnimation_VS(past_position, new_position, window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, player)
        if checkPrincessIsKilled(princess_character2, ghost_character2):
            new_param2["isDead"]=True
            new_param2["dead_coord"]=(princess2["coordinates"][0], princess2["coordinates"][1])
            graphics.enemyMoveAnimation_VS(past_position, new_position, window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, player)
            return 1
        ghost_character2, list_ghost2 = updateGhostList(ghost_character2, list_ghost2) 
    #---Second Move---
    past_position = []
    new_position = []
    if player==1:
        for i in range(len(ghost_character1)):
            past_position.append([ghost_character1[i].getX(), ghost_character1[i].getY()])
            ghost_character1[i] = ghost_character1[i].move(game1.maze, princess_character1)
            new_position.append([ghost_character1[i].getX(), ghost_character1[i].getY()])
        graphics.enemyMoveAnimation_VS(past_position, new_position, window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, player)
        if checkPrincessIsKilled(princess_character1, ghost_character1):
            new_param1["isDead"]=True
            new_param1["dead_coord"]=(princess1["coordinates"][0], princess1["coordinates"][1])
            graphics.enemyMoveAnimation_VS(past_position, new_position, window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, player)
            return 1
        ghost_character1, list_ghost1 = updateGhostList(ghost_character1, list_ghost1)
    else:
        for i in range(len(ghost_character2)):
            past_position.append([ghost_character2[i].getX(), ghost_character2[i].getY()])
            ghost_character2[i] = ghost_character2[i].move(game2.maze, princess_character2)
            new_position.append([ghost_character2[i].getX(), ghost_character2[i].getY()])
        graphics.enemyMoveAnimation_VS(past_position, new_position, window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, player)
        if checkPrincessIsKilled(princess_character2, ghost_character2):
            new_param2["isDead"]=True
            new_param2["dead_coord"]=(princess2["coordinates"][0], princess2["coordinates"][1])
            graphics.enemyMoveAnimation_VS(past_position, new_position, window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, player)
            return 1
        ghost_character2, list_ghost2 = updateGhostList(ghost_character2, list_ghost2) 
    x=y=0
    if player==1:
        x = princess_character1.getX()
        y = princess_character1.getY()
    else:
        x = princess_character2.getX()
        y = princess_character2.getY()
    if game1.maze[x-1][y]=="S" or game1.maze[x+1][y]=="S" or game1.maze[x][y-1]=="S" or game1.maze[x][y+1]=="S":
        return 2
    return 0
    
def checkPrincessIsKilled(princess_character, ghost_character):
    for i in range(len(ghost_character)):
        if princess_character.getX() == ghost_character[i].getX() and princess_character.getY() == ghost_character[i].getY():
            return True
    return False
def updateGhostList(ghost_character, list_ghost):
    i = 0
    while i < len(ghost_character):
        j = 0
        while j < len(ghost_character):
            if j != i and ghost_character[i].checkSamePosition(ghost_character[j]):
                del ghost_character[j]
                del list_ghost[j]
            j += 1
        i += 1
    return ghost_character, list_ghost
def newGame(mapname):
    global game, floor, wall, gate, princess_sheet, ghost_sheet, ghostattack, princess, list_ghost, \
        princess_character, ghost_character, new_param
    game = GameState(mapname)
    background_path, border_path, floor_path, wall_path, gate_path, princess_path, ghost_path, ghostattack_path, \
        signwin_path, signlose_path , close_path, bt_ai_path, bt_analyze_path, bt_restart_path, \
            bt_guide_path, bt_select_map_path, bt_map_path= loadImagePath(game.maze_size)
    floor = pygame.image.load(floor_path)
    wall = graphics.Wall_SpriteSheet(wall_path, game.maze_size)
    gate = graphics.Gate_SpriteSheet(gate_path)
    princess_sheet = graphics.Character_SpiteSheet(princess_path)
    ghost_sheet = graphics.Character_SpiteSheet(ghost_path)
    ghostattack = pygame.image.load(ghostattack_path)
    princess = {
        "sprite_sheet": princess_sheet,
        "coordinates": calcCoordinate(game, game.princess_position[0], game.princess_position[1]),
        "direction": game.princess_direction,
        "cellIndex": 0
        }
    list_ghost = []
    for i in range(len(game.ghost_position)):
         ghost = {
             "sprite_sheet": ghost_sheet,
             "coordinates": calcCoordinate(game, game.ghost_position[i][0], game.ghost_position[i][1]),
             "direction": game.ghost_direction[i],
             "cellIndex": 0
         }
         list_ghost.append(ghost)
    princess_character = characters.Princess(game.princess_position[0], game.princess_position[1])
    ghost_character = []
    for i in range(len(game.ghost_position)):
        ghost_character.append(characters.Ghost(game.ghost_position[i][0], game.ghost_position[i][1]))
    new_param["isDead"]=False
def newGame_VS(mapname):
    global game1, game2, floor, wall, gate, princess_sheet1, princess_sheet2, ghost_sheet1, \
        ghost_sheet2, ghostattack, princess1, princess2, list_ghost1, list_ghost2,\
        princess_character1, princess_character2, ghost_character1, ghost_character2, new_param, new_param1, new_param2
    game1 = GameState(mapname)
    game2 = GameState(mapname)
    game1.coordinate_map_x = 84
    game1.coordinate_map_y = 135
    game2.coordinate_map_x = 753
    game2.coordinate_map_y = 135
    background_path, border_path, floor_path, wall_path, gate_path, princess_path, ghost_path, ghostattack_path, \
        signwin_path, signlose_path , close_path, bt_ai_path, bt_analyze_path, bt_restart_path, \
            bt_guide_path, bt_select_map_path, bt_map_path= loadImagePath(game1.maze_size)
    floor = pygame.image.load(floor_path)
    wall = graphics.Wall_SpriteSheet(wall_path, game1.maze_size)
    gate = graphics.Gate_SpriteSheet(gate_path)
    princess_sheet1 = graphics.Character_SpiteSheet(princess_path)
    princess_sheet2 = graphics.Character_SpiteSheet(princess_path)
    ghost_sheet1 = graphics.Character_SpiteSheet(ghost_path)
    ghost_sheet2 = graphics.Character_SpiteSheet(ghost_path)
    ghostattack = pygame.image.load(ghostattack_path)
    princess1 = {
        "sprite_sheet": princess_sheet1,
        "coordinates": calcCoordinate(game1, game1.princess_position[0], game1.princess_position[1]),
        "direction": game1.princess_direction,
        "cellIndex": 0
        }
    princess2 = {
        "sprite_sheet": princess_sheet2,
        "coordinates": calcCoordinate(game2, game2.princess_position[0], game2.princess_position[1]),
        "direction": game2.princess_direction,
        "cellIndex": 0
        }
    list_ghost1 = []
    list_ghost2 = []
    for i in range(len(game1.ghost_position)):
         ghost = {
             "sprite_sheet": ghost_sheet1,
             "coordinates": calcCoordinate(game1, game1.ghost_position[i][0], game1.ghost_position[i][1]),
             "direction": game1.ghost_direction[i],
             "cellIndex": 0
         }
         list_ghost1.append(ghost)
         ghost = {
             "sprite_sheet": ghost_sheet2,
             "coordinates": calcCoordinate(game2, game2.ghost_position[i][0], game2.ghost_position[i][1]),
             "direction": game2.ghost_direction[i],
             "cellIndex": 0
         }
         list_ghost2.append(ghost)
    princess_character1 = characters.Princess(game1.princess_position[0], game1.princess_position[1])
    princess_character2 = characters.Princess(game2.princess_position[0], game2.princess_position[1])
    ghost_character1 = []
    ghost_character2 = []
    for i in range(len(game1.ghost_position)):
        ghost_character1.append(characters.Ghost(game1.ghost_position[i][0], game1.ghost_position[i][1]))
        ghost_character2.append(characters.Ghost(game2.ghost_position[i][0], game2.ghost_position[i][1]))
    new_param1 = new_param.copy()
    new_param2 = new_param.copy()
    new_param1["isDead"]=False
    new_param2["isDead"]=False
    new_param2["bt_algo"]=bt_algo2
    global isEnd1, isEnd2
    isEnd1=0
    isEnd2=0

def runGame(): 
    global game, floor, wall, gate, princess_sheet, ghost_sheet, ghostattack, princess, list_ghost, \
        princess_character, ghost_character, new_param
    global mapname
    game = GameState(mapname)
    pygame.init()
    global window
    window = pygame.display.set_mode((game.screen_size_x, game.screen_size_y))
    pygame.display.set_caption("Halloween Maze")
    #path=algorithm.Greedy(game.maze, game.princess_position, game.ghost_position, game.gate_position)
    # print(path)
    #game.show_information()
    image_path = os.path.join(project_path, "image")
    background_path, border_path, floor_path, wall_path, gate_path, princess_path, ghost_path, ghostattack_path, \
        signwin_path, signlose_path , close_path, bt_ai_path, bt_analyze_path, bt_restart_path, \
            bt_guide_path, bt_select_map_path, bt_map_path= loadImagePath(game.maze_size)
    background = pygame.image.load(background_path).convert_alpha()
    welcome_background = pygame.image.load(os.path.join(image_path, "bgr_start.png")).convert_alpha()
    border = pygame.image.load(border_path).convert_alpha()
    floor = pygame.image.load(floor_path).convert_alpha()
    wall = graphics.Wall_SpriteSheet(wall_path, game.maze_size)
    gate = graphics.Gate_SpriteSheet(gate_path)
    princess_sheet = graphics.Character_SpiteSheet(princess_path)
    ghost_sheet = graphics.Character_SpiteSheet(ghost_path)
    ghostattack = pygame.image.load(ghostattack_path).convert_alpha()
    signwin = pygame.image.load(signwin_path).convert_alpha()
    signlose = pygame.image.load(signlose_path).convert_alpha()
    text_select_maze = pygame.image.load(os.path.join(image_path, "text_select_maze.png")).convert_alpha()
    close = pygame.image.load(close_path).convert_alpha()
    bt_ai = graphics.Button(bt_ai_path)
    bt_analyze = graphics.Button(bt_analyze_path)
    bt_restart = graphics.Button(bt_restart_path)
    bt_guide = graphics.Button(bt_guide_path)
    bt_select_map = graphics.Button(bt_select_map_path)
    bt_start = graphics.Button(os.path.join(image_path, "bt_start.png"))
    bt_versus = graphics.Button(os.path.join(image_path, "bt_start.png"))
    guide_background = pygame.image.load(os.path.join(image_path, "guide.png")).convert_alpha()
    reddot = pygame.image.load(os.path.join(image_path, "reddot.png")).convert_alpha()
    switch_on = graphics.Button(os.path.join(image_path, "switch_on.png"))
    switch_off = graphics.Button(os.path.join(image_path, "switch_off.png"))
    analyze = pygame.image.load(os.path.join(image_path, "analyze.png")).convert_alpha()
    blank = pygame.image.load(os.path.join(image_path, "blank.png")).convert_alpha()
    guide_key = pygame.image.load(os.path.join(image_path, "guide_key.png")).convert_alpha()
    winstate_vs = pygame.image.load(os.path.join(image_path, "winstate_vs.png")).convert_alpha()
    losestate_vs = pygame.image.load(os.path.join(image_path, "losestate_vs.png")).convert_alpha()
    drawstate_vs = pygame.image.load(os.path.join(image_path, "drawstate_vs.png")).convert_alpha()
    
    bt_main = []
    bt_main.append(bt_restart)
    bt_main.append(bt_ai)
    bt_main.append(bt_select_map)
    bt_main.append(bt_guide)
    bt_main.append(bt_analyze)
    
    bt_exit = graphics.Button(close_path)
    
    bt_map =[]
    dic_map = {}
    for i in range(32):
        bt = graphics.Button(bt_map_path)
        if i<10:
            bt.name="map6_"+str(i+1)+".txt"
        elif i<24:
            bt.name="map8_"+str(i-9)+".txt"
        else:
            bt.name="map10_"+str(i-23)+".txt"
        dic_map[bt.name] = i+1
        bt_map.append(bt)
    
    princess = {
        "sprite_sheet": princess_sheet,
        "coordinates": calcCoordinate(game, game.princess_position[0], game.princess_position[1]),
        "direction": game.princess_direction,
        "cellIndex": 0
        }
    list_ghost = []
    for i in range(len(game.ghost_position)):
         ghost = {
             "sprite_sheet": ghost_sheet,
             "coordinates": calcCoordinate(game, game.ghost_position[i][0], game.ghost_position[i][1]),
             "direction": game.ghost_direction[i],
             "cellIndex": 0
         }
         list_ghost.append(ghost)
    princess_character = characters.Princess(game.princess_position[0], game.princess_position[1])
    ghost_character = []
    for i in range(len(game.ghost_position)):
        ghost_character.append(characters.Ghost(game.ghost_position[i][0], game.ghost_position[i][1]))
    
    
    label_map = graphics.Label("Map : ", "Yellow")
    label_size = graphics.Label("Size : ", "Yellow")
    label_algo = graphics.Label("Algorithm : ", "Yellow")
    label_step = graphics.Label("Steps : 0", "Yellow")
    label_main = []
    label_main.append(label_map)
    label_main.append(label_algo)
    label_main.append(label_size)
    label_main.append(label_step)
    
    bt_back = graphics.Button(os.path.join(image_path, "back.png"))
    bt_algo_path = os.path.join(image_path, "ai_button.png")
    bt_algo = []
    global bt_algo2
    bt_algo2 = []
    for i in range(6):  
        bt = graphics.Button(bt_algo_path)
        bt.name = "algo"+str(i+1)
        bt_algo.append(bt)
    
    for i in range(6):  
        bt = graphics.Button(bt_algo_path)
        bt.name = "algo"+str(i+1)
        bt_algo2.append(bt)
    

    bt_vs=[]
    bt_vs_dic = ["restart", "map", "start"]
    for i in range(3):
        bt=graphics.Button(os.path.join(image_path, "bt_start_s.png"))
        bt.name = bt_vs_dic[i]
        bt_vs.append(bt)
    
    #thêm
    bt_switchplayer = graphics.Button(os.path.join(image_path, "ai_button.png"))
    
    new_param = {
        "isDead": False, 
        "dead_coord": calcCoordinate(game, game.princess_position[0], game.princess_position[1]),
        "close": close,
        "bt_main": bt_main,
        "label_main": label_main,
        "visualize_node": None,
        "reddot": reddot,
        "switch_on": switch_on,
        "switch_off": switch_off,
        "switchIsOn": False,
        "bt_algo": bt_algo,
        "isAlgoSelecting" : False,
        "bt_back": bt_back,
        "bt_vs": bt_vs,
        "guide_key": guide_key,
        "bt_switchplayer" : bt_switchplayer, #thêm
        "isPlayervsAI" : False #thêm
        }
    global mode
    clock = pygame.time.Clock()
    #####Welcome Phase
    click = False
    while not click:
        graphics.drawWelcome(window, welcome_background, bt_start, bt_versus)
        cursor_pos = pygame.mouse.get_pos()
        #print(bt_start.getX(), bt_start.getY(),"_____", cursor_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bt_start.isClicked(cursor_pos):
                    click=True
                    mode = 1
                    break
                if bt_versus.isClicked(cursor_pos):
                    click=True
                    mode = 2
                    break
        pygame.display.update()
        clock.tick(30)
    #####Select Level
    graphics.drawLevel(window, game, background, bt_map, text_select_maze)
    click=False
    while not click:
        graphics.drawLevel(window, game, background, bt_map, text_select_maze)
        cursor_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bt in bt_map:
                    if bt.isClicked(cursor_pos):
                        mapname = bt.name
                        print(mapname)
                        newGame(mapname)
                        label_map.updateText("Map : " + str(dic_map[mapname]))
                        label_size.updateText("Size : " + str(game.maze_size) + "x" + str(game.maze_size))
                        isEnd = 0
                        graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                        click=True
                        break
        clock.tick(30)
        pygame.display.update()
    
    #####Main
    if mode==1:
        isEnd = 0
        step = 0 
        def solveGame(algo):
            step=0
            path = []
            newGame(mapname)
            if(algo=="algo1"):
                path, visualize_node, visited =algorithm.BFS(game.maze, game.princess_position, game.ghost_position)
            if(algo=="algo2"):
                path, visualize_node, visited =algorithm.DFS(game.maze, game.princess_position, game.ghost_position)
            if(algo=="algo3"):
                path, visualize_node, visited =algorithm.IDS(game.maze, game.princess_position, game.ghost_position)
            if(algo=="algo4"):
                path, visualize_node, visited =algorithm.UCS(game.maze, game.princess_position, game.ghost_position)
            if(algo=="algo5"):
                path, visualize_node, visited =algorithm.Greedy(game.maze, game.princess_position, game.ghost_position, game.gate_position)
            if(algo=="algo6"):
                path, visualize_node, visited =algorithm.A_star(game.maze, game.princess_position, game.ghost_position, game.gate_position)
            if (path!=None):
                new_param["visualize_node"]=visualize_node
                if new_param["switchIsOn"]:
                    graphics.visualize(window, game, reddot, visualize_node)
                if (path!=None):
                    for move in path:
                        if move[0]==princess_character.getX()-2:
                            princess["direction"] = "UP"
                        if move[0]==princess_character.getX()+2:
                            princess["direction"] = "DOWN" 
                        if move[1]==princess_character.getY()-2:
                            princess["direction"] = "LEFT"
                        if move[1]==princess_character.getY()+2:
                            princess["direction"] = "RIGHT"
                        if princess_character.getX() != move[0] or princess_character.getY() != move[1]:
                            princess_character.move(move[0], move[1], window, game, background, border, floor, gate, wall, princess, list_ghost, ghostattack, new_param)
                        #pygame.display.update()
                        step += 1
                        label_step.updateText("Step : " + str(step))
                        isEnd = updateEnemyPosition(window, game, background, border, floor, gate, wall, princess, princess_character, ghost_character, list_ghost, ghostattack, new_param)
                        if isEnd==2: #win
                            graphics.raiseSign(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param, signwin)
                            bt_exit.draw(window, 642, 155)
                        cursor_pos = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if switch_off.isClicked(cursor_pos):
                                    if (new_param["switchIsOn"]):
                                        new_param["switchIsOn"]=False
                                    else:
                                        new_param["switchIsOn"]=True
                                                        
        graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
        while True:
            current_princess_x = princess_character.getX()
            current_princess_y = princess_character.getY()
            new_princess_x = current_princess_x
            new_princess_y = current_princess_y
            cursor_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and isEnd==0:
                    if event.key == pygame.K_UP:
                        if princess_character.isEligibleMove(game.maze, current_princess_x, current_princess_y, current_princess_x - 2, current_princess_y):
                            new_princess_x -= 2
                            princess["direction"] = "UP"
                    if event.key == pygame.K_DOWN:
                        if princess_character.isEligibleMove(game.maze, current_princess_x, current_princess_y, current_princess_x + 2, current_princess_y):
                            new_princess_x += 2
                            princess["direction"] = "DOWN"
                    if event.key == pygame.K_LEFT:
                        if princess_character.isEligibleMove(game.maze, current_princess_x, current_princess_y, current_princess_x, current_princess_y - 2):
                            new_princess_y -= 2
                            princess["direction"] = "LEFT"
                    if event.key == pygame.K_RIGHT:
                        if princess_character.isEligibleMove(game.maze, current_princess_x, current_princess_y, current_princess_x, current_princess_y + 2):
                            new_princess_y += 2
                            princess["direction"] = "RIGHT"   
                    
                    if current_princess_x != new_princess_x or current_princess_y != new_princess_y:
                        princess_character.move(new_princess_x, new_princess_y, window, game, background, border, floor, gate, wall, princess, list_ghost, ghostattack, new_param)
                    if (event.key==pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                        step += 1
                        label_step.updateText("Steps : " + str(step))
                        isEnd = updateEnemyPosition(window, game, background, border, floor, gate, wall, princess, princess_character, ghost_character, list_ghost, ghostattack, new_param)
                    if isEnd==1: #lose
                        graphics.raiseSign(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param, signlose)
                        bt_exit.draw(window, 642, 155)
                    elif isEnd==2: #win
                        graphics.raiseSign(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param, signwin)
                        bt_exit.draw(window, 642, 155)
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if isEnd==1 or isEnd==2:
                        #bt_exit.draw(window, 642, 155)
                        if bt_exit.isClicked(cursor_pos):
                            graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                    if switch_off.isClicked(cursor_pos):
                        if (new_param["switchIsOn"]):
                            new_param["switchIsOn"]=False
                        else:
                            new_param["switchIsOn"]=True
                        graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                    for bt in bt_main:
                        if bt.isClicked(cursor_pos):
                            if bt==bt_restart:
                                newGame(mapname)
                                step=0
                                label_step.updateText("Steps : " + str(step))
                                label_algo.updateText("Algorithm : ")
                                isEnd = 0
                                new_param["visualize_node"]=None;
                                graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                                break
                            if bt==bt_select_map:
                                graphics.drawLevel(window, game, background, bt_map, text_select_maze)
                                step=0
                                label_step.updateText("Steps : " + str(step))
                                new_param["visualized"]=False;
                                click=False
                                while not click:
                                    graphics.drawLevel(window, game, background, bt_map, text_select_maze)
                                    cursor_pos = pygame.mouse.get_pos()
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            for bt in bt_map:
                                                if bt.isClicked(cursor_pos):
                                                    mapname = bt.name
                                                    cursor_pos=(0,0)
                                                    newGame(mapname)
                                                    label_map.updateText("Map : " + str(dic_map[mapname]))
                                                    label_size.updateText("Size : " + str(game.maze_size) + "x" + str(game.maze_size))
                                                    isEnd = 0
                                                    graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                                                    click=True
                                                    new_param["visualize_node"]=None
                                                    break
                                    pygame.display.update()
                            if bt==bt_guide: 
                                click=False
                                while not click:
                                    graphics.drawGuide(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param, guide_background, bt_exit )
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            cursor_pos = pygame.mouse.get_pos()
                                            if bt_exit.isClicked(cursor_pos):
                                                click=True
                                                graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                                                break 
                            if bt==bt_ai:
                                click=False
                                new_param["isAlgoSelecting"] = True
                                graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                                pygame.display.update()
                                while not click:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            cursor_pos = pygame.mouse.get_pos()
                                            if bt_exit.isClicked(cursor_pos):
                                                graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                                                pygame.display.update()
                                                break 
                                            if bt_back.isClicked(cursor_pos):
                                                click=True
                                                new_param["isAlgoSelecting"] = False
                                                graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                                                break 
                                            for bt in bt_algo:
                                                if bt.isClicked(cursor_pos):
                                                    new_param["visualize_node"]=None
                                                    newGame(mapname)
                                                    new_param["isAlgoSelecting"] = False
                                                    cursor_pos = (0,0)
                                                    graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                                                    pygame.display.update()
                                                    pygame.time.delay(500)
                                                    list_algo = ["BFS","DFS","IDS","UCS","GREEDY","A*"]
                                                    label_algo.updateText("Algorithm : " + list_algo[int(bt.name[-1])-1])
                                                    solveGame(bt.name)
                                                    click=True
                                                    isEnd=2
                                                    break 
                            if bt==bt_analyze:
                                window.blit(background, (0,0))
                                window.blit(analyze, (0,0))
                                map_lb=graphics.Label(str(dic_map[mapname]),"Black", 35)
                                map_lb.draw(window, 343, 29)
                                size_lb=graphics.Label(str(game.maze_size)+"x"+str(game.maze_size),"Black", 35)
                                size_lb.draw(window, 530, 29)
                                ghost_lb=graphics.Label(str(len(game.ghost_position)),"Black", 35)
                                ghost_lb.draw(window, 730, 29)
                                
                                bt_back.draw(window, 200, 17)
                                pygame.display.update()
                                
                                thread1=graphics.AlgoThread("bfs", 9, 95, window, blank, game)
                                thread2=graphics.AlgoThread("dfs", 275, 95, window, blank, game)
                                thread3=graphics.AlgoThread("ids", 541, 95, window, blank, game)
                                thread4=graphics.AlgoThread("ucs", 9, 314, window, blank, game)
                                thread5=graphics.AlgoThread("greedy", 275, 314, window, blank, game)
                                thread6=graphics.AlgoThread("astar", 541, 314, window, blank, game)
                                
                                thread1.start()
                                thread2.start()
                                thread3.start()
                                thread4.start()
                                thread5.start()
                                thread6.start()
                                
                                back=False
                                while not back:
                                    cursor_pos = pygame.mouse.get_pos()
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            thread1.stopThread()
                                            thread2.stopThread()
                                            thread3.stopThread()
                                            thread4.stopThread()
                                            thread5.stopThread()
                                            thread6.stopThread()
                                            thread1.join()
                                            thread2.join()
                                            thread3.join()
                                            thread4.join()
                                            thread5.join()
                                            thread6.join()
                                            pygame.quit()
                                            sys.exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            if bt_back.isClicked(cursor_pos):
                                                thread1.stopThread()
                                                thread2.stopThread()
                                                thread3.stopThread()
                                                thread4.stopThread()
                                                thread5.stopThread()
                                                thread6.stopThread()
                                                back=True
                                                break
                                    
                                thread1.join()
                                thread2.join()
                                thread3.join()
                                thread4.join()
                                thread5.join()
                                thread6.join()
                                
                                graphics.drawScreen(window, game, background, border, floor, gate,  wall, princess, list_ghost, ghostattack, new_param)
                                pygame.display.update()
                                        
                    break
                pygame.display.update()
            clock.tick(30)
    else:
        bgr_versus = pygame.image.load(os.path.join(image_path, "bgr_versus.png")).convert_alpha()
        window = pygame.display.set_mode((1200,700))
        global game1, game2, princess_sheet1, princess_sheet2, ghost_sheet1, \
            ghost_sheet2, princess1, princess2, list_ghost1, list_ghost2,\
            princess_character1, princess_character2, ghost_character1, \
                ghost_character2, new_param1, new_param2
        newGame_VS(mapname)
        graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
        pygame.display.update()
        global isEnd1, isEnd2
        isEnd1=0
        isEnd2=0
        
        #thêm
        global isStop, stop_flag
        isStop = False
        
        algo_choosen1 = "algo1"
        algo_choosen2 = "algo1"
        fadeOut = 0.6
        for bt in bt_algo: 
            if bt.name != algo_choosen1:
                bt.getImg().set_alpha(255*fadeOut)
        for bt in bt_algo2: 
            if bt.name != algo_choosen2:              
                bt.getImg().set_alpha(255*fadeOut)
        def solveGame_VS(algo, algo2):
            global mapname, window
            path = []
            path2 = []
            newGame_VS(mapname)
            if(algo=="algo1"):
                path, visualize_node, visited =algorithm.BFS(game1.maze, game1.princess_position, game1.ghost_position)
            if(algo=="algo2"):
                path, visualize_node, visited =algorithm.DFS(game1.maze, game1.princess_position, game1.ghost_position)
            if(algo=="algo3"):
                path, visualize_node, visited =algorithm.IDS(game1.maze, game1.princess_position, game1.ghost_position)
            if(algo=="algo4"):
                path, visualize_node, visited =algorithm.UCS(game1.maze, game1.princess_position, game1.ghost_position)
            if(algo=="algo5"):
                path, visualize_node, visited =algorithm.Greedy(game1.maze, game1.princess_position, game1.ghost_position, game1.gate_position)
            if(algo=="algo6"):
                path, visualize_node, visited =algorithm.A_star(game1.maze, game1.princess_position, game1.ghost_position, game1.gate_position)
            if(algo2=="algo1"):
                path2, visualize_node, visited =algorithm.BFS(game2.maze, game2.princess_position, game2.ghost_position)
            if(algo2=="algo2"):
                path2, visualize_node, visited =algorithm.DFS(game2.maze, game2.princess_position, game2.ghost_position)
            if(algo2=="algo3"):
                path2, visualize_node, visited =algorithm.IDS(game2.maze, game2.princess_position, game2.ghost_position)
            if(algo2=="algo4"):
                path2, visualize_node, visited =algorithm.UCS(game2.maze, game2.princess_position, game2.ghost_position)
            if(algo2=="algo5"):
                path2, visualize_node, visited =algorithm.Greedy(game2.maze, game2.princess_position, game2.ghost_position, game2.gate_position)
            if(algo2=="algo6"):
                path2, visualize_node, visited =algorithm.A_star(game2.maze, game2.princess_position, game2.ghost_position, game2.gate_position)
            if (path!=None):
                for i in range(min(len(path),len(path2))):
                    move = path[i]
                    move2 = path2[i]
                    if move[0]==princess_character1.getX()-2:
                        princess1["direction"] = "UP"
                    if move[0]==princess_character1.getX()+2:
                        princess1["direction"] = "DOWN" 
                    if move[1]==princess_character1.getY()-2:
                        princess1["direction"] = "LEFT"
                    if move[1]==princess_character1.getY()+2:
                        princess1["direction"] = "RIGHT"
                    if move2[0]==princess_character2.getX()-2:
                        princess2["direction"] = "UP"
                    if move2[0]==princess_character2.getX()+2:
                        princess2["direction"] = "DOWN" 
                    if move2[1]==princess_character2.getY()-2:
                        princess2["direction"] = "LEFT"
                    if move2[1]==princess_character2.getY()+2:
                        princess2["direction"] = "RIGHT"
                    if princess_character1.getX() != move[0] or princess_character1.getY() != move[1]:
                        princess_character1.move_VS(move[0], move[1], window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 1)
                    if princess_character2.getX() != move2[0] or princess_character2.getY() != move2[1]:
                        princess_character2.move_VS(move2[0], move2[1], window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 2)
                    isEnd1 = updateEnemyPosition_VS(window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, princess_character1, princess_character2, ghost_character1, ghost_character2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 1)
                    isEnd2 = updateEnemyPosition_VS(window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, princess_character1, princess_character2, ghost_character1, ghost_character2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 2)
                    if (isEnd1<=1 and isEnd2==2):
                        graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, losestate_vs, winstate_vs)
                    elif (isEnd1==2 and isEnd2<=1):
                        graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, winstate_vs, losestate_vs)
                    elif (isEnd1==2 and isEnd2==2):
                        graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, drawstate_vs, drawstate_vs)
            click1=False
            while not click1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        cursor_pos = pygame.mouse.get_pos()
                        for bt in bt_algo:
                            if bt.isClicked(cursor_pos):
                                bt.getImg().set_alpha(255)
                                algo_choosen1 = bt.name
                                for bt in bt_algo:
                                    if bt.name!=algo_choosen1:
                                        bt.getImg().set_alpha(255 * fadeOut)
                        for bt in bt_algo2:
                            if bt.isClicked(cursor_pos):
                                bt.getImg().set_alpha(255)
                                algo_choosen2 = bt.name
                                for bt in bt_algo2:
                                    if bt.name!=algo_choosen2:
                                        bt.getImg().set_alpha(255 * fadeOut)
                        pygame.display.update()
                        for bt in bt_vs:
                            if bt.isClicked(cursor_pos):
                                if bt.name == bt_vs_dic[0]:
                                    click1 = True
                                    newGame_VS(mapname)
                                if bt.name == bt_vs_dic[1]:
                                    click1 = True
                                    window = pygame.display.set_mode((game.screen_size_x, game.screen_size_y))
                                    graphics.drawLevel(window, game, background, bt_map, text_select_maze)
                                    click=False
                                    while not click:
                                        graphics.drawLevel(window, game, background, bt_map, text_select_maze)
                                        cursor_pos = pygame.mouse.get_pos()
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                for bt in bt_map:
                                                    if bt.isClicked(cursor_pos):
                                                        mapname = bt.name
                                                        cursor_pos = (0, 0)
                                                        window = pygame.display.set_mode((1200,700))
                                                        newGame_VS(mapname)
                                                        graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                                                        click=True
                                                        break
                                        clock.tick(30)
                                        pygame.display.update()
        #thêm
        def solveGame_VS2(algo): 
            global mapname, window, isStop
            path = []
            newGame_VS(mapname)
            new_param1["isPlayervsAI"] = True
            graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
            if(algo=="algo1"):
                path, visualize_node, visited =algorithm.BFS(game2.maze, game2.princess_position, game2.ghost_position)
            if(algo=="algo2"):
                path, visualize_node, visited =algorithm.DFS(game2.maze, game2.princess_position, game2.ghost_position)
            if(algo=="algo3"):
                path, visualize_node, visited =algorithm.IDS(game2.maze, game2.princess_position, game2.ghost_position)
            if(algo=="algo4"):
                path, visualize_node, visited =algorithm.UCS(game2.maze, game2.princess_position, game2.ghost_position)
            if(algo=="algo5"):
                path, visualize_node, visited =algorithm.Greedy(game2.maze, game2.princess_position, game2.ghost_position, game2.gate_position)
            if(algo=="algo6"):
                path, visualize_node, visited =algorithm.A_star(game2.maze, game2.princess_position, game2.ghost_position, game2.gate_position)
            if (path!=None):
                for move in path:
                    if not stop_flag:
                        if move[0]==princess_character2.getX()-2:
                            princess2["direction"] = "UP"
                        if move[0]==princess_character2.getX()+2:
                            princess2["direction"] = "DOWN" 
                        if move[1]==princess_character2.getY()-2:
                            princess2["direction"] = "LEFT"
                        if move[1]==princess_character2.getY()+2:
                            princess2["direction"] = "RIGHT"
                        if princess_character2.getX() != move[0] or princess_character2.getY() != move[1]:
                            time.sleep(1)
                            princess_character2.move_VS(move[0], move[1], window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 2)
                        isEnd2 = updateEnemyPosition_VS(window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, princess_character1, princess_character2, ghost_character1, ghost_character2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 2)
                        # if isEnd2==2: #win
                        #     graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, winstate_vs, losestate_vs)
            isStop = True

        while True:
            if not new_param1["switchIsOn"]:
                new_param["switchIsOn"]=False
                current_princess_x1 = princess_character1.getX()
                current_princess_y1 = princess_character1.getY()
                new_princess_x1 = current_princess_x1
                new_princess_y1 = current_princess_y1
                current_princess_x2 = princess_character2.getX()
                current_princess_y2 = princess_character2.getY()
                new_princess_x2 = current_princess_x2
                new_princess_y2 = current_princess_y2
                cursor_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if switch_off.isClicked(cursor_pos):
                            if (new_param1["switchIsOn"]):
                                new_param1["switchIsOn"]=False
                            else:
                                new_param1["switchIsOn"]=True
                            graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                            break
                        for bt in bt_vs:
                            if bt==bt_vs[2]:
                                continue
                            if bt.isClicked(cursor_pos):
                                if bt.name == bt_vs_dic[0]:
                                    newGame_VS(mapname)
                                    graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                                    pygame.display.update()
                                if bt.name == bt_vs_dic[1]:
                                    window = pygame.display.set_mode((game.screen_size_x, game.screen_size_y))
                                    graphics.drawLevel(window, game, background, bt_map, text_select_maze)
                                    pygame.display.update()
                                    click=False
                                    while not click:
                                        graphics.drawLevel(window, game, background, bt_map, text_select_maze)
                                        cursor_pos = pygame.mouse.get_pos()
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                for bt in bt_map:
                                                    if bt.isClicked(cursor_pos):
                                                        mapname = bt.name
                                                        cursor_pos = (0, 0)
                                                        window = pygame.display.set_mode((1200,700))
                                                        newGame_VS(mapname)
                                                        graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                                                        click=True
                                                        break
                                            pygame.display.update()
                                            
                        #thêm
                        if bt_switchplayer.isClicked(cursor_pos):
                            if (new_param1["isPlayervsAI"]):
                                new_param1["isPlayervsAI"]=False
                            else:
                                new_param1["isPlayervsAI"]=True
                            graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                        if new_param1["isPlayervsAI"]:
                            for bt in bt_algo2:
                                if bt.isClicked(cursor_pos):
                                    bt.getImg().set_alpha(255)
                                    algo_choosen2 = bt.name
                                    for bt in bt_algo2:
                                        if bt.name!=algo_choosen2:
                                            bt.getImg().set_alpha(255 * fadeOut)   
                                    graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                            for bt in bt_vs:
                                if bt.isClicked(cursor_pos) and bt.name == bt_vs_dic[2]:
                                    for i in range(3):
                                        font = pygame.font.Font(None, 40)
                                        text = font.render("Ready in : " + str(3-i), True, "Yellow")
                                        graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                                        window.blit(text,(520, 100))
                                        pygame.display.update()
                                        time.sleep(1)
                                    stop_flag = False
                                    isEnd1=0 
                                    isStop = False
                                    t = threading.Thread(target=solveGame_VS2, args=(algo_choosen2,))
                                    t.start()
                                    isOver = False
                                    while not isOver:
                                        current_princess_x1 = princess_character1.getX()
                                        current_princess_y1 = princess_character1.getY()
                                        new_princess_x1 = current_princess_x1
                                        new_princess_y1 = current_princess_y1
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()
                                            if event.type == pygame.KEYDOWN:
                                                if event.key == pygame.K_w:
                                                    if princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, current_princess_x1 - 2, current_princess_y1):
                                                        new_princess_x1 -= 2
                                                        princess1["direction"] = "UP"
                                                if event.key == pygame.K_s:
                                                    if princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, current_princess_x1 + 2, current_princess_y1):
                                                        new_princess_x1 += 2
                                                        princess1["direction"] = "DOWN"
                                                if event.key == pygame.K_a:
                                                    if princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, current_princess_x1, current_princess_y1 - 2):
                                                        new_princess_y1 -= 2
                                                        princess1["direction"] = "LEFT"
                                                if event.key == pygame.K_d:
                                                    if princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, current_princess_x1, current_princess_y1 + 2):
                                                        new_princess_y1 += 2
                                                        princess1["direction"] = "RIGHT" 
                                                if (event.key==pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d):
                                                    if current_princess_x1 != new_princess_x1 or current_princess_y1 != new_princess_y1:
                                                        princess_character1.move_VS(new_princess_x1, new_princess_y1, window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 1)
                                                if (event.key==pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d):
                                                    isEnd1 = updateEnemyPosition_VS(window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, princess_character1, princess_character2, ghost_character1, ghost_character2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 1)
                                            if (isEnd1<=1 and isStop):
                                                isEnd2 = 2
                                                t.join()
                                                graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, losestate_vs, winstate_vs)
                                                isOver = True
                                                break
                                            if (isEnd1==2):
                                                stop_flag = True
                                                if not isStop:
                                                    t.join()
                                                    graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, winstate_vs, losestate_vs)
                                                    isOver = True
                                                    break
                                            if (isEnd1==2 and isStop):
                                                t.join()
                                                graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, drawstate_vs, drawstate_vs)
                                                isOver = True
                                                break
                   
                    if event.type == pygame.KEYDOWN and isEnd1==0 and isEnd2==0:
                        if event.key == pygame.K_UP:
                            if princess_character2.isEligibleMove(game2.maze, current_princess_x2, current_princess_y2, current_princess_x2 - 2, current_princess_y2):
                                new_princess_x2 -= 2
                                princess2["direction"] = "UP"
                        if event.key == pygame.K_DOWN:
                            if princess_character2.isEligibleMove(game2.maze, current_princess_x2, current_princess_y2, current_princess_x2 + 2, current_princess_y2):
                                new_princess_x2 += 2
                                princess2["direction"] = "DOWN"
                        if event.key == pygame.K_LEFT:
                            if princess_character2.isEligibleMove(game2.maze, current_princess_x2, current_princess_y2, current_princess_x2, current_princess_y2 - 2):
                                new_princess_y2 -= 2
                                princess2["direction"] = "LEFT"
                        if event.key == pygame.K_RIGHT:
                            if princess_character2.isEligibleMove(game2.maze, current_princess_x2, current_princess_y2, current_princess_x2, current_princess_y2 + 2):
                                new_princess_y2 += 2
                                princess2["direction"] = "RIGHT" 
                        if event.key == pygame.K_w:
                            if princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, current_princess_x1 - 2, current_princess_y1):
                                new_princess_x1 -= 2
                                princess1["direction"] = "UP"
                        if event.key == pygame.K_s:
                            if princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, current_princess_x1 + 2, current_princess_y1):
                                new_princess_x1 += 2
                                princess1["direction"] = "DOWN"
                        if event.key == pygame.K_a:
                            if princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, current_princess_x1, current_princess_y1 - 2):
                                new_princess_y1 -= 2
                                princess1["direction"] = "LEFT"
                        if event.key == pygame.K_d:
                            if princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, current_princess_x1, current_princess_y1 + 2):
                                new_princess_y1 += 2
                                princess1["direction"] = "RIGHT" 
                        if not princess_character1.isEligibleMove(game1.maze, current_princess_x1, current_princess_y1, new_princess_x1, new_princess_y1):
                            continue
                        if not princess_character2.isEligibleMove(game2.maze, current_princess_x2, current_princess_y2, new_princess_x2, new_princess_y2):
                            continue
                        if (event.key==pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                            if current_princess_x2 != new_princess_x2 or current_princess_y2 != new_princess_y2:
                                princess_character2.move_VS(new_princess_x2, new_princess_y2, window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 2)
                        else:
                            if (event.key==pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d):
                                if current_princess_x1 != new_princess_x1 or current_princess_y1 != new_princess_y1:
                                    princess_character1.move_VS(new_princess_x1, new_princess_y1, window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 1)
                        if (event.key==pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                            isEnd2 = updateEnemyPosition_VS(window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, princess_character1, princess_character2, ghost_character1, ghost_character2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 2)
                        else:
                            if (event.key==pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d):
                                isEnd1 = updateEnemyPosition_VS(window, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, princess_character1, princess_character2, ghost_character1, ghost_character2, list_ghost1, list_ghost2, ghostattack, new_param1, new_param2, 1)
                        if (isEnd1==1 or isEnd2==2):
                            graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, losestate_vs, winstate_vs)
                        else:
                            if (isEnd1==2 or isEnd2==1):
                                graphics.raiseVS(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2, winstate_vs, losestate_vs)
                        #break
            if new_param1["switchIsOn"]:
                new_param["switchIsOn"]=True
                graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        cursor_pos = pygame.mouse.get_pos()
                        for bt in bt_algo:
                            if bt.isClicked(cursor_pos):
                                bt.getImg().set_alpha(255)
                                algo_choosen1 = bt.name
                                for bt in bt_algo:
                                    if bt.name!=algo_choosen1:
                                        bt.getImg().set_alpha(255 * fadeOut)
                        for bt in bt_algo2:
                            if bt.isClicked(cursor_pos):
                                bt.getImg().set_alpha(255)
                                algo_choosen2 = bt.name
                                for bt in bt_algo2:
                                    if bt.name!=algo_choosen2:
                                        bt.getImg().set_alpha(255 * fadeOut)
                        pygame.display.update()
                        for bt in bt_vs:
                            if bt.isClicked(cursor_pos):
                                if bt.name == bt_vs_dic[0]:
                                    newGame_VS(mapname)
                                if bt.name == bt_vs_dic[1]:
                                    window = pygame.display.set_mode((game.screen_size_x, game.screen_size_y))
                                    graphics.drawLevel(window, game, background, bt_map, text_select_maze)
                                    click=False
                                    while not click:
                                        graphics.drawLevel(window, game, background, bt_map, text_select_maze)
                                        cursor_pos = pygame.mouse.get_pos()
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                for bt in bt_map:
                                                    if bt.isClicked(cursor_pos):
                                                        mapname = bt.name
                                                        cursor_pos = (0, 0)
                                                        window = pygame.display.set_mode((1200,700))
                                                        newGame_VS(mapname)
                                                        graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                                                        click=True
                                                        break
                                        clock.tick(30)
                                        pygame.display.update()
                                if bt.name == bt_vs_dic[2]:
                                    solveGame_VS(algo_choosen1, algo_choosen2)   
                        if switch_off.isClicked(cursor_pos):
                            if (new_param1["switchIsOn"]):
                                new_param1["switchIsOn"]=False
                                graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                                pygame.display.update()
                            else:
                                new_param1["switchIsOn"]=True
                                graphics.drawVersus(window, game1, game2, bgr_versus, floor, gate,  wall, princess1, list_ghost1, princess2, list_ghost2, ghostattack, new_param1, new_param2)
                                pygame.display.update()
  
            pygame.display.update()
            clock.tick(30)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
project_path = os.getcwd()
maze_path = os.path.join(project_path, "maze")
mapname="map10_3.txt"
runGame()