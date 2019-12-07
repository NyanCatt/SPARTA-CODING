from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## 코딩 할 준비 ##

target_movie = db.users.find_one({'title':'포레스트 검프'})
target_point = target_movie['point']


db.users.update_many(
    {'point':target_point}, #point가 target point 와 같은 애
    {'$set':{'point':0.0}}
)

target_list = db.users.find({'point':0.0})
for movie in target_list:
    print(movie['title'])

#target_list = db.users.find({'point':target_point})

#for movie in target_list:
    #print(movie['title'])
