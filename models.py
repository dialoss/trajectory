class Model:
    def __init__(self, empty=False, **kwargs):
        fields = self.__class__.__annotations__
        for f in fields:
            field_type = fields.get(f)
            val = kwargs.get(f)
            required = not (f == 'id' and not val)
            if not empty and required:
                if val is None:
                    raise Exception(f"Field {f} is required")

                if not isinstance(val, field_type):
                    raise Exception(f"Field {f} must be {field_type}")
            if required:
                self.__setattr__(f, val)

    def json(self):
        return self.__dict__


class Vehicle(Model):
    id: int
    name: str
    model: str
    year: int
    color: str
    price: int
    latitude: float
    longitude: float
