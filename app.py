import logging
from flask import Flask, jsonify
from flaskext.mysql import MySQL
from services.TuriMLService import TuriMLService
from os import getenv
from dotenv import load_dotenv
from redis import StrictRedis

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = getenv("MYSQL_DATABASE_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = getenv("MYSQL_DATABASE_PASSWORD")
app.config['MYSQL_DATABASE_DB'] = getenv("MYSQL_DATABASE_DB")
app.config['MYSQL_DATABASE_HOST'] = getenv("MYSQL_DATABASE_HOST")

redis_config = {
    'host': getenv("REDIS_HOST"),
    'port': int(getenv("REDIS_PORT")),
    'password': getenv("REDIS_PASSWORD"),
    'ssl': bool(getenv("REDIS_SSL")),
    'decode_responses': bool(getenv("REDIS_DECODE_RESPONSES"))
}
redis = StrictRedis(**redis_config)

mysql: MySQL = MySQL(app)

@app.route("/test-redis")
def testRedis():
    todas_las_claves = redis.keys('*')
    datos_redis = {clave: redis.get(clave) for clave in todas_las_claves}
    return jsonify(datos_redis)

@app.route("/recommendation-system/compute-data", methods=['GET'])
def getMLTrainingData():
    service = TuriMLService(mysql)
    service.performRecommendations(redis)
    # todas_las_claves = redis.keys('*')
    # datos_redis = {clave.decode('utf-8'): redis.get(clave).decode('utf-8') for clave in todas_las_claves}
    # return jsonify(datos_redis)
    return "Data computation was successfully done"

@app.route("/recommendation-system/hobbyists/<int:hobbyistId>/recommended-artists")
def getRecommededArtistForSpecificHobbyist(hobbyistId: int):
    if(redis.get(hobbyistId) == None):
        service = TuriMLService(mysql)
        service.performRecommendations(redis)
    return jsonify({ 'artistId': int(redis.get(hobbyistId)) if redis.get(hobbyistId) != None else None})

if __name__ == "__main__":
    app.run(port=8000)