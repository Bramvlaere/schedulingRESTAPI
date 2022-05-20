import pytest
from app import server

#i did not write a test here for the sqlite server

@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client 

