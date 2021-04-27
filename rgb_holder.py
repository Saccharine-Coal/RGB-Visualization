import pygame as pg

import numpy as np

import shapes

class RGBGraph(object):
    """The x axis is R, z axis is G, and y axis is B."""
    def __init__(self, unit_size):
        self.start_G, self.end_G = 0, 255
        self.unit_size = unit_size
        self.step_size = 5
        self.planes = self.get_planes()
        self.current_z = 0
        self.current_y = 0
        self.current_x = 0
        self.plane_xyz = (True, False, False)
        self._foo = 0

    def get_planes(self):
        list_3d = []
        for g_val in range(self.start_G, self.end_G, self.step_size):
            list_3d.append(self.get_plane_of_shapes(g_val))
        return np.array(list_3d)

    def get_plane_of_shapes(self, plane_G):
        print(f"Constructing plane: {plane_G}")
        list_2d = []
        start_R, end_R = 0, 255
        start_B, end_B = 0, 255
        g_val_of_plane = plane_G
        square_size = self.unit_size
        # 2d array creation to represent the plane
        for r_val in range(start_R, end_R, self.step_size):
            list_1d = []
            for b_val in range(start_B, end_B, self.step_size):
                shape_xyz = (b_val*square_size, r_val*square_size, g_val_of_plane*square_size)
                shape_color = (r_val, g_val_of_plane, b_val)
                shape_obj = self.get_square_shape(shape_xyz, square_size+self.step_size, shape_color)
                list_1d.append(shape_obj)
            list_2d.append(list_1d)
        return list_2d


    @staticmethod
    def get_square_shape(shape_xyz, shape_length, color):
        # use pygame rect to construct shape points
        v1 = pg.math.Vector3(shape_xyz)
        v2 = pg.math.Vector3(shape_length, 0, shape_length)
        v3 = pg.math.Vector3(0, shape_length, shape_length)
        return shapes.Rect3(v1, v2, v3, color)

    def change_x_val(self, dval):
        max_val = self.get_stepwise()
        val = self.current_x + dval
        if val < 0:
            val = max_val - 1
        if val > max_val - 1:
            val = 0

        self.current_x = val
        print(f"Current x val {self.current_x}")
    
    
    def change_y_val(self, dval):
        max_val = self.get_stepwise()
        val = self.current_y + dval
        if val < 0:
            val = max_val - 1
        if val > max_val - 1:
            val = 0

        self.current_y = val
        print(f"Current y val {self.current_y}")

    def change_z_val(self, dval):
        max_val = self.get_stepwise()
        val = self.current_z + dval
        if val < 0:
            val = max_val - 1
        if val > max_val - 1:
            val = 0

        self.current_z = val
        print(f"Current z val {self.current_z}")
    
    def get_stepwise(self):
        self.start_G, self.end_G, self.step_size
        return int((self.end_G-self.start_G)/self.step_size)

    def update_plane_xyz(self, dfoo):
        self._foo += dfoo
        if self._foo == 2:
            # x
            self.plane_xyz = (True, False, False)
            self._foo = -1
        if self._foo == 1:
            # y
            self.plane_xyz = (False, True, False)
        if self._foo == 0:   
            # z
            self.plane_xyz = (False, False, True)
        print(f"Current Plane (x, y, z) {self.plane_xyz}")

    def get_slice_of_shapes(self):
        # z, y, x 
        # tuple of True or False values
        plane_x, plane_y, plane_z = (self.plane_xyz)
        if not plane_x and not plane_y and not plane_z:
            raise NotImplementedError
        if not plane_x and not plane_y:
            # plane of z values
            return self.planes[self.current_z, : , :]
        if not plane_x and not plane_z:
            # plane of y values
            return self.planes[: , self.current_y, :]
        if not plane_y and not plane_z:
            return self.planes[:, :, self.current_x]
        else:
            raise NotImplementedError("Line of values not implemented yet!")



    def render(self, screen):
        plane_to_render = self.get_slice_of_shapes()
        for sub_list in plane_to_render:
            if isinstance(sub_list, shapes.Rect3):
                sub_list.render(screen, self.plane_xyz)
            else:
                for shape in sub_list:
                    shape.render(screen, self.plane_xyz)
