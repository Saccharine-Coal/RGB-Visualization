import pygame as pg



class Shape3:
    def __init__(self, points, color):
        self.points = points
        self.color = color

    def get_projected_points(self, lt):
        projected_points = []
        for point in self.points:
            projected_points.append(lt*tuple(point))
        return projected_points

    def translate(self, dx, dy, dz):
        translated_points = []
        for point in self.points:
            x, y, z = point
            trans_point = (x+dx, y+dy, z+dz)
            translated_points.append(trans_point)
        self.points = translated_points

    def render(self, surface, lt):
        projected_points = self.get_projected_points(lt)
        if len(self.color)  == 4:
            self.draw_transparent(surface, projected_points)
        else:
            pg.draw.polygon(surface, self.color, projected_points)
        #pg.draw.lines(surface, self.color, True, projected_points)

    def draw_transparent(self, surface, points):
        rect = surface.get_rect()
        transparent_surface = pg.Surface(rect.size, pg.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        pg.draw.polygon(transparent_surface, self.color, points)
        surface.blit(transparent_surface, (0, 0))


class Rect3(Shape3):
    def __init__(self, position_vector_1, length_vector_2, length_vector_4, color):
        self.vector_1 = position_vector_1
        self.vector_2 = length_vector_2
        self.vector_4 = length_vector_4
        super().__init__(self.get_points(), color)

    def __repr__(self):
        return f"[{self.vector_1}, {self.vector_2}, {self.vector_3}, {self.vector_4}]"
    
    @property
    def vector_3(self):
        # http://thejuniverse.org/PUBLIC/LinearAlgebra/LOLA/planes/vect.html
        v1 = self.vector_1
        v2 = self.vector_2
        v4 = self.vector_4
        # v3 = v1 + s*vector_2 + d*vector_4
        # vector form of the plane
        # assume s=t=1
        return v1 + v2 + v4

    def get_center(self):
        xyz = self.vector_1.lerp(self.vector_3, 0.5).xyz
        return tuple(xyz)

    def get_points(self):
        p1 = self.vector_1.xyz
        p2 = (self.vector_2 + self.vector_1).xyz
        p3 = self.vector_3.xyz
        p4 = (self.vector_4 + self.vector_1).xyz
        return [p1, p2, p3, p4]
