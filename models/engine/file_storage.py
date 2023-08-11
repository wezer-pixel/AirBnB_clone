#!/usr/bin/python3
"""FileStorage class module"""
import datetime
import json
import os

class FileStorage:

    """
    Class for json serialization and deserealization of base classes
    """
    __file_path = "file.json"
    __object = {}

    def all(self):
        """Return __object dict"""
        return FileStorage.__object
    
    def new(self, obj):
        """Return new object in __object dict"""
        key = "{}.{}".format(type(obj).__name__, obj.id)

    def save(self):
        """Serialize __Object to JSON file"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            d = {k: v.todict() for k, v in FileStorage.__object.items()}
            json.dump(d, f)

    def classes(self):
        """Return a dict of valid classes and their references"""

        from base_model import BaseModel
        from user import User
        from state import State
        from city import City
        from amenity import Amenity
        from place import Place
        from review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes
    
    def reload(self):
        """Deserealization JSON to __object"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            obj_dict = {k: self.classes()[v["__class__"]](**v)
                        for k, v in obj_dict.items()}
            FileStorage.__object = obj_dict


    def attr(self):
        """Return attributes anf their type for a class"""
        attr = {
            "BaseModel":
                    {"id": str,
                     "created_at": datetime.datetime,
                     "updated_at": datetime.datetime},
            "User":
                    {"email": str,
                     "password": str,
                     "first_name": str,
                     "last_name": str},
            "State":
                    {"name": str},
            "City":
                    {"state_id": str,
                     "name": str},
            "Amenity":
                    {"name": str},
            "Place":
                    {"city_id": str,
                     "user_id": str,
                     "name": str,
                     "description": str,
                     "number_rooms": int,
                     "number_bathrooms": int,
                     "max_guest":int,
                     "price_by_night": int,
                     "latitude": float,
                     "longitude": float,
                     "amenity_ids": list},
            "Reviews":
                    {"place_id": str,
                     "user_id": str,
                     "text": str}
        }

        return attr