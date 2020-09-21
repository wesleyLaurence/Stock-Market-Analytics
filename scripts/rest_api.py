from flask import Flask 
from flask_cors import CORS 
from flask import jsonify, request
import pymongo 
import getpass
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
  
password = getpass.getpass('Password: ')
collection_title = 'Users'
connection_url = "mongodb+srv://wesley:{}@stock-analytics.vmxv5.mongodb.net/{}?retryWrites=true&w=majority".format(password, collection_title)

# app & database
app = Flask(__name__) 
client = pymongo.MongoClient(connection_url) 
Database = client.get_database('Users') 
UsersTable = Database.Users 


"""
Insert key-value pair into MongoDB Atlas database
"""
@app.route('/insert-one', methods=['POST']) 
def insertOne(): 
    
    _json = request.json
    _id = _json['_id']
    _value = _json['value']

    if _id and _value and request.method == 'POST':
        queryObject = {'_id':_id,
                       '_value':_value}
        query = UsersTable.insert_one(queryObject)
        response = jsonify("Key-Value Added")
        response.status_code = 200 
        return response
    
    else:
        return print("Error: make request method POST and include key value pair.")

    
"""
To find the first document that matches a defined query, 
find_one function is used and the query to match is passed 
as an argument. 
"""
@app.route('/find-one/<argument>/<value>/', methods=['GET']) 
def findOne(argument, value): 
    
    _json = request.json
    _id = _json['_id']
    _value = _json['value']
    
    queryObject = {argument: value} 
    query = UsersTable.find_one(queryObject) 
    query.pop('_id') 
    return jsonify(query) 


"""
To find all the entries/documents in a table/collection, 
find() function is used. If you want to find all the documents 
that matches a certain query, you can pass a queryObject as an 
argument. 
"""
@app.route('/find/', methods=['GET']) 
def findAll(): 
    query = UsersTable.find() 
    output = {} 
    i = 0
    for x in query: 
        output[i] = x 
        output[i].pop('_id') 
        i += 1
    return jsonify(output)


""" 
To update a document in a collection, update_one() 
function is used. The queryObject to find the document is passed as 
the first argument, the corresponding updateObject is passed as the 
second argument under the '$set' index. 
"""
@app.route('/update/<key>/<value>/<element>/<updateValue>/', methods=['GET']) 
def update(key, value, element, updateValue): 
    queryObject = {key: value} 
    updateObject = {element: updateValue} 
    query = UsersTable.update_one(queryObject, {'$set': updateObject}) 
    if query.acknowledged: 
        return "Update Successful"
    else: 
        return "Update Unsuccessful"
    
  
if __name__ == '__main__': 
    app.run(debug=True) 