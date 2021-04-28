from flask import Flask, render_template, request
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/bands', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def bands():
    if request.method == "POST":
        bandName = request.form['bandName']
        numMembers = request.form['numMembers']
        genre = request.form['genre']

        if bandName == '':
            bandName = None
        if numMembers == '':
            numMembers = None
        if genre == '':
            genre = None
        
        insertQuery = "INSERT INTO `Bands` (`bandName`, `numMembers`, `genre`) VALUES (%s,%s,%s);"
        insertTuple = (bandName, numMembers, genre)
        insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple) 
    
    elif request.method == "PUT":
        print('we want to modify some data')
    
    elif request.method == "DELETE":
        print('we want to delete some data')

    query = "SELECT * from Bands;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("bands.j2", Bands=results)

@app.route('/events', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def events():
    if request.method == "POST":
            eventName = request.form['eventName']
            eventDate = request.form['eventDate']
            eventType = request.form['eventType']
            eventLocation = request.form['eventLocation']
            eventCity = request.form['eventCity']
            eventState = request.form['eventState']

            if eventName == '': eventName = None
            if eventDate == '': 
                eventDate = None
            elif eventDate != '':
                date = eventDate[0:10]
                time = eventDate[11:]
                time += ':00'
                eventDate = date + ' ' + time
            if eventType == '': eventType = None
            if eventLocation == '': eventLocation = None
            if eventCity == '': eventCity = None
            if eventState == '': eventState = None

            insertQuery = "INSERT INTO `Events` (`eventName`, `eventDate`, `eventType`, `eventLocation`, `eventCity`, `eventState`);"
            insertTuple = (eventName, eventDate, eventType, eventLocation, eventCity, eventState)
            insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple) 
        
    query = "SELECT * from Events;"    
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("events.j2", Events=results)

@app.route('/bandsevents', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def bandsandevents():
    if request.method == "POST":
            bandName = request.form['bandName']
            eventName = request.form['eventName']
            if bandName == '': bandName = None
            if eventName == '': eventName = None

            insertQuery = "INSERT INTO `BandsEvents` (`bandID`, `eventID`) VALUES ((SELECT bandID from Bands where bandName = %s),(SELECT eventID from Events where eventName = %s));"
            insertTuple = (bandName, eventName)
            insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple)

    query = """SELECT b.bandName
                    , e.eventName
                    , e.eventDate
                    , e.eventLocation
                    , e.eventCity
                    , e.eventState
                 FROM bandcart.Bands b
                 LEFT JOIN bandcart.BandsEvents be on b.bandID = be.bandID
                 LEFT JOIN Events e on e.eventID = be.eventID;"""    
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    print(results)
    return render_template("bandsevents.j2", BE=results)

@app.route('/customers', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def customers():

    query = "SELECT * from Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("customers.j2", Customers=results)

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 