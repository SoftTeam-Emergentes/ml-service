import logging
from flask import Flask
from flaskext.mysql import MySQL
from services.TuriMLService import TuriMLService

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'perustars'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Cambia esto según la ubicación de tu servidor MySQL

mysql: MySQL = MySQL(app)

@app.route("/")
def helloWorld():
    return "Hello World"

@app.route("/ml/all-training-data", methods=['GET'])
def getMLTrainingData():
    service = TuriMLService(mysql)
    return service.performRecommendations()



app.run(port=8000)