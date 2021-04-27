import pygame as pg


import scenes


WIDTH, HEIGHT = 750, 750
FPS = 60

class Game:
    """This class handles initialization of the pygame object, pygame events, game updates, and pygame drawing."""

    def __init__(self):
        self.new()

    # UNMUTABLE LOOP ---------------------------------------

    def new(self):
        """
        Initialize characteristics not specific to pygame here.
        """
        self.init_game()

    def run(self):
        """
        Runs pygame.
        """
        while True:
            # ACTUAL GAME LOOP
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.render()

    # MUTABLE LOOPS ------------------------------------

    def events(self):
        """
        Catch all pygame events here.
        """
        self.active_scene.handle_events()

    def init_game(self):
        """
        Initialize pygame characteristics, programs, and attributes here.
        Iniitialize starting scene here.
        """
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.active_scene = scenes.RGBScene(self.screen)
        print('init GAME')


    def update(self):
        """
        Update active scene here.
        """
        self.active_scene.update()


    def render(self):
        """
        Render directly to the pygame window or 'screen' here.
        """
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.active_scene.render()
        pg.display.flip()


# Create game object.
g = Game()
g.run()


