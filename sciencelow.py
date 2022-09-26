from urllib import request
from flask import Flask, render_template,redirect,url_for,jsonify,request
from flask_mysqldb import MySQL
from collections import Counter

app = Flask(__name__)

mysql = MySQL(app)
app.secret_key = "sciencebitch"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "sciencelow"
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
        searchkey = str(request.form.get("searchkey"))
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM articles WHERE article_title LIKE %s ORDER BY year DESC"
        result = cursor.execute(query,('%'+searchkey+'%',))
        if result == 0:
            dataAll = []
            yearData, yearFreq = searchData(searchkey)
            return render_template("search.html",dataAll=dataAll,yearData=yearData,yearFreq=yearFreq)
        else:
            dataAll = cursor.fetchall()
            cursor.close()
            yearData, yearFreq = searchData(searchkey)
            return render_template("search.html",dataAll=dataAll,yearData=yearData,yearFreq=yearFreq)



@app.route("/admin")
def admin():
    return render_template("admin.html")


# --------------------------------- FUNCTIONS ------------------------------------------------------

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
            j = "".join(ch for ch in j if j.isalnum())
            # j = j.replace(",","")
            # j = j.replace(":", "")
            # j = j.replace("?", "")
            # j = j.replace("-", "")
            # j = j.replace("'", "")
            # j = j.replace("(", "")
            # j = j.replace(")", "")
            if j in commons or j == "":
                pass
            else:
                keywords.append(j)
    cursor.close()
    return keywords

def countedAll():
    data = commonKeywords()
    counted = Counter(data)
    return counted

def topCommonKeywords():
    commonKeys = list()
    commonFreq = list()
    keywords = commonKeywords()
    counted = Counter(keywords)
    counted = counted.most_common(20)
    for i in counted:
        commonKeys.append(i[0])
        commonFreq.append(i[1])
    return commonKeys, commonFreq

def topCommonKeywordsAll():
    commonKey, commonFreq = topCommonKeywords()
    data = {}
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE year = %s AND article_title LIKE %s"
    for year in range(2017,2023):
        tempList = []
        for key in commonKey:
            freq = cursor.execute(query,(year,'%'+key+'%'))
            tempList.append(freq)
        data[year] = tempList
    tempList = []
    for key in commonKey:
        query = "SELECT * FROM articles WHERE article_title LIKE %s"
        freq = cursor.execute(query,('%'+key+'%',))
        tempList.append(freq)
    data["all"] = tempList           
    cursor.close()
    return commonKey, data
      

def searchData(key):
    yearData = []
    yearFreq = []
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE year=%s AND article_title LIKE %s"
    for year in range(2017,2023):
        freq = cursor.execute(query,(year,"%"+key+"%"))
        yearData.append(year)
        yearFreq.append(freq)
    cursor.close()
    return yearData, yearFreq



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

def getCategories():
    categories = {
        "family": {"parenting":0,"parental":0,"parents":0,"maternal":0,"families":0,"mothers":0,"caregiver":0,"caregiver":0,"partner":0,"fathers":0,"siblings":0,"sibling":0,"paternal":0,"coparenting":0,"interparental":0,"carers":0,"familial":0,"foster":0,"overparenting":0},
        "academic": {"learning":0,"reading":0,"literacy":0,"academic":0,"lessons":0,"writing":0,"math":0,"stem":0,"mathematical":0,"vocabulary":0,"literacies":0,"mathematics":0},
        "sen": {"disorder":0,"autism":0,"disabilities":0,"adhd":0,"dyslexia":0,"dysmorphia":0},
        "wellbeing": {"stress":0,"welfare":0,"anxiety":0,"depressive":0,"wellbeing":0,"trauma":0,"distress":0,"healthy":0,"illness":0,"satisfaction":0,"abuse":0},
        "diversity": {"gender":0,"poverty":0,"cultural":0,"immigrant":0,"refugee":0,"diverse":0,"racial":0,"ethnic":0,"minority":0,"inclusive":0,"culturally":0,"migrant":0,"inclusion":0,"gendered":0,"immigrants":0},
        "digital": {"digital":0,"television":0,"mobile":0,"screen":0,"cyberbullying":0},
        "attidute" : {"violence":0,"bullying":0,"maltreatment":0,"aggression":0,"cyberbullying":0}
        }
    common_keywords = commonKeywords()
    counted_keywords = Counter(common_keywords)
    for value in categories.values():
        for key in value:
            value[key] = counted_keywords[key]
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


@app.route("/api/chart-data/")
def allVariables():
    journaldata = journal_infos()
    journalList = [journal["journal_title"] for journal in journaldata]
    articleCount = [num["article_num"] for num in journaldata]
    quartile_list, quartile_num = quartileNum()
    allKey, allValue = allCategories()
    articleNum, articleYear = articlePerYear()
    commonKeys, data = topCommonKeywordsAll()
    familyKey, familyValue = categoryFamily()
    academicKey, academicValue = categoryAcademic()
    senKey, senValue = categorySen()
    wellbeingKey, wellbeingValue = categoryWellbeing()
    diversityKey, diversityValue = categoryDiversity()
    digitalKey, digitalValue = categoryDigital()
    attiduteKey, attiduteValue = categoryAttidute()
    othersKey, othersValue = categoryOthers()
    

    return jsonify(
        quartile_list=quartile_list,
        quartile_num=quartile_num,
        journalList=journalList,
        articleCount=articleCount,
        allKey = allKey,
        allValue = allValue,
        familyKey = familyKey,
        familyValue = familyValue,
        academicKey = academicKey,
        academicValue=academicValue,
        articleNum = articleNum,
        articleYear = articleYear,
        commonKeys = commonKeys,
        freqAll = data["all"],
        freq2017 = data[2017],
        freq2018 = data[2018],
        freq2019 = data[2019],
        freq2020 = data[2020],
        freq2021 = data[2021],
        freq2022 = data[2022],
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












if __name__ == "__main__":
    app.run(debug=True)


