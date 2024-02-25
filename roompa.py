from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

matrix1 = [
  [1, 1, 1, 1, 1, 1],   #we can move  on 1 but not on 0 tile
  [1, 0, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1]]

grid=Grid( matrix=matrix1)  #Grid class requires a binary matrix  

start=grid.node(0,0) #here (0,0) represents the matrix1[0][0] i.e 1
end=grid.node(5,2)  #here it is matrix1[2][5]

#finder with a movement style
finder=AStarFinder()

# using the finder

path,runs=finder.find_path(start,end,grid)        #return the path and return how manby cells was needed to reach the end cell
# print(path)

print([(node.x, node.y) for node in path])
