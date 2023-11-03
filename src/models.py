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
    full_name: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    abbreviation: Mapped[str] = mapped_column(String(3))
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
