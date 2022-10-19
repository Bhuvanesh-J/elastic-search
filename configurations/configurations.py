# from api.search.views import es_search
from api.search.views import es_search


def register_blueprint(app):
    app.register_blueprint(es_search)
    return app
