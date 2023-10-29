#!/usr/local/bin/python

import nfl_data_py as nfl
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from schedule_ingestion.models import Game
from schedule_ingestion.global_variables import ENGINE

if __name__ == '__main__':
    seasons = [2023]
    df = nfl.import_schedules(seasons)

    df = df[['game_id', 'season', 'week', 'home_team', 'away_team']]

    schedules = df.copy()

    columns=[
        'game_id',
        'total_home_score',
        'total_away_score',
        'desc',
    ]

    df = nfl.import_pbp_data(
        years=seasons,
        columns=columns
    )

    df = df[df['desc'] == 'END GAME']

    df = df[['game_id', 'total_home_score', 'total_away_score']]

    for col in df.columns[1:]:
        df[col] = df[col].astype(int)

    results = df.copy()

    df = pd.merge(
        left=schedules,
        right=results,
        how='left',
        on='game_id',
    )

    # df = df[df['game_id'].str.contains('NYJ')]

    df['result'] = np.where(
        df['total_home_score'] > df['total_away_score'],
        df['home_team'],
        np.where(
            df['total_home_score'] < df['total_away_score'],
            df['away_team'],
            np.where(
                df['total_home_score'] == df['total_away_score'],
                'TIE',
                np.nan,
            )
        )
    )

    data = df.to_dict('records')

    with Session(ENGINE) as session:
        for record in data:
            new_game = Game(
                game_id = record['game_id'],
                season = record['season'],
                week = record['week'],
                home_team = record['home_team'],
                away_team = record['away_team'],
                result = record['result']
            )
            session.add(new_game)
        session.commit()
