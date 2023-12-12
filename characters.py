import pygame
import graphics

class Character: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def isEligibleMove(self, maze, x, y, new_x, new_y): 
        if new_x < 1 or new_x >= len(maze)-1 or new_y < 1 or new_y >= len(maze)-1:
            return False 
        elif x + 2 == new_x:
            if maze[x+1][y] == "%":
                return False
        elif x - 2 == new_x:
            if maze[x-1][y] == "%":
                return False
        elif y + 2 == new_y:
            if maze[x][y+1] == "%":
                return False
        elif y - 2 == new_y:
            if maze[x][y-1] == "%":
                return False
        return True
    
    def moveAmination(self, x, y, screen, game, background, border, floor, gate, wall, princess, ghost, ghostattack, new_param):
        raise NotImplementedError("error")
    def moveAmination_VS(self, x, y, screen, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, ghost1, ghost2, ghostattack, new_param1, new_param2, player):
        raise NotImplementedError("error")

    def move(self, new_x, new_y, screen, game, background, border, floor, gate, wall, princess, ghost, ghostattack, new_param):
        self.moveAmination(new_x, new_y, screen, game, background, border, floor, gate, wall, princess, ghost, ghostattack, new_param)
        self.x = new_x
        self.y = new_y
    def move_VS(self, new_x, new_y, screen, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, ghost1, ghost2, ghostattack, new_param1, new_param2, player):
        self.moveAmination_VS(new_x, new_y, screen, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, ghost1, ghost2, ghostattack, new_param1, new_param2, player)
        self.x = new_x
        self.y = new_y
    
    def moveXY(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def checkSamePosition(self, Character):
        return (Character.x == self.x) and (Character.y == self.y)
    
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    
class Princess(Character):
    def moveAmination(self, x, y, screen, game, background, border, floor, gate, wall, princess, ghost, ghostattack, new_param):
        princess_start_x = game.coordinate_map_x + game.cell_width * (self.y // 2)
        princess_start_y = game.coordinate_map_y + game.cell_width * (self.x // 2)
        princess["coordinates"] = [princess_start_x, princess_start_y]
        step_stride = game.cell_width // 3
        coordinates = list(princess["coordinates"])
        for i in range(3):
            if princess["direction"] == "UP":
                coordinates[1] -= step_stride
            if princess["direction"] == "DOWN":
                coordinates[1] += step_stride
            if princess["direction"] == "LEFT":
                coordinates[0] -= step_stride
            if princess["direction"] == "RIGHT":
                coordinates[0] += step_stride
            princess["coordinates"] = list(coordinates)
            princess["cellIndex"] = i % 3
            graphics.drawScreen(screen, game, background, border, floor, gate, wall, princess, ghost, ghostattack, new_param)
            pygame.display.update()
            pygame.time.delay(30)
    def moveAmination_VS(self, x, y, screen, game1, game2, bgr_versus, floor, gate, wall, princess1, princess2, ghost1, ghost2, ghostattack, new_param1, new_param2, player):
        if player==1:
            princess_start_x = game1.coordinate_map_x + game1.cell_width * (self.y // 2)
            princess_start_y = game1.coordinate_map_y + game1.cell_width * (self.x // 2)
            princess1["coordinates"] = [princess_start_x, princess_start_y]
        else:
            princess_start_x = game2.coordinate_map_x + game2.cell_width * (self.y // 2)
            princess_start_y = game2.coordinate_map_y + game2.cell_width * (self.x // 2)
            princess2["coordinates"] = [princess_start_x, princess_start_y]
        step_stride = game1.cell_width // 3
        if player==1:
            coordinates = list(princess1["coordinates"])
        else:
            coordinates = list(princess2["coordinates"])
        for i in range(3):
            if player==1:
                if princess1["direction"] == "UP":
                    coordinates[1] -= step_stride
                if princess1["direction"] == "DOWN":
                    coordinates[1] += step_stride
                if princess1["direction"] == "LEFT":
                    coordinates[0] -= step_stride
                if princess1["direction"] == "RIGHT":
                    coordinates[0] += step_stride
                princess1["coordinates"] = list(coordinates)
                princess1["cellIndex"] = i % 3
            else:
                if princess2["direction"] == "UP":
                    coordinates[1] -= step_stride
                if princess2["direction"] == "DOWN":
                    coordinates[1] += step_stride
                if princess2["direction"] == "LEFT":
                    coordinates[0] -= step_stride
                if princess2["direction"] == "RIGHT":
                    coordinates[0] += step_stride
                princess2["coordinates"] = list(coordinates)
                princess2["cellIndex"] = i % 3
            graphics.drawVersus(screen, game1, game2, bgr_versus, floor, gate,  wall, princess1, ghost1, princess2, ghost2, ghostattack, new_param1, new_param2)       
            pygame.display.update()
            pygame.time.delay(10)
            
class Ghost(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def moveVertical(self, maze, princess):
        new_x = self.getX() + 2 * sign(princess.getX() - self.getX())
        new_y = self.getY()
        if self.isEligibleMove(maze, self.getX(), self.getY(), new_x, new_y):
            self.moveXY(new_x, new_y)
            return self
        else: 
            return self

    def moveHorizontal(self, maze, princess):
        new_x = self.getX()
        new_y = self.getY() + 2 * sign(princess.getY() - self.getY())
        if self.isEligibleMove(maze, self.getX(), self.getY(), new_x, new_y):
            self.moveXY(new_x, new_y)
            return (self, True)
        else: 
            return (self, False)
    
    def move(self, maze, princess):
        isMoved = False
        if self.checkSamePosition(princess):
            return self
        else:
            if self.getY() != princess.getY():
                self, isMoved = self.moveHorizontal(maze, princess) 
            if self.checkSamePosition(princess):
                return self
            if isMoved: 
                return self   
            else:
                self = self.moveVertical(maze, princess)
            if (self.checkSamePosition(princess)):
                return self
        return self
    
def sign(x):
    if x == 0:
        return x
    else:
        return x // abs(x)            