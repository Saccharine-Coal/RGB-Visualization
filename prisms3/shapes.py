import pygame as pg



class Shape3:
    """Collection of points in Euclidean 3-space (x, y, z). This class will modify a list of points (3-tuples)."""
    def __init__(self, points, color, fill=True):
        """"
        @param a list of tuples
        @param RGB tuple
        @param True = draw filled shape, False = draw hollow shape
        """
        self.points = points
        self.color = color
        self.fill = fill

    def get_projected_points(self, linear_transformation):
        """
        This function multiplies a projection matrix to a list of points.
            @param linear transformation instance
            @return list of projected 2-tuples
        """
        projected_points = []
        for point in self.points:
            transformed_point = linear_transformation * tuple(point)
            projected_points.append(transformed_point)
        return projected_points

    def translate(self, dx, dy, dz):
        """
        Apply a translation to a list of points.
            @param translation x
            @param translation y
            @param translation z
        """
        translated_points = []
        for point in self.points:
            x, y, z = point
            trans_point = (x+dx, y+dy, z+dz)
            translated_points.append(trans_point)
        self.points = translated_points

    def render(self, surface, linear_transformation):
        """
        Blit to the target surface.
            @param target surface
            @param projection matrix (x, y, z) -> (x, y)
        """
        projected_points = self.get_projected_points(linear_transformation)
        if len(self.color)  == 4:
            # (RGB[A])
            self._draw_transparent(surface, projected_points)
        else:
            # (RGB)
            self._draw_points(surface, projected_points)

    def _draw_transparent(self, surface, points):
        """
        Draw the shape transparently by making a transparent surface. Color must be (RGB[A]).
            @param target surface
            @param list of 2-tuples
        """
        rect = surface.get_rect()
        transparent_surface = pg.Surface(rect.size, pg.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        self._draw_points(transparent_surface, points)
        surface.blit(transparent_surface, (0, 0))

    def _draw_points(self, surface, points):
        """
        Draw the shape on target surface. Accepts (RGB) & (RGB[A]).
            @param target surface
            @param list of 2-tuples
        """
        if self.fill:
            # filled polygon
            pg.draw.polygon(surface, self.color, points)
        else:
            # hollow polygon
            pg.draw.lines(surface, self.color, False, points)



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
        # v3 = v1 + s*vector_2 + t*vector_4
        # vector form of the plane
        # assume s=t=1
        return v1 + v2 + v4

    def get_center(self):
        """
        Get the center of the 3D plane by linearly interpolating between the origin vector and vector 3.
            @return 3-tuple representing the center of the rect3 object
        """
        xyz = self.vector_1.lerp(self.vector_3, 0.5).xyz
        return tuple(xyz)

    def get_points(self):
        """
        Get the 3-tuple representation of the rect3 vectors.
            @return list of 3-tuples
        """
        p1 = self.vector_1.xyz
        p2 = (self.vector_2 + self.vector_1).xyz
        p3 = self.vector_3.xyz
        p4 = (self.vector_4 + self.vector_1).xyz
        return [p1, p2, p3, p4]
