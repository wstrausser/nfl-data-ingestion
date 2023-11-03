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

from src.global_variables import METADATA_OBJ


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
    color_3: Mapped[str] = mapped_column(String(7))
    color_4: Mapped[str] = mapped_column(String(7))
    logo: Mapped[str] = mapped_column(Text)
    wordmark: Mapped[str] = mapped_column(Text)

    team_home_games: Mapped[List["Game"]] = relationship("Game", back_populates="game_home_team", foreign_keys="Game.home_team_id")
    team_away_games: Mapped[List["Game"]] = relationship("Game", back_populates="game_away_team", foreign_keys="Game.away_team_id")

    def __init__(self, record):
            self.abbreviation = record['team_abbr'],
            self.name = record['team_name'],
            self.mascot = record['team_nick'],
            self.conference = record['team_conf'],
            self.division = record['team_division'],
            self.color_1 = record['team_color'],
            self.color_2 = record['team_color2'],
            self.color_3 = record['team_color3'],
            self.color_4 = record['team_color4'],
            self.logo = record['team_logo_wikipedia'],
            self.wordmark = record['team_wordmark'],
    
    def __repr__(self):
         obj_dict = self.__dict__
         obj_dict.pop("_sa_instance_state")

         for key, value in obj_dict.items():
              if isinstance(value, tuple) and len(value) == 1:
                   obj_dict[key] = value[0]
         return f"{obj_dict}"

    def exists(self, session):
        stmt = select(Team).where(Team.abbreviation==self.abbreviation)
        first = session.execute(stmt).first()
        if first is not None:
             self.existing_record = first
             return True
        else:
             self.existing_record = None
             return False



class Game(Base):
    __tablename__ = "games"

    game_id: Mapped[int] = mapped_column(primary_key=True)
    result_updated: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    api_game_id: Mapped[str] = mapped_column(String(20))
    season: Mapped[int]
    week: Mapped[int]
    game_date: Mapped[date]
    game_start_time: Mapped[time]
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.team_id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.team_id"))
    home_score: Mapped[Optional[int]]
    away_score: Mapped[Optional[int]]

    game_home_team: Mapped[Team] = relationship("Team", back_populates="team_home_games", foreign_keys="Game.home_team_id")
    game_away_team: Mapped[Team] = relationship("Team", back_populates="team_away_games", foreign_keys="Game.away_team_id")

    def exists(self, session):
        q = session.query(Game).filter(
            Game.api_game_id == self.api_game_id,
        )
        exists = session.query(q.exists()).first()[0]
        return exists

    def existing_record(self, session):
        q = session.query(Game).filter(
            Game.api_game_id == self.api_game_id,
        )
        existing_record = q.first()
        return existing_record
