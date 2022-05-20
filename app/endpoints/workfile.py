
'''
DOCUMENT IS SOLEY CREATED AS A SANDBOX TO WRITE CODE IN 
NO CODE FOUND HERE ACTS LIVE IN THE API CALLS
YOU WILL FIND HERE UNFINISHED CODE OR SNIPPETS USED IN PRODUCTION
'''










from flask import Flask,Blueprint,request
import sqldatabase_declaration.Model_implementation as decl
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

from app.endpoints.guard_endpoints import guard_modify
from app.endpoints.contract_endpoints import Contract_modify

app = Flask(__name__)
#app.register_blueprint(guard_modify, url_prefix='')
#app.register_blueprint(Contract_modify, url_prefix='') #i potentially could use similar blueprints here for adding and deleting if the field where different if time allows i might look into it
#possability to make the code more scalable if rewritting the modify apis

#don't forget to add docstring to functions
'''



def checker(check,dbstr):
    for i in contractlist:
        for k,v in i.items():
            for z in v:
                for y,t in z.items():
                    if y==check:
                        pass

    datesched=[]
    startnum=start.weekday()
    if week[startnum]:
        datesched=[start]
        curr=0
        for x in range(3):
            if x==0:
                for i in week[startnum:]:
                    if i==False:
                        curr+=1
                        print(i)
                    else:
                        datesched.append(datesched[-1]+datetime.timedelta(days=i+curr))
                        curr=0
                        print(i)
                    
            else:
                for i in week:
                    if i==False:
                        curr+=1
                        print(i)
                    else:
                        datesched.append(datesched[-1]+datetime.timedelta(days=i+curr))
                        curr=0
                        print(i)

'''


#not used
def finddate(s):
    scale = [0,1,2,3,4,5,6]
    scale=scale[-s:]+scale[:s+1]
    return scale




class schedinquery:
    def __init__(self,cdate,cname,gname):
        self.cdate=datetime.strptime(cdate,"%Y-%m-%d").date()
        self.cname=cname
        self.gname=gname
        


newinq=schedinquery('2019-08-02','Chase','Peter')
newinq.returner()


#if __name__ == '__main__':
#    app.run(debug=True)


'''
   
    for i in mapper:
        print(i,scale.index(i),scale)
        #if i==startnum:
            #datesched.append(datesched[-1]+datetime.timedelta(days=1))
        datesched.append(datesched[-1]+datetime.timedelta(days=scale[i]))
    #for x in range(5):

    for i in mapper:
            print(i,startnum)
            print(len(datesched))
            if i==startnum and start not in datesched:
                datesched.append(start)
            elif len(datesched)!=0:
                x=datesched[-1]+datetime.timedelta(days=1)
                if x.weekday() in mapper:
                    datesched.append(x)
                else:
                    for day in mapper:
                        print(day)
                        x=datesched[-1]+datetime.timedelta(days=day)
                        print(x)
                        print(x.weekday(),mapper,datesched[-1].weekday())
                        if x.weekday() in mapper :
                            datesched.append(x)
                            break
            else:
                pass





def datecount(start,week):
    datesched=[]
    mapper=[i for i,v in enumerate(week) if v]
    print(mapper)
    startnum=start.weekday()
    for x in range(5):
        for i in mapper:
                print(i,startnum)
                print(len(datesched))
                if i==startnum and start not in datesched:
                    datesched.append(start)
                elif len(datesched)!=0:
                    x=datesched[-1]+datetime.timedelta(days=1)
                    if x.weekday() in mapper:
                        datesched.append(x)
                    else:
                        for day in mapper:
                            print(day)
                            x=datesched[-1]+datetime.timedelta(days=day)
                            print(x)
                            print(x.weekday(),mapper,datesched[-1].weekday())
                            if x.weekday() in mapper :
                                datesched.append(x)
                                break
                else:
                    pass


                        
    return(datesched)

- Schedule: 
    - Represented as a list of ( Date - Contract name - Guard name) tuples.
    - When scheduling guards to shifts, we want to:
        - Ensure all shifts are filled.
        - Minimize overtime
            - Any hours worked over 40 hours in a given contiguous 7 day period are counted as overtime hours.
            - Making sure all shifts are filled is more important than minimizing overtime.
        - All licensing requirements are respected.
        - Return an error message for shifts which are unable to be filled given the limitation of available guards.    
    - Example:
        - [(05-01-2022, "Sally's Mall", "Jackson"), (05-02-2022, "Sally's Mall", "Sarah"), (05-03-2022, "Sally's Mall", "Jackson")]

'''