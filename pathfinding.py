import pygame
import sys
import time
from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw() #to hide the main window
messagebox.showinfo('Info','Welcome to my a* visualization, the start is the blue square the end is the red square. To move the red square hover over a square and press \'Z\' to place walls hold left click to draw and use right click to erase them. Press \'P\' to solve the path. To clear the board press \'C\'')
#ddd
window_size = [610,610]
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
lightblue = (51,255,255)
lightbluegreen = (51,255,153)
red = (255,0,0)
blue = (0,0,255)
width = 30
height = 30
margin = 10
grid = []
start = (0,0)
end = (9,9)
gridsize = 15
#look at what the algo does next to a border can only enter the top
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(start,end):
    start = start
    endlist = end
    start_node = Node(None,start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None,endlist)
    end_node.g = end_node.h = end_node.f = 0

    openlist = []
    closedlist = []
    openlist.append(start_node)
    count = 0
    checkedlist = []
    eraseprevpath()
    start_time = time.time()
    while len(openlist) > 0 and count < (len(grid)//2)**10:
        current_node = openlist[0]
        current_index = 0
        for index,item in enumerate(openlist):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        openlist.pop(current_index)
        closedlist.append(current_node)
        if current_node == end_node:
            path = []
            current = current_node
            print("---%s seconds ---" % (time.time()-start_time))
            while current is not None:
                path.append(current.position)
                grid[current.position[0]][current.position[1]] = 4
                current = current.parent

            print("Found solution!")
            return path[::-1],checkedlist
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > len(grid)-1 or node_position[0] < 0 or node_position[1] > len(grid)-1 or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] == 1:
                continue
            if node_position[0] == start[0] and node_position[1] == start[1]:
                continue

            #make sure not travelling through "cracks" in the walls
            if new_position in[(1,1),(-1,1),(-1,-1),(1,-1)]:
                if  -1 < node_position[0]-new_position[0] < len(grid) and -1 < node_position[1]-new_position[1] < len(grid):
                    if grid[node_position[0]-new_position[0]][node_position[1]] == 1 and grid[node_position[0]][node_position[1]-new_position[1]] == 1:
                            
                            continue
            # Create new node
            new_node = Node(current_node, node_position)
            
            if node_position not in checkedlist:
                checkedlist.append(node_position)
            for closed_child in closedlist:
                if new_node.position == closed_child.position:
                    continue
            new_node.g = current_node.g + 1
            if new_node not in openlist:
                new_node.h = ((new_node.position[0]-end_node.position[0])**2)+((new_node.position[1]-end_node.position[1])**2)
                new_node.f = new_node.g + new_node.h
                openlist.append(new_node)
            for openchild in openlist:  
                if openchild == new_node and new_node.f >= openchild.f:
                    continue

        count += 1
        

def eraseprevpath():
    for row in range(len(grid)):
        for column in range(len(grid)):
            if grid[row][column] == 3 and not (row == start[0] and column == start[1]):
                grid[row][column] = 0 
            if grid[row][column] == 4:
                grid[row][column] = 0
            if row == start[0] and column == start[1]:
                grid[row][column] = 5
            if row == end[0] and column == end[1]:
                grid[row][column] = 2
def doanimation(checkedlist,data):
    eraseprevpath()
    for count,x in enumerate(checkedlist):
        count += 1
        screen.fill(black)
        grid[x[0]][x[1]] = 3
        for row in range(len(grid)):
            for column in range(len(grid)):
                color = white
                if grid[row][column] == 1:
                    color = black
                if grid[row][column] == 2:
                    color = red
                if grid[row][column] == 3 and not (row == start[0] and column == start[1]):
                    color = lightbluegreen
                if row == start[0] and column == start[1]:
                    color = blue
                if grid[row][column] == 4:
                    color = lightblue
                if row == end[0] and column == end[1]:
                    color = red
                pygame.draw.rect(screen, 
                                color,
                                [(margin+width)*column+margin,
                                (margin+height)*row+margin,
                                width,
                                height])
        pygame.display.flip()
        time.sleep(.4/count)


    for x in data:
        if not (x[0] == start[0] and x[1] == start[1]):
            grid[x[0]][x[1]] = 4
        color = white
        if grid[x[0]][x[1]] == 1:
            color = black
        if grid[x[0]][x[1]] == 2:
            color = red
        if grid[x[0]][x[1]] == 3 and not (x[0] == start[0] and x[1] == start[1]):
            color = lightbluegreen
        if x[0] == start[0] and x[1] == start[1]:
            color = blue
        if grid[x[0]][x[1]] == 4:
            color = lightblue
        if x[0] == end[0] and x[1] == end[1]:
            color = red
        pygame.draw.rect(screen, 
                        color,
                        [(margin+width)*x[1]+margin,
                        (margin+height)*x[0]+margin,
                        width,
                        height])
        pygame.display.flip()
        time.sleep(.1)
    




for row in range(gridsize):
    grid.append([])
    for column in range(gridsize):
        grid[row].append(0)

pygame.init()
screen = pygame.display.set_mode(window_size)
done = False
clock = pygame.time.Clock()
while not done:
    grid[0][0] = 5
    grid[end[0]][end[1]] = 2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (width+margin)
            row = pos[1] // (height+margin)
            if row < len(grid) and column < len(grid):
                if not (row == start[0] and column == start[1]):
                    grid[row][column] = 1
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (width+margin)
            row = pos[1] // (height+margin)
            if row < len(grid) and column < len(grid):
                if not (row == start[0] and column == start[1]):
                    grid[row][column] = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (width+margin)
                row = pos[1] // (height+margin)
                if row < len(grid) and column < len(grid):
                    grid[end[0]][end[1]] = 0
                    if not (row == start[0] and column == start[1]):
                        grid[row][column] = 2
                        end = (row,column)
                print("z key pressed")
            if event.key == pygame.K_c:
                for x in range(len(grid)):
                    for y in range(len(grid)):
                        colorid = grid[x][y]
                        if(colorid == 3 or colorid == 1 or colorid == 4):
                            grid[x][y] = 0
            if event.key == pygame.K_p:
                eraseprevpath()
                data,checkedlist = astar(start,end)
                doanimation(checkedlist,data)

    screen.fill(black)

    
    for row in range(len(grid)):
        for column in range(len(grid)):
            color = white
            if grid[row][column] == 1:
                color = black
            if grid[row][column] == 2:
                color = red
            if grid[row][column] == 3:
                color = lightbluegreen
            if grid[row][column] == 4:
                color = lightblue
            if row == start[0] and column == start[1]:
                color = blue
            if row==end[0] and column == end[1]:
                color = red
            pygame.draw.rect(screen, 
                            color,
                            [(margin+width)*column+margin,
                            (margin+height)*row+margin,
                            width,
                            height])
    clock.tick(60)
    pygame.display.flip()