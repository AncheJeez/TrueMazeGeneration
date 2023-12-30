import pygame as pg
import random
from .settings import *
from .sprites import Wall, Path, Boundary_wall

class Maze:

    def __init__(self, game, screen, clock):
        self.game = game
        self.screen = screen
        self.clock = clock

        # we create a new 2d vector to store the walls 32 x 24
        self.maze_grid = [[0 for x in range(int(GRIDWIDTH))] for y in range(int(GRIDHEIGHT))]
        #self.maze_grid = [[1] * int(GRIDWIDTH) for _ in range(int(GRIDHEIGHT))]

        self.create_maze()

        # test feature to check if well stored
        for row in self.maze_grid:
            print(row)

    def draw(self):
        self.draw_grid()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def create_maze(self):
        self.create_border_walls()
        self.create_perfect_maze()
        self.create_wall_objects()

    def create_border_walls(self):
        # horizontal
        for x in range(0, int(GRIDWIDTH)):
            self.maze_grid[0][x] = 3
            self.maze_grid[int(GRIDHEIGHT)-1][x] = 3
        # vertical
        for y in range(1, int(GRIDHEIGHT)-1):
            self.maze_grid[y][0] = 3
            self.maze_grid[y][int(GRIDWIDTH)-1] = 3

    def create_perfect_maze(self):
        # Initialize the maze with walls
        for x in range(1,int(GRIDWIDTH)-1):
            for y in range(1,int(GRIDHEIGHT)-1):
                if x % 2 == 0 and y % 2 == 0:
                    self.maze_grid[y][x] = 1

        stack = [(1, 1)]
        visited = {(1, 1)}

        self.recursive_backtracking(stack, visited)

        for x in range(1,int(GRIDWIDTH)):
            for y in range(1,int(GRIDHEIGHT)):
                if self.maze_grid[y][x] == 0:
                    self.maze_grid[y][x] = 1
        
        #self.make_it_spicier()

    def recursive_backtracking(self, stack, visited):
        
        while stack:
            print("Stack: ",stack[-1],", actual size: ",len(stack))
            x, y = stack[-1]
            stack.pop()

            neighbors = [(x + dx, y + dy) for dx, dy in [(2, 0), (0, 2), (-2, 0), (0, -2)]]
            random.shuffle(neighbors)

            for neighbor in neighbors:
                nx, ny = neighbor
                path_between = self.get_path_between((x,y),neighbor)
                bx, by = path_between
                if not self.is_out_bounds(neighbor):
                    if neighbor in visited:
                        self.maze_grid[ny][nx] = 2
                        visited.add(neighbor)
                    else:
                        visited.add(neighbor)
                        visited.add(path_between)
                        self.maze_grid[int((y + by) / 2)][int((x + bx) / 2)] = 2
                        self.maze_grid[int((y + ny) / 2)][int((x + nx) / 2)] = 2
                        stack.append(neighbor)


    def make_it_spicier(self):
        for x in range(1,int(GRIDWIDTH)):
            for y in range(1,int(GRIDHEIGHT)):
                if self.maze_grid[y][x] == 1 and random.random() < 0.2: #and not self.is_adjacent_2(self.maze_grid,x, y)
                    self.maze_grid[y][x] = 2
    
    def is_adjacent_2(self, maze, row, col):
        rows, cols = len(maze), len(maze[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 2:
                return True

        return False

    def can_move_to(self,startPos, endPos):
        ax, ay = startPos
        bx, by = endPos
        wall = (ax+(bx//2),ay+(by//2))
        if self.is_out_bounds(wall):
            return True
        if self.maze_grid[wall[1]][wall[0]] == 0:
            return True
        else:
            return False
        
    def get_path_between(self,startPos, endPos):
        ax, ay = startPos
        bx, by = endPos
        return ((ax+bx)//2,(ay+by)//2)
        
    def is_out_bounds(self, wall):
        if (0 <= wall[0] < int(GRIDWIDTH)-1 and 0 <= wall[1] < int(GRIDHEIGHT)-1):
            return False
        return True


    def create_wall_objects(self):
        for y in range(len(self.maze_grid)):
            for x in range(len(self.maze_grid[0])):
                if self.maze_grid[y][x] == 1:
                    Wall(self.game, x, y)
                elif self.maze_grid[y][x] == 2:
                    Path(self.game, x, y)
                elif self.maze_grid[y][x] == 3:
                    Boundary_wall(self.game, x, y)

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # keeping the player centered
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)