## Overview

Notably, there isn't a clear separation; however, it appears as if results (for sizes) at least are bimodal around really bad runs and really good runs. E.g., we may need to show (rather than that all runs succeed), that runs either fail horribly or perform really well (very unconcentrated inbetween). Playing around with the threshold `log_2(n)` is definitely too low of a random restart point and most likely `n/c` is closer to the restart point we want (because at this point, if the threshold is satisfied, almost all runs maintain the invariant we want). So we may be able to show that starting from this point (with a minimum size) the rest of it works really well?

One note for the calculations is that the invariant may be a bit too soft / vanishing constant, etc. so we need to be careful to be as loose as possible for this.


## TODO

Definitely still need to look at what the intersection size is (relative to the size) at the random restart point, as well as what the size of the runs is at the random restart point (for all runs as well as specifically for the successful runs). This will give an idea of whether the threshold is too successful. Also coloring these by invariant satisfying runs as well as non-invariant satisfying runs would be REALLY nice because then we could use that to determine a reasonable threshold (at least for this value of n)?