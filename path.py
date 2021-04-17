import pygame

import blocks as b

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# node representation -> block
class  Block:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        
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
    
    def update_neighbours(self):
        pass

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
# and draw_grid_lines() to draw grid lines
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


def main(win):
    ROWS = 20
    grid = make_grid(ROWS)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
            if started:
                continue

            # reset obstacle when R pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    for row in grid:
                        for block in row:
                            if block.color == b.BLACK:
                                block.reset()

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
            

    pygame.quit()

main(WIN)



