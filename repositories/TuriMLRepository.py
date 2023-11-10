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
        self.logger.info('Executing db query: SELECT * FROM m_l_training_data')
        cursor.execute('SELECT * FROM m_l_training_data')
        data = cursor.fetchall()
        cursor.close()
        self.logger.info('---- Out of to getAllMLTrainingData-----------')
        return self.filterData(data)
    def filterData(self, mlData: Tuple[Tuple[int,int,int,int,str, bool]]) -> Tuple[List[int], List[int], List[int]]:
        partialResult = tuple( (hobbyistId, artistId, score) for _, hobbyistId, artistId, score, _, _ in mlData)
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