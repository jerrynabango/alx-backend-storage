#!/usr/bin/env python3
"""Log stats - new version"""

from pymongo import MongoClient


def log_stat() -> None:
    """
    Improve 12-log_stats.py by adding the top 10 of the most present
    IPs in the collection nginx of the database logs:
    """
    statas = ""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    statas += "{} logs\nMethods:\n".format(nginx_collection.count_documents({}))
    for m in method:
        method_count = nginx_collection.count_documents({"method": m})
        statas += "\tmethod {}: {}\n".format(m, method_count)
    statas += "{} status check".format(
        nginx_collection.count_documents({"path": "/status"}))
    statas += "\nIPs:\n"
    top_ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, {"$limit": 10}])
    for ip in top_ips:
        statas += "\t{}: {}\n".format(ip.get("_id"), ip.get("count"))
    print(statas, end='')


if __name__ == '__main__':
    log_stat()
