import json
import traceback
from datetime import datetime
import uuid
from PyPDF2 import PdfFileReader

from flask import Blueprint
from flask import request

from common.responses import success, failed
es_search = Blueprint('search', __name__, url_prefix='/api/v1/es/')


@es_search.route('insert_data', methods=['POST'])
def insert_data():
    try:
        from app import es
        mapping = { "settings": { "number_of_shards": 2, "number_of_replicas": 1 }, "mappings": { "properties": { "content": { "type": "text" } } } }
        response = es.indices.create(
            index="some_new_index",
            body=mapping,
            ignore=400  # ignore 400 already exists code
        )
        file_obj = request.files['file']
        filename=file_obj.filename
        file_format=filename.split('.')
        pdf = PdfFileReader(file_obj)
        # content_list=[]
        text=''
        for page in range(pdf.getNumPages()):
            text+=pdf.getPage(page).extractText()
            # content_list.append({
            #     'page_'+str(page):text
            # })

        id = uuid.uuid4()
        body = {
            'id': id,
            'file_name': filename,
            'content': text,
            'file_type':file_format[-1],
            'timestamp': datetime.now()
        }

        result = es.index(index='some_new_index', id=id, body=body)
        # print(result)
        # result = es.index(index='content', id=slug, body=body)

        return success({"result": body}, "Successfully created")
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
                    "fields": ["content",'file_name','file_type','data','content']
                }
            }
        }
        res = es.search(index="some_new_index", body=body)
        data = res['hits']['hits']
        return success({"result": data}, "Successfully retrieved")
    except Exception as e:
        # print(traceback.format_exc())
        return failed({}, str(e))

