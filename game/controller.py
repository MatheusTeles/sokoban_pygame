import sys
import pygame
import utils
import objects
from pygame.locals import * 

""" Color constants. Colors are represented as RGBA tuples and defined preemptively for
    convenience. """
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (0  ,255,  0)
BLUE  = (0  ,  0,255)
DARKGRAY  = ( 60, 60, 60)
LIGHTGRAY = (185,185,185)

""" Binding for the background color. """
BACKGROUND_COLOR = BLACK

""" Binding for the game variables. 
    Window Width and Heigth are represented in pixels.
    FPS is the amount of frames per second rendered by the game. """
WINDOWWIDTH = 400
WINDOWHEIGHT = 300
FPS = 60

""" Definition of the size of the cells, necessary for rendering
    of the grid and correct sizing and spacing of the entities. 
    This section shall be revisited once game sprites are adopted."""
CELLSIZE = 25
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE) 
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

""" Maximum number of moves that can be undone by the player """
MAX_UNDOS = 5

""" Definitions of 2D directions. These are used alongside the utils.coordinates module
    to simplify calculations in a 2D plane. """
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = ( 1, 0)

""" Syntatic sugar for the typing of entities. """
CIRCLE = 0
SQUARE = 1
TRIANGLE = 2
ELLIPSE = 3

class game_controller:

    def __init__(self, window_size:tuple, caption:str):
        self.entities = []
        self.game_state = {}
        pygame.init()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        self.BIGFONT = pygame.font.Font('freesansbold.ttf', 72)
        self.surface = pygame.display.set_mode(window_size)
        pygame.display.set_caption(caption)
        self.fps_clock = pygame.time.Clock()

    def assign_player(self, entity):
        """ Assigns an object to be the player object (Probably bad design).
            Player objects are a separate variable, and do not stay in the 
            entity list. """
        self.player = entity

    def draw_loop(self):
        """ Draws the game in layers (as per function names). """        
        self.draw_background()        
        self.draw_map()
        self.draw_entity(self.player)
        for entity in self.entities:
            self.draw_entity(entity)

    def draw_background(self):
        """ Function for drawing the background. Simply floodfills the surface
            with a solid color defined by the constant BACKGROUND_COLOR. """
        self.surface.fill(BACKGROUND_COLOR)

    def draw_map(self):
        """ Function for drawing the map. In the future, there will be tilemaps
            in here. """
        for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
            pygame.draw.line(self.surface, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
            pygame.draw.line(self.surface, DARKGRAY, (0, y), (WINDOWWIDTH, y))

    def draw_entity(self, entity:objects.game_object):
        """ Draws an entity of the game depending on its type. """
        if entity.type == CIRCLE:
            pygame.draw.circle(self.surface,
                            entity.color, 
                            utils.coordinate_sum(
                                self.grid_to_pixel(entity.pos),
                                (int(CELLSIZE/2), int(CELLSIZE/2))), 
                            int(CELLSIZE/2))
        elif entity.type == SQUARE:
            pygame.draw.rect(entity.surface, 
                                entity.color,
                                (*self.grid_to_pixel(entity.pos), CELLSIZE, CELLSIZE))

    def tick(self):
        """ Unused. """
        for entity in self.entities:
            entity.tick()

    def pixel_to_grid(self, pos:tuple) -> tuple:
        """ Convert pixel coordinates to grid coordinates.
            grid_coords = pixel_coords / CELLSIZE """
        return (utils.coordinate_scalar_div(pos, CELLSIZE))

    def grid_to_pixel(self, pos:tuple) -> tuple:
        """ Convert grid coordinates to pixel coordinates. 
            pixel_coords = grid_coords * CELLSIZE """
        return (utils.coordinate_scalar_mult(pos, CELLSIZE))

    def create_text_objects(self, text:str, font:pygame.font.Font, color:tuple):
        """ Creates a text surface to be drawn in the game 
            with the given text, font and color. """
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def create_text_screen(self, text:str, subtext:str = None):
        """ Function for the main screen of the game. Receives string variables
            for the main (bigger) text and the subtext (smaller). Subtext is optional. """
        title_surface, title_rect = self.create_text_objects(text, self.BIGFONT, LIGHTGRAY)
        title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        self.surface.blit(title_surface, title_rect)

        title_surface, title_rect = self.create_text_objects(text, self.BIGFONT, WHITE)
        title_rect.center = (int(WINDOWWIDTH / 2 - 3), int(WINDOWHEIGHT / 2 - 3))
        self.surface.blit(title_surface, title_rect)
        
        if subtext:
            subtext_surface, subtext_rect = self.create_text_objects(subtext, self.BASICFONT, WHITE)
            subtext_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
            self.surface.blit(subtext_surface, subtext_rect)

    def start(self):
        """ Creates and references game entities.
            Player object will be stored in the self.player variable.
            Other entities will be grouped in the self.entities list. """
        player = objects.ball(1, self.surface, CIRCLE, (5,5), WHITE)
        box1 = objects.box(2, self.surface, SQUARE, (7,7), GREEN)
        box2 = objects.box(3, self.surface, SQUARE, (8,9), GREEN)
        self.entities.append(box1)
        self.entities.append(box2)
        self.assign_player(player)
        self.game_state["MOVES_NO"] = 0
        self.game_state["MOVES"] = {"PLAYER":{}}
        for entity in self.entities:
            self.game_state["MOVES"][entity.id] = {}
        self.play()

    def play(self):
        """ Rendering of the main menu (Bad function name).
            Once the player hits Enter, the loop will stop and
            the actual game loop will start. """        
        self.draw_background()        
        self.draw_map()
        self.create_text_screen('Welcome!', subtext = 'Press Enter key to play. Press esc to quit.')
        start = False
        while not start:        
            for event in pygame.event.get(QUIT):
                self.terminate()    
            for event in pygame.event.get(KEYUP):
                if event.key == K_ESCAPE:
                    self.terminate()
                if event.key == K_RETURN:
                    start = True
            
            pygame.display.update()
            self.fps_clock.tick()

        self.game_loop()

    def game_loop(self):
        """ Game loop. 
            Draws elements, compute events and updates game state. """
        while True: # main game loop
            self.draw_loop()            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYUP:
                    if (event.key == K_UP):
                        self.move_player(UP)
                    elif (event.key == K_DOWN):
                        self.move_player(DOWN)
                    elif (event.key == K_LEFT):
                        self.move_player(LEFT)
                    elif (event.key == K_RIGHT):
                        self.move_player(RIGHT)
                    elif event.key == K_u:
                        self.undo_move()
            self.tick()
            pygame.display.update()
            self.fps_clock.tick(FPS)

    def move_player(self, direction:tuple):
        """ Updates the player object position given a direction,
            only if the movement is valid (not out-of-bounds). 
            If it collides with another entity, also checks if the entity
            can be moved. """        
        future_pos = utils.coordinate_sum(self.player.pos, direction)
        if not self.out_of_bounds(future_pos):
            self.player.pos = future_pos
            moved = True
            entity = self.collided_with_entity()
            if entity:
                future_pos = utils.coordinate_sum(direction, entity.pos)
                if not self.out_of_bounds(future_pos) and not self.is_blocked(future_pos):
                    entity.pos = future_pos
                    self.game_state["MOVES"][entity.id][self.game_state["MOVES_NO"] + 1] = direction
                else:
                    self.player.pos = utils.coordinate_sub(self.player.pos, direction)
                    moved = False
            if moved:    
                self.game_state["MOVES"]["PLAYER"][self.game_state["MOVES_NO"] + 1] = direction
                self.game_state["MOVES_NO"] += 1
                undo_limit = self.game_state["MOVES_NO"] - MAX_UNDOS
                if undo_limit in self.game_state["MOVES"]["PLAYER"].keys():
                    self.game_state["MOVES"]["PLAYER"].pop(undo_limit)

    def out_of_bounds(self, pos:tuple) -> bool:
        """ Check if the given position is out of bounds. """
        return False if 0 <= pos[0] < CELLWIDTH and 0 <= pos[1] < CELLHEIGHT else True

    def is_blocked(self, pos:tuple) -> bool:
        """ Check if the given position is already occupied by another entity. """
        for entity in self.entities:
            if pos == entity.pos:
                return True
        return False

    def collided_with_entity(self) -> objects.game_object:
        """ Checks if player collided with another entity. """
        for entity in self.entities:
            if self.player.pos == entity.pos:
                return entity
        return None

    def undo_move(self):
        """ Undoes previous moves stored in gamestate. """
        current_move = self.game_state["MOVES_NO"]
        if current_move in self.game_state["MOVES"]["PLAYER"].keys():
            self.player.pos = utils.coordinate_sub(self.player.pos, self.game_state["MOVES"]["PLAYER"].pop(current_move))
            for entity in self.entities:
                if current_move in self.game_state["MOVES"][entity.id].keys():
                    entity.pos = utils.coordinate_sub(entity.pos, self.game_state["MOVES"][entity.id].pop(current_move))
            if current_move > 0:
                self.game_state["MOVES_NO"] -= 1    
        
    def terminate(self):
        """ Functions for smoothly ending the game. """
        pygame.quit()
        sys.exit()

def main():
    """ Main function. Instances and starts the game. """
    g = game_controller((WINDOWWIDTH , WINDOWHEIGHT), 'Teste')
    g.start()


if __name__ == "__main__":
    main()