#!/usr/bin/env python3
"""Log stats"""

from pymongo import MongoClient


def log_stats() -> None:
    """provides some stats about Nginx logs stored in MongoDB"""
    stats = ""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    stats += "{} logs\nMethods:\n".format(nginx_collection.count_documents({}))
    for method in methods:
        method_count = nginx_collection.count_documents({"methods": method})
        stats += '\tmethod {}: {}\n'.format(method, method_count)
    stats += "{} status check".format(
            nginx_collection.count_documents({"path": "/status"}))
    print(stats)


if __name__ == '__main__':
    log_stats()
