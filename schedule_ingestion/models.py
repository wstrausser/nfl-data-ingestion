
from sqlalchemy import (
    String
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from schedule_ingestion.global_variables import METADATA_OBJ


# Base class
class Base(DeclarativeBase):
    metadata = METADATA_OBJ


# Tables
class Account(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[str] = mapped_column(String(20))
    season: Mapped[int]
    week: Mapped[int]
    home_team: Mapped[str] = mapped_column(String(3))
    away_team: Mapped[str] = mapped_column(String(3))
    result: Mapped[str] = mapped_column(String(3))
