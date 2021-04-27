import sys


import pygame as pg

import rgb_holder
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
        plane_size = int(1*cube_size)
        self.p1 = tuple(a-b for a, b in zip(self.point, (-cube_size/2, -cube_size/2, cube_size/2)))
        self.planeXY = prisms.PlaneXY(self.point, plane_size, cube_size)
        self.planeYZ = prisms.PlaneYZ(self.point, plane_size, cube_size)
        self.planeXZ = prisms.PlaneXZ(self.point, plane_size, cube_size)
        self.planes = {"xy": self.planeXY, "yz": self.planeYZ, "xz": self.planeXZ}
        self.isometric_scene = IsometricScene(self.screen, rect, self.planes, self.cube)

    def handle_events(self):
        events = pg.event.get()
        self.isometric_scene.handle_events(events)
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_UP:
                    self.RGBGraph.change_z_val(1)
                    self.planeXY.translate(0, 0, 1)
                if event.key == pg.K_DOWN:
                    self.RGBGraph.change_y_val(1)
                    self.planeXZ.translate(0, 1, 0)
                if event.key == pg.K_LEFT:
                    self.RGBGraph.update_plane_xyz(1)
                if event.key == pg.K_RIGHT:
                    self.RGBGraph.change_x_val(1)
                    self.planeYZ.translate(1, 0, 0)

    def render(self):
        self.screen.fill((100, 100, 100))
        self.RGBGraph.render(self.screen)
        self.blit_text(self.screen, self.name_surface, (0, 0))
        self.isometric_scene.render(self.RGBGraph.plane_xyz)

    def update(self):
        """Group update functions."""
        pass


class IsometricScene(SubScene):
    def __init__(self, screen, rect, planes, *shapes):
        self.planes = planes
        super().__init__(screen, rect, *shapes)

    def init(self):
        self.iso_transform = point_projection.Isometric(1)

    def update(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def render(self, plane_xyz):
        self.subsurface.fill((155, 155, 155))
        self.blit_text(self.subsurface, self.name_surface, (0, 0))
        x, y, z = plane_xyz
        if x:
            self.planes.get("yz").render(self.subsurface, self.iso_transform)
        if y:
            self.planes.get("xz").render(self.subsurface, self.iso_transform)
        if z:
            self.planes.get("xy").render(self.subsurface, self.iso_transform)
        for shape in self.args:
            shape.render(self.subsurface, self.iso_transform)


