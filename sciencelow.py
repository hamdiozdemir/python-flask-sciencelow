from urllib3 import request
from flask import Flask, render_template,jsonify,request
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)
app.secret_key = "sciencebitch"

app.config["MYSQL_HOST"] = "sciencelow.mysql.pythonanywhere-services.com"
app.config["MYSQL_USER"] = "sciencelow"
app.config["MYSQL_PASSWORD"] = "flaskpassword"
app.config["MYSQL_DB"] = "sciencelow$default"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


# --------------------------------- PAGES ------------------------------------------------------

@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from journals")
    journaldata = cursor.fetchall()
    cursor.close()
    return render_template("index.html",journaldata=journaldata)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/articlecharts")
def articleCharts():
    return render_template("articlecharts.html")

@app.route("/journalcharts")
def journalCharts():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from journals")
    journaldata = cursor.fetchall()
    cursor.close()
    return render_template("journalcharts.html", journaldata=journaldata)

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        dataAll = []
        dataYear = []
        dataFreq = []
        if "searchkey" in request.form:
            searchkey = str(request.form.get("searchkey"))
            dataYear, dataFreq = searchData(searchkey)
            cursor = mysql.connection.cursor()
            result = cursor.execute("SELECT * FROM articles WHERE article_title LIKE '%"+searchkey+"%' ORDER BY year DESC")
            if result == 0:
                dataAll = []
            else:
                dataAll = cursor.fetchall()
            cursor.close()
            return render_template("search.html",dataAll=dataAll,dataYear=dataYear,dataFreq=dataFreq)
        elif "searchkey2" in request.form:
            searchkey = str(request.form.get("searchkey2"))
            dataYear, dataFreq = searchData2(searchkey)
            cursor = mysql.connection.cursor()
            result = cursor.execute("SELECT * FROM articles WHERE abstract LIKE '%"+searchkey+"%' ORDER BY year DESC")
            if result == 0:
                dataAll = []
            else:
                dataAll = cursor.fetchall()
            cursor.close()
            return render_template("search.html",dataAll=dataAll,dataYear=dataYear,dataFreq=dataFreq)

        elif "searchkey3" in request.form:
            searchkey = str(request.form.get("searchkey3"))
            dataYear, dataFreq = searchData3(searchkey)
            cursor = mysql.connection.cursor()
            result = cursor.execute("SELECT * FROM articles WHERE authors LIKE '%"+searchkey+"%' ORDER BY year DESC")
            if result == 0:
                dataAll = []
            else:
                dataAll = cursor.fetchall()
            cursor.close()
            return render_template("search.html",dataAll=dataAll,dataYear=dataYear,dataFreq=dataFreq)
        else:
            dataAll = []
            dataYear = [0]
            dataFreq = [0]
            return render_template("search.html",dataAll=dataAll,dataYear=dataYear,dataFreq=dataFreq)


@app.route("/api/title/<string:searchkey>/", methods=["GET"])
def api_title(searchkey):

    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM articles WHERE article_title LIKE '%"+searchkey+"%' ORDER BY year DESC")
    if result == 0:
        data = {"abstract": None,"article_link": None,"article_title": None,"authors": None,"id": None,"issue": None,"journal_title": None,"volume": None,"year": None}
    else:
        data = cursor.fetchall()
    cursor.close()
    return jsonify(data)


@app.route("/api/abstract/<string:searchkey>/", methods=["GET"])
def api_abstract(searchkey):

    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM articles WHERE abstract LIKE '%"+searchkey+"%' ORDER BY year DESC")
    if result == 0:
        data = {"abstract": None,"article_link": None,"article_title": None,"authors": None,"id": None,"issue": None,"journal_title": None,"volume": None,"year": None}
    else:
        data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route("/api/year/<string:searchkey>/", methods=["GET"])
def api_year(searchkey):
    try:
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM articles WHERE year="+searchkey +" ORDER BY year DESC")
        if result == 0:
            data = {"abstract": None,"article_link": None,"article_title": None,"authors": None,"id": None,"issue": None,"journal_title": None,"volume": None,"year": None}
        else:
            data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except:
        data = {"error": "API error. "}
        return jsonify(data)

@app.route("/api/top_keywords/<string:limit>/", methods=["GET"])
def api_top_keywords(limit):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM keywords ORDER BY freqSum DESC LIMIT "+limit)
        data_all = cursor.fetchall()
        cursor.close()
        data = dict()
        for item in data_all:
            data.update({item["keyword"]: item["freqSum"]})
        return jsonify(data)
    except:
        data = {"error": "Key or Limit error."}
        return jsonify(data)


@app.route("/admin")
def admin():
    return render_template("admin.html")

# --------------------------------- FUNCTIONS ------------------------------------------------------

# Some main funcs to extract keywords at the begining, to insert them to DB
def commonWords():
    common_words = list()
    file = open("bilgiler.txt","r")
    for word in file:
        word = word.rstrip("\n")
        common_words.append(word)
    file.close()
    return common_words

def commonKeywords():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT article_title FROM articles")
    titledata = cursor.fetchall()
    keywords = list()
    commons = commonWords()

    for i in titledata:
        i = i["article_title"]
        i = i.split(" ")
        for j in i:
            j = j.lower()
            j = "".join(ch for ch in j if j.isalpha())
            # j = j.replace(",","")
            # j = j.replace(":", "")
            # j = j.replace("?", "")
            # j = j.replace("-", "")
            # j = j.replace("'", "")
            # j = j.replace("(", "")
            # j = j.replace(")", "")
            if j in commons or j == "" or len(j) < 4:
                pass
            else:
                keywords.append(j)
    cursor.close()
    return keywords

# Journal related funcs
def journal_infos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM journals ORDER BY article_num DESC")
    data = cursor.fetchall()
    cursor.close()
    return data

def article_number():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(id), journal_title FROM articles GROUP BY journal_title")
    data = cursor.fetchall()
    cursor.close()
    return data

def articlePerYear():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(article_title),year FROM articles GROUP BY year ORDER BY year")
    data = cursor.fetchall()
    articleNum = list()
    articleYear = list()
    for i in data:
        articleNum.append(i['COUNT(article_title)'])
        articleYear.append(i["year"])

    return articleNum, articleYear

def quartileNum():
    quartile_list = list()
    quartile_num = list()
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT SUM(article_num), quartile FROM journals GROUP BY quartile ORDER BY quartile ASC")
    all_data = cursor.fetchall()
    cursor.close()
    for data in all_data:
        quartile_list.append(data["quartile"])
        quartile_num.append(data["SUM(article_num)"])
    return quartile_list, quartile_num

# Category Funcs
# getCategories func, gets the datas from db and prettify a bit by turning them as a nested dicts
def getCategories():
    cursor = mysql.connection.cursor()
    query = "SELECT keywords.keyword, keywords.freqSum, categories.category FROM keywords INNER JOIN categories ON keywords.keyword = categories.keyword"
    cursor.execute(query,)
    datas = cursor.fetchall()
    cursor.close()
    categories = {}
    for data in datas:
        categories.update({data["category"]:{}})
    for data in datas:
        for k,v in categories.items():
            if data["category"] == k:
                v.update({data["keyword"]:data["freqSum"]})
    return categories

def allCategories():
    data = getCategories()
    for key,value in data.items():
        total = 0
        for i in value.values():
            total += i
        data[key] = total
    allKey = list(data.keys())
    allValue = list(data.values())

    return allKey,allValue

def categoryFamily():
    data = getCategories()
    x = data.get("family")
    familyKey = list(x.keys())
    familyValue = list(x.values())
    return familyKey,familyValue

def categoryAcademic():
    data = getCategories()
    x = data.get("academic")
    academicKey = list(x.keys())
    academicValue = list(x.values())
    return academicKey, academicValue

def categorySen():
    data = getCategories()
    x = data.get("sen")
    senKey = list(x.keys())
    senValue = list(x.values())
    return senKey, senValue

def categoryWellbeing():
    data = getCategories()
    x = data.get("wellbeing")
    wellbeingKey = list(x.keys())
    wellbeingValue = list(x.values())
    return wellbeingKey, wellbeingValue

def categoryDiversity():
    data = getCategories()
    x = data.get("diversity")
    diversityKey = list(x.keys())
    diversityValue = list(x.values())
    return diversityKey, diversityValue

def categoryDigital():
    data = getCategories()
    x = data.get("digital")
    digitalKey = list(x.keys())
    digitalValue = list(x.values())
    return digitalKey, digitalValue

def categoryAttidute():
    data = getCategories()
    x = data.get("attidute")
    attitudeKey = list(x.keys())
    attiduteValue = list(x.values())
    return attitudeKey,attiduteValue

def categoryOthers():
    othersKey = ["pandemi","covid","adjustment","mindful","scale","sustain"]
    othersValue = []
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE article_title LIKE %s"
    for key in othersKey:
        tempNum = 0
        tempNum = cursor.execute(query,('%'+key+'%',))
        othersValue.append(tempNum)
    cursor.close()
    return othersKey, othersValue

# SEARCH Funcs
def searchData(key):
    dataYear = []
    dataFreq = []
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE year=%s AND article_title LIKE %s"
    for year in range(2017,2023):
        freq = cursor.execute(query,(year,"%"+key+"%",))
        dataYear.append(year)
        dataFreq.append(freq)
    cursor.close()
    return dataYear, dataFreq

def searchData2(key):
    dataYear = []
    dataFreq = []
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE year=%s AND abstract LIKE %s"
    for year in range(2017,2023):
        freq = cursor.execute(query,(year,"%"+key+"%",))
        dataYear.append(year)
        dataFreq.append(freq)
    cursor.close()
    return dataYear, dataFreq

def searchData3(key):
    dataYear = []
    dataFreq = []
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE year=%s AND authors LIKE %s"
    for year in range(2017,2023):
        freq = cursor.execute(query,(year,"%"+key+"%",))
        dataYear.append(year)
        dataFreq.append(freq)
    cursor.close()
    return dataYear, dataFreq


# ---------- CHART APIs ---------------
# API's are seperated for better performance
@app.route("/api/chart-data-top/")
def topKeywords():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM keywords ORDER BY freqSum DESC LIMIT 20")
    dataAll = cursor.fetchall()
    topKeys = [data["keyword"] for data in dataAll]
    freqSum = [data["freqSum"] for data in dataAll]
    freq2017 = [data["freq2017"] for data in dataAll]
    freq2018 = [data["freq2018"] for data in dataAll]
    freq2019 = [data["freq2019"] for data in dataAll]
    freq2020 = [data["freq2020"] for data in dataAll]
    freq2021 = [data["freq2021"] for data in dataAll]
    freq2022 = [data["freq2022"] for data in dataAll]

    return jsonify(
        topKeys = topKeys,
        freqSum = freqSum,
        freq2017 = freq2017,
        freq2018 = freq2018,
        freq2019 = freq2019,
        freq2020 = freq2020,
        freq2021 = freq2021,
        freq2022 = freq2022
    )

@app.route("/api/chart-data-categories/")
def categoryVariables():
    familyKey, familyValue = categoryFamily()
    academicKey, academicValue = categoryAcademic()
    senKey, senValue = categorySen()
    wellbeingKey, wellbeingValue = categoryWellbeing()
    diversityKey, diversityValue = categoryDiversity()
    digitalKey, digitalValue = categoryDigital()
    attiduteKey, attiduteValue = categoryAttidute()
    othersKey, othersValue = categoryOthers()
    allKey, allValue = allCategories()
    return jsonify(
        allKey = allKey,
        allValue = allValue,
        familyKey = familyKey,
        familyValue = familyValue,
        academicKey = academicKey,
        academicValue=academicValue,
        senKey = senKey,
        senValue=senValue,
        wellbeingKey=wellbeingKey,
        wellbeingValue=wellbeingValue,
        diversityKey=diversityKey,
        diversityValue=diversityValue,
        digitalKey=digitalKey,
        digitalValue=digitalValue,
        attiduteKey=attiduteKey,
        attiduteValue=attiduteValue,
        othersKey=othersKey,
        othersValue=othersValue
    )

@app.route("/api/chart-data/")
def allVariables():
    journaldata = journal_infos()
    journalList = [journal["journal_title"] for journal in journaldata]
    articleCount = [num["article_num"] for num in journaldata]
    quartile_list, quartile_num = quartileNum()
    articleNum, articleYear = articlePerYear()
    return jsonify(
        quartile_list=quartile_list,
        quartile_num=quartile_num,
        journalList=journalList,
        articleCount=articleCount,
        articleNum = articleNum,
        articleYear = articleYear,
    )



if __name__ == "__main__":
    app.run(debug=True)


