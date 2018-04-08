import DistBetDest
import EZ_Cal
from flask import *
app = Flask(__name__)
 
@app.route("/")
def login():
    return render_template('home.html')
 
@app.route("/itinerary")
def hello():
    return "Hello World!" 
 
@app.route("/calendar")
def members():
    return "Members"
 
@app.route("/members/<string:name>/")
def getMember(name):
    return name
 
if __name__ == "__main__":
    app.run()