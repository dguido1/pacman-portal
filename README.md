
![logo](https://user-images.githubusercontent.com/47490318/134833056-d6ec6eac-8ae2-4772-b731-7140d8325937.png)
# Pacman Portal
  
### A twist on the original Pacman allowing the use of portals

#### &nbsp;&nbsp;&nbsp;&nbsp;Made by David Guido (@dguido1)
<br/>&nbsp;&nbsp;&nbsp;&nbsp;Built with [Pygame](https://www.pygame.org/news), an open source game engine
<br> &nbsp;&nbsp;&nbsp;&nbsp;For CPSC 386 (Introduction to Game Design and Production) at [***California State University Fullerton***](http://www.fullerton.edu/)<br><br>&nbsp;&nbsp;&nbsp;&nbsp;Spring 20'

***

## Table of contents
- [Pacman Portal](#pacman-portal)
  - [Controls](#controls)
  - [Demo](#demo)
  - [Development](#development)
    - [Map](#map)
    - [Player Movement](#player-movement)
    - [Enemy Pathfinding](#enemy-pathfinding)

***

## Controls 
- **W** to move the player **up**
- **D** to move the player **right**
- **S** to move the player **down**
- **A** to move the player **left**
- **P** to set down a **portal**

***

## Demo

#### Note: This is the state of the game at final submission (March 11, 2020 - ***All features finished!***)

![pac-portal](https://user-images.githubusercontent.com/47490318/134831676-c563ef8b-3c11-473d-a37e-aca184fadb42.gif)
<br>

***

## Development

### Map
- Two early sketches of the Pacman map/grid: <br><br>
![grid](https://user-images.githubusercontent.com/47490318/135906393-6550f25c-f04b-494d-b56e-d3592181a60b.png)
  - A minimum of 64 nodes are required for a Pacman implementation <br><br>

### Player Movement
- Player moving between nodes 0, 1, 6 and 7 <br><br>
![ezgif com-gif-maker(3)](https://user-images.githubusercontent.com/47490318/135908367-ad0e3bdc-87f3-44e1-9155-c7854bc42cce.gif)

<br>

### Enemy Pathfinding

#### A Star Algorithm

- *"**Dijkstra’s Algorithm** works well to find the shortest path, but it **wastes time exploring in directions that aren’t promising**. **Greedy Best First Search** explores in promising directions but it **may not find the shortest path**"*
- *"The **A Algorithm** uses both the **actual distance from the start** and the **estimated distance to the goal**"* <br><br>
  ![ezgif com-gif-maker(1)](https://user-images.githubusercontent.com/47490318/135904741-a4ecfdc6-30ff-4436-8410-332e43de57ec.gif) <br>

```python
frontier = PriorityQueue()
frontier.put(start, 0)
came_from = dict()
cost_so_far = dict()
came_from[start] = None
cost_so_far[start] = 0

while not frontier.empty():
   current = frontier.get()

   if current == goal:
      break
   
   for next in graph.neighbors(current):
      new_cost = cost_so_far[current] + graph.cost(current, next)
      if next not in cost_so_far or new_cost < cost_so_far[next]:
         cost_so_far[next] = new_cost
         priority = new_cost + heuristic(goal, next)
         frontier.put(next, priority)
         came_from[next] = current
```

For more information on the A-Star Algorithm check out Red Blob Games: <br> https://www.redblobgames.com/pathfinding/a-star/introduction.html <br><br>

***

<br/>
Thanks for reading!<br/><br/>
 
If you like what you see give this repo  
a star and share it with your friends.

Your support is greatly appreciated!<br/><br/>

<br/><br/>
