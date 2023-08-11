#!/usr/bin/python3
"""Place class module"""

from base_model import BaseModel

class Place(BaseModel):

    """Class to rep a place"""
    city_id = ""
    user_id = ""
    name = ""
    description =""
    number_rooms = ""
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = None
    longitude = None
    amenity_ids = []
