from flaskext.mysql import MySQL
from typing import Tuple, List
import logging

class TuriMlRepository:
    def __init__(self, mysql: MySQL) -> None:
        self.dbHandler = mysql
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)

    def getAllMLTrainingData(self):
        self.logger.info('---- Entered to getAllMLTrainingData-----------')
        cursor = self.dbHandler.get_db().cursor()
        self.logger.info('Executing db query: SELECT * FROM ml_training_data')
        cursor.execute('SELECT * FROM ml_training_data')
        data = cursor.fetchall()
        cursor.close()
        self.logger.info('---- Out of to getAllMLTrainingData-----------')
        return self.filterData(data)
    def filterData(self, mlData: Tuple[Tuple[int,int,int,str]]) -> Tuple[List[int], List[int], List[int]]:
        partialResult = ( (hobbyistId, artistId, score) for hobbyistId, artistId, score, _ in mlData)
        usersId = []
        itemsId = []
        ratings = []
        for hobbystId, _, _ in partialResult:
            usersId.append(hobbystId)
        for _, artistId, _ in partialResult:
            itemsId.append(artistId)
        for _, _, score in partialResult:
            ratings.append(score)
        return (usersId, itemsId, ratings)