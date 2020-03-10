from flask import render_template, Blueprint, request, jsonify, abort, url_for
# from app.models import Post, Comment
import requests
import json
import os
import random
import pandas as pd
import time

main = Blueprint('main', __name__)

@main.route("/one")
def home():
   images = os.listdir("app/static/one")
   random_image = random.choice(images)
   image_path = "static/one/" + random_image
   image_name = random_image[:-4]
   return render_template('index.html', image_path=image_path, image_name=image_name)

@main.route("/")
def zhuanlan():
   path = "app/static/zhuanlan/2020-03-08/math/math.xlsx"
   df = pd.read_excel(path, index_col=0)
   index = []
   columnNames = []
   columnUrls = []
   authorNames = []
   authorUrls = []
   followers = []
   articlesCounts = []
#  meanVoteupCounts = []
#  meanCommentCounts =[]
   columnScores = []
   columnIDs = []

   for i in range(len(df)):
      columnIDs.append(df.iloc[i, 1].split("/")[-1])
      index.append(i+1)
      columnNames.append(df.loc[i+1, "columnName"])
      columnUrls.append(df.loc[i+1, "columnUrl"])
      authorNames.append(df.loc[i+1, "authorName"])
      authorUrls.append(df.loc[i+1, "authorUrl"])
      followers.append(format(df.loc[i+1, "followers"], '0,.0f'))
      articlesCounts.append(df.loc[i+1, "articlesCount"])
#meanVoteupCounts.append(int(df.loc[i+1, "meanVoteupCount"]))
#     meanCommentCounts.append(int(df.loc[i+1, "meanCommentCount"]))
      columnScores.append(format(round(df.loc[i+1, "columnScore"], 2), '0,.0f'))

   return render_template('gaokao.html', 
         index = index,
         columnNames = columnNames,
         columnUrls = columnUrls,
         authorNames = authorNames,
         authorUrls = authorUrls,
         followers = followers,
         articlesCounts = articlesCounts,
#meanVoteupCounts = meanVoteupCounts, 
#        meanCommentCounts = meanCommentCounts,
         columnScores = columnScores,
         columnIDs = columnIDs
         )


@main.route("/zhuanlan/<columnID>")
def column(columnID):
   columnID = columnID

   columnArticlesDir = os.listdir("/root/zhihu/知乎/文章/2020-03-08/数学类/")
   
   for i in columnArticlesDir:
       if columnID == i[:-5]:
           columnDir = "/root/zhihu/知乎/文章/2020-03-08/数学类/" + i
   
   df = pd.read_excel(columnDir, index_col=0)
   
   df = df.sort_values(by="articleUpdatedTime", ascending=False)
   
   index = []
   articleTitle = []
   articleUrl = []
   articleAuthorName = []
   articleAuthorUrl = []
   articleVoteupCount = []
   articleCommentCount = []
   articleUpdatedTime = []
   
   for i in range(len(df)):
       index.append(i+1)
       articleTitle.append(df.loc[i+1, "articleTitle"])
       articleUrl.append(df.loc[i+1, "articleUrl"])    
       articleAuthorName.append(df.loc[i+1, "articleAuthorName"])    
       articleAuthorUrl.append(df.loc[i+1, "articleAuthorUrl"])    
       articleVoteupCount.append(df.loc[i+1, "articleVoteupCount"])    
       articleCommentCount.append(df.loc[i+1, "articleCommentCount"])    
       articleUpdatedTime.append(time.strftime("%Y/%m/%d", time.localtime(df.loc[i+1, "articleUpdatedTime"])))    
   
   path = "app/static/zhuanlan/2020-03-08/math/math.xlsx"
   columns = pd.read_excel(path, index_col=0)

   for i in range(len(columns)):
      if columnID == columns.iloc[i, 1].split("/")[-1]:
         columnName = columns.iloc[i, 0]
         columnUrl = columns.iloc[i, 1]
         authorName = columns.iloc[i, 2]
         authorUrl = columns.iloc[i, 3]
   return render_template('article.html', 
         index = index,
         columnName = columnName,
         columnUrl = columnUrl,
         authorName = authorName,
         authorUrl = authorUrl,
         articleTitle = articleTitle,
         articleUrl = articleUrl,
         articleAuthorName = articleAuthorName,
         articleAuthorUrl = articleAuthorUrl,
         articleVoteupCount = articleVoteupCount,
         articleCommentCount = articleCommentCount,
         articleUpdatedTime = articleUpdatedTime)




@main.route("/bqb")
def bqb():
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # comments = Comment.query.all()
    # return render_template('index.html', posts=posts, comments=comments)
    return render_template('bqb.html')

@main.route('/about')
def about():
    return render_template('about.html', title='关于我们')

@main.route('/get_my_ip', methods=['GET'])
def get_my_ip():
    ip = request.headers['X-Forwarded-For']
    # url = f'http://api.ipstack.com/{ip}?access_key=341690b835d7bde8702d3bb6d99e4d3a'
    # r = requests.get(url)
    # j = json.loads(r.text)
    # user_agent = user_agent_parser.Parse(request.headers.get('User-Agent'))
    b = f'http://api.map.baidu.com/location/ip?ip={ip}&ak=fGG3zvzvtNThoWldreWBi3FbKjNxhZbK&coor=bd09ll'
    r = requests.get(b)
    j = json.loads(r.text)
    return jsonify(j), 200
