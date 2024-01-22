#!/usr/bin/env python3
"""List all documents in Python"""

from typing import Iterator
from pymongo import MongoClient


def list_all(mongo_collection: MongoClient) -> Iterator:
    """function that lists all documents in a collection"""
    if mongo_collection.count() == 0:
        return []
    return mongo_collection.find()
