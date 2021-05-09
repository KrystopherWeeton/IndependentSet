import itertools
import numpy as np
from typing import Tuple, List
from pprint import pprint
import math
import copy


def mean(X: np.array) -> float:
    return sum(X) / X.size


class ResultTensor:
    def __init__(self):
        self.__dimension_names: [str] = []
        self.__dimension_sizes: [int] = []
        self.__dimension_keys: [[int]] = []
        self.__dimension_indices: dict = {}
        self.__num_dimensions = 0
        self.dimensions_fixed = False

        self.results = None
        self.results_total = -1
        self.results_collected = -1
        self.__index_list = []


    def __dim_size(self, dimension: str) -> int:
        return self.__dimension_sizes[self.__dimension_indices[dimension]]    


    # Might not be strictly necessary, but not bad to do overall    
    def keys(self, dimension: str) -> [int]:
        return copy.copy(self.__dim_keys(dimension))


    def __dim_keys(self, dimension: str) -> [int]:
        return self.__dimension_keys[self.__dimension_indices[dimension]]

    
    def __get_index(self, dimension: str, key: int) -> int:
        return self.__dim_keys(dimension).index(key)


    def add_dimension(self, dimension_name: str, dimension_keys: [int]):
        if self.dimensions_fixed:
            raise Exception("Attempt to add a dimension to a result object when the dimension have already been fixed")
        
        self.__dimension_names.append(dimension_name)
        self.__dimension_sizes.append(len(dimension_keys))
        self.__dimension_keys.append(dimension_keys)
        self.__dimension_indices[dimension_name] = len(self.__dimension_names) - 1
        self.__num_dimensions += 1


    def fix_dimensions(self):
        # Set trackers
        self.dimensions_fixed = True

        # Initialize the results object to track all the actual results now
        self.results = np.zeros(self.__dimension_sizes)
        self.results_collected = 0
        self.results_total = np.prod(self.__dimension_sizes)
        self.__index_list = list(itertools.product(*self.__dimension_keys))

    
    def __validate_kwargs_access(self, kwargs):
        if len(kwargs) != self.__num_dimensions:
            raise Exception("Wrong number of dimensions for accessing results dict.")
        items = list(kwargs.items())
        for i in range(self.__num_dimensions):
            dimension, k = items[i]
            if dimension != self.__dimension_names[i]:
                raise Exception("Wrong ordering of dimensions for accessing results dict.")
            if k not in self.__dimension_keys[i]:
                raise Exception("Bad key passed into results dict access")

    
    def __to_indices(self, kwargs) -> Tuple:
        return tuple([self.__get_index(dim, k) for dim, k in kwargs.items()])

    
    def add_result(self, result, **kwargs) -> bool:
        if not self.dimensions_fixed:
            raise Exception("Attempt to add result with dimensions not fixed in results dict")

        self.__validate_kwargs_access(kwargs)
        indices = self.__to_indices(kwargs)
        self.results[indices] = result
        self.results_collected += 1
        #result.put(indices, result)


    def get_results(self, **kwargs) -> bool:
        if not self.dimensions_fixed:
            raise Exception("Attempt to get result with dimensions not fixed in results dict")

        self.__validate_kwargs_access(kwargs)
        indices = self.__to_indices(kwargs)
        return self.results[indices]
        #result.put(indices, result)


    def all_results_collected(self) -> bool:
        return self.results_collected == self.results_total


    def collapse_to_matrix(self, f = mean) -> np.ndarray:
        m: np.array = np.zeros(self.__dimension_sizes[0:2])
        outer_size: int = self.__dimension_sizes[0]
        inner_size: int = self.__dimension_sizes[1]
        for r in range(outer_size):
            for c in range(inner_size):
                m[r][c] = f(self.results[r][c])
        return m

    
    def collapse_to_list(self, f = mean) -> np.ndarray:
        m: np.array = np.zeris(self.__dimension_sizes[0])
        size: int = self.__dimension_sizes[0]
        for r in range(size):
            m[r] = f(self.results[r])
        return m


    def collapse_to_2d_list(self, f = mean) -> [(int, float)]:
        M = self.collapse_to_matrix(f)
        l: [(int, float)] = []
        keys = self.__dimension_keys[0]

        for row in range(M.shape[0]):
            for col in range(M.shape[1]):
                key = keys[row]
                l.append((key, M[row][col]))
        return l


    def get_index_list(self) -> List:
        return copy.copy(self.__index_list)


    def __str__(self) -> str:
        return f"<{[self.__dimension_names]}>"