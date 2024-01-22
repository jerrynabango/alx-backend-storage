#!/usr/bin/env python3
"""Log stats"""

from pymongo import MongoClient


def log_stats() -> None:
    """provides some stats about Nginx logs stored in MongoDB"""
    statas = ""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    statas += "{} logs\nMethods:\n".format(nginx_collection.count_documents({}))
    for m in method:
        method_count = nginx_collection.count_documents({"method": m})
        statas += '\tmethod {}: {}\n'.format(m, method_count)
    statas += "{} status check".format(
            nginx_collection.count_documents({"path": "/status"}))
    print(statas)


if __name__ == '__main__':
    log_stats()
