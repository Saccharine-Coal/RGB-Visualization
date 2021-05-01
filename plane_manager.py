import itertools


from prisms3 import prisms

class PlaneManager(object):
    def __init__(self, origin, plane_size, limits_tuple):
        self.origin = origin
        self.plane_size = plane_size
        self._set_planes(plane_size, limits_tuple)
        self.plane_iter = self._get_next_plane()
        self.set_active_plane()

    # Setters --------------------------

    def _set_planes(self, plane_size, limits_tuple):
        limit_x, limit_y, limit_z = limits_tuple
        self.planes = {"YZ": prisms.PlaneYZ(self.origin, plane_size, limit_x),
                       "XZ": prisms.PlaneXZ(self.origin, plane_size, limit_y),
                       "XY": prisms.PlaneXY(self.origin, plane_size, limit_z)
                      }

    def _get_next_plane(self):
        """
        Generator object to iterate through the dictionary of planes endlessly.
            @yield plane object
        """
        # iterate the values of dict endlessly
        for key_val in itertools.cycle(self.planes.items()):
            yield key_val[1]

    def set_active_plane(self):
        self.active_plane = next(self.plane_iter)

    def move_active_plane(self, translation):
        """
        Move active plane along plane's axis by a translation
            @param translation distance to move plane along axis
        """
        self.active_plane.translate(translation)

    def render(self, surface, projection_matrix):
        """
        Render to target surface.
            @param target surface
            @param projection matrix
        """
        self.active_plane.render(surface, projection_matrix)
