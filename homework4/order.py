from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')


#1. name
#2. count
#3. address
#4. phone

@app.route('/order', methods=['POST'])
def order():
   name = request.form['name_give']
   count = int(request.form['count_give'])
   address = request.form['address_give']
   phone = request.form['phone_give']

   doc = {
       'name': name,
       'count': count,
       'address': address,
       'phone': phone
   }

   db.order.insert_one(doc)

   return jsonify({'result': 'success'})

@app.route('/order', methods=["GET"])
def get_info():
    order = list(db.order.find({}, {'_id': False}))

    result = {
        'orders': order,
        'result': 'success'
    }

    return jsonify(result)


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
