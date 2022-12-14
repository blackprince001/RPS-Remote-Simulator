import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from rps_remote_simulator.database.models import Base

@pytest.fixture(scope="session")
def engine():
    return create_engine(url="sqlite+pysqlite:///:memory:", future=True)

@pytest.fixture
def db(engine):
    with Session(engine) as session:
        Base.metadata.create_all(bind=engine)
        yield session