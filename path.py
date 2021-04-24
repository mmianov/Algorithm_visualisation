import pygame
import math
from queue import PriorityQueue

import blocks as b

# WIDTH OF THE WINDOW
WIDTH = 800
GRID_SIZE = {'small': 20,'medium':40,'large':80}
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# node representation -> block
class  Block:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width # width of the block
        self.total_rows = WIDTH//width
        
        self.x = col*width
        self.y = row*width
        self.color = b.WHITE
        self.neighbours = []


    def get_position(self):
        return self.row, self.col

    def is_opened(self):
        return self.color == b.GREEN
    def is_closed(self):
        return self.color == b.RED
    def is_obstacle(self):
        return self.color == b.BLACK
    def is_start(self):
        return self.color == b.ORANGE
    def is_end(self):
        return self.color == b.BLUE

    def make_open(self):
        self.color = b.GREEN
    def make_closed(self):
        self.color = b.RED
    def make_obstacle(self):
        self.color = b.BLACK
    def make_start(self):
        self.color = b.ORANGE
    def make_end(self):
        self.color = b.BLUE
    def make_path(self):
        self.color = b.PURPLE
    def reset(self):
        self.color = b.WHITE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbours(self, grid):
        self.neighbours = []
        # check if neighbour DOWN is available 
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbours.append(grid[self.row +1][self.col])

         # check if neighbour UP is available 
        if self.row > 0  and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbours.append(grid[self.row - 1][self.col])

        # check if neighbour LEFT is available 
        if self.col > 0  and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbours.append(grid[self.row][self.col - 1])

        # check if neighbour RIGHT is available 
        if self.col < self.total_rows - 1  and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbours.append(grid[self.row][self.col + 1])

        # check if neighbour DIAGONAL UP LEFT  is available 
        if self.col > 0 and self.row > 0 and not grid[self.row -1][self.col -1].is_obstacle():
             self.neighbours.append(grid[self.row -1][self.col -1])

        # check if neighbour DIAGONAL UP RIGHT  is available
        if self.col < self.total_rows -1 and self.row > 0 and not grid[self.row -1][self.col +1].is_obstacle():
             self.neighbours.append(grid[self.row -1][self.col +1])

        # check if neighbour DIAGONAL DOWN LEFT  is available
        if self.col > 0 and self.row < self.total_rows -1 and not grid[self.row + 1][self.col -1].is_obstacle():
            self.neighbours.append(grid[self.row + 1][self.col -1])
        
        # check if neighbour DIAGONAL DOWN RIGHT  is available  
        if self.col < self.total_rows -1 and self.row < self.total_rows -1 and not grid[self.row +1][self.col +1].is_obstacle():
            self.neighbours.append(grid[self.row +1][self.col +1])

       
    def __lt__(self, other):
        return False

    #debugging
    def __str__(self):
        return f"({self.row}, {self.col})"
    def __repr__(self):
        return self.__str__()


# WIDTH = GRID WIDTH 

# Creates MxM matrix as a list of lists, which contain Block objects (row, col, width) - width argument not shown below
# [ [(row1, col1),(row1, col2)  ... (row1, col m)],
#   [(row2, col1),(row2, col2)  ... (row2, col m)],
#   .
#   .
#   .
#   [(row m, col1),(row2, col2) ... (row m, col m)],
# ]

def make_grid(rows):
    block_width = WIDTH//rows
    grid = []
    # iterate over rows
    for i in range(rows):
        # make list of row-column pairs for particular row
        columns = []
        grid.append(columns)
        for j in range(rows):
            columns.append(Block(i, j, block_width))
    return grid


def draw_grid_lines(win, rows):
    block_width = WIDTH//rows
    for i in range(rows):
        #draw horizontal lines
        pygame.draw.line(win, b.GRAY, (0,i*block_width),(WIDTH,i*block_width))
        #draw vertical lines
        pygame.draw.line(win, b.GRAY, (i*block_width, 0),(i*block_width,WIDTH))


# Uses Block.draw() method to draw blocks created by make_grid()
# and draw_grid_lines() to draw grid lines - esentially upadtes the whole board
def draw(win, grid, rows):
    win.fill(b.WHITE)
    for row in grid:
        for block in row:
            block.draw(win)
    draw_grid_lines(win ,rows)
    pygame.display.update()


# Returns row and column of a block that was clicked
def get_clicked_block_pos(pos, rows):
    block_width = WIDTH//rows
    x,y = pos

    row = y // block_width
    col = x // block_width

    return row, col

def cost(p1, p2):
    # Diagonal distance
    x1, y1 = p1  
    x2, y2 = p2  

    d_max = max(abs(x1-x2),abs(y1-y2))
    d_min = min(abs(x1-x2),abs(y1-y2))
    return int((1.4*d_min + (d_max-d_min))*10)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def A_Star_Algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    ''' 
    Add start block tuple (F score, count, block) to the open set.
    PriorityQueue will look at the first objct in the tuple (F score) when called by .get() method,
    so it will choose the lowest F score block. If there are mutliple lowest scores, then it will decide
    based on the second item in the tuple (count) and will choose the one which was put first.
    '''
    start_position = start.get_position()
    end_position = end.get_position()

    # keep track of which node came from which node
    came_from = {}

    # store all of G scores - start them at infinity
    g_score = {block : float("inf") for row in grid for block in row}
    g_score[start] = 0

    # store all of F scores - start them at infinity
    f_score = {block : float("inf") for row in grid for block in row}
    f_score[start] = cost(start_position, end_position)

    # green blocks
    open_set_hash = {start}
 
    # search until all viable neigbours have been evaluated
    while not open_set.empty():
        # allow to quit a game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        '''
        What we want to do now is check all the neighbours of the current block.
        For each neighbour we will calucate its G score first and see if it is lower than
        it has been. That is to avoid a situation in which we override a block's G score with a higher one.
        '''    
        for neighbour in current.neighbours:
            neighbour_position = neighbour.get_position()
            # calculate possible G score of a neighbour
            temp_g_score = cost(start_position, neighbour_position)

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                # F score = G score + H score
                f_score[neighbour] = temp_g_score + cost(neighbour_position, end_position)
                
                if neighbour not in open_set_hash:
                    count += 1
                    # add to open_set for dealing with priority queue  
                    open_set.put((f_score[neighbour], count, neighbour))
                    # add to open_set_hash for dealing with duplicates
                    open_set_hash.add(neighbour)
                    neighbour.make_open()      

        draw()
        if current != start:
            current.make_closed()
    return False


def main(win):
    ROWS = GRID_SIZE['medium']
    grid = make_grid(ROWS)

    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
            

            # if left mouse button clicked
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_block_pos(pos, ROWS)
                block = grid[row][col]
                if not start and block != end:
                    start = block
                    start.make_start()
                elif not end and block!= start:
                    end = block 
                    end.make_end() 
                elif block != start and block != end:
                    block.make_obstacle()

            # if right mouse button clicked
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_block_pos(pos, ROWS)
                block = grid[row][col]
                block.reset()
                if block == start:
                    start = None
                elif block == end:
                    end = None
            
            
            if event.type == pygame.KEYDOWN:
                # reset obstacle when R pressed
                if event.key == pygame.K_r: 
                    for row in grid:
                        for block in row:
                            if block.color == b.BLACK:
                                block.reset()
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for block in row:
                            block.update_neighbours(grid)          
                    A_Star_Algorithm(lambda: draw(win, grid, ROWS), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS)

    pygame.quit()

main(WIN)


