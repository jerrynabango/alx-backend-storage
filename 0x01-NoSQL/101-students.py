#!/usr/bin/env python3
"""Top students"""

from pymongo import MongoClient
from typing import Iterator


def top_students(mongo_collection: MongoClient) -> Iterator:
    """returns all students sorted by average score"""
    return mongo_collection.aggregate([
        {"$addFields": {"averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ])
