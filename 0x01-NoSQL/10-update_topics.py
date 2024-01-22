#!/usr/bin/env python3
"""Change school topics"""

from typing import List
from pymongo import MongoClient


def update_topics(mongo_collection: MongoClient,
                  name: str, topics: List[str]) -> str:
    """changes all topics of a school document based on the name"""
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
