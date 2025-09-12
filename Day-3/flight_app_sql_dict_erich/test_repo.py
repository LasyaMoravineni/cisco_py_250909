import pytest
from db import db_setup
from db import repo_sql_dict as repo

@pytest.fixture(autouse=True)
def setup():
    db_setup.Base.metadata.drop_all(db_setup.engine)
    #
    db_setup.Base.metadata.create_all(db_setup.engine)
    yield
    db_setup.Base.metadata.drop_all(db_setup.engine)

def test_create_flight():
    fl={'id':100,'flight_number':'IB75','airline':'IndiGo','seats':900,'price':8000,'source':'Bangalore','destination':'Hyderabad'}
    repo.create_flight(fl)

    savedFlight = repo.read_by_id(100)
    assert (savedFlight!=None)
    assert (savedFlight['id']==100)
    assert (savedFlight['flight_number']=='IB75')
    assert (savedFlight['airline']=='IndiGo')
    assert (savedFlight['seats']==900)
    assert (savedFlight['source']=='Bangalore')
    assert (savedFlight['destination']=='Hyderabad')