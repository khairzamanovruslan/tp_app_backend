from pydantic import BaseModel


class SSubstation_Coordinates(BaseModel):
    latitude: str = "57.042185"
    longitude: str = "60.504975"

class SSubstation_NameCoordinates(SSubstation_Coordinates):
    name: str = "777"

class SSubstation_FullData(SSubstation_NameCoordinates):
    link: str = 'https://yandex.ru/maps/?pt=60.504975,57.042185&z=18&l=map'
