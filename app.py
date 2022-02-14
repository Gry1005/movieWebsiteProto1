from flask import Flask,request,jsonify
import urllib
import json
import time

#movie对照表
movieDZ={
    28:'Action',
    12:'Adventure',
    16:'Animation',
    35:'Comedy',
    80:'Crime',
    99:'Documentary',
    18:'Drama',
    10751:'Family',
    14:'Fantasy',
    36:'History',
    27:'Horror',
    10402:'Music',
    9648:'Mystery',
    10749:'Romance',
    878:'Science Fiction',
    10770:'TV Movie',
    53:'Thriller',
    10752:'War',
    37:'Western'
}

#TV shows对照
tvDZ={
    10759:'Action & Adventure',
    16:'Animation',
    35:'Comedy',
    80:'Crime',
    99:'Documentary',
    18:'Drama',
    10751:'Family',
    10762:'Kids',
    9648:'Mystery',
    10763:'News',
    10764:'Reality',
    10765:'Sci-Fi & Fantasy',
    10766:'Soap',
    10767:'Talk',
    10768:'War & Politics',
    37:'Western'
}

app=Flask(__name__,static_url_path='')

def getValidText(t):
    if t and t!="":
        return t
    else:
        return "N/A"

def getValidList(l):
    if len(l)==0:
        l.append("N/A")

    return l.copy()

def getValidPosterPath(p):
    if p and p!="":
        return 'https://image.tmdb.org/t/p/w185' + p
    else:
        #return 'https://cinemaone.net/images/movie_placeholder.png'
        return 'images/movie_placeholder.png'

def getValidBackDropPath(p):
    if p and p!="":
        return 'https://image.tmdb.org/t/p/w780' + p
    else:
        #return 'https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg'
        return 'images/movie-placeholder.jpg'

def getValidProfilePath(p):
    if p and p!="":
        return 'https://image.tmdb.org/t/p/w185' + p
    else:
        #return 'https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/person-placeholder.png'
        return 'images/person-placeholder.png'

def getValidDate(d):
    if d and str(d)!="":
        return str(d).split("-")[0]
    else:
        return "N/A"

def getValidVoteAverage(va):
    if va:
        return float(va)/2
    else:
        return 0.0

def getValidVoteCount(vc):
    if vc:
        return vc
    else:
        return 0




def getMoiveItem(result):

    MItem = {}

    MItem["id"] = getValidText(result["id"])
    MItem["title"] = getValidText(result["title"])
    MItem["overview"] = getValidText(result["overview"])

    MItem["poster_path"] = getValidPosterPath(result["poster_path"])

    # vote_average变为5
    MItem["vote_average"] = getValidVoteAverage(result["vote_average"])

    MItem["vote_count"] = getValidVoteCount(result["vote_count"])

    gArray = result["genre_ids"]
    gList = []
    for j in range(0, len(gArray)):
        gList.append(movieDZ[gArray[j]])

    MItem["gList"] = getValidList(gList)

    MItem["date"] = getValidDate(result["release_date"])

    MItem["type"] = "M"

    return MItem.copy()

def getTVItem(result):
    MItem = {}

    MItem["id"] = getValidText(result["id"])
    MItem["title"] = getValidText(result["name"])
    MItem["overview"] = getValidText(result["overview"])

    MItem["poster_path"] = getValidPosterPath(result["poster_path"])

    # vote_average变为5
    MItem["vote_average"] = getValidVoteAverage(result["vote_average"])

    MItem["vote_count"] = getValidVoteCount(result["vote_count"])

    gArray = result["genre_ids"]
    gList = []
    for j in range(0, len(gArray)):
        gList.append(tvDZ[gArray[j]])

    MItem["gList"] = getValidList(gList)

    MItem["date"] = getValidDate(result["first_air_date"])

    MItem["type"] = "T"

    return MItem.copy()


@app.route('/',methods=['GET','POST'])
def index():
    return app.send_static_file('main.html')


@app.route('/endpoint',methods=['GET'])
def endPoint():

    page=request.args.get("page");

    if not page or page=='0':

        #home页面
        print("At home!")
        page=0

        homeDic={}

        # 获取TMDB数据: movie
        url = "https://api.themoviedb.org/3/trending/movie/week?api_key=1e1812e68efb5ee050d27b75411686a3"
        req = urllib.request.Request(url)

        res_data = urllib.request.urlopen(req)
        res = res_data.read()

        # 解析json
        res_dic = json.loads(res)

        results = res_dic['results']

        movieList = []

        for i in range(0, len(results)):
            if i>=5:
                break

            movieItem = {}

            movieItem["title"] = getValidText(results[i]["title"])

            movieItem["backdrop_path"] = getValidBackDropPath(results[i]["backdrop_path"])

            movieItem["release_date"] = getValidDate(results[i]["release_date"])

            movieList.append(movieItem.copy())

        # 获取TMDB数据: TV
        url = "https://api.themoviedb.org/3/tv/airing_today?api_key=1e1812e68efb5ee050d27b75411686a3"
        req = urllib.request.Request(url)

        res_data = urllib.request.urlopen(req)
        res = res_data.read()

        # 解析json
        res_dic = json.loads(res)

        results = res_dic['results']

        TVList = []

        for i in range(0, len(results)):
            if i>=5:
                break

            TVItem = {}

            TVItem["name"] = getValidText(results[i]["name"])
            TVItem["backdrop_path"] = getValidBackDropPath(results[i]["backdrop_path"])

            TVItem["date"] = getValidDate(results[i]["first_air_date"])

            TVList.append(TVItem.copy())

        homeDic["movieList"] = movieList
        homeDic["TVList"] = TVList

        return jsonify(homeDic)


@app.route('/search',methods=['GET'])
def handleSearch():
    # search页面
    print("At search!")

    keyword = request.args.get("keyword")
    category = request.args.get("category")

    if keyword and category:

        # print('keyword:',keyword,' category:',category)

        searchList = None

        if category == 'M':
            # movies

            search_query = keyword.replace(" ", "%20")

            # 获取TMDB数据: Movies
            url = "https://api.themoviedb.org/3/search/movie?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US&query=" + search_query + "&page=1&include_adult=false"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            res_dic = json.loads(res)

            results = res_dic['results']

            MList = []

            for i in range(0, len(results)):
                if i >= 10:
                    break

                MItem = getMoiveItem(results[i])

                MList.append(MItem)

            # print(MList[0])
            searchList = MList.copy()

        elif category == 'T':
            # TV

            search_query = keyword.replace(" ", "%20")

            # 获取TMDB数据: TV
            url = "https://api.themoviedb.org/3/search/tv?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US&query=" + search_query + "&page=1&include_adult=false"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            res_dic = json.loads(res)

            results = res_dic['results']

            MList = []

            for i in range(0, len(results)):
                if i >= 10:
                    break

                MItem = getTVItem(results[i])

                MList.append(MItem)

            # print(MList[0])
            searchList = MList.copy()

        else:
            # multiple-search

            search_query = keyword.replace(" ", "%20")

            # 获取TMDB数据: multi
            url = "https://api.themoviedb.org/3/search/multi?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US&query=" + search_query + "&page=1&include_adult=false"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            res_dic = json.loads(res)

            results = res_dic['results']

            MList = []

            for i in range(0, len(results)):
                if len(MList) >= 10:
                    break

                type = results[i]["media_type"]

                if type == "tv":
                    MItem = getTVItem(results[i])
                    MList.append(MItem)

                elif type == "movie":
                    MItem = getMoiveItem(results[i])
                    MList.append(MItem)

                else:
                    continue

            # print(MList[0])
            searchList = MList.copy()

        return jsonify(searchList)


@app.route('/showMore',methods=['GET'])
def handleShowMore():
    itemId = request.args.get("itemId")
    itemType = request.args.get("type")

    # 处理详情页
    if itemId:
        # print('itemId:',itemId,' type:',itemType,' keyword:',keyword,' category:',category)
        resultList={};

        if itemType == "M":
            # 影片详情
            # 获取TMDB数据

            url = "https://api.themoviedb.org/3/movie/" + itemId + "?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            infoDic = {}

            res_dic = json.loads(res)

            infoDic["link"] = 'https://www.themoviedb.org/movie/' + str(res_dic['id'])

            infoDic["id"] = getValidText(res_dic['id'])
            infoDic["title"] = getValidText(res_dic['title'])
            infoDic["overview"] = getValidText(res_dic['overview'])

            infoDic["release_date"] = getValidDate(res_dic['release_date'])

            infoDic["vote_average"] = getValidVoteAverage(res_dic['vote_average'])

            infoDic["vote_count"] = getValidVoteCount(res_dic['vote_count'])

            infoDic["backdrop_path"] = getValidBackDropPath(res_dic['backdrop_path'])

            infoDic["poster_path"] = getValidPosterPath(res_dic['poster_path'])

            infoDic['runtime'] = res_dic['runtime']

            # spoken languages
            lList = []
            lArray = res_dic['spoken_languages']

            for j in range(0, len(lArray)):
                lList.append(lArray[j]['english_name'])

            infoDic['lList'] = getValidList(lList)

            # genres
            gList = []
            gArray = res_dic["genres"]

            for j in range(0, len(gArray)):
                gList.append(gArray[j]['name'])

            infoDic['gList'] = getValidList(gList)

            # print(infoDic)
            resultList["infoDic"]=infoDic

            # get movie casts
            # 获取TMDB数据

            url = "https://api.themoviedb.org/3/movie/" + itemId + "/credits?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            res_dic = json.loads(res)

            casts = res_dic['cast']

            castList = []

            for i in range(0, len(casts)):

                if i == 8:
                    break

                castDic = {}

                castDic['name'] = getValidText(casts[i]['name'])
                castDic['profile_path'] = getValidProfilePath(casts[i]['profile_path'])
                castDic['character'] = getValidText(casts[i]['character'])

                castList.append(castDic.copy())

            if len(castList) == 0:
                castList = None
            # print(castList)
            resultList["castList"] = castList

            # get movie reviews
            # 获取TMDB数据

            url = "https://api.themoviedb.org/3/movie/" + itemId + "/reviews?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            res_dic = json.loads(res)

            reviews = res_dic['results']

            reviewList = []

            for i in range(0, len(reviews)):
                if i == 5:
                    break

                reviewDic = {}

                reviewDic["username"] = getValidText(reviews[i]["author_details"]["username"])
                reviewDic["content"] = getValidText(reviews[i]["content"])

                # ratings可以不显示
                if reviews[i]["author_details"]["rating"]:
                    rating = float(reviews[i]["author_details"]["rating"])
                    reviewDic["rating"] = rating / 2

                # 处理created_at
                if reviews[i]["created_at"]:
                    dateStr = reviews[i]["created_at"].split("T")[0]
                    # 年月日
                    dateList = dateStr.split("-")
                    reviewDic["created_at"] = dateList.copy()
                else:
                    reviewDic["created_at"] = ['N/A', 'N/A', 'N/A']

                reviewList.append(reviewDic.copy())

            if len(reviewList) == 0:
                reviewList = None
            # print(reviewList[0])
            resultList["reviewList"] = reviewList

        else:
            # TV
            # TV详情
            # 获取TMDB数据

            url = "https://api.themoviedb.org/3/tv/" + itemId + "?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            infoDic = {}

            res_dic = json.loads(res)

            infoDic["link"] = 'https://www.themoviedb.org/tv/' + str(res_dic['id'])

            infoDic["id"] = getValidText(res_dic['id'])
            infoDic["title"] = getValidText(res_dic['name'])
            infoDic["overview"] = getValidText(res_dic['overview'])
            infoDic["release_date"] = getValidDate(res_dic['first_air_date'])
            infoDic["vote_average"] = getValidVoteAverage(res_dic['vote_average'])
            infoDic["vote_count"] = getValidVoteCount(res_dic['vote_count'])

            infoDic["backdrop_path"] = getValidBackDropPath(res_dic['backdrop_path'])

            infoDic["poster_path"] = getValidPosterPath(res_dic['poster_path'])

            infoDic['episode_run_time'] = res_dic['episode_run_time']

            # spoken languages
            lList = []
            lArray = res_dic['spoken_languages']

            for j in range(0, len(lArray)):
                lList.append(lArray[j]['english_name'])

            infoDic['lList'] = getValidList(lList)

            # genres
            gList = []
            gArray = res_dic["genres"]

            for j in range(0, len(gArray)):
                gList.append(gArray[j]['name'])

            infoDic['gList'] = getValidList(gList)

            # print(infoDic)
            resultList["infoDic"] = infoDic

            # get tv casts
            # 获取TMDB数据

            url = "https://api.themoviedb.org/3/tv/" + itemId + "/credits?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            res_dic = json.loads(res)

            casts = res_dic['cast']

            castList = []

            for i in range(0, len(casts)):

                if i == 8:
                    break

                castDic = {}

                castDic['name'] = getValidText(casts[i]['name'])
                castDic['profile_path'] = getValidProfilePath(casts[i]['profile_path'])
                castDic['character'] = getValidText(casts[i]['character'])

                castList.append(castDic.copy())

            if len(castList) == 0:
                castList = None
            # print(castList)
            resultList["castList"] = castList

            # get movie reviews
            # 获取TMDB数据

            url = "https://api.themoviedb.org/3/tv/" + itemId + "/reviews?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
            req = urllib.request.Request(url)

            res_data = urllib.request.urlopen(req)
            res = res_data.read()

            # 解析json
            res_dic = json.loads(res)

            reviews = res_dic['results']

            reviewList = []

            for i in range(0, len(reviews)):
                if i == 5:
                    break

                reviewDic = {}

                reviewDic["username"] = getValidText(reviews[i]["author_details"]["username"])
                reviewDic["content"] = getValidText(reviews[i]["content"])

                # ratings可以没有
                if reviews[i]["author_details"]["rating"]:
                    rating = float(reviews[i]["author_details"]["rating"])
                    reviewDic["rating"] = rating / 2

                # 处理created_at
                if reviews[i]["created_at"]:
                    dateStr = reviews[i]["created_at"].split("T")[0]
                    # 年月日
                    dateList = dateStr.split("-")
                    reviewDic["created_at"] = dateList.copy()
                else:
                    reviewDic["created_at"] = ["N/A", "N/A", "N/A"]

                reviewList.append(reviewDic.copy())

            if len(reviewList) == 0:
                reviewList = None
            # print(reviewList[0])
            resultList["reviewList"] = reviewList

        return jsonify(resultList)


'''
@app.route('/template',methods=['GET'])
def home():

    #request.form获取post方法传来的值
    #request.args获取get方法传来的值

    page=request.args.get("page")

    if (not page) or page=='0':

        #home页面
        print("At home!")
        page=0

        # 获取TMDB数据: movie
        url = "https://api.themoviedb.org/3/trending/movie/week?api_key=1e1812e68efb5ee050d27b75411686a3"
        req = urllib.request.Request(url)

        res_data = urllib.request.urlopen(req)
        res = res_data.read()

        # 解析json
        res_dic = json.loads(res)

        results = res_dic['results']

        movieList = []

        for i in range(0, len(results)):
            if i>=5:
                break

            movieItem = {}

            movieItem["title"] = getValidText(results[i]["title"])

            movieItem["backdrop_path"] = getValidBackDropPath(results[i]["backdrop_path"])

            movieItem["release_date"] = getValidDate(results[i]["release_date"])

            movieList.append(movieItem.copy())

        # 获取TMDB数据: TV
        url = "https://api.themoviedb.org/3/tv/airing_today?api_key=1e1812e68efb5ee050d27b75411686a3"
        req = urllib.request.Request(url)

        res_data = urllib.request.urlopen(req)
        res = res_data.read()

        # 解析json
        res_dic = json.loads(res)

        results = res_dic['results']

        TVList = []

        for i in range(0, len(results)):
            if i>=5:
                break

            TVItem = {}

            TVItem["name"] = getValidText(results[i]["name"])
            TVItem["backdrop_path"] = getValidBackDropPath(results[i]["backdrop_path"])

            TVItem["date"] = getValidDate(results[i]["first_air_date"])

            TVList.append(TVItem.copy())

        return render_template('home.html', page=page, movieList=movieList, TVList=TVList)

    else:
        #search页面
        print("At search!")
        page=1
        #condition:0 不需要显示结果; 1 显示无结果; 2 显示有结果
        condition=0

        keyword = request.args.get("keyword")
        category = request.args.get("category")
        itemId=request.args.get("itemId")

        if keyword and category:

            #print('keyword:',keyword,' category:',category)

            searchList=None

            if category=='M':
                #movies

                search_query=keyword.replace(" ","%20")

                # 获取TMDB数据: Movies
                url = "https://api.themoviedb.org/3/search/movie?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US&query="+search_query+"&page=1&include_adult=false"
                req = urllib.request.Request(url)

                res_data = urllib.request.urlopen(req)
                res = res_data.read()

                # 解析json
                res_dic = json.loads(res)

                results = res_dic['results']

                MList = []

                for i in range(0, len(results)):
                    if i>=10:
                        break

                    MItem=getMoiveItem(results[i])

                    MList.append(MItem)


                #print(MList[0])
                searchList=MList.copy()

            elif category=='T':
                #TV

                search_query = keyword.replace(" ", "%20")

                # 获取TMDB数据: TV
                url = "https://api.themoviedb.org/3/search/tv?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US&query=" + search_query + "&page=1&include_adult=false"
                req = urllib.request.Request(url)

                res_data = urllib.request.urlopen(req)
                res = res_data.read()

                # 解析json
                res_dic = json.loads(res)

                results = res_dic['results']

                MList = []

                for i in range(0, len(results)):
                    if i>=10:
                        break

                    MItem = getTVItem(results[i])

                    MList.append(MItem)

                # print(MList[0])
                searchList = MList.copy()

            else:
                #multiple-search

                search_query = keyword.replace(" ", "%20")

                # 获取TMDB数据: multi
                url = "https://api.themoviedb.org/3/search/multi?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US&query=" + search_query + "&page=1&include_adult=false"
                req = urllib.request.Request(url)

                res_data = urllib.request.urlopen(req)
                res = res_data.read()

                # 解析json
                res_dic = json.loads(res)

                results = res_dic['results']

                MList = []

                for i in range(0, len(results)):
                    if len(MList)>=10:
                        break

                    type = results[i]["media_type"]

                    if type=="tv":
                        MItem = getTVItem(results[i])
                        MList.append(MItem)

                    elif type=="movie":
                        MItem = getMoiveItem(results[i])
                        MList.append(MItem)

                    else:
                        continue

                # print(MList[0])
                searchList = MList.copy()

            infoDic=None
            castList=None
            reviewList=None

            #处理详情页
            if itemId:
                itemType = request.args.get("type")
                #print('itemId:',itemId,' type:',itemType,' keyword:',keyword,' category:',category)

                if itemType=="M":
                    # 影片详情
                    # 获取TMDB数据

                    url = "https://api.themoviedb.org/3/movie/"+itemId+"?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
                    req = urllib.request.Request(url)

                    res_data = urllib.request.urlopen(req)
                    res = res_data.read()

                    # 解析json
                    infoDic={}

                    res_dic = json.loads(res)

                    infoDic["link"]='https://www.themoviedb.org/movie/'+str(res_dic['id'])

                    infoDic["id"] = getValidText(res_dic['id'])
                    infoDic["title"] = getValidText(res_dic['title'])
                    infoDic["overview"] = getValidText(res_dic['overview'])

                    infoDic["release_date"] = getValidDate(res_dic['release_date'])

                    infoDic["vote_average"] = getValidVoteAverage(res_dic['vote_average'])

                    infoDic["vote_count"] = getValidVoteCount(res_dic['vote_count'])

                    infoDic["backdrop_path"] = getValidBackDropPath(res_dic['backdrop_path'])

                    infoDic["poster_path"] = getValidPosterPath(res_dic['poster_path'])

                    infoDic['runtime'] = res_dic['runtime']

                    #spoken languages
                    lList=[]
                    lArray=res_dic['spoken_languages']

                    for j in range(0,len(lArray)):
                        lList.append(lArray[j]['english_name'])

                    infoDic['lList']=getValidList(lList)

                    #genres
                    gList=[]
                    gArray=res_dic["genres"]

                    for j in range(0,len(gArray)):
                        gList.append(gArray[j]['name'])

                    infoDic['gList']=getValidList(gList)

                    #print(infoDic)

                    # get movie casts
                    # 获取TMDB数据

                    url = "https://api.themoviedb.org/3/movie/" + itemId + "/credits?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
                    req = urllib.request.Request(url)

                    res_data = urllib.request.urlopen(req)
                    res = res_data.read()

                    #解析json
                    res_dic = json.loads(res)

                    casts=res_dic['cast']

                    castList = []

                    for i in range(0,len(casts)):

                        if i==8:
                            break

                        castDic = {}

                        castDic['name'] = getValidText(casts[i]['name'])
                        castDic['profile_path'] = getValidProfilePath(casts[i]['profile_path'])
                        castDic['character'] = getValidText(casts[i]['character'])

                        castList.append(castDic.copy())

                    if len(castList)==0:
                        castList=None
                    #print(castList)

                    #get movie reviews
                    # 获取TMDB数据

                    url = "https://api.themoviedb.org/3/movie/" + itemId + "/reviews?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
                    req = urllib.request.Request(url)

                    res_data = urllib.request.urlopen(req)
                    res = res_data.read()

                    # 解析json
                    res_dic = json.loads(res)

                    reviews = res_dic['results']

                    reviewList = []

                    for i in range(0, len(reviews)):
                        if i==5:
                            break

                        reviewDic={}

                        reviewDic["username"]=getValidText(reviews[i]["author_details"]["username"])
                        reviewDic["content"]=getValidText(reviews[i]["content"])

                        #ratings可以不显示
                        if reviews[i]["author_details"]["rating"]:
                            rating = float(reviews[i]["author_details"]["rating"])
                            reviewDic["rating"] = rating/2

                        # 处理created_at
                        if reviews[i]["created_at"]:
                            dateStr = reviews[i]["created_at"].split("T")[0]
                            #年月日
                            dateList=dateStr.split("-")
                            reviewDic["created_at"]=dateList.copy()
                        else:
                            reviewDic["created_at"] = ['N/A','N/A','N/A']

                        reviewList.append(reviewDic.copy())

                    if len(reviewList)==0:
                        reviewList=None
                    #print(reviewList[0])

                else:
                    #TV
                    # TV详情
                    # 获取TMDB数据

                    url = "https://api.themoviedb.org/3/tv/" + itemId + "?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
                    req = urllib.request.Request(url)

                    res_data = urllib.request.urlopen(req)
                    res = res_data.read()

                    # 解析json
                    infoDic = {}

                    res_dic = json.loads(res)

                    infoDic["link"] = 'https://www.themoviedb.org/tv/' + str(res_dic['id'])

                    infoDic["id"] = getValidText(res_dic['id'])
                    infoDic["title"] = getValidText(res_dic['name'])
                    infoDic["overview"] = getValidText(res_dic['overview'])
                    infoDic["release_date"] = getValidDate(res_dic['first_air_date'])
                    infoDic["vote_average"] = getValidVoteAverage(res_dic['vote_average'])
                    infoDic["vote_count"] = getValidVoteCount(res_dic['vote_count'])

                    infoDic["backdrop_path"] = getValidBackDropPath(res_dic['backdrop_path'])

                    infoDic["poster_path"] = getValidPosterPath(res_dic['poster_path'])

                    infoDic['episode_run_time'] = res_dic['episode_run_time']

                    # spoken languages
                    lList = []
                    lArray = res_dic['spoken_languages']

                    for j in range(0, len(lArray)):
                        lList.append(lArray[j]['english_name'])

                    infoDic['lList'] = getValidList(lList)

                    # genres
                    gList = []
                    gArray = res_dic["genres"]

                    for j in range(0, len(gArray)):
                        gList.append(gArray[j]['name'])

                    infoDic['gList'] = getValidList(gList)

                    # print(infoDic)

                    # get tv casts
                    # 获取TMDB数据

                    url = "https://api.themoviedb.org/3/tv/" + itemId + "/credits?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
                    req = urllib.request.Request(url)

                    res_data = urllib.request.urlopen(req)
                    res = res_data.read()

                    # 解析json
                    res_dic = json.loads(res)

                    casts = res_dic['cast']

                    castList = []

                    for i in range(0, len(casts)):

                        if i == 8:
                            break

                        castDic = {}

                        castDic['name'] = getValidText(casts[i]['name'])
                        castDic['profile_path'] = getValidProfilePath(casts[i]['profile_path'])
                        castDic['character'] = getValidText(casts[i]['character'])

                        castList.append(castDic.copy())

                    if len(castList)==0:
                        castList=None
                    # print(castList)

                    # get movie reviews
                    # 获取TMDB数据

                    url = "https://api.themoviedb.org/3/tv/" + itemId + "/reviews?api_key=1e1812e68efb5ee050d27b75411686a3&language=en-US"
                    req = urllib.request.Request(url)

                    res_data = urllib.request.urlopen(req)
                    res = res_data.read()

                    # 解析json
                    res_dic = json.loads(res)

                    reviews = res_dic['results']

                    reviewList = []

                    for i in range(0, len(reviews)):
                        if i == 5:
                            break

                        reviewDic = {}

                        reviewDic["username"] = getValidText(reviews[i]["author_details"]["username"])
                        reviewDic["content"] = getValidText(reviews[i]["content"])

                        #ratings可以没有
                        if reviews[i]["author_details"]["rating"]:
                            rating = float(reviews[i]["author_details"]["rating"])
                            reviewDic["rating"] = rating / 2

                        # 处理created_at
                        if reviews[i]["created_at"]:
                            dateStr = reviews[i]["created_at"].split("T")[0]
                            # 年月日
                            dateList = dateStr.split("-")
                            reviewDic["created_at"] = dateList.copy()
                        else:
                            reviewDic["created_at"] = ["N/A","N/A","N/A"]

                        reviewList.append(reviewDic.copy())

                    if len(reviewList)==0:
                        reviewList=None
                    # print(reviewList[0])


            if searchList and len(searchList)>0:

                if not itemId:
                    return render_template('home.html', page=page, condition=2,searchList=searchList,keyword=keyword,category=category)
                else:
                    return render_template('home.html', page=page, condition=2,searchList=searchList,keyword=keyword,category=category,itemId=str(itemId),infoDic=infoDic,castList=castList,reviewList=reviewList)
            else:
                return render_template('home.html', page=page, condition=1, searchList=searchList,keyword=keyword,category=category)

        else:
            return render_template('home.html', page=page,condition=0)
'''


if __name__=="__main__":
    app.run()