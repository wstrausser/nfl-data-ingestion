from datetime import (
    date,
    datetime,
    time,
)
from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    select,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from typing import (
    List,
    Optional,
)

from src import utils
from src.global_variables import (
    METADATA_OBJ,
    NOW,
)


# Base class
class Base(DeclarativeBase):
    metadata = METADATA_OBJ


# Tables
class Team(Base):
    __tablename__ = "teams"

    team_id: Mapped[int] = mapped_column(primary_key=True)
    abbreviation: Mapped[str] = mapped_column(String(3))
    name: Mapped[str] = mapped_column(String(50))
    mascot: Mapped[str] = mapped_column(String(50))
    conference: Mapped[str] = mapped_column(String(3))
    division: Mapped[str] = mapped_column(String(10))
    color_1: Mapped[str] = mapped_column(String(7))
    color_2: Mapped[str] = mapped_column(String(7))
    color_3: Mapped[Optional[str]] = mapped_column(String(7))
    color_4: Mapped[Optional[str]] = mapped_column(String(7))
    logo: Mapped[str] = mapped_column(Text)
    wordmark: Mapped[str] = mapped_column(Text)

    team_home_games: Mapped[List["Game"]] = relationship(
        "Game", back_populates="game_home_team", foreign_keys="Game.home_team_id"
    )
    team_away_games: Mapped[List["Game"]] = relationship(
        "Game", back_populates="game_away_team", foreign_keys="Game.away_team_id"
    )

    def __init__(self, record, session):
        self.abbreviation = record["team_abbr"]
        self.name = record["team_name"]
        self.mascot = record["team_nick"]
        self.conference = record["team_conf"]
        self.division = record["team_division"]
        self.color_1 = record["team_color"]
        self.color_2 = record["team_color2"]
        self.color_3 = record["team_color3"]
        self.color_4 = record["team_color4"]
        self.logo = record["team_logo_wikipedia"]
        self.wordmark = record["team_wordmark"]

        self.exists = self.check_exists(session)

    def __repr__(self):
        obj_dict = self.__dict__
        obj_dict.pop("_sa_instance_state")

        for key, value in obj_dict.items():
            if isinstance(value, tuple) and len(value) == 1:
                obj_dict[key] = value[0]
        string_rep = str(obj_dict).replace("{", "(").replace("}", ")")
        return f"Team{string_rep}"

    def check_exists(self, session):
        stmt = select(Team).where(Team.abbreviation == self.abbreviation)
        first = session.execute(stmt).first()
        if first is not None:
            self.existing_record = first[0]
            return True
        else:
            self.existing_record = None
            return False

    def insert(self, session):
        if not self.exists:
            session.add(self)

    def from_abbreviation(abbreviation, session):
        stmt = select(Team).where(Team.abbreviation == abbreviation)
        return session.execute(stmt).first()[0]


class Game(Base):
    __tablename__ = "games"

    game_id: Mapped[int] = mapped_column(primary_key=True)
    result_updated: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    api_game_id: Mapped[str] = mapped_column(String(20))
    season: Mapped[int]
    week: Mapped[int]
    game_date: Mapped[date]
    game_time: Mapped[time]
    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id", ondelete="CASCADE", onupdate="CASCADE")
    )
    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id", ondelete="CASCADE", onupdate="CASCADE")
    )
    home_score: Mapped[Optional[int]]
    away_score: Mapped[Optional[int]]

    game_home_team: Mapped[Team] = relationship(
        "Team", back_populates="team_home_games", foreign_keys="Game.home_team_id"
    )
    game_away_team: Mapped[Team] = relationship(
        "Team", back_populates="team_away_games", foreign_keys="Game.away_team_id"
    )

    def __init__(self, record, session):
        self.result_updated = NOW
        self.api_game_id = record["game_id"]
        self.season = record["season"]
        self.week = record["week"]
        self.game_date = date.fromisoformat(record["gameday"])
        self.game_time = time.fromisoformat(record["gametime"])
        self.home_score = record["home_score"]
        self.away_score = record["away_score"]

        self.game_home_team = Team.from_abbreviation(
            abbreviation=record["home_team"], session=session
        )
        self.game_away_team = Team.from_abbreviation(
            abbreviation=record["away_team"], session=session
        )

        self.exists = self.check_exists(session)

    def __repr__(self):
        obj_dict = self.__dict__
        obj_dict.pop("_sa_instance_state")

        for key, value in obj_dict.items():
            if isinstance(value, tuple) and len(value) == 1:
                obj_dict[key] = value[0]
        string_rep = str(obj_dict).replace("{", "(").replace("}", ")")
        return f"Game{string_rep}"

    def check_exists(self, session):
        stmt = select(Game).where(Game.api_game_id == self.api_game_id)
        first = session.execute(stmt).first()
        if first is not None:
            return True
        else:
            return False

    def insert(self, session):
        if not self.exists:
            session.add(self)

    def update(self, new, session):
        if self.home_score != new.home_score and self.away_score != new.away_score:
            self.result_updated = NOW
            self.home_score = new.home_score
            self.away_score = new.away_score

            session.add(self)

    def from_api_game_id(api_game_id, session):
        stmt = select(Game).where(Game.api_game_id == api_game_id)
        return session.execute(stmt).first()[0]
