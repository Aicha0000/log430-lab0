import redis
import json
import os
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
    def get(self, key):
        """recupere une valeur du cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except:
            return None
    
    def set(self, key, value, ttl_seconds=300):
        """met une valeur dans le cache avec TTL"""
        try:
            serialized = json.dumps(value, default=str)
            return self.redis_client.setex(key, ttl_seconds, serialized)
        except:
            return False
    
    def delete(self, key):
        """supprime une cle du cache"""
        try:
            return self.redis_client.delete(key)
        except:
            return False
    
    def delete_pattern(self, pattern):
        """supprime toutes les cles qui matchent le pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except:
            return 0
    
    def is_connected(self):
        """verifie si redis est connecte"""
        try:
            self.redis_client.ping()
            return True
        except:
            return False

# instance globale du cache
cache = CacheManager()