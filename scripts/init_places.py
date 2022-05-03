import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend import crud
from backend.database.session import SessionLocal
from backend.schemas.place import PlaceCreate


db = SessionLocal()

places = [
    {
        "label": "Малый Аякс",
        "latitude": 43.036145,
        "longitude": 131.890044
    },
    {
        "label": "Корпус 11",
        "latitude": 43.026774,
        "longitude": 131.901925
    },
    {
        "label": "Корпус 10",
        "latitude": 43.02559,
        "longitude": 131.900383
    },
    {
        "label": "Корпус 9",
        "latitude": 43.02482,
        "longitude": 131.898367
    },
    {
        "label": "Корпус 8.1",
        "latitude": 43.027556,
        "longitude": 131.886741
    },
    {
        "label": "Корпус 8.2",
        "latitude": 43.028656,
        "longitude": 131.886355
    },
    {
        "label": "Корпус 7.1",
        "latitude": 43.030105,
        "longitude": 131.88622
    },
    {
        "label": "Корпус 7.2",
        "latitude": 43.031282,
        "longitude": 131.886481
    },
    {
        "label": "Корпус 6.1",
        "latitude": 43.032755,
        "longitude": 131.887079
    },
    {
        "label": "Корпус 6.2",
        "latitude": 43.033749,
        "longitude": 131.887754
    },
    {
        "label": "Корпус 5",
        "latitude": 43.032984,
        "longitude": 131.889897
    },
    {
        "label": "Корпус 4",
        "latitude": 43.031823,
        "longitude": 131.88906
    },
    {
        "label": "Корпус 3",
        "latitude": 43.030547,
        "longitude": 131.888647
    },
    {
        "label": "Корпус 2",
        "latitude": 43.029196,
        "longitude": 131.888659
    },
    {
        "label": "Корпус 1",
        "latitude": 43.02786,
        "longitude": 131.889103
    },
    {
        "label": "Корпус G",
        "latitude": 43.02595,
        "longitude": 131.888494
    },
    {
        "label": "Корпус G",
        "latitude": 43.026684,
        "longitude": 131.890336
    },
    {
        "label": "Корпус D",
        "latitude": 43.025793,
        "longitude": 131.891582
    },
    {
        "label": "Корпус B",
        "latitude": 43.025286,
        "longitude": 131.892527
    },
    {
        "label": "Корпус A",
        "latitude": 43.025004,
        "longitude": 131.894041
    },
    {
        "label": "Корпус C",
        "latitude": 43.024694,
        "longitude": 131.894879
    },
    {
        "label": "Корпус E",
        "latitude": 43.024673,
        "longitude": 31.896114
    },
    {
        "label": "Корпус F",
        "latitude": 43.024616,
        "longitude": 131.897406
    },
    {
        "label": "Корпус L",
        "latitude": 43.024912,
        "longitude": 131.887107
    },
    {
        "label": "Корпус M",
        "latitude": 43.02171,
        "longitude": 131.891468
    },
    {
        "label": "Стадион",
        "latitude": 43.029911,
        "longitude": 131.890511
    },
    {
        "label": "Парк",
        "latitude": 43.026718,
        "longitude": 131.895024
    },
    {
        "label": "Набережная",
        "latitude": 43.030101,
        "longitude": 131.895424
    },
    {
        "label": "Южные ворота",
        "latitude": 43.023294,
        "longitude": 131.898468
    },
    {
        "label": "ДВФУ",
        "latitude": 43.02361,
        "longitude": 131.891898
    },
    {
        "label": "Лаборатория",
        "latitude": 43.02517,
        "longitude": 131.887892
    },
    {
        "label": "Вертодром",
        "latitude": 43.030122,
        "longitude": 131.884223
    },
    {
        "label": "Мини-ТЭЦ",
        "latitude": 43.036829,
        "longitude": 131.884692
    },
]
if not crud.place.get_multi(db):
    for place in places:
        crud.place.create(db, obj_in=PlaceCreate(**place))
