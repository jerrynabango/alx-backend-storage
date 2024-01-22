#!/usr/bin/env python3
""" Log stats"""

from pymongo import MongoClient


if __name__ == "__main__":
    """provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    log_stat = client.logs.nginx
    print("{} logs".format(log_stat.estimated_document_count()))
    print("Methods:")
    for methods in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = log_stat.count_documents({'methods': methods})
        print("\tmethod {}: {}".format(methods, count))
    status_get = log_stat.count_documents({'methods': 'GET', 'path': "/status"})
    print("{} status check".format(status_get))
