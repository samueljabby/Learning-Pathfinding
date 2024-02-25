import pygame
import sys
pygame.init()


window_width=600
window_height=600

window=pygame.display.set_mode((window_width,window_height))
clock=pygame.time.Clock()

columns=30
rows=30

box_width=window_width//columns
box_height=window_height//rows

grid=[]
queue=[]
path=[]

class Box:
    def __init__(self,i,j):
        self.x=i
        self.y=j
        self.start=False
        self.wall=False
        self.target=False
        self.queued=False
        self.visited=False
        self.neighbours=[]
        self.prior=None

    def draw(self,win,color):
        pygame.draw.rect(win,color,(self.x*box_width,self.y*box_height,box_width-2,box_height-2))

    def set_neighbours(self):  #this will set the boxes as neighbours by putting themm in the neighbours list
        # sets the horizontal boxes
        if self.x>0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x<columns-1:
            self.neighbours.append(grid[self.x + 1][self.y])
        # sets the vertical boxes
        if self.y>0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y<rows-1:
            self.neighbours.append(grid[self.x][self.y + 1])
            


# create a grid
for i in range(columns):     #Box ka ek instance bana ke grid mein daal diya 
    arr=[]                      # aur wo instances ko dusre loop ke use se  draw kar diya 
    for j in range(rows):
        arr.append(Box(i,j))
    grid.append(arr)

#setting neighbours          #make all the boxes in the grid as neighbours
for i in range(columns):
    for j in range (rows):
        grid[i][j].set_neighbours()

#the origin box
start_box=grid[0][0]
start_box.start=True
start_box.visited=True
queue.append(start_box)

def main():
    begin_search=False
    target_box_set=False
    searching=True
    target_box=None
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEMOTION:
                x=pygame.mouse.get_pos()[0]
                y=pygame.mouse.get_pos()[1]
                   #seeting the walls
                   
                if event.buttons[0]:      #left mouse if clicked
                    i=x//box_width
                    j=y//box_height
                    grid[i][j].wall=True
                  #setting the target
                if event.buttons[2] :
                    # x_pos=pygame.mouse.get_pos()[0]
                    # y_pos=pygame.mouse.get_pos()[1]
                    i=x//box_width
                    j=y//box_height
                    target_box=grid[i][j]
                    target_box.target=True
                    target_box_set=True
            if event.type==pygame.KEYDOWN and target_box_set:
                begin_search=True
                



        if begin_search:
            if len(queue)>0 and searching:
                current_box=queue.pop(0)
                current_box.visited=True
                if current_box==target_box:
                    searching=False
                    while current_box.prior!=start_box:
                        path.append(current_box.prior)
                        current_box=current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued=True
                            neighbour.prior=current_box
                            queue.append(neighbour)
            else:
                if searching:
                    print("NO SOLUTION AVAILABLE")
                    searching=False


            #drwawing the boxes
        for i in range(columns):
            for j in range(rows):
                box=grid[i][j]
                box.draw(window,("gray"))
                if box.queued:
                    box.draw(window,("black"))
                if box.visited:
                    box.draw(window,("white"))
                if box in path:
                    box.draw(window,"gold")
                if box.start:
                    box.draw(window,("red"))
                if box.wall:
                    box.draw(window,("red"))
                if box.target:
                    box.draw(window,("green"))

        pygame.display.flip()
        clock.tick(60)

main()