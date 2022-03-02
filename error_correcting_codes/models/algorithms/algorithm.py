from typing import List, Union


class Algorithm:

    def __init__(self, solution_class, verbose=False, debug=False):
        self._solution_class = solution_class
        self._verbose: bool = verbose
        self._debug: bool = debug
        self._solution: solution_class = None
    
    def __print(self, msg: Union[str, List[str]], condition):
        if condition:
            if isinstance(msg, List):
                msg = "\n".join(msg)
            print(f"[V] {msg}")

    def verbose_print(self, msg: Union[str, List[str]]):
        self.__print(msg, self._verbose)

    def debug_print(self, msg: Union[str, List[str]]):
        self.__print(msg, self._debug)

    def step_hook(self, *args):
        if self._step_hook is not None:
            self._step_hook(**args)
    
    def phase_hook(self, *args):
        if self._phase_hook is not None:
            self._phase_hook(**args)
    
    def clear(self):
        self._solution = None
        self._seed = None
        self._clear()

    def _is_solution(self, sol) -> bool:
        return isinstance(sol, self._solution_class)
    
    def set_solution(self, solution):
        if not self._is_solution(solution):
            raise Exception("Bad Solution Type")
        self._solution = solution
    
    def get_solution(self):
        if self._solution == None:
            raise Exception("Attempt to get none solution")
        return self._solution

    def run(self, seed = None, **kwargs):
        self.clear()
        if seed is not None:
            if not self._is_solution(seed):
                raise Exception(f"Seed is not correct type. seed={seed}")
            self._seed = seed
        self._run(**kwargs)
        if not self._is_solution(self._solution):
            raise Exception(f"Solution is of wrong type after running algorithm. solution={self._solution}")

    def _clear(self):
        raise NotImplementedError()

    def _run(self):
        raise NotImplementedError()
