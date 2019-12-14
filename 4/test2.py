from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('note.html')


## API 역할을 하는 부분
@app.route('/test', methods=['POST'])
def test_post():
    # rank_give로 클라이언트가 준 rank을 가져오기 & 숫자변환
    rank_receive = request.form['rank_give']
    rank_receive = int(rank_receive)

    # star_give로 클라이언트가 준 star를 가져오기 & 숫자변환
    star_receive = request.form['star_give']
    star_receive = int(star_receive)

    # 해당 순위의 영화를 받은 score로 업데이트 해주기
    db.movies.update_one({'rank': rank_receive}, {'$set': {'point': star_receive}})

    # 다했으면 성공여부만 보냄
    return jsonify({'result': 'success'})



@app.route('/test', methods=['GET'])
def test_get():
    # rank_give로 클라이언트가 준 rank을 가져오기
    rank_receive = request.args.get('rank_give')

    # rank_receive를 숫자로 만들어주기 (db엔 숫자로 저장되어있으니까!)
    rank_receive = int(rank_receive)

    # rank의 값이 받은 rank와 일치하는 document 찾기 & _id 값은 출력에서 제외하기
    movie_info = db.movies.find_one({'rank':rank_receive},{'_id':0})

    # info라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'info':movie_info})


#localhost:5000/new POST 내가원하는 영화 정보를 넘겨주면
#그걸 mongodb 에 저장해주는 녀석을 하나 만들어야겠다.

#1. 랭킹 정보 : rank_give
#2. 점수 : point_give
#3. 영화 제목 : title_give

@app.route('/new', methods=['POST'])
def new_post():
   rank_receive = int(request.form['rank_give'])
   star_receive = request.form['star_give']
   title_receive = request.form['title_give']

   db.movies.insert_one({'rank': rank_receive, 'point': star_receive, 'title':title_receive})

   return jsonify({'result': 'success'})


@app.route('/post', methods=["POST"])
def save():
    # 내가 찾아가야 할 URL과, 유저가 넘긴 코멘트
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    # 1. 크롤링
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url=url_receive, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")
    title = soup.select('meta[property="og:title"]')[0]['content']
    desc = soup.select('meta[property="og:description"]')[0]['content']
    img = soup.select('meta[property="og:image"]')[0]['content']

    # 2. 저장 -> DB에 저장을 한다.
    doc = {
        'title': title,
        'desc': desc,
        'image': img,
        'comment': comment_receive,
        'url': url_receive
    }
    db_insert_result = db.memos.insert_one(doc)


    # 3. 잘 됐는지 여부 판단해서 넘기기
    result = {}
    if db_insert_result is not None:
        result = {'result':'success'}
    else:
        result = {'result':'failure'}

    return jsonify(result)

@app.route('/post', methods=["GET"])
def get_info():
    memos = list(db.memos.find({}, {'_id': False}))

    result = {
        'articles': memos,
        'result': 'success'
    }

    return jsonify(result)


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
