from flask import Flask

from configurations.configurations import register_blueprint
from elasticsearch import Elasticsearch


app = Flask(__name__)
app = register_blueprint(app)

# ELASTIC_USER='elastic'
# ELASTIC_PASS='_VVwXtRyQtvvZ9Hz7h89'
# es = Elasticsearch(hosts='https://100.26.110.188:9200',
#                    basic_auth=(ELASTIC_USER, ELASTIC_PASS),
#                    verify_certs=False)

es=Elasticsearch('https://elastic:_VVwXtRyQtvvZ9Hz7h89@100.26.110.188:9200',verify_certs=False)
print(es.info())

# @app.route('/',methods=['GET'])
# def home():
#    return "<h1 style='text-align:center'>ELASTIC SEARCH</h1>"




if __name__ == "__main__":
  app.run(host='0.0.0.0', port=9000,debug=True)
'''gunicorn -w 4 -b 0.0.0.0:8000 'app:app'''