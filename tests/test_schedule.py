import json


def test_base_route(client):
    """test main page"""
    response = client.get('/')
    assert b'Home of Belfry' in response.data

#this is with the example of the schedule to change to live data base call uncomment schedule=sorter()
#database test calls need to be done in unit test before this test can be done with database data
def test_schedule_endpoint_data(client):
    """GET the endpoint data """
    url = '/schedule'
    mock_request_dates = {

    "date_1":"5-1-2022",
    "date_2":"5-2-2022"
    }
    response = client.get(url, data=json.dumps(mock_request_dates),content_type='application/json')
    assert response.status_code == 200


def test_schedule_endpoint_data_json(client):
    """GET the endpoint data """
    url = '/schedule'
    mock_request_dates = {

    "date_1":"5-1-2022",
    "date_2":"5-2-2022"
    }

    assert(client.get(url, data=json.dumps(mock_request_dates),content_type='application/json'),'application/json')



    