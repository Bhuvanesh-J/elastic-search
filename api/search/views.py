import json
import traceback
from datetime import datetime
import uuid
from PyPDF2 import PdfFileReader

from flask import Blueprint
from flask import request
import pandas as pd

from common.responses import success, failed
import json
import traceback
import uuid
from datetime import datetime

import pandas as pd
from PyPDF2 import PdfFileReader
from flask import Blueprint
from flask import request

from common.responses import success, failed

es_search = Blueprint('search', __name__, url_prefix='/api/v1/es/')


@es_search.route('insert_data', methods=['POST'])
def insert_data():
    try:
        from app import es
        mapping = {"settings": {"number_of_shards": 2, "number_of_replicas": 1},
                   "mappings": {"properties": {"content": {"type": "text"}}}}
        es.indices.create(
            index="file_searching",
            body=mapping,
            ignore=400  # ignore 400 already exists code
        )
        if 'file' not in request.files:
            return failed({}, "File is missing please send the file.")
        file_obj = request.files['file']

        filename = file_obj.filename
        file_format = filename.split('.')
        if file_format[-1] not in ['pdf']:

            excel_data = pd.read_excel(file_obj)
            data_list = json.loads(excel_data.to_json(orient='records'))
            for data_dict in data_list:
                id = uuid.uuid4()
                data_dict['id'] = str(id)
                data_dict['file_name'] = filename
                data_dict['file_type'] = file_format[-1]
                data_dict['timestamp'] = datetime.now()

                es.index(index='file_searching', id=id, body=data_dict)
            id = uuid.uuid4()
            es.index(index='file_history', id=id, body={
                'id': id,
                'file_name': filename,
                'file_type': file_format[-1],
                'timestamp': datetime.now(),
                'search':"all_files"
            })

            return success({})

        pdf = PdfFileReader(file_obj)
        text = ''
        for page in range(pdf.getNumPages()):
            text += pdf.getPage(page).extractText()
        id = uuid.uuid4()
        body = {
            'id': id,
            'file_name': filename,
            'content': text,
            'file_type': file_format[-1],
            'timestamp': datetime.now()
        }

        es.index(index='file_searching', id=id, body=body)
        es.index(index='file_history', id=id, body={
            'id': id,
            'file_name': filename,
            'file_type': file_format[-1],
            'timestamp': datetime.now(),
            'search':"all_files"
        })
        return success({})
    except Exception as e:
        print(traceback.format_exc())
        return failed({}, str(e))


@es_search.route('search', methods=['POST'])
def search():
    try:
        from app import es

        keyword = request.get_json()['keyword']

        body = {
            "query": {
                "multi_match": {
                    "query": keyword
                    # "fields": ["content",'file_name','file_type','data','content']
                    # "fields": ['content']
                }
            }
        }
        res = es.search(index="file_searching", body=body)
        data = res['hits']['hits']
        return success({"result": data}, "Successfully retrieved")
    except Exception as e:
        print(traceback.format_exc())
        return failed({}, str(e))

@es_search.route('get_file_history', methods=['GET'])
def get_file_history():
    try:
        from app import es
        body = {
            "query": {
                "multi_match": {
                    "query": 'all_files',
                    "fields": ['search']
                    # "fields": ['content']
                }
            }
        }
        res = es.search(index="file_history", body=body)
        data = res['hits']['hits']
        return success({"result": data}, "Successfully retrieved")
    except Exception as e:
        print(traceback.format_exc())
        return failed({}, str(e))
