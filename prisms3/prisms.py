import pygame as pg


import prisms3.shapes


# DEFAULT CUBE COLORS
FACE1_COLOR = (255, 0, 0)
FACE2_COLOR = (0, 255, 0)
BLUE_FACE = (0, 0, 255)
YELLOW_FACE = (255, 255, 0)
PURPLE_FACE = (255, 0, 255)
CYAN_FACE = (0, 255, 255)



class Cube(object):
    """Uses shape class to represent each face of the cube."""
    def __init__(self, origin, side_length):
        self.origin = origin
        self.side_length = side_length
        self.faces = self._construct_faces()
        self.center = pg.math.Vector3(self.origin) + pg.math.Vector3(side_length/2, side_length/2, side_length/2)
        self.theta_xyz = (0, 0, 0)

    @staticmethod
    def _construct_top_face(origin, l, w, h):
        """
        Get Rect3 on the xy plane.
            @param origin of prism
            @param length of prism
            @param width of prism
            @param height of prism
            @return Rect3
        """
        x, y, z = (origin)
        v1 = pg.math.Vector3(x, y, z+h)
        # +l, +w, 0
        v2 = pg.math.Vector3(l, 0, 0)
        v4 = pg.math.Vector3(0, w, 0)
        face = prisms3.shapes.Rect3(v1, v2, v4, FACE1_COLOR)
        return face

    @staticmethod
    def _construct_bottom_face(origin, l, w, h):
        """
        Get Rect3 on the xy plane.
            @param origin of prism
            @param length of prism
            @param width of prism
            @param height of prism
            @return Rect3
        """
        x, y, z = (origin)
        v1 = pg.math.Vector3(x, y, z)
        #  +length, +width, 0
        v2 = pg.math.Vector3(l, 0, 0)
        v4 = pg.math.Vector3(0, w, 0)
        face = prisms3.shapes.Rect3(v1, v2, v4, FACE2_COLOR)
        return face

    @staticmethod
    def _construct_foward_face(origin, l, w, h):
        """
        Get Rect3 on the yz plane.
            @param origin of prism
            @param length of prism
            @param width of prism
            @param height of prism
            @return Rect3
        """
        x, y, z = (origin)
        v1 = pg.math.Vector3(x, y, z)
        #  0, +width, +height
        v2 = pg.math.Vector3(0, w, 0)
        v4 = pg.math.Vector3(0, 0, h)
        face = prisms3.shapes.Rect3(v1, v2, v4, BLUE_FACE)
        return face

    @staticmethod
    def _construct_back_face(origin, l, w, h):
        """
        Get Rect3 on the yz plane.
            @param origin of prism
            @param length of prism
            @param width of prism
            @param height of prism
            @return Rect3
        """
        x, y, z = (origin)
        v1 = pg.math.Vector3(x + l , y, z)
        # 0, +w, +h
        v2 = pg.math.Vector3(0, w, 0)
        v4 = pg.math.Vector3(0, 0, h)
        face = prisms3.shapes.Rect3(v1, v2, v4, YELLOW_FACE)
        return face

    @staticmethod
    def _construct_left_face(origin, l, w, h):
        """
        Get Rect3 on the xz plane.
            @param origin of prism
            @param length of prism
            @param width of prism
            @param height of prism
            @return Rect3
        """
        x, y, z = (origin)
        v1 = pg.math.Vector3(x, y, z)
        # +l, 0, +h
        v2 = pg.math.Vector3(l, 0, 0)
        v4 = pg.math.Vector3(0, 0, h)
        face = prisms3.shapes.Rect3(v1, v2, v4, PURPLE_FACE)
        return face

    @staticmethod
    def _construct_right_face(origin, l, w, h):
        """
        Get Rect3 on the xz plane.
            @param origin of prism
            @param length of prism
            @param width of prism
            @param height of prism
            @return Rect3
        """
        x, y, z = (origin)
        v1 = pg.math.Vector3(x, y + w, z)
        # +l, +h, 0
        v2 = pg.math.Vector3(h, 0, 0)
        v4 = pg.math.Vector3(0, 0, l)
        face = prisms3.shapes.Rect3(v1, v2, v4, CYAN_FACE)
        return face

    def _construct_faces(self):
        """
           Constructs Rect3 objects to represent the faces of the cube
           @return list of Rect3 objects
        """
        length = width = height = self.side_length
        self.f1 =  self._construct_foward_face(self.origin, length, width, height) 
        self.f2 = self._construct_right_face(self.origin, length, width, height) 
        self.f3 = self._construct_back_face(self.origin, length, width, height) 
        self.f4 = self._construct_left_face(self.origin, length, width, height) 
        self.f5 = self._construct_top_face(self.origin, length, width, height) 
        self.f6 = self._construct_bottom_face(self.origin, length, width, height) 
        return [self.f1, self.f2, self.f3, self.f4, self.f5, self.f6]

    def sort_faces(self, rect3):
        """
        Function is intended to be used with list sort() and sorted() methods to sort based on "depth".
            @param Rect3 instance
            @return tuple
        """
        return rect3.get_center().xyz

    def apply_rotation(self):
        """
        Apply rotation of theta_x, theta_y, and theta_z to all Shape3 instances.
        """
        for face in self.faces:
            face.theta_xyz = self.theta_xyz

    def apply_translation(self, dx, dy, dz):
        """
        Apply translation of dx, dy, dz to all Shape3 instances. This function will be replaced by a
        linear transformation matrix in the future.
            @param translation in x direction
            @param translation in y direction
            @param translation in z direction
        """
        for face in self.faces:
            face.translate(dx, dy, dz)

    def apply_alpha(self, alpha):
        """
        Apply alpha Shape3 instance color attr. (RGB) -> (RGB[A])
            @param alpha value to set
        """
        for face in self.faces:
            if len(face.color) == 3:
                face.color = (*face.color, alpha)
            else:
                face.color = (*face.color[0:3], alpha)

    def render(self, surface, camera):
        """
        Blit to target surface.
            @param target surface
            @param camera / linear transformation
        ** Need to differentiate between regular rendering and camera / projective rendering in the future.
        """
        y_sorted_faces = sorted(self.faces, key=lambda face: face.get_center()[1], reverse=False)
        sorted_faces = sorted(y_sorted_faces, key=lambda face: face.get_center()[2], reverse=True)
        for face in sorted_faces:
            face.render(surface, camera)


class PlaneXY(prisms3.shapes.Rect3):
    def __init__(self, origin, size, limit):
        """
            @param xyz origin
            @param size of the plane
            @param limit of the plane in +-x, y, z relative to the origin
        """
        self.origin = origin
        self.size = size
        self.limit = limit
        self.position = origin
        super().__init__(*self.get_plane(origin, size))

    def get_plane(self, origin, size):
        """
        Get pygame vectors and color of shape for super() call.
            @param origin
            @param size
            @return origin_vector, length_vector, length_vector, color tuple
        """
        v1 = pg.math.Vector3(origin)
        v2 = pg.math.Vector3((size, 0, 0))
        v3 = pg.math.Vector3((0, size, 0))
        color = (20, 60, 80)
        return v1, v2, v3, color

    def update_position(self, dx=0, dy=0, dz=0):
        """
        This function is solely intended to be used with the constrain() function for now.
            @param translation x
            @param translation y
            @param translation z
        """
        self.position = tuple((a-b) for a, b in zip(self.position, (dx, dy, dz)))

    def constrain(self, translation):
        """
        Constrain along z-axis (limit).
            @return constrained 3-tuple
        """
        origin_x, origin_y, origin_z = self.origin
        x, y, z = self.position
        dz = origin_z - z + translation
        max, min = self.limit, -self.limit
        if dz >= max:
            translation = min + translation
        elif dz <= min:
            translation = max - translation
        return (0, 0, translation)

    def translate(self, translation):
        """
        Apply translation to to xyz tuples and constrain if needed.
            @param translation x
        """
        translated_points = []
        constrained_translation = self.constrain(translation)
        self.update_position(*constrained_translation)
        for point in self.points:
            translated_point = tuple(a + b for a, b in zip (constrained_translation, point))
            translated_points.append(translated_point)
        self.points = translated_points


class PlaneYZ(PlaneXY):
    def __init__(self, origin, size, limit):
        """
            @param xyz origin
            @param size of the plane
            @param limit of the plane in +-x, y, z relative to the origin
        """
        super().__init__(origin, size, limit)

    def get_plane(self, origin, size):
        """
        Get pygame vectors and color of shape for super() call.
            @param origin
            @param size
            @return origin_vector, length_vector, length_vector, color tuple
        """
        v1 = pg.math.Vector3(origin)
        v2 = pg.math.Vector3((0, size, 0))
        v3 = pg.math.Vector3((0, 0, size))
        color = (80, 60, 20)
        return [v1, v2, v3, color]


    def constrain(self, translation):
        """
        If translated point > max set to min. If tranlated point < min set to max. Else, translate normally.
        Constrain along x-axis (limit).
            @return 3-tuple within limits
        """
        origin_x, origin_y, origin_z = self.origin
        x, y, z = self.position
        dx = origin_x - x + translation
        max, min = self.limit, -self.limit
        if dx >= max:
            translation = min + translation
        elif dx <= min:
            translation = max - translation
        return (translation, 0, 0)

    def translate(self, translation):
        """
        Apply translation to to xyz tuples and constrain if needed.
            @param translation x
        """
        translated_points = []
        constrained_translation = self.constrain(translation)
        self.update_position(*constrained_translation)
        for point in self.points:
            translated_point = tuple(a + b for a, b in zip (constrained_translation, point))
            translated_points.append(translated_point)
        self.points = translated_points


class PlaneXZ(PlaneXY):
    def __init__(self, origin, size, limit):
        """
            @param xyz origin
            @param size of the plane
            @param limit of the plane in +-x, y, z relative to the origin
        """
        super().__init__(origin, size, limit)

    def get_plane(self, origin, size):
        """
        Get pygame vectors and color of shape for super() call.
            @param origin
            @param size
            @return origin_vector, length_vector, length_vector, color tuple
        """
        v1 = pg.math.Vector3(origin)
        v2 = pg.math.Vector3((size, 0, 0))
        v3 = pg.math.Vector3((0, 0, size))
        color = (80, 20, 60)
        return [v1, v2, v3, color]

    def constrain(self, translation):
        """
        Constrain along y-axis (limit).
            @return constrained 3-tuple
        """
        origin_x, origin_y, origin_z = self.origin
        x, y, z = self.position
        dy = origin_y - y + translation
        max, min = self.limit, -self.limit
        if dy >= max:
            translation = min + translation
        elif dy <= min:
            translation = max - translation
        return (0, translation, 0)

    def translate(self, translation):
        """
        Apply translation to to xyz tuples and constrain if needed.
            @param translation y
        """
        translated_points = []
        constrained_translation = self.constrain(translation)
        self.update_position(*constrained_translation)
        for point in self.points:
            translated_point = tuple(a + b for a, b in zip (constrained_translation, point))
            translated_points.append(translated_point)
        self.points = translated_points