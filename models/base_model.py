#!/usr/bin/python3
"""Module for the base class
It has the base class for the console
"""

import uuid
from datetime import datetime
from models import storage

class BaseModel:
    """Class for base model"""

    def __init__(self, *args, **kwargs):
        """Initialize base instance
    
        Args:
            - *args: ist of arguments
            - **kwargs: dictionary of key-value arguments(key worded)
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return a string representation of an instance"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)
    
    def save(self):
        """Updates the updated_at attrib with the current datetime"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return a dictionary rep of an instance"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["__created_at"] = my_dict["__created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict