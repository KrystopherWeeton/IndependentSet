import copy
import itertools
import math
from pprint import pprint
from typing import List, Tuple

import numpy as np


def mean(X: np.array) -> float:
    return sum(X) / X.size

def next_power_of_2(x):
    return 1 if x == 0 else 2**math.ceil(math.log2(x))

class DynamicResultTensor:
    def __init__(self):
        self.__dimension_names: [str] = []
        self.__dimension_sizes: [int] = []
        self.__dimension_keys: [[int]] = []
        self.__dimension_indices: dict = {}
        self.__num_dimensions = 0

        self.__dynamic_dimension_name: str = None
        self.__dynamic_dimension_capacity: int = None
        self.__dynamic_dimension_size: int = None

        self.results = None
        self.results_collected = -1

        #? State trackers
        self.dimensions_fixed = False
        self.dynamic_dimension_added = False


    def __verify_dimensions_fixed(self):    
        """
            Verify that the dimensions have been fixed and error if they haven't
        """
        if not self.dimensions_fixed:
            raise Exception("Dimensions have not been fixed.")

    def __verify_dimensions_not_fixed(self):
        """
            Verify that the dimensions haven't been fixed and error if they have
        """
        if self.dimensions_fixed:
            raise Exception("Dimensions have already been fixed.")
    
    def ___verify_dynamic_dimension_added(self):
        """
            Verify that the dynamic dimension has been added and error if it hasn't
        """
        if not self.dynamic_dimension_added:
            raise Exception("Dynamic dimension hasn't been added yet. Cannot collect results.")

    def __increase_dynamic_capacity(self, min_capacity: int):
        if not self.dimensions_fixed:
            raise Exception("Can only increase dynamic capacity after dimensions have been fixed.")
        elif min_capacity < self.__dynamic_dimension_capacity:
            raise Exception("Cannot increase dynamic capacity to a smaller amount.")
        # Calculate new capacity as a power of 2 (minimize runtime)
        cur_capacity: int = self.__dynamic_dimension_capacity
        new_capacity: int = next_power_of_2(min_capacity)
        pad_amount: int = new_capacity - cur_capacity
        pad_width: [(int, int)] = [(0, pad_amount)] + [(0, 0)] * self.__num_dimensions
        self.results = np.pad(self.results, pad_width, 'constant', constant_values=(0))
        self.__dynamic_dimension_capacity = new_capacity

    def __dim_size(self, dimension: str) -> int:
        return self.__dimension_sizes[self.__dimension_indices[dimension]]

    # Might not be strictly necessary, but not bad to do overall
    def keys(self, dimension: str) -> [int]:
        return copy.copy(self.__dim_keys(dimension))

    def __dim_keys(self, dimension: str) -> [int]:
        return self.__dimension_keys[self.__dimension_indices[dimension]]

    def __get_index(self, dimension: str, key: int) -> int:
        return self.__dim_keys(dimension).index(key)
    
    def set_dynamic_dimension(self, dimension_name: str, init_capacity: int = 64):
        self.__verify_dimensions_not_fixed()
        self.__dynamic_dimension_name = dimension_name
        self.__dynamic_dimension_capacity = next_power_of_2(init_capacity)
        self.__dynamic_dimension_size = 0
        self.dynamic_dimension_added = True

    def add_dimension(self, dimension_name: str, dimension_keys: [int]):
        self.__verify_dimensions_not_fixed()

        self.__dimension_names.append(dimension_name)
        self.__dimension_sizes.append(len(dimension_keys))
        self.__dimension_keys.append(dimension_keys)
        self.__dimension_indices[dimension_name] = len(self.__dimension_names) - 1
        self.__num_dimensions += 1

    def fix_dimensions(self):
        self.___verify_dynamic_dimension_added()
        # Set tracker
        self.dimensions_fixed = True
        # Initialize the results object to track all the actual results now
        self.results = np.zeros([self.__dynamic_dimension_capacity] + self.__dimension_sizes)
        self.results_collected = 0


    def __validate_kwargs_access(self, access: List[Tuple[str, int]]) -> [int]:
        """
            Verifies that the access provided is valid within the current size(s) of the dimensions existing.
            Returns the access converted into a list of proper indices to access the results object, and
            errors on error.
        """
        assert(len(access) == self.__num_dimensions + 1)
        dynamic_name, dynamic_index = access[0]
        access = access[1:]
        assert(dynamic_name == self.__dynamic_dimension_name)
        # Don't need to check capacity, as we will resize when appropriate for the dynamic dimension
        for i in range(len(access)):
            dim_name, dim_index = access[i]
            assert(dim_name == self.__dimension_names[i])
            assert(dim_index in self.__dimension_keys[i])
        # Convert everything to indices and return the value
        return tuple([dynamic_index] + [self.__get_index(dim_name, k) for dim_name, k in access])
    
    def __resize_dynamic_dimension_if_necessary(self, index: int):
        # Check which case we fall into
        if index < self.__dynamic_dimension_size:
            # Already in size, so we can just return
            return
        elif index < self.__dynamic_dimension_capacity:
            # In capacity, so we only need to update size
            self.__dynamic_dimension_size = index + 1   # account for 0 index
        else:
            self.__increase_dynamic_capacity(index + 1)
            self.__dynamic_dimension_size = index + 1

    def add_result(self, result, **kwargs) -> bool:
        self.__verify_dimensions_fixed()
        # Convert to indices then check dynamic size and update results object
        indices: [int] = self.__validate_kwargs_access(list(kwargs.items()))
        # Resize and set the result
        self.__resize_dynamic_dimension_if_necessary(indices[0])
        self.results[indices] = result
        self.results_collected += 1

    def get_results(self, **kwargs) -> bool:
        self.__verify_dimensions_fixed()
        indices: [int] = self.__validate_kwargs_access(list(kwargs.items()))
        return self.results[indices]

    def collapse_to_matrix(self, f=mean) -> np.ndarray:
        m: np.array = np.zeros(self.__dimension_sizes[0:2])
        outer_size: int = self.__dimension_sizes[0]
        inner_size: int = self.__dimension_sizes[1]
        for r in range(outer_size):
            for c in range(inner_size):
                m[r][c] = f(self.results[r][c])
        return m

    def collapse_to_list(self, f=mean) -> np.ndarray:
        m: np.array = np.zeros(self.__dimension_sizes[0])
        size: int = self.__dimension_sizes[0]
        for r in range(size):
            m[r] = f(self.results[r])
        return m

    def collapse_to_2d_list(self, f=mean) -> [(int, float)]:
        M = self.collapse_to_matrix(f)
        l: [(int, float)] = []
        keys = self.__dimension_keys[0]

        for row in range(M.shape[0]):
            for col in range(M.shape[1]):
                key = keys[row]
                l.append((key, M[row][col]))
        return l
    
    def get_results(self) -> np.array:
        return self.results[0:self.__dynamic_dimension_size]

    def __str__(self) -> str:
        return f"<{[self.__dimension_names]}>"

# TODO: Move to disallowed value to be a bit more clean