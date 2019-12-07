from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers=headers)


# mongo db와 연결한다.
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

soup = BeautifulSoup(data.text, 'html.parser')

# 곡 순위, 제목, 가수를 포함하는 tr 가져오기
songs = soup.select('.music-list-wrap > table > tbody > tr')


rank = 0
for song in songs:
    rank += 1
    title = song.select_one('td.info > a.title').text.strip()
    artist = song.select_one('td.info > a.artist').text

    doc = {
        'rank': rank,
        'title': title,
        'artist': artist
    }

    db.music.insert_one(doc)








