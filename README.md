# python-flask-sciencelow

A mini website for some basic analysis of the scientific articles on Early Childhood
- Used Python/Flask
- MySQL for database
- and some visiualization with ChartJS


API

 - ./api/abstract/<string:searchkey>/        returns the records that titles have the searching keyword
 - ./api/year/<string:year>/       returns the records that published in the year given
 - ./api/top_keywords/<string:limit>/       returns the records that top common keywords with the lenght given

Can be visited from here: http://sciencelow.pythonanywhere.com/
