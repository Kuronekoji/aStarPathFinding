from pygame import *
from random import randint


squares = 50 # Change how many tiles are on the screen



class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = float("inf")
        self.g = float('inf')
        self.h = float("inf")
        self.came_from = None
        self.n = []
        self.wall = False

    def update(self,surface, color):
        square = Rect(self.x * (width/squares), self.y * (height/squares), width/squares - 1, height/squares - 1)
        surface.fill(Color("black"), square)
        surface.fill(color, square.inflate(-1, -1))


init()

display.set_caption("A* Visualization")

screen = display.set_mode((600, 600)) # Change Resolution of window here
screen.fill((255, 255, 255), rect=None)

width, height = display.get_surface().get_size()


def check_event(event):
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        x, y = mouse.get_pos()
        return int(y/(width/squares)), int(x/(height/squares))

def test():
    x, y = mouse.get_pos()
    return int(y / (width / squares)), int(x / (height / squares))


def lowest_f(list):
    if len(list) > 0:
        lowest = list[0]
        for i in list:
            if i.f < lowest.f:
                lowest = i
        return lowest

grid = []

for i in range(squares):
    inner = []
    for j in range(squares):
        inner.append(Spot(i, j))
    grid.append(inner)


def get_h(start, end):
    return (abs(start.x - end.x) + abs(start.y - end.y))


start = grid[0][0]
end = grid[-1][-1]
closed_set = []
open_set = [start]
path_found = False
no_path = False

for i in range(len(grid)):
    for j in range(len(grid[i])):
        a = randint(3, 10)
        if a < 5 and grid[i][j] != start and grid[i][j] != end:
            grid[i][j].wall = True


def create_path(end):
    path = []
    path.append(end.came_from)
    while True:
        current = path[-1].came_from
        if current == start:
            break

        path.append(current)
    return path

def update_screen():
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == start:
                grid[i][j].update(screen, (0, 0, 255))
            elif grid[i][j] == end:
                grid[i][j].update(screen, (255, 0, 255))
            elif grid[i][j] in open_set:
                grid[i][j].update(screen, (0, 255, 0))
            elif grid[i][j] in closed_set:
                grid[i][j].update(screen, (255, 0, 0))
            else:
                grid[i][j].update(screen, (255, 255, 255))
            if path_found:
                if grid[i][j] in create_path(end):
                    grid[i][j].update(screen, (51, 255, 255))
            if grid[i][j].wall is True:
                grid[i][j].update(screen, (0, 0, 0))

def a_star():
    global start
    global end
    global closed_set
    global open_set
    global path_found
    global no_path

    if len(open_set) > 0:

        start.g = 0
        start.f = start.g + get_h(start, end)

        current = lowest_f(open_set)

        if current == end:
            create_path(current)
            path_found = True


        open_set.remove(current)
        closed_set.append(current)

        if current.x > 0:
            if grid[current.x - 1][current.y].wall is False:
                current.n.append(grid[current.x - 1][current.y])

            if current.y > 0:
                if grid[current.x - 1][current.y - 1].wall is False:
                    if grid[current.x - 1][current.y].wall is False:
                        if grid[current.x][current.y - 1].wall is False:
                            current.n.append(grid[current.x - 1][current.y - 1])

            if current.y < squares - 1:
                if grid[current.x - 1][current.y + 1].wall is False:
                    if grid[current.x - 1][current.y].wall is False:
                        if grid[current.x][current.y + 1].wall is False:
                             current.n.append(grid[current.x - 1][current.y + 1])

        if current.x < squares - 1:
            if grid[current.x + 1][current.y].wall is False:
                current.n.append(grid[current.x + 1][current.y])

            if current.y > 0:
                if grid[current.x + 1][current.y - 1].wall is False:
                    if grid[current.x + 1][current.y].wall is False:
                        if grid[current.x][current.y - 1].wall is False:
                            current.n.append(grid[current.x + 1][current.y - 1])

            if current.y < squares - 1:
                if grid[current.x + 1][current.y + 1].wall is False:
                    if grid[current.x + 1][current.y].wall is False:
                        if grid[current.x][current.y + 1].wall is False:
                            current.n.append(grid[current.x + 1][current.y + 1])

        if current.y > 0:
            if grid[current.x][current.y - 1].wall is False:
                current.n.append(grid[current.x][current.y - 1])

        if current.y < squares - 1:
            if grid[current.x][current.y + 1].wall is False:
                current.n.append(grid[current.x][current.y + 1])


        for neighbor in current.n:
            if neighbor in closed_set:
                continue

            temp_g = current.g + 1

            if neighbor not in open_set:
                open_set.append(neighbor)

            elif temp_g >= neighbor.g:
                continue

            neighbor.g = temp_g
            neighbor.f = neighbor.g + (abs(neighbor.x - end.x) + (abs(neighbor.y - end.y)))
            neighbor.came_from = current

        update_screen()


    else:
        no_path = True
        #Add some graphics eventually




running = True
loop = False

update_screen()

walls = False

while running:
    for events in event.get():
        if events.type == MOUSEBUTTONDOWN:
            walls = True
        elif events.type == MOUSEBUTTONUP:
            walls = False
        if walls:
            print(test())
        if check_event(events) is not None:
            j, i = check_event(events)
            if grid[i][j].wall is False:
                grid[i][j].wall = True
            elif grid[i][j].wall is True:
                grid[i][j].wall = False
            update_screen()
        if events.type == QUIT:
            running = False
        elif events.type == KEYDOWN:
            if events.key == K_SPACE:
                loop = True

    if loop and not path_found and not no_path:
        a_star()

    display.flip()

