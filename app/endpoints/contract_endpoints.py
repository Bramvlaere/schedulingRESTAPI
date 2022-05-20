import sqldatabase_declaration.Model_implementation as decl
from function_classer import create_session
from flask import request,Blueprint,jsonify
import datetime

session=create_session()


Contract_modify = Blueprint('Contract_modify', __name__) #might need to add template folder and static folder

@Contract_modify.route('/contract/new-contract',methods=['POST'])
def Add_Contract():
    ''''
    Takes in info through json request to create new contract and commits it to the database
    :PARAM None
    :RETURN json Succes statement

    ''' 
    a_contract=decl.requr_Contract(
        Contract_id=request.json['Contract_id'],Contract_name=request.json['Contract_name'],
        weekd_mo=request.json['wd_mo'],weekd_tu=request.json['wd_tu'],weekd_we=request.json['wd_we'],weekd_th=request.json['wd_th'],weekd_fr=request.json['wd_fr'],weekd_sa=request.json['wd_sa'],weekd_su=request.json['wd_su'],
        Armed_Guard_req=request.json['ArmedGuardreq'],
        Shift_start=datetime.datetime.strptime(request.json['Shift_start'],'%H:%M').time(),Shift_end=datetime.datetime.strptime(request.json['Shift_end'],'%H:%M').time(),
        Guard_on_site=request.json['Guardonsite'])
    session.add(a_contract)
    session.commit()
    return jsonify({"Succes": f"{a_contract.Contract_name}!"})


#have to lookinto the safest way to avoid sql injection I know its not important but still good practice 

@Contract_modify.route('/contract/end/<Contract_id>',methods=['DELETE'])
def Del_Contract(Contract_id):

    ''''
    Looks up contract based on id and deletes it if found
    :PARAM Contract_id:Contract_id
    :RETURN json deleted statement

    ''' 
    d_contract = session.query(decl.requr_Contract).get(Contract_id)
    if d_contract is None:
        return jsonify({'Contract':'Not found'})
    session.delete(d_contract)
    session.commit()
    return jsonify({"Deleted": f"{d_contract.Contract_name}!"})
