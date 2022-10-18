import json
import traceback
from datetime import datetime

from flask import Blueprint
from flask import request

from common.responses import success, failed
es_search = Blueprint('search', __name__, url_prefix='/api/v1/es/')


@es_search.route('insert_data', methods=['POST'])
def insert_data():
    try:
        from app import es
        slug = 'file_name'
        body = {
            'slug': slug,
            'title': 'search_something',
            'content': 'byte_data',
            'timestamp': datetime.now()
        }

        result = es.index(index='contents', id=slug, body=body,request_timeout=30)
        # result = es.index(index='content', id=slug, body=body)

        return success({"result": ""}, "Successfully created")
    except Exception as e:
        # print(traceback.format_exc())
        return failed({}, str(e))


# @es_search.route('create', methods=['POST'])
# def insert_data():
#     try:
#         from app import es
#         slug = '4'
#         body = {
#             'slug': slug,
#             'title': 'search_something',
#             'content': "Check Your Text Thoroughly To Eliminate Any Kind Of Grammar or Punctuation Errors. With Grammarly's App, You Can Check Grammar In Real Time As You Type On Almost Any Website. AI Writing Assistant. Eliminate Grammar Errors. Improve Word Choice",
#             'timestamp': datetime.now()
#         }
#
#         result = es.index(index='contents', id=slug, body=body,request_timeout=30)
#         # result = es.index(index='content', id=slug, body=body)
#         return success({"result": ""}, "Successfully created")
#     except Exception as e:
#         # print(traceback.format_exc())
#         return failed({}, str(e))

@es_search.route('search', methods=['POST'])
def search():
    try:
        from app import es

        keyword = request.get_json()['keyword']

        body = {
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["content", "title"]
                }
            }
        }
        res = es.search(index="contents", body=body,request_timeout=30)
        data = res['hits']['hits']
        return success({"result": data}, "Successfully retrieved")
    except Exception as e:
        # print(traceback.format_exc())
        return failed({}, str(e))

