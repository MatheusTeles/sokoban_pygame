class game_object:
    def __init__(self, id:int, surface, type:int, pos:tuple, color:tuple):
        self.id = id
        self.surface = surface
        self.type = type
        self.pos = pos
        self.color = color
    def draw_self(self, surface):
        pass
    def tick(self):
        pass

class ball(game_object):
    def __init__(self, id:int, surface, type:int , pos:tuple, color:tuple):
        super().__init__(id, surface, type, pos, color)        

class box(game_object):
    def __init__(self, id:int, surface, type:int, pos:tuple, color:tuple):
        super().__init__(id, surface, type, pos, color)
