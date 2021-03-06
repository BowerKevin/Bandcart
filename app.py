from flask import Flask, render_template, request
import os
import database.db_connector as db
from datetime import date
# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 
today = date.today()

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/bands', methods = ['POST', 'GET'])
def bands():
    PUT = False
    Bresults = None
    Error = False
    if request.method == "POST":
        if "bandName" in request.form:
            bandName = request.form['bandName']
            numMembers = request.form['numMembers']
            genre = request.form['genre']

            if bandName == '': 
                Error = True
                return render_template("bands.j2", Error = Error)
            if numMembers == '': numMembers = None
            if genre == '': genre = None

            query = "SELECT * from bands;"
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()
            for row in results:
                if row['bandName'] == bandName:
                    Error = True
                    return render_template("bands.j2", Error = Error)

            insertQuery = "INSERT INTO `bands` (`bandName`, `numMembers`, `genre`) VALUES (%s,%s,%s);"
            insertTuple = (bandName, numMembers, genre)
            insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple) 
        elif "PUT" in request.form:
            PUT = True
            bandID = request.form["PUT"]
            print(bandID)
            bandQuery = "SELECT * from bands where bandID = %s;"
            bandTuple = (bandID, )
            cursor = db.execute_query(db_connection=db_connection, query=bandQuery, query_params=bandTuple)
            Bresults = cursor.fetchall()
        elif "updateRequest" in request.form:
            bandID = request.form["bandIDU"]
            bandName = request.form["bandNameU"]
            numMembers = request.form["numMembersU"]
            genre = request.form["genreU"]
            if numMembers == '': numMembers = None
            if genre == '': genre = None
            updateTuple = (bandName, numMembers, genre, bandID)
            updateQuery = "UPDATE `bands` SET `bandName` = %s, `numMembers` = %s, `genre` = %s where `bandID` = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=updateQuery, query_params=updateTuple)
        elif "DEL" in request.form:
            bandID = request.form['DEL']
            deleteMtM = "DELETE from `bandsevents` where `bandID` = %s;"
            deleteQuery = "DELETE from `bands` where `bandID` = %s;"
            deleteTuple = (bandID, )
            cursor = db.execute_query(db_connection=db_connection, query=deleteMtM, query_params=deleteTuple)    
            cursor = db.execute_query(db_connection=db_connection, query=deleteQuery, query_params=deleteTuple)      
    
    query = "SELECT * from bands;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("bands.j2", Bands=results, Bresults=Bresults, PUT=PUT)

@app.route('/events', methods = ['POST', 'GET'])
def events():
    PUT = False
    Bresults = None
    valueDate = ''
    Error = False
    if request.method == "POST":
        if "eventName" in request.form:
            eventName = request.form['eventName']
            eventDate = request.form['eventDate']
            eventType = request.form['eventType']
            eventCity = request.form['eventCity']
            eventState = request.form['eventState']

            if eventName == '' or eventDate == '' or eventDate == '' or eventType == '' or eventCity == '' or eventState == '':
                Error = True
                return render_template("events.j2", Error = Error)
            if eventDate != '':
                date = eventDate[0:10]
                time = eventDate[11:]
                time += ':00'
                eventDate = date + ' ' + time
            
            query = "SELECT * from events;"
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()
            for row in results:
                if row['eventName'] == eventName:
                    Error = True
                    return render_template("bands.j2", Error = Error)

            insertQuery = "INSERT INTO `events` (`eventName`, `eventDate`, `eventType`, `eventCity`, `eventState`) VALUES (%s,%s,%s,%s,%s);"
            insertTuple = (eventName, eventDate, eventType, eventCity, eventState)
            insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple) 
        elif "PUT" in request.form:
            PUT = True
            eventID = request.form["PUT"]
            eventQuery = "SELECT * from events where eventID = %s;"
            eventTuple = (eventID, )
            cursor = db.execute_query(db_connection=db_connection, query=eventQuery, query_params=eventTuple)
            Bresults = cursor.fetchall()
            fullDate = str(Bresults[0]['eventDate'])
            date = (fullDate[:10])
            time = (fullDate[11:16])
            valueDate = date + "T" + time
        elif "updateRequest" in request.form:
            eventID = request.form["eventIDU"]
            eventName = request.form["eventNameU"]
            eventDate = request.form["eventDateU"]
            eventType = request.form["eventTypeU"]
            eventCity = request.form["eventCityU"]
            eventState = request.form["eventStateU"]
            if eventName == '': eventName = None
            if eventDate == '': 
                eventDate = None
            elif eventDate != '':
                date = eventDate[0:10]
                time = eventDate[11:]
                time += ':00'
                eventDate = date + ' ' + time
            if eventType == '': eventType = None
            if eventCity == '': eventCity = None
            if eventState == '': eventState = None
            updateTuple = (eventName, eventType, eventDate, eventCity, eventState, eventID)
            updateQuery = "UPDATE `events` SET `eventName` = %s, `eventType` = %s, `eventDate` = %s, `eventCity` = %s, `eventState` = %s where `eventID` = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=updateQuery, query_params=updateTuple)
        elif "DEL" in request.form:
            eventID = request.form['DEL']
            deleteMtM = "DELETE from `bandsevents` where `eventID` = %s;"
            deleteQuery = "DELETE from `events` where `eventID` = %s;"
            deleteTuple = (eventID, )
            cursor = db.execute_query(db_connection=db_connection, query=deleteMtM, query_params=deleteTuple)    
            cursor = db.execute_query(db_connection=db_connection, query=deleteQuery, query_params=deleteTuple) 

    query = "SELECT * from events;"    
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    print(today)
    return render_template("events.j2", Events=results, Bresults=Bresults, PUT=PUT, valueDate = valueDate, today=today)

@app.route('/bandsevents', methods = ['POST', 'GET'])
def bandsandevents():
    if request.method == "POST":
        if "delBand" in request.form:
            bandID = request.form['delBand']
            eventID = request.form['delEvent']
            deleteQuery = "DELETE from `bandsevents` where `bandID` = %s and `eventID` = %s;"
            deleteTuple = (bandID, eventID)  
            cursor = db.execute_query(db_connection=db_connection, query=deleteQuery, query_params=deleteTuple)      
    
        else:
            bandName = request.form['bandName']
            eventName = request.form['eventName']

            queryEventName = "SELECT eventID from events where eventName = %s;"
            queryBandName = "SELECT bandID from bands where bandName = %s;"
            cursorEventName = db.execute_query(db_connection=db_connection, query=queryEventName, query_params=(eventName,))
            cursorBandName = db.execute_query(db_connection=db_connection, query=queryBandName, query_params=(bandName,))
            resultsEN = cursorEventName.fetchall()
            resultsBN = cursorBandName.fetchall()
            eventID = resultsEN[0]['eventID']
            bandID = resultsBN[0]['bandID']
            print(eventID, bandID)

            queryAll = "SELECT * from bandsevents;"
            cursorAll = db.execute_query(db_connection=db_connection, query=queryAll)
            resultsAll = cursorAll.fetchall()
            for row in resultsAll:
                if row['eventID'] == eventID and row['bandID'] == bandID:
                    Error = True
                    return render_template("bandsevents.j2", Error = Error)

            insertQuery = "INSERT INTO `bandsevents` (`bandID`, `eventID`) VALUES ((SELECT bandID from bands where bandName = %s),(SELECT eventID from events where eventName = %s));"
            insertTuple = (bandName, eventName)
            insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple)

    query = """SELECT e.eventID
                    , b.bandID
                    , b.bandName
                    , e.eventName
                    , e.eventDate
                    , e.eventCity
                    , e.eventState
                 FROM events e
                 LEFT JOIN bandsevents be on e.eventID = be.eventID
                 LEFT JOIN bands b on b.bandID = be.bandID;"""

    query2 = """SELECT b.bandID 
                    , b.bandName
                    , e.eventName
                    , e.eventDate
                    , e.eventCity
                    , e.eventState
                 FROM bands b
                 LEFT JOIN bandsevents be on b.bandID = be.bandID
                 LEFT JOIN events e on e.eventID = be.eventID;"""

    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()
    
    uniqueEvents = set()
    uniqueBands = set()

    for x in results:
        if x.get('eventName') != None:
            uniqueEvents.add(x.get('eventName'))
    
    for x in results2:
        if x.get('bandName') != None:
            uniqueBands.add(x.get('bandName'))
    return render_template("bandsevents.j2", BE=results, EV=results2, uniqueEvents=uniqueEvents, uniqueBands=uniqueBands)

@app.route('/customers', methods = ['POST', 'GET'])
def customers():
    Error = False
    PUT = False
    Cresults = None
    if request.method == "POST":
        if 'customerFirst' in request.form:
            customerFirst = request.form['customerFirst']
            customerLast = request.form['customerLast']
            customerDoB = request.form['customerDoB']
            phoneNum = request.form['phoneNum']
            email = request.form['email']

            if customerFirst == '' or customerLast == '' or customerDoB == '' or phoneNum == '' or email == '':
                Error = True
                return render_template("customers.j2", Error = Error)
            
            insertQuery = "INSERT INTO `customers` (`customerFirst`, `customerLast`, `customerDoB`,`phoneNum`, `email`) VALUES (%s,%s,%s,%s,%s);"
            insertTuple = (customerFirst, customerLast, customerDoB, phoneNum, email)
            insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple) 
        elif "DEL" in request.form:
            customerID = request.form["DEL"]
            deleteCustomer = "DELETE from `customers` where `customerID` = %s;"
            deleteTuple = (customerID,)
            cursor = db.execute_query(db_connection=db_connection, query=deleteCustomer, query_params=deleteTuple)
            deleteTickets = "DELETE from `tickets` where `customerID` =%s;"
            deleteTuple = (customerID,)
            cursor = db.execute_query(db_connection=db_connection, query=deleteTickets, query_params=deleteTuple)
        elif 'PUT' in request.form:
            PUT = True
            customerID = request.form["PUT"]
            customerQuery = "SELECT * from customers where customerID = %s;"
            customerTuple = (customerID, )
            cursor = db.execute_query(db_connection=db_connection, query=customerQuery, query_params=customerTuple)
            Cresults = cursor.fetchall()
            print(Cresults)
        elif 'updateRequest' in request.form:
            customerID = request.form["customerIDU"]
            customerFirst = request.form["customerFirstU"]
            customerLast = request.form["customerLastU"]
            customerDoB = request.form["customerDoBU"]
            phoneNum = request.form["phoneNumU"]
            email = request.form["emailU"]
            if customerFirst == '' or customerLast == '' or customerDoB == '' or phoneNum == '' or email == '':
                Error = True
                return render_template("customers.j2", Error = Error)

            updateTuple = (customerFirst, customerLast, customerDoB, phoneNum, email, customerID)
            updateQuery = "UPDATE `customers` SET `customerFirst` = %s, `customerLast` = %s, `customerDoB` = %s, `phoneNum` = %s, `email` = %s where `customerID` = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=updateQuery, query_params=updateTuple)    

    query = "SELECT * from customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("customers.j2", Customers=results, Cresults=Cresults, PUT=PUT)

@app.route('/tickets', methods = ['POST', 'GET'])
def tickets():
    Error = False
    if request.method == "POST":
        if "filterEvent" in request.form:
            filterEvent = request.form['filterEvent']
            query1 = """SELECT t.orderDate
                    , t.price
                    , t.numTickets
                    , e.eventDate
                    , e.eventName
                    , c.customerFirst
                    , c.customerLast
                    , c.email
                 FROM events e
                 LEFT JOIN tickets t on e.eventID = t.eventID
                 LEFT JOIN customers c on c.customerID = t.customerID
                 WHERE eventName = %s;""" 
            insertTuple = (filterEvent, )
            print(insertTuple)
            cursor = db.execute_query(db_connection=db_connection, query=query1, query_params=insertTuple)
            results = cursor.fetchall()
            return render_template("ticketsFiltered.j2", Tickets=results)
        elif 'DEL' in request.form:
            ticketID = request.form['DEL']
            deleteTicket = "DELETE from `tickets` where `ticketID` = %s;"
            deleteTuple = (ticketID, )
            cursor = db.execute_query(db_connection=db_connection, query=deleteTicket, query_params=deleteTuple)
        else:
            customerName = request.form['customerName']
            eventName = request.form['eventName']
            custList = customerName.split(' ')
            customerFirst = custList[0]
            customerLast = custList[1]

            orderDate = request.form['orderDate']
            price = request.form['price']
            numTickets = request.form['numTickets']

            if orderDate == '' or price == '' or numTickets == '': 
                Error = True
                return render_template("tickets.j2", Error = Error)

            insertQuery = """INSERT INTO `tickets` (`orderDate`, `price`, `numTickets`, `customerID`, `eventID`) VALUES 
            (%s, %s, %s,
            (SELECT customerID from customers where customerFirst = %s and customerLast = %s),
            (SELECT eventID from events where eventName = %s));"""
            insertTuple = (orderDate, price, numTickets, customerFirst, customerLast, eventName)
            insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple)

    query1 = """SELECT t.ticketID 
                    , t.orderDate
                    , t.price
                    , t.numTickets
                    , e.eventDate
                    , e.eventName
                    , c.customerFirst
                    , c.customerLast
                    , c.email
                 FROM events e
                 LEFT JOIN tickets t on e.eventID = t.eventID
                 LEFT JOIN customers c on c.customerID = t.customerID;"""  

    query2 = """SELECT t.orderDate
                    , t.price
                    , t.numTickets
                    , e.eventDate
                    , e.eventName
                    , c.customerFirst
                    , c.customerLast
                    , c.email
                 FROM customers c
                 LEFT JOIN tickets t on c.customerID = t.customerID
                 LEFT JOIN events e on t.eventID = e.eventID;"""  
    
    cursor = db.execute_query(db_connection=db_connection, query=query1)
    results = cursor.fetchall()
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()

    uniqueEvents = set()
    uniqueCustomers = set()
    for x in results:
        if x.get('eventName') != None:
            uniqueEvents.add(x.get('eventName'))
    for x in results2:
        if x.get('customerFirst') != None:
            uniqueCustomers.add(x.get('customerFirst') + " " + x.get('customerLast'))

    return render_template("tickets.j2", Tickets=results, uniqueEvents=uniqueEvents, uniqueCustomers=uniqueCustomers)

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 