import pygame
from threading import Thread
import algorithm
import time
class AlgoThread(Thread):
    def __init__(self, name, x, y, screen, blank, game):
        super().__init__()
        self.name=name
        self.x=x
        self.y=y
        self.screen=screen
        self.blank=blank
        self.game=game
        self.stop=False
    def run(self):
        if (self.stop):
            return
        start_time = time.time()
        if(self.name=="bfs"):
            path, visualize_node, visited =algorithm.BFS(self.game.maze, self.game.princess_position, self.game.ghost_position)
        if(self.name=="dfs"):
            path, visualize_node, visited =algorithm.DFS(self.game.maze, self.game.princess_position, self.game.ghost_position)
        if(self.name=="ids"):
            path, visualize_node, visited =algorithm.IDS(self.game.maze, self.game.princess_position, self.game.ghost_position)
        if(self.name=="ucs"):
            path, visualize_node, visited =algorithm.UCS(self.game.maze, self.game.princess_position, self.game.ghost_position)
        if(self.name=="greedy"):
            path, visualize_node, visited =algorithm.Greedy(self.game.maze, self.game.princess_position, self.game.ghost_position, self.game.gate_position)
        if(self.name=="astar"):
            path, visualize_node, visited =algorithm.A_star(self.game.maze, self.game.princess_position, self.game.ghost_position, self.game.gate_position)
        end_time = time.time()
        execution_time = end_time - start_time
        if (self.stop):
            return
        lb_time = Label(str("{:.3f}".format(execution_time))+"s", "black")
        self.screen.blit(self.blank, (self.x+128, self.y+52))
        lb_time.draw(self.screen, self.x+128+10, self.y+52+5)
        pygame.display.update()
        
        for i in range(0, visited+1, visited//20):
            if (self.stop):
                return
            lb_state =Label(str(i), "black")
            self.screen.blit(self.blank, (self.x+128, self.y+86))
            lb_state.draw(self.screen, self.x+128+10, self.y+86+5)
            pygame.display.update()
            pygame.time.delay(20)
        lb_state =Label(str(visited), "black")
        self.screen.blit(self.blank, (self.x+128, self.y+86))
        lb_state.draw(self.screen, self.x+128+10, self.y+86+5)
        pygame.display.update()
        
        for i in range(len(visualize_node)+1):
            if (self.stop):
                return
            lb_node =Label(str(i)+"/"+str(self.game.maze_size**2), "black")
            self.screen.blit(self.blank, (self.x+128, self.y+120))
            lb_node.draw(self.screen, self.x+128+10, self.y+120+5)
            pygame.display.update()
            pygame.time.delay(1000//len(visualize_node))
        lb_node =Label(str(len(visualize_node))+"/"+str(self.game.maze_size**2), "black")
        self.screen.blit(self.blank, (self.x+128, self.y+120))
        lb_node.draw(self.screen, self.x+128+10, self.y+120+5)
        pygame.display.update()
            
        for i in range(len(path)+1):
            if (self.stop):
                return
            lb_node =Label(str(i), "black")
            self.screen.blit(self.blank, (self.x+128, self.y+154))
            lb_node.draw(self.screen, self.x+128+10, self.y+154+5)
            pygame.display.update()
            pygame.time.delay(1000//len(path))
    def stopThread(self):
        self.stop=True
        

class Character_SpiteSheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rows = 4
        self.cols = 3
        self.totalCell = self.rows * self.cols

        self.rect = self.sheet.get_rect()   #return kich thuoc
        w = self.cellWidth = self.rect.width / self.cols
        h = self.cellHeight = self.rect.height / self.rows

        self.cells = list()
        for y in range(self.rows):
            for x in range(self.cols):
                self.cells.append([x * w, y * h, w, h])
    def draw(self, surface, x, y, cellIndex, direction):
        if direction == "UP":
            pass
        if direction == "RIGHT":
            cellIndex = cellIndex + 3
        if direction == "DOWN":
            cellIndex = cellIndex + 6
        if direction == "LEFT":
            cellIndex = cellIndex + 9
        surface.blit(self.sheet, (x, y), self.cells[cellIndex])

class Wall_SpriteSheet:
    def __init__(self, image_spritesheet_path, maze_size):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.left_wall = []
        self.right_wall =[]
        self.up_wall = []
        if maze_size == 6:
            self.left_wall = [0, 0, 12, 78]
            self.right_wall = [84, 0, 12, 78]
            self.up_wall = [12, 0, 72, 18]
            self.up_wall_no_shadow = [12, 0, 66, 18]
        elif maze_size == 8:
            self.left_wall = [0, 2, 9, 58]
            self.right_wall = [63, 2, 9, 58]
            self.up_wall = [9, 0, 54, 12]
            self.up_wall_no_shadow = [9, 0, 49, 12]
        elif maze_size == 10:
            self.left_wall = [0, 1, 7, 47]
            self.right_wall = [51, 1, 7, 47]
            self.up_wall = [8, 0, 43, 11]
            self.up_wall_no_shadow = [8, 0, 39, 11]

    def drawLeftWall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.left_wall)

    def drawRightWall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.right_wall)

    def drawUpWall(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.up_wall)

    def drawUpWallNoShadow(self, surface, x, y):
        surface.blit(self.sheet, (x, y), self.up_wall_no_shadow)


class Gate_SpriteSheet:
    def __init__(self, image_spritesheet_path):
        self.sheet = pygame.image.load(image_spritesheet_path)
        self.rect = self.sheet.get_rect()
        self.cell_w = self.rect.width // 4
        self.cell_h = self.rect.height
        # UP, RIGHT, DOWN, LEFT = (0, 1, 2, 3)
        self.gates = []
        for x in range(4):
            self.gates.append([x * self.cell_w, 0, self.cell_w, self.cell_h])
    def draw(self, surface, x, y, cellIndex):
        surface.blit(self.sheet, (x, y), self.gates[cellIndex])

class Button():
    def __init__(self, image_path, name=None):
        self.img = pygame.image.load(image_path)
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        if name!=None:
            self.name = name
        
    def draw(self, surface, x, y):
        self.x = x 
        self.y = y
        self.rect.topleft = (x, y)
        surface.blit(self.img, (x, y))
    
    def isClicked(self, cursor_pos):
        return self.rect.collidepoint(cursor_pos) and self.mask.get_at((cursor_pos[0] - self.x, cursor_pos[1] - self.y))
        
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setImg(self, imgpath):
        self.img = pygame.image.load(imgpath)
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getImg(self):
        return self.img
class Label():
    def __init__(self, text, color, size=None):
        if size==None:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = pygame.font.Font(None, size)
        self.color = color
        self.textsurface = self.font.render(text, 1, pygame.Color(self.color))
        
    def draw(self, surface, x, y):
        self.x = x 
        self.y = y 
        surface.blit(self.textsurface, (self.x, self.y))
    
    def updateText(self, text):
        self.textsurface = self.font.render(text, 1, pygame.Color(self.color))
def drawWelcome(screen, welcome_background, bt_start, bt_versus):
    screen.blit(welcome_background, (0, 0))
    bt_x = 250 
    bt_y = 270
    bt_start.draw(screen, bt_x, bt_y)
    font = pygame.font.Font(None, 40)
    text = font.render("START", True, (247,162,0))
    screen.blit(text, (bt_x+105,bt_y+27))
    
    bt_versus.draw(screen, bt_x, bt_y+90)
    font = pygame.font.Font(None, 40)
    text = font.render("VERSUS", True, (247,162,0))
    screen.blit(text, (bt_x+93,bt_y+27+90))

def drawGuide(screen, game, background, border, floor, gate,  wall, princess, ghost, ghostattack, new_param, guide_background, bt_exit):
    drawScreen(screen, game, background, border, floor, gate,  wall, princess, ghost, ghostattack, new_param)  
    background_x = 80
    background_y = 50
    screen.blit(guide_background, (background_x, background_y))
    font = pygame.font.Font(None, 14)
    font = pygame.font.SysFont("TimesNewRoman", 14)

    lines = [
        "Once upon a time, there was a beautiful princess who lived in a grand castle.",
        "She always loved the Halloween festival and all the exciting things it brought.",
        "This year, however, while she was out wandering, a wicked witch had evil plans.",
        "She had lured the princess away from her castle and cast a spell on her, teleporting her to a mysterious, never-ending maze.",
        "The princess was scared and confused, unsure of where she was or what it was",
        "As she wandered the maze, she could sense a strange, ghostly creature lurking in the dark.",
        "Just when the princess thought she was doomed, she heard a tinkling sound coming from the sky, her beloved guardian fairy, coming for her rescue.",
        "The litte fairy friend guide her owner step by step, using following buttons: \u2190\u2191\u2192\u2193. And beware little friends, deadend might be your owner grave.",
        "                                                                                          ",
        "                                                                                          ",
        "                                                                                          ",
        "                                                                                          "
        "Souless ghost hungry for hundread years, striking at full speed, moving twice as the princess. But they seems to prefer moving HORIZONTALLY than VERTICALLY"
    ]
    y_offset = 0
    
    scrollwidth = 450
    for line in lines:
        words = line.split()
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            test_width, _ = font.size(test_line)
            if test_width > scrollwidth:
                text = font.render(current_line, True, (0, 0, 0))
                screen.blit(text, (background_x + 95, background_y + 60 + y_offset))
                y_offset += 15
                current_line = word + ' '
            else:
                current_line = test_line
        
        text = font.render(current_line, True, (0, 0, 0))
        screen.blit(text, (background_x + 95, background_y + 60 + y_offset))
        y_offset += 15
    bt_exit.draw(screen, 630, 70)  
    pygame.display.update()
    
def drawLevel(screen, game, background, bt_map, text_select_maze):
    screen.blit(background, (0, 0))
    screen.blit(text_select_maze, (0, 0))
    bt_x = 10
    bt_y = 120
    font = pygame.font.Font(None, 40)
    for index, bt in enumerate(bt_map):
        bt.draw(screen, bt_x, bt_y)
        text = font.render(str(index+1), True, (0,0,0))
        if index<9:
            screen.blit(text, (bt_x+32,bt_y+27))
        else:
            screen.blit(text, (bt_x+25,bt_y+27))
        bt_x+=80+20
        if (index%8==7):
            bt_x=10
            bt_y+=100

def drawScreen(screen, game, background, border, floor, gate,  wall, princess, ghost, ghostattack, new_param):
    coordinate_X = 380
    coordinate_Y = 114
    screen.blit(background, (0, 0))
    screen.blit(border, (340, 85))
    screen.blit(floor, (coordinate_X, coordinate_Y))
    #draw gate
    gate_px = game.gate_position[1] // 2
    gate_py = game.gate_position[0] // 2
    gate_x = coordinate_X + game.cell_width * (gate_px)
    gate_y = coordinate_Y + game.cell_width * (gate_py)
    #UP
    gate_index = 0
        #RIGHT
    if (gate_px == game.maze_size and game.gate_position[0] > 0 and game.gate_position[0] < 2 * game.maze_size):
        gate_index = 1
        #LEFT
    elif (gate_px == 0 and game.gate_position[0] > 0 and game.gate_position[0] < 2 * game.maze_size):
        gate_index = 3
        #DOWN
    elif (gate_py == game.maze_size and game.gate_position[1] > 0 and game.gate_position[1] < 2 * game.maze_size):
        gate_index = 2
    if (gate_index == 0):
        gate_y = coordinate_Y - gate.cell_h
    if (gate_index == 3):
        gate_x = coordinate_X - gate.cell_w
    gate.draw(screen, gate_x, gate_y, gate_index)
    # vusualize
    if (new_param["switchIsOn"]):
        if (new_param["visualize_node"]!=None):
            for node in new_param["visualize_node"]:
                x = coordinate_X + game.cell_width * (node[1] // 2)
                y = coordinate_Y + game.cell_width * (node[0] // 2)
                if (game.maze_size==6):
                    x+=25
                    y+=25
                if (game.maze_size==8):
                    x+=17
                    y+=17
                if (game.maze_size==10):
                    x+=13
                    y+=13
                if (x, y)!=princess["coordinates"]:
                    screen.blit(new_param["reddot"], (x, y))
    if new_param["isDead"]==False:
        # draw princess
        if princess["coordinates"]:
            princess["sprite_sheet"].draw(screen, princess["coordinates"][0], princess["coordinates"][1], princess["cellIndex"], princess["direction"])
        # draw ghost
        for i in range(len(ghost)):
            ghost[i]["sprite_sheet"].draw(screen, ghost[i]["coordinates"][0], ghost[i]["coordinates"][1], ghost[i]["cellIndex"], ghost[i]["direction"])
    else:
        screen.blit(ghostattack, new_param["dead_coord"])
        #pygame.display.update()
    # draw wall
    # ngang
    for i in range(0, len(game.maze)-1, 2):
        for j in range(1, len(game.maze[i]), 2):
            if game.maze[i][j] == "%":
                wall_x = coordinate_X + game.cell_width * (j // 2)
                wall_y = coordinate_Y + game.cell_width * (i // 2)
                if game.maze_size == 6:
                    wall_x -= 6
                    wall_y -= 12
                if game.maze_size == 8:
                    wall_x -= 4
                    wall_y -= 9
                if game.maze_size == 10:
                    wall_x -= 3
                    wall_y -= 7
                wall.drawUpWall(screen, wall_x, wall_y)
    # dọc
    for j in range(0, len(game.maze), 2):
        for i in range(1, len(game.maze[j]), 2):
            if game.maze[i][j] == "%":
                wall_x = coordinate_X + game.cell_width * (j // 2)
                wall_y = coordinate_Y + game.cell_width * (i // 2)
                if game.maze_size == 6:
                    wall_x -= 6
                    wall_y -= 12
                if game.maze_size == 8:
                    wall_x -= 4
                    wall_y -= 9
                if game.maze_size == 10:
                    wall_x -= 3
                    wall_y -= 7
                if (j<len(game.maze)-1 and game.maze[i+1][j+1] == "%"):
                    wall.drawRightWall(screen, wall_x, wall_y)
                    redraw_x = coordinate_X + game.cell_width * ((j+1) // 2)
                    redraw_y = coordinate_Y + game.cell_width * ((i+1) // 2)
                    if game.maze_size == 6:
                        redraw_x -= 6
                        redraw_y -= 12
                    if game.maze_size == 8:
                        redraw_x -= 4
                        redraw_y -= 9
                    if game.maze_size == 10:
                        redraw_x -= 3
                        redraw_y -= 7
                    if (i + 1 < game.maze_size * 2 and j + 1 < game.maze_size * 2):
                        wall.drawUpWallNoShadow(screen, redraw_x, redraw_y)
                    # if (i==len(game.maze[j])-2 and j==0):
                    #     wall.drawUpWall(screen, redraw_x, redraw_y)
                else:
                    wall.drawLeftWall(screen, wall_x, wall_y)
    # ngang cuối
    for j in range(1, len(game.maze), 2):
        if game.maze[len(game.maze)-1][j] == "%":
            wall_x = coordinate_X + game.cell_width * (j // 2)
            wall_y = coordinate_Y + game.cell_width * ((len(game.maze)-1) // 2)
            if game.maze_size == 6:
                wall_x -= 6
                wall_y -= 12
            if game.maze_size == 8:
                wall_x -= 4
                wall_y -= 9
            if game.maze_size == 10:
                wall_x -= 3
                wall_y -= 7
            wall.drawUpWall(screen, wall_x, wall_y)
                    
    # button  
    if new_param["switchIsOn"]:
        new_param["switch_on"].draw(screen, 300, 20)
    else:
        new_param["switch_off"].draw(screen, 300, 20)
    if not new_param["isAlgoSelecting"]:
        bt_landmark_x = 50 
        bt_landmark_y = 100
        for index, bt in enumerate(new_param["bt_main"]):
            bt.draw(screen, bt_landmark_x, bt_landmark_y+index*80)    
    #thêm        
    list_algo = ["BFS","DFS","IDS","UCS","GREEDY","A*"]
    if new_param["isAlgoSelecting"]:
        bt_algo_landmark_x = 50
        bt_algo_landmark_y = 110
        new_param["bt_back"].draw(screen, bt_algo_landmark_x, bt_algo_landmark_y )
        bt_algo_landmark_x +=15
        bt_algo_landmark_y += 80
        font = pygame.font.Font(None, 24)
        for index, bt in enumerate(new_param["bt_algo"]):
            text = font.render(list_algo[index], True, (0,0,0))
            if index % 2 == 0 and index!=4: 
                bt.draw(screen, bt_algo_landmark_x , bt_algo_landmark_y )
                screen.blit(text, (bt_algo_landmark_x + 35, bt_algo_landmark_y + 13))
            elif index==4:
                bt.draw(screen, bt_algo_landmark_x , bt_algo_landmark_y )
                screen.blit(text, (bt_algo_landmark_x + 16, bt_algo_landmark_y + 13))
            elif index==5:
                bt.draw(screen, bt_algo_landmark_x + 120, bt_algo_landmark_y)
                screen.blit(text, (bt_algo_landmark_x + 165, bt_algo_landmark_y + 13)) 
            else:
                bt.draw(screen, bt_algo_landmark_x + 120, bt_algo_landmark_y)
                screen.blit(text, (bt_algo_landmark_x + 155, bt_algo_landmark_y + 13))
                bt_algo_landmark_y+=80 
    # label
    label_landmark_x = 150
    label_landmark_y = 20
    for index, label in enumerate(new_param["label_main"]):
        if index % 2 != 0: 
            label.draw(screen, label_landmark_x , label_landmark_y + 40)  
        else:
            label_landmark_x += 250
            label.draw(screen, label_landmark_x , label_landmark_y ) 

    font = pygame.font.Font(None, 30)
    text = font.render("Visualize", True, "Yellow")
    screen.blit(text, (200, 23))

def drawVersus(screen, game1, game2, background, floor, gate,  wall, princess1, ghost1, princess2, ghost2, ghostattack, new_param1, new_param2):
    coordinate_X1 = 84
    coordinate_Y1 = 135
    coordinate_X2 = 753
    coordinate_Y2 = 135
    screen.blit(background, (0, 0))
    #sửa
    if not new_param1["switchIsOn"] and not new_param1["isPlayervsAI"]:
        screen.blit(new_param1["guide_key"],(0, 0))
    #thêm
    if not new_param1["switchIsOn"] and new_param1["isPlayervsAI"]: 
        crop_rect = pygame.Rect(0, 500, 400, 200)
        screen.blit(new_param1["guide_key"].subsurface(crop_rect), (0, 500))
    screen.blit(floor, (coordinate_X1 , coordinate_Y1))
    screen.blit(floor, (coordinate_X2, coordinate_Y2))

    #draw gate
    gate_px = game1.gate_position[1] // 2
    gate_py = game1.gate_position[0] // 2
    global gate_x1, gate_y1, gate_x2, gate_y2
    gate_x1 = coordinate_X1 + game1.cell_width * (gate_px)
    gate_y1 = coordinate_Y1 + game1.cell_width * (gate_py)
    gate_x2 = coordinate_X2 + game1.cell_width * (gate_px)
    gate_y2 = coordinate_Y2 + game1.cell_width * (gate_py)
    #UP
    gate_index = 0
        #RIGHT
    if (gate_px == game1.maze_size and game1.gate_position[0] > 0 and game1.gate_position[0] < 2 * game1.maze_size):
        gate_index = 1
        #LEFT
    elif (gate_px == 0 and game1.gate_position[0] > 0 and game1.gate_position[0] < 2 * game1.maze_size):
        gate_index = 3
        #DOWN
    elif (gate_py == game1.maze_size and game1.gate_position[1] > 0 and game1.gate_position[1] < 2 * game1.maze_size):
        gate_index = 2
    if (gate_index == 0):
        gate_y1 = coordinate_Y1 - gate.cell_h
        gate_y2 = coordinate_Y2 - gate.cell_h
    if (gate_index == 3):
        gate_x1 = coordinate_X1 - gate.cell_w
        gate_x2 = coordinate_X2 - gate.cell_w
    gate.draw(screen, gate_x1, gate_y1, gate_index)
    gate.draw(screen, gate_x2, gate_y2, gate_index)

    if new_param1["isDead"]==False:
        # draw princess
        if princess1["coordinates"]:
            princess1["sprite_sheet"].draw(screen, princess1["coordinates"][0], princess1["coordinates"][1], princess1["cellIndex"], princess1["direction"])
        # draw ghost
        for i in range(len(ghost1)):
            ghost1[i]["sprite_sheet"].draw(screen, ghost1[i]["coordinates"][0], ghost1[i]["coordinates"][1], ghost1[i]["cellIndex"], ghost1[i]["direction"])
    else:
        screen.blit(ghostattack, new_param1["dead_coord"])
        
    if new_param2["isDead"]==False:
        # draw princess
        if princess2["coordinates"]:
            princess2["sprite_sheet"].draw(screen, princess2["coordinates"][0], princess2["coordinates"][1], princess2["cellIndex"], princess2["direction"])
        # draw ghost
        for i in range(len(ghost2)):
            ghost2[i]["sprite_sheet"].draw(screen, ghost2[i]["coordinates"][0], ghost2[i]["coordinates"][1], ghost2[i]["cellIndex"], ghost2[i]["direction"])
    else:
        screen.blit(ghostattack, new_param2["dead_coord"])
        #pygame.display.update()
    # draw wall
    # ngang
    for i in range(0, len(game1.maze)-1, 2):
        for j in range(1, len(game1.maze[i]), 2):
            if game1.maze[i][j] == "%":
                wall_x1 = coordinate_X1 + game1.cell_width * (j // 2)
                wall_y1 = coordinate_Y1 + game1.cell_width * (i // 2)
                wall_x2 = coordinate_X2 + game1.cell_width * (j // 2)
                wall_y2 = coordinate_Y2 + game1.cell_width * (i // 2)
                if game1.maze_size == 6:
                    wall_x1 -= 6
                    wall_y1 -= 12
                    wall_x2 -= 6
                    wall_y2 -= 12
                if game1.maze_size == 8:
                    wall_x1 -= 4
                    wall_y1 -= 9
                    wall_x2 -= 4
                    wall_y2 -= 9
                if game1.maze_size == 10:
                    wall_x1 -= 3
                    wall_y1 -= 7
                    wall_x2 -= 3
                    wall_y2 -= 7
                wall.drawUpWall(screen, wall_x1, wall_y1)
                wall.drawUpWall(screen, wall_x2, wall_y2)
    # dọc
    for j in range(0, len(game1.maze), 2):
        for i in range(1, len(game1.maze[j]), 2):
            if game1.maze[i][j] == "%":
                wall_x1 = coordinate_X1 + game1.cell_width * (j // 2)
                wall_y1 = coordinate_Y1 + game1.cell_width * (i // 2)
                wall_x2 = coordinate_X2 + game1.cell_width * (j // 2)
                wall_y2 = coordinate_Y2 + game1.cell_width * (i // 2)
                if game1.maze_size == 6:
                    wall_x1 -= 6
                    wall_y1 -= 12
                    wall_x2 -= 6
                    wall_y2 -= 12
                if game1.maze_size == 8:
                    wall_x1 -= 4
                    wall_y1 -= 9
                    wall_x2 -= 4
                    wall_y2 -= 9
                if game1.maze_size == 10:
                    wall_x1 -= 3
                    wall_y1 -= 7
                    wall_x2 -= 3
                    wall_y2 -= 7
                if (j<len(game1.maze)-1 and game1.maze[i+1][j+1] == "%"):
                    wall.drawRightWall(screen, wall_x1, wall_y1)
                    wall.drawRightWall(screen, wall_x2, wall_y2)
                    redraw_x1 = coordinate_X1 + game1.cell_width * ((j+1) // 2)
                    redraw_y1 = coordinate_Y1 + game1.cell_width * ((i+1) // 2)
                    redraw_x2 = coordinate_X2 + game1.cell_width * ((j+1) // 2)
                    redraw_y2 = coordinate_Y2 + game1.cell_width * ((i+1) // 2)
                    if game1.maze_size == 6:
                        redraw_x1 -= 6
                        redraw_y1 -= 12
                        redraw_x2 -= 6
                        redraw_y2 -= 12
                    if game1.maze_size == 8:
                        redraw_x1 -= 4
                        redraw_y1 -= 9
                        redraw_x2 -= 4
                        redraw_y2 -= 9
                    if game1.maze_size == 10:
                        redraw_x1 -= 3
                        redraw_y1 -= 7
                        redraw_x2 -= 3
                        redraw_y2 -= 7
                    if (i + 1 < game1.maze_size * 2 and j + 1 < game1.maze_size * 2):
                        wall.drawUpWallNoShadow(screen, redraw_x1, redraw_y1)
                        wall.drawUpWallNoShadow(screen, redraw_x2, redraw_y2)
                    # if (i==len(game.maze[j])-2 and j==0):
                    #     wall.drawUpWall(screen, redraw_x, redraw_y)
                else:
                    wall.drawLeftWall(screen, wall_x1, wall_y1)
                    wall.drawLeftWall(screen, wall_x2, wall_y2)
    # ngang cuối
    for j in range(1, len(game1.maze), 2):
        if game1.maze[len(game1.maze)-1][j] == "%":
            wall_x1 = coordinate_X1 + game1.cell_width * (j // 2)
            wall_y1 = coordinate_Y1 + game1.cell_width * ((len(game1.maze)-1) // 2)
            wall_x2 = coordinate_X2 + game1.cell_width * (j // 2)
            wall_y2 = coordinate_Y2 + game1.cell_width * ((len(game1.maze)-1) // 2)
            if game1.maze_size == 6:
                wall_x1 -= 6
                wall_y1 -= 12
                wall_x2 -= 6
                wall_y2 -= 12
            if game1.maze_size == 8:
                wall_x1 -= 4
                wall_y1 -= 9
                wall_x2 -= 4
                wall_y2 -= 9
            if game1.maze_size == 10:
                wall_x1 -= 3
                wall_y1 -= 7
                wall_x2 -= 3
                wall_y2 -= 7
            wall.drawUpWall(screen, wall_x1, wall_y1)
            wall.drawUpWall(screen, wall_x2, wall_y2)
    # button                
    if new_param1["switchIsOn"]:
        new_param1["switch_on"].draw(screen, 598, 54)
    else:
        new_param1["switch_off"].draw(screen, 598, 54)
    
    # bt_landmark_x = 500 
    # bt_landmark_y = 180
    # for index, bt in enumerate(new_param1["bt_vs"]):
    #     bt.draw(screen, bt_landmark_x, bt_landmark_y+index*70) 
    
    #thêm
    if not new_param1["isPlayervsAI"] and not new_param1["switchIsOn"]:
        font = pygame.font.Font(None, 25)
        text = font.render("AI", True, "Black")
        new_param1["bt_switchplayer"].draw(screen, 750, 597)
        screen.blit(text, (790, 610))
    if  new_param1["isPlayervsAI"] and not new_param1["switchIsOn"]: 
        font = pygame.font.Font(None, 25)
        text = font.render("Human", True, "Black")
        new_param1["bt_switchplayer"].draw(screen, 630, 525)
        screen.blit(text, (650, 535))
        bt_algo_landmark_x = 760
        bt_algo_landmark_y = 525
        list_algo = ["BFS","DFS","IDS","UCS","GREEDY","A*"]
        for index, bt in enumerate(new_param2["bt_algo"]):
            text = font.render(list_algo[index], True, (0,0,0))
            if index % 2 == 0 and index!=4: 
                bt.draw(screen, bt_algo_landmark_x , bt_algo_landmark_y )
                screen.blit(text, (bt_algo_landmark_x + 35, bt_algo_landmark_y + 13))
            elif index==4:
                bt.draw(screen, bt_algo_landmark_x + 240, bt_algo_landmark_y - 160)
                screen.blit(text, (bt_algo_landmark_x + 16 + 240, bt_algo_landmark_y + 13 - 160))
            elif index==5:
                bt.draw(screen, bt_algo_landmark_x + 240, bt_algo_landmark_y - 80)
                screen.blit(text, (bt_algo_landmark_x + 165 + 120, bt_algo_landmark_y + 13 - 80)) 
            else:
                bt.draw(screen, bt_algo_landmark_x + 120, bt_algo_landmark_y)
                screen.blit(text, (bt_algo_landmark_x + 155, bt_algo_landmark_y + 13))
                bt_algo_landmark_y+=80
        bt_landmark_x = 500 
        bt_landmark_y = 180        
        font = pygame.font.Font(None, 30)
        list_vs = ["RESTART", "MAP", "START"]
        for index, bt in enumerate(new_param1["bt_vs"]):
            text = font.render(list_vs[index], True, "Yellow")
            bt.draw(screen, bt_landmark_x, bt_landmark_y+index*70) 
            if (index==0):
                screen.blit(text, (bt_landmark_x + 55, bt_landmark_y+index*70+20))
            if (index==1):
                screen.blit(text, (bt_landmark_x + 55 + 20, bt_landmark_y+index*70+20))
            if (index==2):
                screen.blit(text, (bt_landmark_x + 55 + 13, bt_landmark_y+index*70+20))
    
            
    bt_landmark_x = 500 
    bt_landmark_y = 180
    font = pygame.font.Font(None, 30)
    list_vs = ["RESTART", "MAP", "START"]
    for index, bt in enumerate(new_param1["bt_vs"]):
        text = font.render(list_vs[index], True, "Yellow")
        if not new_param1["switchIsOn"]:
            if index==2:
                continue
            bt.draw(screen, bt_landmark_x, bt_landmark_y+index*70) 
            if (index==0):
                screen.blit(text, (bt_landmark_x + 55, bt_landmark_y+index*70+20))
            if (index==1):
                screen.blit(text, (bt_landmark_x + 55 + 20, bt_landmark_y+index*70+20))
        else:
            bt.draw(screen, bt_landmark_x, bt_landmark_y+index*70) 
            if (index==0):
                screen.blit(text, (bt_landmark_x + 55, bt_landmark_y+index*70+20))
            if (index==1):
                screen.blit(text, (bt_landmark_x + 55 + 20, bt_landmark_y+index*70+20))
            if (index==2):
                screen.blit(text, (bt_landmark_x + 55 + 13, bt_landmark_y+index*70+20))

            
    if new_param1["switchIsOn"]:
        list_algo = ["BFS","DFS","IDS","UCS","GREEDY","A*"]
        bt_algo_landmark_x = 90
        bt_algo_landmark_y = 525
        font = pygame.font.Font(None, 24)
        for index, bt in enumerate(new_param1["bt_algo"]):
            text = font.render(list_algo[index], True, (0,0,0))
            if index % 2 == 0 and index!=4: 
                bt.draw(screen, bt_algo_landmark_x , bt_algo_landmark_y )
                screen.blit(text, (bt_algo_landmark_x + 35, bt_algo_landmark_y + 13))
            elif index==4:
                bt.draw(screen, bt_algo_landmark_x + 240, bt_algo_landmark_y - 160)
                screen.blit(text, (bt_algo_landmark_x + 16 + 240, bt_algo_landmark_y + 13 - 160))
            elif index==5:
                bt.draw(screen, bt_algo_landmark_x + 240, bt_algo_landmark_y - 80)
                screen.blit(text, (bt_algo_landmark_x + 165 + 120, bt_algo_landmark_y + 13 - 80)) 
            else:
                bt.draw(screen, bt_algo_landmark_x + 120, bt_algo_landmark_y)
                screen.blit(text, (bt_algo_landmark_x + 155, bt_algo_landmark_y + 13))
                bt_algo_landmark_y+=80 
        bt_algo_landmark_x = 760
        bt_algo_landmark_y = 525
        for index, bt in enumerate(new_param2["bt_algo"]):
            text = font.render(list_algo[index], True, (0,0,0))
            if index % 2 == 0 and index!=4: 
                bt.draw(screen, bt_algo_landmark_x , bt_algo_landmark_y )
                screen.blit(text, (bt_algo_landmark_x + 35, bt_algo_landmark_y + 13))
            elif index==4:
                bt.draw(screen, bt_algo_landmark_x + 240, bt_algo_landmark_y - 160)
                screen.blit(text, (bt_algo_landmark_x + 16 + 240, bt_algo_landmark_y + 13 - 160))
            elif index==5:
                bt.draw(screen, bt_algo_landmark_x + 240, bt_algo_landmark_y - 80)
                screen.blit(text, (bt_algo_landmark_x + 165 + 120, bt_algo_landmark_y + 13 - 80)) 
            else:
                bt.draw(screen, bt_algo_landmark_x + 120, bt_algo_landmark_y)
                screen.blit(text, (bt_algo_landmark_x + 155, bt_algo_landmark_y + 13))
                bt_algo_landmark_y+=80

def visualize(screen, game, reddot, visualize_node):
    coordinate_X = 380
    coordinate_Y = 114
    for node in visualize_node:
        x = coordinate_X + game.cell_width * (node[1] // 2)
        y = coordinate_Y + game.cell_width * (node[0] // 2)
        if (game.maze_size==6):
            x+=25
            y+=25
        if (game.maze_size==8):
            x+=17
            y+=17
        if (game.maze_size==10):
            x+=13
            y+=13
        screen.blit(reddot, (x, y))
        pygame.time.delay(50)
        pygame.display.update()
        
def raiseSign(screen, game, background, border, floor, gate,  wall, princess, ghost, ghostattack, new_param, sign):
    start_x=412
    start_y=-200
    while start_y<0:
        start_y+=5
        drawScreen(screen, game, background, border, floor, gate,  wall, princess, ghost, ghostattack, new_param)
        screen.blit(sign, (start_x, start_y))
        screen.blit(new_param["close"], (start_x+230, start_y+155))
        pygame.time.delay(5)
        pygame.display.update()

def raiseVS(screen, game1, game2, background, floor, gate,  wall, princess1, ghost1, princess2, ghost2, ghostattack, new_param1, new_param2, s1, s2):
    if s1!=s2:
        start_x=71
        start_y=700
        while start_y>517:
            start_y-=5
            drawVersus(screen, game1, game2, background, floor, gate,  wall, princess1, ghost1, princess2, ghost2, ghostattack, new_param1, new_param2)       
            screen.blit(s1, (start_x, start_y))
            screen.blit(s2, (749, start_y))
            pygame.time.delay(5)
            pygame.display.update()
    else:
        start_x=404
        start_y=700
        while start_y>400:
            start_y-=5
            drawVersus(screen, game1, game2, background, floor, gate,  wall, princess1, ghost1, princess2, ghost2, ghostattack, new_param1, new_param2)       
            screen.blit(s1, (start_x, start_y))
            pygame.time.delay(5)
            pygame.display.update()


def getMovingDirection(past_position, new_position):
    if past_position[0] == new_position[0] + 2:
        return "UP"
    if past_position[0] == new_position[0] - 2:
        return "DOWN"
    if past_position[1] == new_position[1] + 2:
        return "LEFT"
    if past_position[1] == new_position[1] - 2:
        return "RIGHT"

def enemyMoveAnimation(ghost_past_position, ghost_new_position, screen, game, background, border, floor, gate,  wall, princess, ghost, ghostattack, new_param):
    
    ghost_check_movement = [False for _ in range(len(ghost_past_position))]

    ghost_start_coordinate = []
    for i in range(len(ghost_past_position)):
        ghost_start_x = game.coordinate_map_x + game.cell_width * (ghost_past_position[i][1] // 2)
        ghost_start_y = game.coordinate_map_y + game.cell_width * (ghost_past_position[i][0] // 2)
        if game.maze[ghost_new_position[i][0] - 1][ghost_new_position[i][1]] == "%":
            ghost_start_y += 3
        ghost_start_coordinate.append([ghost_start_x, ghost_start_y])
        if ghost_past_position[i][0] != ghost_new_position[i][0] or ghost_past_position[i][1] != ghost_new_position[i][1]:
            ghost_check_movement[i] = True
        if ghost_check_movement[i]:
            ghost[i]["direction"] = getMovingDirection(ghost_past_position[i], ghost_new_position[i])

    step_stride = game.cell_width // 3
    for i in range(len(ghost)):
        ghost[i]["coordinates"] = ghost_start_coordinate[i]

    for i in range(3):
        for j in range(len(ghost)):
                if ghost[j]["direction"] == "UP" and ghost_check_movement[j]:
                    ghost[j]["coordinates"][1] -= step_stride
                if ghost[j]["direction"] == "DOWN" and ghost_check_movement[j]:
                    ghost[j]["coordinates"][1] += step_stride
                if ghost[j]["direction"] == "LEFT" and ghost_check_movement[j]:
                    ghost[j]["coordinates"][0] -= step_stride
                if ghost[j]["direction"] == "RIGHT" and ghost_check_movement[j]:
                    ghost[j]["coordinates"][0] += step_stride
                if ghost_check_movement[j]:
                    ghost[j]["cellIndex"] = i % 3
                    
        drawScreen(screen, game, background, border, floor, gate, wall, princess, ghost, ghostattack, new_param)
        pygame.display.update()
        pygame.time.delay(30)
        
def enemyMoveAnimation_VS(ghost_past_position, ghost_new_position, screen, game1, game2, background, floor, gate,  wall, princess1, ghost1, princess2, ghost2, ghostattack, new_param1, new_param2, player):
    ghost_check_movement = [False for _ in range(len(ghost_past_position))]
    ghost_start_coordinate = []
    for i in range(len(ghost_past_position)):
        if player==1:
            ghost_start_x = game1.coordinate_map_x + game1.cell_width * (ghost_past_position[i][1] // 2)
            ghost_start_y = game1.coordinate_map_y + game1.cell_width * (ghost_past_position[i][0] // 2)
            if game1.maze[ghost_new_position[i][0] - 1][ghost_new_position[i][1]] == "%":
                ghost_start_y += 3
        else:
            ghost_start_x = game2.coordinate_map_x + game1.cell_width * (ghost_past_position[i][1] // 2)
            ghost_start_y = game2.coordinate_map_y + game1.cell_width * (ghost_past_position[i][0] // 2)
            if game2.maze[ghost_new_position[i][0] - 1][ghost_new_position[i][1]] == "%":
                ghost_start_y += 3
        ghost_start_coordinate.append([ghost_start_x, ghost_start_y])
        if ghost_past_position[i][0] != ghost_new_position[i][0] or ghost_past_position[i][1] != ghost_new_position[i][1]:
            ghost_check_movement[i] = True
        if ghost_check_movement[i]:
            if player==1:
                ghost1[i]["direction"] = getMovingDirection(ghost_past_position[i], ghost_new_position[i])
            else:
                ghost2[i]["direction"] = getMovingDirection(ghost_past_position[i], ghost_new_position[i])   

    step_stride = game1.cell_width // 3
    if player==1:
        for i in range(len(ghost1)):
            ghost1[i]["coordinates"] = ghost_start_coordinate[i]
    else:
        for i in range(len(ghost2)):
            ghost2[i]["coordinates"] = ghost_start_coordinate[i]

    for i in range(3):
        if player==1:
            for j in range(len(ghost1)):
                    if ghost1[j]["direction"] == "UP" and ghost_check_movement[j]:
                        ghost1[j]["coordinates"][1] -= step_stride
                    if ghost1[j]["direction"] == "DOWN" and ghost_check_movement[j]:
                        ghost1[j]["coordinates"][1] += step_stride
                    if ghost1[j]["direction"] == "LEFT" and ghost_check_movement[j]:
                        ghost1[j]["coordinates"][0] -= step_stride
                    if ghost1[j]["direction"] == "RIGHT" and ghost_check_movement[j]:
                        ghost1[j]["coordinates"][0] += step_stride
                    if ghost_check_movement[j]:
                        ghost1[j]["cellIndex"] = i % 3
        else:
            for j in range(len(ghost2)):
                    if ghost2[j]["direction"] == "UP" and ghost_check_movement[j]:
                        ghost2[j]["coordinates"][1] -= step_stride
                    if ghost2[j]["direction"] == "DOWN" and ghost_check_movement[j]:
                        ghost2[j]["coordinates"][1] += step_stride
                    if ghost2[j]["direction"] == "LEFT" and ghost_check_movement[j]:
                        ghost2[j]["coordinates"][0] -= step_stride
                    if ghost2[j]["direction"] == "RIGHT" and ghost_check_movement[j]:
                        ghost2[j]["coordinates"][0] += step_stride
                    if ghost_check_movement[j]:
                        ghost2[j]["cellIndex"] = i % 3
                    
        drawVersus(screen, game1, game2, background, floor, gate,  wall, princess1, ghost1, princess2, ghost2, ghostattack, new_param1, new_param2)       
        pygame.display.update()
        pygame.time.delay(10)
