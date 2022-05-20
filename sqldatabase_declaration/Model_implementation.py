from sqlalchemy import DATETIME, Column, ForeignKey, Integer, String,Boolean,TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import datetime



# ---------------------------------------------
Base = declarative_base()


class requr_Contract(Base):
    created=datetime.datetime.now()
    __tablename__ = 'Contract'
    Contract_id = Column(Integer, primary_key=True)
    Contract_name = Column(String(250), nullable=False)
    #Days_of_Week = Column(String(1500), nullable=False) #debating doing a bitwise operator here or just fields for everyday would def make queries easier also might just store a list in here
    weekd_mo = Column(Boolean,default=False, nullable=False)
    weekd_tu = Column(Boolean,default=False, nullable=False)
    weekd_we = Column(Boolean,default=False, nullable=False)
    weekd_th = Column(Boolean,default=False, nullable=False)
    weekd_fr = Column(Boolean,default=False, nullable=False)
    weekd_sa = Column(Boolean,default=False, nullable=False)
    weekd_su = Column(Boolean,default=False, nullable=False)
    Armed_Guard_req = Column(Boolean,default=False,nullable=False)
    Shift_start = Column(TIME, nullable=False)
    Shift_end = Column(TIME, nullable=False)
    Guard_on_site = Column(Integer,default=False, nullable=False)
    Contract_start=Column(DATETIME, default=created, nullable=False)
    Contract_end=Column(DATETIME, nullable=True) #currently true because contracts havent ended yet
    


class emp_Guard(Base):#if spare time left can add a emp id and link this with schedules already
    __tablename__ = 'Guard'
    Emp_id = Column(Integer, primary_key=True)
    First_name = Column(String(250), nullable=False)
    Last_name = Column(String(1500), nullable=False)
    Armedguard_lic = Column(Boolean,default=False, nullable=False)


class PTO(Base):
    __tablename__ = 'PTO'
    PTO_id=Column(Integer, primary_key=True)#not sure if this is needed but to avoid messing with the primary keys makes the most sense
    Emp_id = Column(Integer, ForeignKey('Guard.Emp_id')) # in the future when a pto date passes delete the record
    PTO_date=Column(DATETIME, nullable=True)
    Guard_id = relationship(emp_Guard)

#class Schedulereg(Base):
#    __tablename__ = 'Schedule'
#    Contract_date = Column(DATETIME, nullable=False)
#    Contract_name = Column(String(250), ForeignKey('Contract.Contract_name'))
#    Guardname = Column(String(250), ForeignKey('Guard.Lastname'))
        




engine = create_engine('sqlite:////Users/vanlaere/Documents/RESTAPIrepo/Belfry assignment/guard-scheduling-jpyonj/solution/python/code/schedule.sqlite3',echo=True) 
Base.metadata.create_all(engine)



