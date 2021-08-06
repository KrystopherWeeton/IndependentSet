import copy
import itertools
from typing import List, Tuple

import numpy as np

import util.tensor as tensor


def mean(X: np.array) -> float:
    return sum(X) / X.size


class ResultTensor:
    def __init__(self):
        self.__dimension_names: List[str] = []
        self.__dimension_sizes: List[int] = []
        self.__dimension_keys: List[List[int]] = []
        self.__dimension_indices: dict = {}
        self.__num_dimensions = 0
        self.dimensions_fixed = False

        self.results: np.ndarray = None
        self.results_total = -1
        self.results_collected = -1
        self.__index_list = []

    def __dim_size(self, dimension: str) -> int:
        return self.__dimension_sizes[self.__dimension_indices[dimension]]

    # Might not be strictly necessary, but not bad to do overall
    def keys(self, dimension: str) -> List[int]:
        return copy.copy(self.__dim_keys(dimension))
    
    def __get_dimension_index(self, dimension: str) -> int:
        """ Returns the index of the dimension """
        return self.__dimension_indices[dimension]

    def __dim_keys(self, dimension: str) -> List[int]:
        """ Returns the keys for the specified dimension as a list """
        dim_index: int = self.__get_dimension_index(dimension)
        return self.__dimension_keys[dim_index]

    def __get_index(self, dimension: str, key: int) -> int:
        """ Returns the appropriate index for the tensor from the provided key """
        return self.__dim_keys(dimension).index(key)

    def add_dimension(self, dimension_name: str, dimension_keys: List[int]):
        if self.dimensions_fixed:
            raise Exception(
                "Attempt to add a dimension to a result object when the dimension have already been fixed"
            )

        self.__dimension_names.append(dimension_name)
        self.__dimension_sizes.append(len(dimension_keys))
        self.__dimension_keys.append(dimension_keys)
        self.__dimension_indices[dimension_name] = len(self.__dimension_names) - 1
        self.__num_dimensions += 1

    def fix_dimensions(self):
        # Set trackers
        self.dimensions_fixed = True

        # Initialize the results object to track all the actual results now
        self.results: np.ndarray = np.zeros(self.__dimension_sizes)
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
                raise Exception(
                    "Wrong ordering of dimensions for accessing results dict."
                )
            if k not in self.__dimension_keys[i]:
                raise Exception(f"Bad key passed into results dict access\nKey: {k}\tKeys:{self.__dimension_keys[i]}")

    def __to_indices(self, kwargs) -> Tuple:
        return tuple([self.__get_index(dim, k) for dim, k in kwargs.items()])

    def add_result(self, result, **kwargs) -> bool:
        if not self.dimensions_fixed:
            raise Exception(
                "Attempt to add result with dimensions not fixed in results dict"
            )

        self.__validate_kwargs_access(kwargs)
        indices = self.__to_indices(kwargs)
        self.results[indices] = result
        self.results_collected += 1
        # result.put(indices, result)

    def get_results(self, **kwargs) -> bool:
        if not self.dimensions_fixed:
            raise Exception(
                "Attempt to get result with dimensions not fixed in results dict"
            )

        self.__validate_kwargs_access(kwargs)
        indices = self.__to_indices(kwargs)
        return self.results[indices]
        # result.put(indices, result)

    def all_results_collected(self) -> bool:
        return self.results_collected == self.results_total

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

    def collapse_to_2d_list(self, f=mean) -> List[Tuple[int, float]]:
        M = self.collapse_to_matrix(f)
        l: List[Tuple[int, float]] = []
        keys = self.__dimension_keys[0]

        for row in range(M.shape[0]):
            for col in range(M.shape[1]):
                key = keys[row]
                l.append((key, M[row][col]))
        return l
    
    def get_sub_tensor(self, dimension_name: str, index: int) -> tensor.tensor:
        """
            Returns a sub-tensor restricted to `index` at dimension `dimension_name`

            EXAMPLE:
                x.get_sub_tensor("trial", t)

                > Returns sub-tensor corresponding to a specific trial
        """
        entry_index: int = self.__get_index(dimension_name, index)
        dim_index: int = self.__get_dimension_index(dimension_name)
        return tensor.get_sub_tensor(self.results, dim_index, entry_index)

    def get_index_list(self) -> List:
        return copy.copy(self.__index_list)

    def __str__(self) -> str:
        return f"<{[self.__dimension_names]}>"
