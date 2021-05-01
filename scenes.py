import sys


import pygame as pg

import rgb_holder
import plane_manager
from projections import point_projection
from prisms3 import prisms


class Scene:
    # https://stackoverflow.com/a/14727074
    """Base class of scene objects."""
    def __init__(self, screen):
        self.screen = screen
        self.next = self
        self.previous = self
        self.t0 = 0
        self.font = pg.font.Font('freesansbold.ttf', 24)
        self.name_surface = self.get_scene_name_surface()
        self.init()

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def get_scene_name_surface(self):
        """
        Get the class name as a pygame surface to blit onto the screen.
            @return name of the class as a text surface
        """
        name = self.__repr__()
        name_surface = self.render_text(self.font, name)
        return name_surface

    def init(self):
        """Group initialize functions."""
        pass

    def render(self):
        """Group draw functions."""
        raise NotImplementedError

    def update(self):
        """Group update functions."""
        raise NotImplementedError

    def handle_events(self):
        """Pass pygame events to do specific things for each child class."""
        raise NotImplementedError

    def get_change_of_time(self):
        if self.t0 is not 0:
            # correct change in time, since non active scenes are not updated
            dt = time.clock() - self.t0
            self.t0 = 0
            return dt
        else:
            return 0

    def switch_to_scene(self, next_scene):
        # switch current scene to new scene
        self.next = next_scene
        # set new scene to itself
        next_scene.next = next_scene
        # set previous scene of the new scene, if the scene does not have a previous scene yet
        if next_scene.previous is next_scene:
            next_scene.previous = self
        self.t0 = time.clock()

    def switch_to_previous(self):
        self.switch_to_scene(self.previous)

    # TEXT FUNCTIONS ----------------------------------

    @staticmethod
    def render_text(font, text_list):
        """
        Renders text lines as font.render can only render 1 line of text.
            @param pygame font instance
            @param list of strings or 1 string
            @return list of pygame text surfaces or 1 pygame text surface
        """
        text_surfaces = []
        if isinstance(text_list, str):
            text_list = [text_list]
        for text in text_list:
            text_surfaces.append(font.render(text, True, (255, 255, 255)))
        return text_surfaces

    @staticmethod
    def blit_text(target_surface, text_surfaces, pos, descending=True):
        """
        Draw text surface onto target surface using surface.blit()
            @param target surface to blit onto
            @param text surface to blit
            @param position of text surface on target surface
            @param whether to blit list of surfaces ascending or descending
        """
        # direction = True = descending, direction = False = Ascending
        for i, text_surface in enumerate(text_surfaces):
            h, w = text_surface.get_rect().h, text_surface.get_rect().w
            if descending:
                offset = (pos[0], pos[1]+(i*h))
            else:
                offset = (pos[0], pos[1]-(i*h))
            target_surface.blit(text_surface, offset)


class SubScene(Scene):
    def __init__(self, parent_surface, rect, *args):
        self.subsurface = self._get_subsurface(parent_surface, rect)
        self.rect = rect
        self.args = args
        super().__init__(self.subsurface)

    def render(self):
        self.subsurface.fill((155, 155, 155))
        self.subsurface.fill((255, 255, 255))
        for arg in self.args:
            arg.render(self.subsurface)
        self.blit_text(self.subsurface, self.name_surface, (0, 0))

    @staticmethod
    def _get_subsurface(surface, rect):
        """
        Get a pygame subsurface from parent surface.
            @param parent surface
            @param pygame rect that represents the subsurface size from parent surface
            @return pygame subsurface from parent surface
        """
        return surface.subsurface(rect)


class MultiScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.subscenes = self.init_subscenes()

    def init_subscenes(self):
        list_of_subscenes = []
        # add classes on a child by child basis
        return list_of_subscenes


class RGBScene(MultiScene):
    def __init__(self, screen):
        super().__init__(screen)

    def init(self):
        # instances
        self.RGBGraph = rgb_holder.RGBGraph(1)
        rect = pg.Rect((255, 0), (255, 255))
        self.point = (100, 10, -15)
        cube_size = self.RGBGraph.get_stepwise()
        self.cube = prisms.Cube(self.point, cube_size)
        self.cube.apply_alpha(100)
        plane_size = cube_size
        self.plane_manager = plane_manager.PlaneManager(self.point, plane_size, (cube_size, cube_size, cube_size))
        self.isometric_scene = IsometricScene(self.screen, rect, self.plane_manager, self.cube)

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_UP:
                    translation = 1
                    self.plane_manager.move_active_plane(translation)
                    self.RGBGraph.translate(translation)
                if event.key == pg.K_DOWN:
                    pass
                if event.key == pg.K_LEFT:
                    self.RGBGraph.update_active_plane()
                    self.plane_manager.set_active_plane()
                if event.key == pg.K_RIGHT:
                    pass

    def render(self):
        self.screen.fill((100, 100, 100))
        self.RGBGraph.render(self.screen)
        self.blit_text(self.screen, self.name_surface, (0, 0))
        self.isometric_scene.render()

    def update(self):
        """Group update functions."""
        pass


class IsometricScene(SubScene):
    def __init__(self, screen, rect, *shapes):
        super().__init__(screen, rect, *shapes)

    def init(self):
        self.iso_transform = point_projection.Isometric(1)

    def render(self):
        self.subsurface.fill((155, 155, 155))
        self.blit_text(self.subsurface, self.name_surface, (0, 0))
        for shape in self.args:
            shape.render(self.subsurface, self.iso_transform)

