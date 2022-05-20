import sqldatabase_declaration.Model_implementation as decl
from function_classer import create_session,sorter,date_config
from flask import Flask, jsonify,request,Blueprint
import datetime
import json



session=create_session()

Schedule_display = Blueprint('Schedule_display', __name__) #might need to add template folder and static folder

#test purposes

@Schedule_display.route('/schedule',methods=['GET'])
def displayschedule():
    date_1=request.json['date_1']
    date_2=request.json['date_2']
    ''''
    Takes in two dates ( in this format 5-2-2022 ) and calulates the range in the schedule based on it
    :PARAM date1,date2
    :RETURN range of schedules

    ''' 
    if date_1 is None or date_2 is None:
        return 'ERROR enter date to see schedule'

    #schedule=[('5-1-2022', "Sally's Mall", "Jackson"), ('5-2-2022', "Sally's Mall", "Sarah"), ('5-3-2022', "Sally's Mall", "Jackson"),('5-4-2022', "Sally's Mall", "Jackson"),('5-5-2022', "Sally's Mall", "Jackson"),('5-6-2022', "Sally's Mall", "Jackson"),('5-7-2022', "Sally's Mall", "Jackson")]
    #schedule above for reference test cases only

    #uncomment to work with database data
    schedule=sorter()
    
    '''
    take in the begin date and end date for the range 
    then we select these from the list and put them into a variable
    we make a new list with indices to create the correct range
    then we add the tags onto it with a dictionary for the jsonformat
    then we do a json dump
    we return this
    '''

    #begin=[i for i in schedule if i[0]==date_1][0]
    #end=[i for i in schedule if i[0]==date_2][0]

    #if len(begin)<1 or len(end)<1:
    #    return jsonify({'Data':'Not found'})
    #returnschedule=[i for i in schedule[schedule.index(begin):schedule.index(end)+1]]
    #key=['Date','company','guard']
    #data = [dict(zip(key, user)) for user in returnschedule]
    #json_data = json.dumps(data)
    #return json_data
    
    #this one line argument is faster but harder to read for more readable format look above 
    return json.dumps([dict(zip(['Date','Company','Guard'], i)) for i in schedule[schedule.index([i for i in schedule if i[0]==date_1][0]):schedule.index([i for i in schedule if i[0]==date_2][0])+1]])
   



   

#have to lookinto the safest way to avoid sql injection I know its not important but still good practice 


