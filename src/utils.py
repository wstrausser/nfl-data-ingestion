import nfl_data_py as nfl
import pandas as pd
import numpy as np
from src.global_variables import NOW


def get_schedule():
    seasons = get_available_seasons()
    df = nfl.import_schedules(seasons)

    df = df[["game_id", "season", "week", "home_team", "away_team"]]

    schedules = df.copy()

    columns = [
        "game_id",
        "total_home_score",
        "total_away_score",
        "desc",
    ]

    df = nfl.import_pbp_data(years=seasons, columns=columns)

    df = df[df["desc"] == "END GAME"]

    df = df[["game_id", "total_home_score", "total_away_score"]]

    for col in df.columns[1:]:
        df[col] = df[col].astype(int)

    results = df.copy()

    df = pd.merge(
        left=schedules,
        right=results,
        how="left",
        on="game_id",
    )

    df["result"] = np.where(
        df["total_home_score"] > df["total_away_score"],
        df["home_team"],
        np.where(
            df["total_home_score"] < df["total_away_score"],
            df["away_team"],
            np.where(
                df["total_home_score"] == df["total_away_score"],
                "TIE",
                np.nan,
            ),
        ),
    )

    return df.to_dict("records")


def get_available_seasons():
    min_season = 2009
    if NOW.month > 8:
        max_season = NOW.year
    else:
        max_season = NOW.year - 1
    return list(range(min_season, max_season + 1))
