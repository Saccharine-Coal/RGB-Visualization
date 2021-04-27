import numpy as np


class LinearTransformation(object):
    """Basic linear transformation object. 
    Handles multiplication of tuples and multiplication of other linear transformations."""
    def __init__(self, std_matrix_repr):
        if isinstance(std_matrix_repr, list):
            self.std_matrix_repr = np.array(std_matrix_repr)
        elif isinstance(std_matrix_repr, np.ndarray):
            self.std_matrix_repr = std_matrix_repr
        elif self.check_nested_list(std_matrix_repr):
            self.std_matrix_repr = np.array(std_matrix_repr)
        else:
            print(std_matrix_repr, type(std_matrix_repr))
            raise NotImplementedError("INIT")

    def __repr__(self):
        return f'Linear Transformation: {self.std_matrix_repr}'

    def __mul__(self, other):
        """Left multiplication. self * other"""
        if isinstance(other, tuple):
            return self.transform_point(other)
        if isinstance(other, LinearTransformation):
            return self.left_composition(other)
        else:
            print(other, type(other))
            raise NotImplementedError

    def __rmul__(self, other):
        """Right multiplication. other * self"""
        if isinstance(other, tuple):
            return self.transform_point(other)
        if isinstance(other, LinearTransformation):
            return self.right_composition(other)
        else:
            raise NotImplementedError

    def __neg__(self):
        return LinearTransformation(np.negative(self.std_matrix_repr))

    def check_nested_list(self, nested_list):
        return any(isinstance(sub_list, list) for sub_list in nested_list)

    def left_composition(self, LT_obj2):
        left_std_matrix_repr = self.std_matrix_repr
        right_std_matrix_repr_2 = LT_obj2.std_matrix_repr
        product_arr = np.multiply(left_std_matrix_repr, right_std_matrix_repr_2)
        return self.new_linear_transformation(product_arr)

    def right_composition(self, LT_obj2):
        left_std_matrix_repr = LT_obj2.std_matrix_repr
        right_std_matrix_repr_2 = self.std_matrix_repr
        product_arr = np.multiply(left_std_matrix_repr, right_std_matrix_repr_2)
        return self.new_linear_transformation(product_arr)

    def new_linear_transformation(self, std_matrix_repr):
        return LinearTransformation(std_matrix_repr)

    def transform_point(self, point):
        vector_repr = np.array(point)
        product_arr = np.dot(self.std_matrix_repr, vector_repr)
        return tuple(product_arr)

    def update_std_mx_repr(self, new_std_mx_repr):
        self.std_matrix_repr = new_std_mx_repr
