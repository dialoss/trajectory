import math
from math import cos, asin, sqrt

from api import API
from middlewares import MiddlewareDecorator, APIMiddleware, ManagerMiddleware
from models import Vehicle


class VehicleManager(MiddlewareDecorator):
    def __init__(self, url):
        self.api = API(url=url)
        self.api.use(APIMiddleware(), pre=True, post=True)  # use requests cache

    def get_all(self):
        return self.api.get().data

    def filter(self, params={}):
        data = self.get_all()
        filtered = []
        for it in data:
            if not len(params) or all(it.__getattribute__(f) == params[f] for f in params):
                filtered.append(it)
        return filtered

    def get(self, id):
        return self.api.get(id).data

    def create(self, instance: Vehicle):
        return self.api.post(instance).data

    def remove(self, id):
        return self.api.delete(id).data

    def update(self, instance: Vehicle):
        return self.api.put(instance).data

    def get_distance(self, id1, id2):
        if not id1 or not id2:
            raise Exception("Invalid id")
        v1 = self.get(id1)
        v2 = self.get(id2)
        lat1, lon1 = v1.latitude, v1.longitude
        lat2, lon2 = v2.latitude, v2.longitude
        p = math.pi / 180
        r = 12742
        a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return r * asin(sqrt(a)) * 1000

    def get_nearest(self, id):
        current = self.get(id)
        min_dist = 1e15
        nearest = None
        for it in self.get_all():
            if it.id == current.id:
                continue
            dist = self.get_distance(it.id, current.id)
            if min_dist > dist:
                min_dist = dist
                nearest = it
        return nearest


manager = VehicleManager(url="https://test.tspb.su/test-task/")

manager.use(ManagerMiddleware())  # logging middleware

manager.get(2)
manager.get_all()
manager.get_distance(3, 4)
manager.get_nearest(2)

new = manager.get(2)
new.name = 'Audi'
manager.update(new)

manager.create(Vehicle(name='Toyota',
                       model='Camry',
                       year=2021,
                       color='red',
                       price=21000,
                       latitude=55.753215,
                       longitude=37.620393))
