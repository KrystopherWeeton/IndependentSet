import cProfile
import io
import pstats
from pstats import SortKey


def profile(f):
    """Wrapper which wraps a profiler with output around a function"""
    def wrapped(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        f(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print("---------------PROFILER------------------------------------")
        print(s.getvalue())
        print("-----------------------------------------------------------")
        pass
    return wrapped
