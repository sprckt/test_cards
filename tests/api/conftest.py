import pytest
from cards import CardsDB, Card


@pytest.fixture(scope='session')
def db_session(tmpdir_factory):
    db_path = tmpdir_factory.mktemp('data').join('.cards_db.json')
    db = CardsDB(db_path)
    assert 0 == db.count()
    return db


@pytest.fixture()
def db_empty(db_session):
    db = db_session
    db.delete_all()
    assert 0 == db.count()
    return db


@pytest.fixture()
def db_non_empty(db_session):
    db = db_session
    db.add(Card(summary='first item'))
    db.add(Card(summary='second item'))
    db.add(Card(summary='third item'))
    return db
