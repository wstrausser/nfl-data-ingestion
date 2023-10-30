from datetime import datetime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from typing import Optional

from src.global_variables import METADATA_OBJ


# Base class
class Base(DeclarativeBase):
    metadata = METADATA_OBJ


# Tables
class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    result_updated: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    game_id: Mapped[str] = mapped_column(String(20))
    season: Mapped[int]
    week: Mapped[int]
    home_team: Mapped[str] = mapped_column(String(3))
    away_team: Mapped[str] = mapped_column(String(3))
    result: Mapped[Optional[str]] = mapped_column(String(3))

    def exists(self, session):
        q = session.query(Game).filter(
            Game.game_id == self.game_id,
        )
        exists = session.query(q.exists()).first()[0]
        return exists

    def existing_record(self, session):
        q = session.query(Game).filter(
            Game.game_id == self.game_id,
        )
        existing_record = q.first()
        return existing_record
