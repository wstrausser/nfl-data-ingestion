import nfl_data_py as nfl
from numpy import nan
from sqlalchemy.orm import Session

from src import utils
from src.global_variables import (
    ENGINE,
    NOW,
)
from src.models import (
    Game,
    Team,
)


def update_teams():
    print("Retrieving raw teams data...")
    teams_raw = nfl.import_team_desc()
    teams_raw = teams_raw.replace(nan, None)
    print("Updating teams table...")
    with Session(ENGINE) as session:
        for team in teams_raw.to_dict("records"):
            team_obj = Team(team, session)
            team_obj.insert(session)

        session.commit()


def update_games(seasons="latest"):
    print("Retrieving raw games data...")
    available_seasons = utils.get_available_seasons()
    if seasons == "all":
        games_raw = nfl.import_schedules(available_seasons)
    elif seasons == "latest":
        games_raw = nfl.import_schedules(available_seasons[-1:])
    games_raw = games_raw.replace(nan, None)
    records = games_raw.to_dict("records")

    print("Updating games table...")
    with Session(ENGINE, autoflush=False) as session:
        for record in records:
            game_obj = Game(record=record, session=session)
            if game_obj.exists:
                existing_game_obj = Game.from_api_game_id(game_obj.api_game_id, session)
                existing_game_obj.update(game_obj, session)
            else:
                game_obj.insert(session)

        session.commit()
