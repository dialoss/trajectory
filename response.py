from models import Vehicle


class Response:
    data: Vehicle | list[Vehicle]
    raw: object

    def __init__(self, response=None, instance: Vehicle = None, many=False):
        self.raw = response
        if instance:
            self.data = instance
            return
        if str(response.status_code)[0] != '2':
            raise Exception("Failed to fetch")
        if response.status_code == 204:
            self.data = Vehicle(empty=True)
            return
        json = response.json()
        if many:
            self.data = []
            for it in json:
                self.data.append(Vehicle(**it))
        else:
            self.data = Vehicle(**json)
