from datetime import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Canada/Pacific")
NOW = datetime.now(TIMEZONE)

PG_LOCN = os.getenv("PG_LOCN")
PG_DTBS = os.getenv("PG_DTBS")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
SCHEMA = "schedule"

DB_URL = rf"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_LOCN}/{PG_DTBS}"

ENGINE = create_engine(DB_URL)
METADATA_OBJ = MetaData(schema=SCHEMA)
