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

# @app.route('/bsg-people')
# def bsg_people():
#     query = "SELECT * FROM bsg_people;"
#     cursor = db.execute_query(db_connection=db_connection, query=query)
#     results = cursor.fetchall()
#     return render_template("bsg.j2", bsg_people=results)

@app.route('/bands', methods = ['POST', 'GET'])
def bands():
    if request.method == "POST":
        print("Hello")
        bandName = request.form['bandName']
        numMembers = request.form['numMembers']
        genre = request.form['genre']

        if bandName == '':
            return
        if numMembers == '':
            numMembers = None
        if genre == "":
            genre = None
        
        insertQuery = "INSERT INTO `Bands` (`bandName`, `numMembers`, `genre`) VALUES (%s,%s,%s);"
        insertTuple = (bandName, numMembers, genre)
        insertCursor = db.execute_query(db_connection=db_connection, query=insertQuery, query_params=insertTuple) 
        print(insertTuple)

    query = "SELECT * from Bands;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("bands.j2", Bands=results)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    app.run(port=port, debug=True) 