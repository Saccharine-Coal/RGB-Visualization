import pygame as pg

import numpy as np

import shapes

class RGBGraph(object):
    """The x axis is R, z axis is G, and y axis is B."""
    def __init__(self, unit_size):
        """
        @param size between points
        """
        self.start_G, self.end_G = 0, 255
        self.unit_size = unit_size
        self.step_size = 5
        self.planes = self.get_planes()
        self.current_z = self.current_y = self.current_x = 0
        self.active_plane_bools = (False, False, True)
        self.plane_increment = -1

    def get_planes(self):
        """
        Get 3D numpy array of Rect3 objects.
            @return 3D numpy array
        """
        list_3d = []
        for g_val in range(self.start_G, self.end_G, self.step_size):
            list_3d.append(self.get_plane_of_shapes(g_val))
        return np.array(list_3d)

    def get_plane_of_shapes(self, plane_G):
        """
        Get a 2D list of Rect3 objects.
            @param current green value/ z value
            @return 2D list
        """
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
        """
        CHANGE ME IN THE FUTURE!
        """
        # use pygame rect to construct shape points
        v1 = pg.math.Vector3(shape_xyz)
        v2 = pg.math.Vector3(shape_length, 0, shape_length)
        v3 = pg.math.Vector3(0, shape_length, shape_length)
        return shapes.Rect3(v1, v2, v3, color)

    def change_x_val(self, dval):
        """
        Change x value to slice 3D numpy array. Constrains value to array index limits.
            @param value to increment/decrement by
        """
        max_val = self.get_stepwise()
        val = self.current_x + dval
        if val < 0:
            val = max_val - dval
        if val > max_val - dval:
            val = 0
        self.current_x = val
    
    def change_y_val(self, dval):
        """
        Change y value to slice 3D numpy array. Constrains value to array index limits.
            @param value to increment/decrement by
        """
        max_val = self.get_stepwise()
        val = self.current_y + dval
        if val < 0:
            val = max_val - 1
        if val > max_val - 1:
            val = 0
        self.current_y = val

    def change_z_val(self, dval):
        """
        Change z value to slice 3D numpy array. Constrains value to array index limits.
            @param value to increment/decrement by
        """
        max_val = self.get_stepwise()
        val = self.current_z + dval
        if val < 0:
            val = max_val - 1
        if val > max_val - 1:
            val = 0
        self.current_z = val
    
    def get_stepwise(self):
        """
        This function is intended to get the index limits of a list.
            @return max list integer index
        """
        return int((self.end_G-self.start_G)/self.step_size)

    def update_active_plane(self):
        """
        Update the active plane by changing a tuple of booleans.
        """
        self.plane_increment += 1
        if self.plane_increment == 2:
            # x
            self.active_plane_bools = (False, True, False)
            self.plane_increment = -1
            print("Current Plane: YZ")
        if self.plane_increment == 1:
            # y
            self.active_plane_bools = (True, False, False)
            print("Current Plane: XZ")
        if self.plane_increment == 0:   
            # z
            self.active_plane_bools = (False, False, True)
            print("Current Plane: XY")

    def get_slice_of_shapes(self):
        """
        Slice a 3D numpy array to yield a 2D array of Rect3 objects.
            @return 2D numpy array
        """
        # z, y, x 
        # tuple of True or False values
        plane_x, plane_y, plane_z = (self.active_plane_bools)
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

    def translate(self, translation):
        """
        translate the along the active axis
            @param translation
        """
        x_bool, y_bool, z_bool = self.active_plane_bools
        if x_bool:
            self.change_x_val(translation)
        if y_bool:
            self.change_y_val(translation)
        if z_bool:
            self.change_z_val(translation)



    def render(self, surface):
        """
        Render to target surface.
            @param pygame surface
        """
        plane_to_render = self.get_slice_of_shapes()
        for sub_list in plane_to_render:
            for shape in sub_list:
                shape.render(surface, self.active_plane_bools)
