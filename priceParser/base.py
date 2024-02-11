import redis
import os
from dotenv import load_dotenv
from typing import Optional
import logging

class RedisConnection():
    def __init__(self) -> None:
        load_dotenv()
        self.r = redis.StrictRedis(host='localhost',port=6379,db=0,password=os.getenv('REDIS_PASSWORD'))

    def get(self, key : str) -> Optional[bytes]:
        try:
            return self.r.get(key)
        except Exception as e:
            logging.critical("Can not get info from redis database", exc_info=e)
        return None
    
    def set(self, key : str, value : str, storageDuration : int) -> None:
        try:
            self.r.set(key, value, storageDuration) 
        except Exception as e:
            logging.critical("Can not set info to redis database", exc_info=e)