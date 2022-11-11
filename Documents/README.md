# Mario Kart 12
https://bunardsheng.github.io/site/marioElements.html

2.5D Graphics
-------------
In order to achieve a psuedo-3D feel, isometric concepts were applied in order to create a multi-dimensional map. First, a polygon was drawn based on a given slope and it's endpoints, followed by connecting rectangles that created a three-dimensional cube. Gouraud shading was applied to each polygon. The points were passed in from a 2D list, and each block was removed and newly appended based on a set bounds.

2D Elastic Collisions
----------------------
Fundamental physics collisions were applied in order to achieve a sense of realism. The player's current x and y location are calculated on impact, and their new velocity values are given based on the following equation.

v2f = ( ( (2 * m1) / (m2+m1) ) * v1o ) + ( (m2-m1) / (m2+m1) ) * v2o
v1f = ( (m1-m2) / (m2+m1 ) * v1o ) + ( (2 * m2) / (m2+m1) ) * v2o

Item Creation
--------------
Red Shell: travels towards the nearest player based on an updating dictionary of AI locations.
Bullet Bill: increases current speed to a player's max speed + 10.
Mushroom: increases current speed by a value of 5, results in a slight deceleration for 1.5s.
