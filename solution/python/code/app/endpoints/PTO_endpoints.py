import sqldatabase_declaration.Model_implementation as decl
from function_classer import notify_manager,name_to_id,create_session,Pto_available
from flask import jsonify,Blueprint
import datetime


session=create_session()
Ptorequester = Blueprint('Ptorequester', __name__) #might need to add template folder and static folder
#test purposes

@Ptorequester.route('/PTO/request/<lastname_guard>/<date>',methods=['PUT'])
def pto_scheduler(lastname_guard,date):
    ''''
    Takes in two parameters to delete determine if Guard is allowed to book PTO and commits it if so
    :PARAM lastname_guard,date
    :RETURN json Succes statement

    ''' 
    guard_id=name_to_id(lastname_guard)
    if Pto_available(guard_id):
        return jsonify({'PTO':'already have PTO scheduled'})#would have to update the database that if the date of the pto passes the record get deleted might do that if time allows it
    else:
        Pto_request=decl.PTO(Emp_id=guard_id,PTO_date=datetime.datetime.strptime(date,"%d-%m-%Y"))
        notify_manager(lastname_guard,date) #later we can implement to only schedule time off when we get a response from manager
        session.add(Pto_request)
        session.commit()
        return jsonify({'PTO':'Requested'})

