import sqldatabase_declaration.Model_implementation as decl
from function_classer import duplicate_check,create_session
from flask import request,jsonify,Blueprint



session=create_session()


guard_modify = Blueprint('guard_modify', __name__) #might need to add template folder and static folder

@guard_modify.route('/guard/new-guard',methods=['POST'])
def add_guard():
    ''''
    Takes in info through json (guard lastname) request to create new guard and commits it to the database after it checks if there are no duplicates
    :PARAM None
    :RETURN json Succes statement

    ''' 
    if duplicate_check(request.json['Lastname']):
        return jsonify({'Guard':'already in database'})
    else:
        a_guard=decl.emp_Guard(Emp_id=request.json['Emp_id'],First_name=request.json['Firstname'],Last_name=request.json['Lastname'],Armedguard_lic=request.json['Armedguard_lic'])
        session.add(a_guard)
        session.commit()
        return jsonify({a_guard.First_name:'added'})


#have to lookinto the safest way to avoid sql injection I know its not important but still good practice 

@guard_modify.route('/guard/end/<emp_id>',methods=['DELETE'])
def del_guard(emp_id):
    ''''
    Takes in info as parameter(guard employee id) to delete guarding matching with the id
    :PARAM emp_id:emp_id
    :RETURN json Succes statement

    ''' 
    d_guard = session.query(decl.emp_Guard).get(emp_id)
    if d_guard is None:
        return {'No guard was found'}
    session.delete(d_guard)
    session.commit()
    return jsonify({"Deleted": f"{d_guard.First_name}!"})
