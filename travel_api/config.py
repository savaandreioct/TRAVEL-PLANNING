import connexion
from connexion.apps.flask_app import FlaskJSONEncoder
from flask_cors import CORS
from db import Neo4jConfig
from flask import Flask


class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def i(self, service="NotSet"):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls(service)
            return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through `i()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)

    def destroy(self):
        del self._instance


@Singleton
class ApiConfig:
    def __init__(self, service):
        print(service)
        # self.app = connexion.App(
        #     __name__,
        #     spe
        # )
        self.app = Flask(__name__)
        # self.app.add_api(
        #     "/swagger/swagger.yml",
        #     arguments={"title": "Harlock Server"},
        # )
        # self.app.app.json_encoder = FlaskJSONEncoder
        # CORS(self.app.app)
        # self.app.app.debug = True
        self.db = Neo4jConfig(
            "neo4j+s://4dfb58fc.databases.neo4j.io",
            "neo4j",
            "3plt7Uk_9GsAXmzUiYd06rqETV7LzYDAUnwOTu_An6Q",
        )
