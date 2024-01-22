#!/usr/bin/env python3
"""Insert a document in Python"""

from typing import Mapping
from pymongo import MongoClient


def insert_school(mongo_collection: MongoClient,
                  **kwargs: Mapping[str, str]) -> str:
    """inserts a new document in a collection based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id
