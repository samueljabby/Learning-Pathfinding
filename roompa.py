import pygame,sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class Roomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("roomba.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(20,20))
        self.rect=self.image.get_rect(center=(60,60))

        self.pos=self.rect.center
        self.speed=3
        self.direction=pygame.math.Vector2(0,0)

        self.path=[]
        self.collision_rects=[]
    
    def get_cordi(self):
        col=self.rect.centerx//9
        row=self.rect.centery//9
        return [col,row]
    
    def set_path(self,path):   #helps getting shortest path genreated Pathfinder class 
        self.path=path
        self.create_collision_rect()
        self.get_direction()

    def create_collision_rect(self):  #creates  a rect at every point in the in the self.path
        if self.path:
            self.collision_rects=[]
            for points in self.path:
                x=(points[0]* 9) + 4.5
                y=(points[1]* 9) + 4.5
                rect=pygame.Rect((x-2,y-2),(4,4))  #-2 puts the cemter of the rect at center cuz its half of 4
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start=pygame.math.Vector2(self.pos)
            end=pygame.math.Vector2(self.collision_rects[0].center)
            self.direction=(end-start).normalize()    #Normalizing this vector involves converting it to a unit vector, which means it will have a magnitude of 1 while retaining the same direction
        else:
            self.direction=pygame.math.Vector2(0,0)
            self.path=[]
        
#we cant do rect.center = direction because the way vectors work  in pygame
    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()

    def update(self):
        self.pos+=self.direction*self.speed
        self.check_collisions()
        self.rect.center=self.pos

class Pathfinder:
    def __init__(self,matrix):
        
        self.matrix=matrix
        self.grid=Grid(matrix=matrix)
        self.select_surf=pygame.image.load("selection.png").convert_alpha()

        self.path=[]

        self.roomba=pygame.sprite.GroupSingle(Roomba())
    def draw_active_cell(self):
         mouse_pos=pygame.mouse.get_pos()
         row=mouse_pos[1]//9
         col=mouse_pos[0]//9
         current_cell_value=self.matrix[row][col]
         if current_cell_value:
           rect=pygame.Rect((col*9,row*9),(9,9))
           screen.blit(self.select_surf,rect)

    def create_path(self):
        #start
        start_x,start_y=self.roomba.sprite.get_cordi()      #i think sprite laga kar  hum grp ke andar jo sprite hai usko acce kar rahe hai  aur na laga ye toh error deta hai
        start=self.grid.node(start_x,start_y)
        #end 
        mouse_pos=pygame.mouse.get_pos()
        end_x,end_y=[mouse_pos[0]//9,mouse_pos[1]//9]
        end=self.grid.node(end_x,end_y)
        #path
        # finder=AStarFinder(diagonal_movement=DiagonalMovement.always)
        finder=AStarFinder()
        self.path,_=finder.find_path(start,end,self.grid)#here this doesnt gives an acuurate tuples
        self.path=[(node.x, node.y) for node in self.path]#here it converts the self,path onto tuples with cordinates
        self.grid.cleanup()           #if this line is not present the algo will run once and will retun empty list afterwards do this ensures thst doent happens
        self.roomba.sprite.set_path(self.path)  #self.path ko roomba class mein behj sakte
   
    def draw_path(self):
        if self.path:
            points=[]
            for point in self.path:
                x=(point[0]*9)+4.5#convering the box cordinates to screen cordinates
                y=(point[1]*9)+4.5
                points.append((x,y))

            pygame.draw.lines(screen,"red",False,points,2)
            

    def update(self):
        self.draw_active_cell()
        self.draw_path()

        #roombs
        self.roomba.update()
        self.roomba.draw(screen)

pygame.init()
screen=pygame.display.set_mode((396,396))
clock=pygame.time.Clock()

bg_surf=pygame.image.load("pac_map.jpeg").convert()
bg_surf=pygame.transform.scale(bg_surf,(396,396))
matrix=[
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,0,0,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,0,0,0,0,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0],
[0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,0],
[0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,0,0,0,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1,0,0,0,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


pathfinder=Pathfinder(matrix)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            pathfinder.create_path()

    screen.blit(bg_surf,(0,0))
    # pathfinder.draw_active_cell()
    pathfinder.update()

    pygame.display.update()
    clock.tick(40)
