#!/usr/bin/env python
import logging
import datetime
from pymongo import MongoClient
from django.conf import settings

LOGGING = logging.getLogger('')


def mongodb_get_cpu(uuid, start, end):
    mongodb_client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    db = mongodb_client.VmDataBase
    collection = db[uuid]

    if start is not None and end is not None:
        match = {
            '$match': {
                'time': {
                    '$gt': start,
                    '$lt': end
                }
            }
        }
    elif start is not None and end is None:
        match = {
            '$match': {
                'time': {
                    '$gt': start
                }
            }
        }
    else:
        match = {'$match': {}}

    results =collection.aggregate([match, {'$project': {'_id': 0, 'time': 1, 'cpu.cpu_usage': 1}}])

    return [{'time': result['time'], 'cpu_usage': result['cpu']['cpu_usage']} for result in results]


def mongodb_get_memory(uuid, start, end):
    mongodb_client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    db = mongodb_client.VmDataBase
    collection = db[uuid]

    if start is not None and end is not None:
        match = {
            '$match': {
                'time': {
                    '$gt': start,
                    '$lt': end
                }
            }
        }
    elif start is not None and end is None:
        match = {
            '$match': {
                'time': {
                    '$gt': start
                }
            }
        }
    else:
        match = {'$match': {}}

    results = collection.aggregate([match, {'$project': {'_id': 0, 'time': 1, 'memory.usage': 1}}])

    return [{'time': result['time'], 'memory_usage': result['memory']['usage']} for result in results]


def mongodb_get_disk(uuid, start, end, item):
    mongodb_client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    db = mongodb_client.VmDataBase
    collection = db[uuid]

    if start is not None and end is not None:
        match = {
            '$match': {
                'time': {
                    '$gt': start,
                    '$lt': end
                }
            }
        }
    elif start is not None and end is None:
        match = {
            '$match': {
                'time': {
                    '$gt': start
                }
            }
        }
    else:
        match = {'$match': {}}

    if item == 'rds':
        item = 'rd_bytes_speed'
    elif item == 'rdops':
        item = 'rd_req_speed'
    elif item == 'wrs':
        item = 'wr_bytes_speed'
    elif item == 'wrops':
        item = 'wr_req_speed'
    else:
        return []

    project = {
        '$project': {
            '_id': 0,
            'time': 1,
            'disk': 1
        }
    }

    results = collection.aggregate([match, project])

    data = {}
    for result in results:
        for key, value in result['disk'].items():
            if data.get(key, None) is None:
                data[key] = []

            data[key].append({'time': result['time'], 'value': value[item]})

    return data


def mongodb_get_interface(uuid, start, end, item):
    mongodb_client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    db = mongodb_client.VmDataBase
    collection = db[uuid]

    if start is not None and end is not None:
        match = {
            '$match': {
                'time': {
                    '$gt': start,
                    '$lt': end
                }
            }
        }
    elif start is not None and end is None:
        match = {
            '$match': {
                'time': {
                    '$gt': start
                }
            }
        }
    else:
        match = {'$match': {}}

    if item == 'rxs':
        item = 'rx_bytes_speed'
    elif item == 'txs':
        item = 'tx_bytes_speed'
    else:
        return []

    project = {
        '$project': {
            '_id': 0,
            'time': 1,
            'interface': 1
        }
    }

    results = collection.aggregate([match, project])

    data = {}
    for result in results:
        for key, value in result['interface'].items():
            if data.get(key, None) is None:
                data[key] = []

            data[key].append({'time': result['time'], 'value': value[item]})

    return data


def mongodb_get_last(uuid):
    mongodb_client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    db = mongodb_client.VmDataBase
    collection = db[uuid]

    sort = {
        '$sort': {
            'time': -1
        }
    }

    datas = collection.aggregate([sort])

    try:
        data = datas.next()
    except StopIteration:
        data = {}

    for key, value in data['disk'].items():
        data['disk'][key].pop('err')
        data['disk'][key].pop('rd_bytes')
        data['disk'][key].pop('rd_req')
        data['disk'][key].pop('rd_req_speed')
        data['disk'][key].pop('wr_bytes')
        data['disk'][key].pop('wr_req')
        data['disk'][key].pop('wr_req_speed')

    for key, value in data['interface'].items():
        data['interface'][key].pop('rx_bytes')
        data['interface'][key].pop('rx_drop')
        data['interface'][key].pop('rx_errs')
        data['interface'][key].pop('rx_packets')
        data['interface'][key].pop('tx_bytes')
        data['interface'][key].pop('tx_drop')
        data['interface'][key].pop('tx_errs')
        data['interface'][key].pop('tx_packets')

    return {'uuid': data['uuid'],
            'time': data['time'],
            'cpu_usage': data['cpu']['cpu_usage'],
            'memory_usage': data['memory']['usage'],
            'disk': data['disk'],
            'interface': data['interface']}


def mongodb_get_data(uuid, start, end, item=None):
    if start:
        start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    if end:
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

    uuid = uuid.strip()

    if item == 'cpu usage':
        data = mongodb_get_cpu(uuid, start, end)
    elif item == 'memory usage':
        data = mongodb_get_memory(uuid, start, end)
    elif item == 'disk read speed':
        data = mongodb_get_disk(uuid, start, end, 'rds')
    elif item == 'disk write speed':
        data = mongodb_get_disk(uuid, start, end, 'wrs')
    elif item == 'incoming network traffic':
        data = mongodb_get_interface(uuid, start, end, 'rxs')
    elif item == 'outgoing network traffic':
        data = mongodb_get_interface(uuid, start, end, 'txs')
    else:
        data = mongodb_get_last(uuid)

    return data

