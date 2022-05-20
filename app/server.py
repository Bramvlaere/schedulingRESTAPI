from flask import Flask
from app.endpoints.guard_endpoints import guard_modify
from app.endpoints.contract_endpoints import Contract_modify
from app.endpoints.schedule_endpoints import Schedule_display
from app.endpoints.PTO_endpoints import Ptorequester

app = Flask(__name__)
app.register_blueprint(guard_modify, url_prefix='')
app.register_blueprint(Contract_modify, url_prefix='') #i potentially could use similar blueprints here for adding and deleting if the field where different if time allows i might look into it
app.register_blueprint(Schedule_display, url_prefix='')
app.register_blueprint(Ptorequester, url_prefix='')
#possability to make the code more scalable if rewritting the modify apis

@app.route('/')
def index():
    return 'Home of Belfry'

if __name__ == '__main__':
    app.run(debug=True) #have turned debugging on for the sake of allowing to save while running server