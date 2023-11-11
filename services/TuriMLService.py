import turicreate as tc
from flaskext.mysql import MySQL
from repositories.TuriMLRepository import TuriMlRepository
import logging
from typing import Tuple, List
from redis import StrictRedis

class TuriMLService:
    def __init__(self, mysql: MySQL) -> None:
        self.usersId = []
        self.itmsId = []
        self.ratings = []
        self.turiMLRepository = TuriMlRepository(mysql)
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
    def foo(self) -> Tuple[List[int], List[int], List[int]]:
        self.logger.info("------------Entered in foo method ------------")
        try:
            # self.logger.info("Type of result from repository: %s", type(self.turiMLRepository.getAllMLTrainingData()))
            # self.logger.info("Result from repository: %s", self.turiMLRepository.getAllMLTrainingData())
            result: Tuple[Tuple[int,int,int]] = self.turiMLRepository.getAllMLTrainingData()
        except Exception as e:
            self.logger.error("An error occured while trying to execute a repository method")
            self.logger.info("------------Out of foo method with error ------------")
            return (None, None, None)
        self.logger.info("------------Out of foo method with success ------------")
    def performRecommendations(self, redis: StrictRedis):
        userIdList, itemIdList, ratingList = self.turiMLRepository.getAllMLTrainingData()
        if len(userIdList) == 0 and len(itemIdList) == 0 and len(ratingList) == 0:
            return
        sframe = tc.SFrame({'user_id': userIdList,
                      'item_id': itemIdList,
                       'rating': ratingList})
        mlRecommender = tc.recommender.create(sframe, target='rating')
        results = tuple(mlRecommender.recommend())
        filteredResults = []
        redis.flushdb()
        for result in results:
            if(result.get('rank') != 1):
                continue
            hobbyistId = result.get('user_id')
            artistId = result.get('item_id')
            redis.set(hobbyistId, artistId)
        self.logger.info("Result from ML Rating Recommender %s", filteredResults)

    