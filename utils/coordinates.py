import math

def coordinate_sum(a:tuple, b:tuple) -> tuple:
    return (a[0] + b[0], a[1] + b[1])

def coordinate_sub(a:tuple, b:tuple) -> tuple:
    return (a[0] - b[0], a[1] - b[1])

def coordinate_scalar_mult(a:tuple, b:float) -> tuple:
    return (a[0] * b, a[1] * b)

def coordinate_scalar_div(a:tuple, b:float) -> tuple:
    return (a[0] / b, a[1] / b)

def coordinate_dot(a:tuple, b:tuple) -> tuple:
    return a[0] * b[0] + a[1] * b[1]

def coordinate_unitary(a:tuple) -> tuple:
    module = coordinate_module(a)
    return (a[0]/module, a[1]/module)

def coordinate_module(a:tuple) -> tuple:
    return math.sqrt(a[0] ** 2 + a[1] ** 2)

def coordinate_distance(a:tuple, b:tuple):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def coordinate_2d_grid_distance(a:tuple, b:tuple):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


"""
   0 1 2 3 4 5 6
   - - - - - - -
0 |. . . 4 5 . .        
1 |. . 4 3 4 5 X       
2 |. 4 3 2 3 4 5     
3 |4 3 2 1 2 3 4       
4 |3 2 1 X 1 2 3        
5 |4 3 2 1 2 3 4          
6 |. 4 3 2 3 4 .         
"""