import copy
import itertools
import math
from pprint import pprint
from typing import List, Tuple, Callable

import numpy as np


def mean(X: np.array) -> float:
    return sum(X) / X.size


class DynamicResultTensor:
    def __init__(self):
        self.__dynamic_keys: [int] = []
        self.__dynamic_name: str = None

        self.__dimension_names: [str] = []
        self.__dimension_sizes: [int] = []
        self.__dimension_capacities: [int] = []
        self.__dimension_keys: [[int]] = []
        self.__dimension_indices: dict = {}
        self.__dimension_capacities: [int] = []
        # TODO: Remove unused class variables
        self.__num_dimensions = 0

        self.dimensions_fixed = False

        self.results = None
        self.results_total = -1
        self.results_collected = -1
        self.__index_list = []

    #***********************************************************************************************
    #*                                      Private Helpers
    #***********************************************************************************************

    def __dim_size(self, dimension: str) -> int:
        """ Returns the size of the provided dimension """
        return self.__dimension_sizes[self.__dimension_indices[dimension]]

    def __dim_keys(self, dimension: str) -> [int]:
        """ Returns the keys (shallow copy) of the provided dimension """
        return self.__dimension_keys[self.__dimension_indices[dimension]]

    def __get_index(self, dimension: str, key: int) -> int:
        """ Turns the key into an index for the provided dimension """
        return self.__dim_keys(dimension).index(key)

    def __to_indices(self, kwargs) -> Tuple:
        """ Returns a tuple of all the keys turned into indices """
        return tuple([self.__get_index(dim, k) for dim, k in kwargs.items()]) 

    #***********************************************************************************************
    #*                                      Dimension Generation / Management
    #***********************************************************************************************
    
    def add_dimension(self, dimension_name: str, initial_capacity: int = 100):
        """
            Adds in a dimension with the provided name, and the provided initial capacity with 0 entries
                NOTE: `initial_capacity` defaults to 100 if not provided.
        """
        if self.dimensions_fixed:
            raise Exception(
                "Attempt to add a dimension to a result object when the dimension have already been fixed"
            )

        self.__dimension_names.append(dimension_name)
        self.__dimension_sizes.append(0)
        self.__dimension_capacities.append(initial_capacity)
        self.__num_dimensions += 1

    def fix_dimensions(self):
        """
            Fixes the dimensions, moving the tensor into result gathering stage
        """
        # Set trackers
        self.dimensions_fixed = True

        # Initialize the results object to track all the actual results now
        self.results = np.zeros(self.__dimension_capacities)
        self.results_collected = 0

    #***********************************************************************************************
    #*                                      Data access / placement
    #***********************************************************************************************

    def __validate_kwargs_access(self, kwargs):
        """
            Validates the kwargs provided to ensure no OOB errors, etc. when accessing data. Can be
            removed for speed for well tested code.
        """
        # Validates correct number of dimensions
        if len(kwargs) != self.__num_dimensions:
            raise Exception("Wrong number of dimensions for accessing results dict.")
        items = list(kwargs.items())

        for i in range(self.__num_dimensions):
            dimension, k = items[i]
            if dimension != self.__dimension_names[i]:
                raise Exception(
                    "Wrong ordering of dimensions for accessing results dict."
                )
            # Validate index is within the correct index ranges for dimension
            if k < 0 or k >= self.__dimension_sizes[i]:
                raise Exception(
                    "Invalid index access to dimension."
                )

    def __does_capacity_need_to_change(self, kwargs) -> (int, int):
        """
            Determines if the access requires rebalancing the provided dimensions.

                `None` is returned when no resizing needs to be done

                (dimension, minimum_capacity)  is returned when `dimension` needs to be resized to at least
                `minimum_size`
        """
        items = list(kwargs.items())
        # Iterate through the dimensions so we can check them 1 by 1
        for dim_index in range(self.__num_dimensions):
            dim_name, j = items[dim_index]
            capacity: int = self.__dimension_capacities[i]
            # Validate value provided is within current capacity
            if j >= i:
                return (i, j + 1)
        return None
    

    def __increase_capacity(self, dimension: int, min_capacity: int):
        """
            Resizes the provided dimension by making it the first power of two at least as large as
            minimum capacity.
        """
        # TODO: Implement this.

    def __increase_sizes(self, kwargs):
        # TODO: Implement this
        pass

    def add_result(self, result, **kwargs) -> bool:
        """
            Adds the provided result after validating kwarg arguments.
                NOTE: Requires kwargs be provided in the order of dimensions
        """
        # Validate state and arguments provided
        if not self.dimensions_fixed:
            raise Exception(
                "Attempt to add result with dimensions not fixed in results dict"
            )
        self.__validate_kwargs_access(kwargs)
        # Until all dimensions have enough capacity, repeatedly increase capacity
        t = self.__does_capacity_need_to_change(kwargs)
        while t != None:
            self.__increase_capacity(t[0], t[1])
        # Increase size where appropriate
        self.__increase_sizes(kwargs)
        # Translate to proper indices and set value
        indices = self.__to_indices(kwargs)
        self.results[indices] = result
        self.results_collected += 1


    def get_results(self, **kwargs) -> bool:
        # Validate state and arguments provided
        if not self.dimensions_fixed:
            raise Exception(
                "Attempt to get result with dimensions not fixed in results dict"
            )
        self.__validate_kwargs_access(kwargs)

        indices = self.__to_indices(kwargs)
        return self.results[indices]

    #***********************************************************************************************
    #*                                      Formatted Data Exports
    #***********************************************************************************************

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
    
    def validate_filled(self) -> bool:
        """
            Validates that all entries up to the size of each dimension have been filled.
            Used to validate that an experiment has left no holes, e.g. skipping some 
            trials or steps.
        """
        # TODO: Implement validate_filled

    def __str__(self) -> str:
        return f"<{[self.__dimension_names]}>"
