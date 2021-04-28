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

            insertQuery = "INSERT INTO `Events` (`eventName`, `eventDate`, `eventType`, `eventLocation`, `eventCity`, `eventState`) VALUES (%s,%s,%s,%s,%s,%s);"
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
                 FROM Events e
                 LEFT JOIN BandsEvents be on e.eventID = be.eventID
                 LEFT JOIN Bands b on b.bandID = be.bandID;"""    
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    uniqueEvents = set()
    uniqueBands = set()
    for x in results:
        if x.get('eventName') != None:
            uniqueEvents.add(x.get('eventName'))
        if x.get('bandName') != None:
            uniqueBands.add(x.get('bandName'))
    print(uniqueEvents)
    return render_template("bandsevents.j2", BE=results, uniqueEvents=uniqueEvents, uniqueBands=uniqueBands)

@app.route('/customers', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def customers():
    if request.method == "POST":
        customerFirst = request.form['customerFirst']
        customerLast = request.form['customerLast']
        customerDoB = request.form['customerDoB']
        phoneNum = request.form['phoneNum']
        email = request.form['email']

        if customerFirst == '': customerFirst = None
        if customerLast == '': customerLast = None
        if phoneNum == '': phoneNum = None
        if phoneNum == '': phoneNum = None
        if email == '': email = None
        
        insertQuery = "INSERT INTO `Customers` (`customerFirst`, `customerLast`, `customerDoB`,`phoneNum`, `email`) VALUES (%s,%s,%s,%s,%s);"
        insertTuple = (customerFirst, customerLast, customerDoB, phoneNum, email)
        insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple) 
    

    query = "SELECT * from Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("customers.j2", Customers=results)

@app.route('/tickets', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def tickets():
    query = """SELECT t.orderDate
                    , t.price
                    , e.eventDate
                    , e.eventName
                    , c.customerFirst
                    , c.customerLast
                    , c.email
                 FROM Events e
                 LEFT JOIN Tickets t on e.eventID = t.eventID
                 LEFT JOIN Customers c on c.customerID = t.customerID;"""    
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    uniqueEvents = set()
    uniqueCustomers = set()
    for x in results:
        if x.get('eventName') != None:
            uniqueEvents.add(x.get('eventName'))
        if x.get('customerFirst') != None:
            uniqueCustomers.add(x.get('customerFirst') + " " + x.get('customerLast'))
    print(uniqueCustomers)

    return render_template("tickets.j2", Tickets=results, uniqueEvents=uniqueEvents, uniqueCustomers=uniqueCustomers)

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 