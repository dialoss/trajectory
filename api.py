import requests

from middlewares import MiddlewareDecorator
from models import Vehicle
from response import Response


class API(MiddlewareDecorator):
    def __init__(self, url):
        self.url = url + 'vehicles'

    def get(self, id=None):
        if id is None:
            return Response(requests.get(self.url), many=True)
        else:
            return Response(requests.get(f"{self.url}/{id}"))

    def post(self, instance: Vehicle):
        return Response(requests.post(self.url, json=instance.json()))

    def delete(self, id):
        return Response(requests.delete(f"{self.url}/{id}"))

    def put(self, instance: Vehicle):
        return Response(requests.put(f"{self.url}/{instance.id}", json=instance.json()))
