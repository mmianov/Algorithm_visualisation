# **Algorithm visualisation**

Pygame algorithm visualisation tool, currently supporting A* Path Finding algorithm.

It allows user to see an algorithm in work as it progresses towards finding the path between two points. 

**How to use the program:**

- create start and end points (first **two clicks** of the left mouse button)
- put barriers on the grid to make path finding a bit more interesting (click the **left** mouse button)
- start the algorithm (press **Space**)
- delete start point, end point or a barrier (click the **right** mouse button)
- reset the barrier (press **R**)
- reset the whole grid (press **C**)

**Note**: algorithm can move diagonally and calculates the F cost based on Diagonal Distance. It also won't start until both start and end points are placed.

# Requirements 

- Python 3.9
- Pygame

# How it looks

**A Star Path Finding Algorithm:**

![A* Path Finding GIF](https://github.com/mmianov/Algorithm_visualisation/blob/mmianov/dev/img/path_finding_for_docs.gif)



# Acknowledgements

This program was made for educational purposes and with the help of:

-  https://www.youtube.com/c/TechWithTim/videos 

    The cornerstone of this project, his tutorials helped a ton with both algorithm visualisation and its implementation

- https://www.growingwiththeweb.com/2012/06/a-pathfinding-algorithm.html

  Very helpful article describing ways of calculating the F cost.

- http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html

  A great article to grasp a basic understanding of search algorithms 
  
Feel free to fork the repository or copy the code if you want to try it yourself and/or build additional features on top of it.  


