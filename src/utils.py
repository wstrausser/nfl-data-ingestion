import nfl_data_py as nfl
import pandas as pd
import numpy as np
from src.global_variables import NOW


def get_available_seasons():
    min_season = 2009
    if NOW.month > 8:
        max_season = NOW.year
    else:
        max_season = NOW.year - 1
    return list(range(min_season, max_season + 1))
