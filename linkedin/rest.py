# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json
from bson import json_util
from pymongo import MongoClient

from scrapy.signalmanager import SignalManager
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from multiprocessing import Process, Queue
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from linkedin.spiders.bing import BingSpider

from flasgger import Swagger

class CrawlerScript():
    def __init__(self):
        settings = get_project_settings()
        settings.set('LOG_ENABLED', False, priority='cmdline')
        self.crawler = CrawlerProcess(settings)
        self.items = []
        SignalManager(dispatcher.Any).connect(self._item_passed, signal=signals.item_scraped)

    def _item_passed(self, item, response, spider):
        self.items.append(item)

    def _crawl(self, q, queue):
        self.crawler.crawl(BingSpider, q=q)
        self.crawler.start()
        self.crawler.stop()
        queue.put(self.items)

    def crawl(self, q):
        queue = Queue()
        p = Process(target=self._crawl, args=[q, queue])
        p.start()
        p.join()
        return queue.get(True)

# Flask
app = Flask(__name__)

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "0.0.1",
            "title": "Api v1",
            "endpoint": 'v1_spec',
            "route": '/v1/spec',
        }
    ]
}

Swagger(app)

crawler = CrawlerScript()
# MongoDB connection
connection = MongoClient('localhost', 27017)
db = connection.linkedin

def toJson(data):
    """Convert object(s) to JSON"""
    return json.dumps(data, default=json_util.default)

@app.route('/users/', methods=['GET'])
def users():
    """
    Return a list of all users possible filtered by company and full_name
    ---
    tags:
      - users
    parameters:
      - name: limit
        in: query
        type: integer
        description: limit of users returned
        required: false
        default: 10
      - name: offset
        in: query
        type: integer
        description: offset of users to start with
        required: false
        default: 0
      - name: company
        in: query
        type: string
        description: name of company
        required: false
      - name: full_name
        in: query
        type: string
        description: user's full name
        required: false
    responses:
      200:
        description: user items
        schema:
          id: return_user
          properties:
            result:
              type: json array
              description: array of user's info
      404:
        description: users not found
    """
    if request.method == 'GET':
        lim = int(request.args.get('limit', 10))
        off = int(request.args.get('offset', 0))
        full_name = request.args.get('full_name', '')
        current = request.args.get('company', '')
        q = {'topcard': {'$exists': True}}
        if full_name:
            q['topcard.full_name'] = full_name
        if current:
            q['topcard.current'] = current
        results = db['users'].find(q, {'_id':0}).skip(off).limit(lim)
        json_results = []
        if (full_name or current) and results.count() == 0:
            q = "%s %s linkedin" % (full_name, current)
            r = crawler.crawl(q)
            if r:
                r = [ dict(i) for i in r if 'topcard' in i ]
                json_results.extend(r)
        else:
            for result in results:
                json_results.append(result)
        if json_results:
            return toJson(json_results)
        else:
            return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=False)
