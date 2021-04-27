import pygame as pg



class Shape3:
    def __init__(self, points, color):
        self.points = points
        self.color = color

    def render(self, surface, plane_xyz):
        points_pairs = []
        for xyz in self.points:
            points_pairs.append(self.get_point_pair(plane_xyz, xyz))
        pg.draw.polygon(surface, self.color, points_pairs)

    def get_point_pair(self, plane_xyz, point):
        plane_x, plane_y, plane_z = plane_xyz
        x, y, z = point
        if plane_x:
            return (y, z)
        if plane_y:
            return (x, z)
        if plane_z:
            return (x, y)



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