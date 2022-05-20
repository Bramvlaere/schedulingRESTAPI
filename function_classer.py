import smtplib
import sqldatabase_declaration.Model_implementation as decl
from sqlalchemy import create_engine, false,text
import datetime
from sqlalchemy.orm import sessionmaker
from copy import deepcopy

#sql statements would need .format( table_name = sql.Identifier(table_name),limit = sql.Literal(limit) to be absolutly safe might still implement later

schedule=[]
contract_armreq=[]
contract_nonarmreq=[]
arm_g=[]
non_g=[]
hourlog=[] # structured like this [empid,hours worked in 7 day week,current day in 7 day period]
reg={}



def create_session():
    ''''
    shortcut to create session to the database
    :PARAM None
    :RETURN session object

    ''' 
    engine = create_engine('sqlite:////Users/vanlaere/Documents/RESTAPIrepo/Belfry assignment/guard-scheduling-jpyonj/solution/python/code/schedule.sqlite3',echo=True) 
    decl.Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

session=create_session()


def duplicate_check(last_name):
        ''''
    checks in the guard table of the database if the name exists if so returns yes
    :PARAM last_name guard
    :RETURN Boolean

        ''' 
        exist = session.query(decl.emp_Guard).from_statement(text(f"SELECT * FROM Guard WHERE Last_name LIKE '%{last_name}%'")).all()
        if exist:return True


def name_to_id(last_name):
    ''''
    takes in the last name of a guard and returns the employee id if only 1 guard is found
    :PARAM last_name guard
    :RETURN Emp_id

     ''' 
    guard_emp_id = session.query(decl.emp_Guard).from_statement(text(f"SELECT Emp_id from Guard WHERE Last_name LIKE '%{last_name}%'")).all()
    if len(guard_emp_id)>1:
        raise Exception("multiple People found")
    id_from_name=[i.Emp_id for i in guard_emp_id]
    return id_from_name[0]

def Pto_available(Emp_id):
        ''''
    takes in employee id and looks if somebody already has pto scheduled
    :PARAM Emp_id
    :RETURN Boolean

        ''' 
        available = session.query(decl.PTO).from_statement(text(f"SELECT * FROM PTO WHERE Emp_id LIKE '%{Emp_id}%'")).all()
        if available:return True
        

def notify_manager(Guard_lastname,date):
    #later down the line i would convert this to amazon ses like the file included here above its more scalable but due to them needing to approve it this was the easier purpose for demonstration
    ''''
    Sends out an email based on the guard and the date it takes in to notify the future manaeger
    :PARAM guard last_name,Date
    :RETURN None

    ''' 
    gmail_user = 'bram.vanlaere@codeimmersives.com'
    gmail_password = 'Stad8483'

    sent_from = gmail_user
    to = ['bram.vanlaere@codeimmersives.com']
    subject = 'PTO REQUEST Belfry'
    body = f'Hi there,\n you just got a request from {Guard_lastname} on Belfry to take time off on {date} \n'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
    return'Email sent!'


def datecount(start,week,contractlength):
    #contractlength=contractlength*52 make it yearly input
    '''
    Function that take in the first day of the contract and looks at the schedule given by the company
    then the function calculates the next schedule for the period of contract length
    '''
    datesched=[start]
    startnum=start.weekday()
    curr=0
    for x in range(contractlength): #3 for testing purposes (shows schedule for the next 3-4 weeks)
        if x==0:
            for i in week[startnum+1:]:
                if i==False:
                    curr+=1
                else:
                    datesched.append(datesched[-1]+datetime.timedelta(days=i+curr))
                    curr=0
                
        else:
            for i in week:
                if i==False:
                    curr+=1
                else:
                    datesched.append(datesched[-1]+datetime.timedelta(days=i+curr))
                    curr=0


                        
    return(datesched)


def date_config(date):
    '''
    Takes Date and reconfigures it
    '''
    date=date.replace('/','-')
    return date


def availablechecker(date,reg):
    '''
    Based on the register we are going to check if the person or employee ID is already working or not by matching the date
    :PARAM date,register
    :RETURN employee id
    
    '''
    if len(reg)!=0:
        for k,v in reg.items():
            for regitem in v:
                if date==regitem[1]:
                    return k
    else: return False


def regupdater(item,reg):
    '''
    small function to keep a register who worked takes in the existing register and updates it like a regular dictionary if its not already in there
    :PARAM item is a dictionary and so is reg
    :RETURN None
    
    '''
    for k,v in item.items():
        if k not in reg:
            reg[k]=[v]
        elif k in reg:
            reg[k].append(v)


def logger(id=0,overtimelogging=False,day=0):
    #Making sure all shifts are filled is more important than minimizing overtime.
    #in future overtime could be limited here building that after 4 workdays automatically it puts in a rest day
    '''
    the function looks if the day is true or not if so we add a counted day to the hourlog
    if day is false we look to assign the workhours to the person with the id entered
    :PARAM id,overtimelogger,day
    :RETURN Boolean

    '''
    if day:
        for i in hourlog:
            if i[-1]>=7:
                i[-1]=0
                i[1]=0
            else:
                i[-1]+=1
        return True
    if overtimelogging: #this might need another look
        for i in hourlog:
            if i[0]==id:
                if i[-1]>=7:
                 i[-1]=0
                 i[1]=0
                 return True
                elif i[-1]<7 and i[1]<40:
                    i[1]+=10
                    return True
                elif i[-1]<7 and i[1]>40 :
                    i[1]+=20
                    return True
    else:
        for i in hourlog:
            if i[0]==id:
                if i[-1]<7 and i[1]<40:
                    i[1]+=10
                    return True
                elif i[-1]<7 and i[1]>=40 :
                    return False
                elif i[-1]>=7:
                    i[-1]=0
                    i[1]=0
                    return True


def match(company,date,ptolist,reqguardlist):
    '''
    Takes in company,date,ptolist,and guard list armed or unarmed based on this the match function returns the person optimal to work
    :PARAM Company,date,ptolist,guardlist
    :RETURN tuple
    '''
    logger(None,None,1)
    availlist=deepcopy(reqguardlist)
    date=date.strftime("%m/%d/%Y")
    #print(date)
    for i in reqguardlist:
        for k,v in i.items():
            if k==availablechecker(date,reg):
                print(f'found conflict for{v} and is removed from list')
                availlist.remove(i)
                #print('only available',availlist)
    for i in availlist:
        for k,v in i.items():
            for ptoitem in ptolist:
                x=ptoitem[1].strftime("%m/%d/%Y")
                if k==ptoitem[0]:
                    if date==x:
                        print(f'CANT ASSIGN {v[0]} ON {ptoitem[1]}')
                        availlist.remove(i)
                        if len(availlist)==0:
                            return f'[Error] This shift could not be filled nobody is available'
                        else:break

                    else: 
                        if len(availlist)==0:
                            return f'[Error] This shift could not be filled nobody is available'
                        else:
                            if logger(k):
                                reglog={k:(company,date)}
                                regupdater(reglog,reg)
                                print(reglog,'assigned')
                                return (date_config(date),company,v[0])#could be a good use of recursion here
                            else:
                                if len(availlist)==0:
                                    return f'[Error] This shift could not be filled nobody is available'
                                else:break
                else:
                    if len(availlist)==0:
                            return f'[Error] This shift could not be filled nobody is available'
                    else:
                        if logger(k):
                            reglog={k:(company,date)}
                            regupdater(reglog,reg)
                            print(reglog,'assigned')
                            return (date_config(date),company,v[0])
                        else: 
                            if len(availlist)==0:
                                logger(k,True) #forcing here to run overtime 
                                print(f'{v[0]} has been scheduled to work overtime')
                                reglog={k:(company,date)}
                                print(reglog,'assigned')
                                regupdater(reglog,reg)
                                return (date_config(date),company,v[0])                           #return f'[Error] This shift could not be filled nobody is available Due to Overtime'
                                
                            else:break
                                

                    

def sorter():
    contracall = session.query(decl.requr_Contract).from_statement(text(f"SELECT * from Contract")).all()
    guardall = session.query(decl.emp_Guard).from_statement(text(f"SELECT * from Guard")).all()
    ptoall = session.query(decl.PTO).from_statement(text(f"SELECT * from PTO")).all()
    contractlist=[{i.Contract_id:[{'Company info':[i.Contract_name,i.Contract_start]},{'Weeksched':[i.weekd_mo,i.weekd_tu,i.weekd_we,i.weekd_th,i.weekd_fr,i.weekd_sa,i.weekd_su]},{'Armed:':i.Armed_Guard_req},{'Shift time':[i.Shift_start,i.Shift_end]},{'Guards on site':i.Guard_on_site}]} for i in contracall]
    Guardlist=[{i.Emp_id:[i.Last_name,i.Armedguard_lic]} for i in guardall]
    PTOlist=[[i.Emp_id,i.PTO_date] for i in ptoall]

    for i in contractlist:
        for k,v in i.items():
            for z in v:
                for y,t in z.items():
                    if y=='Armed:':
                        if t:contract_armreq.append(i)
                        else:contract_nonarmreq.append(i) #sort by arm requirement maybe used a little bit to much lists/dictionaries here

    for i in Guardlist:
        for k,v in i.items():
            hourlog.append([k,0,0])
            if v[1]:arm_g.append(i)
            else:non_g.append(i)

    constructschedule=[]

    for i in contract_armreq:
        for x,y in i.items():
            for z in y:
                #print(z)
                for k,v in z.items():
                    #print(k,v)
                    if k=='Company info':
                        cname=v[0]
                        cstartingdate=v[1]
                        #print(cstartingdate)
                    elif k=='Weeksched':
                        weeksched=v
                        #print(weeksched)
                    elif k=='Guards on site':
                        personalreq=v
                        #print(personalreq)
            oneschedule=[(i,cname) for i in datecount(cstartingdate,weeksched,4)]
            constructschedule.append(oneschedule)

    #schedule=[i for i in constructschedule]

    for i in constructschedule:
        for x in i:
            #print(x)
            scheduleitem=match(x[1],x[0],PTOlist,arm_g)
            schedule.append(scheduleitem)
            #print(hourlog)



    for i in contract_nonarmreq:
        for x,y in i.items():
            for z in y:
                #print(z)
                for k,v in z.items():
                    #print(k,v)
                    if k=='Company info':
                        cname=v[0]
                        cstartingdate=v[1]
                        #print(cstartingdate)
                    elif k=='Weeksched':
                        weeksched=v
                        #print(weeksched)
                    elif k=='Guards on site':
                        personalreq=v
                        #print(personalreq)
            oneschedule=[(i,cname) for i in datecount(cstartingdate,weeksched,4)]
            constructschedule.append(oneschedule)

    #schedule=[i for i in constructschedule]

    for i in constructschedule:
        for x in i:
            #print(x)
            scheduleitem=match(x[1],x[0],PTOlist,non_g)
            schedule.append(scheduleitem)
            #print(hourlog)
    return(schedule)






        


