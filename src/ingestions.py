from sqlalchemy.orm import Session
from tqdm import tqdm

from src import utils
from src.global_variables import (
    ENGINE,
    NOW,
)
from src.models import Game


def update_games(seasons=None):
    print("Retrieving raw data...")
    data = utils.get_schedule(seasons)

    with Session(ENGINE) as session:
        print("Processing games...")
        for record in tqdm(
            data,
        ):
            game = Game(
                game_id=record["game_id"],
                season=record["season"],
                week=record["week"],
                home_team=record["home_team"],
                away_team=record["away_team"],
                result=record["result"],
            )

            if game.exists(session):
                game = game.existing_record(session)
                if game.result != record["result"]:
                    game.result_updated = NOW
                    game.result = record["result"]
                    session.add(game)
            else:
                game.result_updated = NOW
                session.add(game)
            game.result = record["result"]

        print("Updating database...")
        session.commit()
