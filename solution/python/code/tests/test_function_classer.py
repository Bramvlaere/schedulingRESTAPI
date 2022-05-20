from urllib import response

from click import Tuple
import function_classer
import datetime

#might use a class here
class tester():
    def __init__(self,input1,input2) -> None:
        self.input1=input1
        self.input2=input2


def test_base_route(client):
    response = client.get('/')
    assert response.get_data() == b'Home of Belfry'
    assert response.status_code == 200

#database test calls need to be done in unit test before these pass
#def test_duplicate_check_found_duplicates(client):
#    assert(function_classer.duplicate_check("Evans"), True)
#database test calls need to be done in unit test before these pass
#def test_name_to_id(client):
#    assert(function_classer.name_to_id("Evans"), 1)

def test_Pto_available(client):
    assert(function_classer.Pto_available(4), False)

def test_Pto_available_Not(client):
    assert(function_classer.Pto_available(3), True)

def test_notify_manager(client):
    assert(function_classer.notify_manager('Evans','05-05-2022'), 'Email sent!')

def test_datecount(client):
    assert(function_classer.datecount(datetime.datetime.strptime('2022/05/17',"%Y/%m/%d"),[True,True,True,True,True,True,True],5),list)

def test_date_config(client):
    assert(function_classer.date_config('2022/05/17'),'2022-05-17')

def test_availablechecker_fail(client):
    assert(function_classer.availablechecker(datetime.datetime.strptime('2022/05/17',"%Y/%m/%d"),{}),False)

def test_availablechecker_success(client):
    assert(function_classer.availablechecker(datetime.datetime.strptime('2022/05/17',"%Y/%m/%d"),{4:[['cvs',datetime.datetime.strptime('2022/05/17',"%Y/%m/%d")]]}),4)

def test_logger_day_only(client):
    assert(function_classer.logger(None,None,1),True)

def test_logger_day_id_only(client):
    assert(function_classer.logger(4),True)

def test_logger_day_id_and_day(client):
    assert(function_classer.logger(4,True),True)

def test_match(client):
    assert(function_classer.match('CVS',datetime.datetime.strptime('2022/05/17',"%Y/%m/%d"),[[4,datetime.datetime.strptime('2022/05/17',"%Y/%m/%d")]],[{4:['Evans',True]}]),Tuple)

