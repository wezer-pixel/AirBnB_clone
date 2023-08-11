#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(plc))
        self.assertNotIn("city_id", plc.__dict__)

    def test_user_id_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(plc))
        self.assertNotIn("user_id", plc.__dict__)

    def test_name_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(plc))
        self.assertNotIn("name", plc.__dict__)

    def test_description_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(plc))
        self.assertNotIn("desctiption", plc.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(plc))
        self.assertNotIn("number_rooms", plc.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(plc))
        self.assertNotIn("number_bathrooms", plc.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(plc))
        self.assertNotIn("max_guest", plc.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(plc))
        self.assertNotIn("price_by_night", plc.__dict__)

    def test_latitude_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(plc))
        self.assertNotIn("latitude", plc.__dict__)

    def test_longitude_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(plc))
        self.assertNotIn("longitude", plc.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        plc = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(plc))
        self.assertNotIn("amenity_ids", plc.__dict__)

    def test_two_places_unique_ids(self):
        plc1 = Place()
        plc2 = Place()
        self.assertNotEqual(plc1.id, plc2.id)

    def test_two_places_different_created_at(self):
        plc1 = Place()
        sleep(0.05)
        plc2 = Place()
        self.assertLess(plc1.created_at, plc2.created_at)

    def test_two_places_different_updated_at(self):
        plc1 = Place()
        sleep(0.05)
        plc2 = Place()
        self.assertLess(plc1.updated_at, plc2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        plc = Place()
        plc.id = "123456"
        plc.created_at = pl.updated_at = dt
        plcstr = plc.__str__()
        self.assertIn("[Place] (123456)", plcstr)
        self.assertIn("'id': '123456'", plcstr)
        self.assertIn("'created_at': " + dt_repr, plcstr)
        self.assertIn("'updated_at': " + dt_repr, plcstr)

    def test_args_unused(self):
        plc = Place(None)
        self.assertNotIn(None, plc.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        plc = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(plc.id, "345")
        self.assertEqual(plc.created_at, dt)
        self.assertEqual(plc.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        plc = Place()
        sleep(0.05)
        first_updated_at = plc.updated_at
        plc.save()
        self.assertLess(first_updated_at, plc.updated_at)

    def test_two_saves(self):
        plc = Place()
        sleep(0.05)
        first_updated_at = plc.updated_at
        plc.save()
        second_updated_at = plc.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        plc.save()
        self.assertLess(second_updated_at, plc.updated_at)

    def test_save_with_arg(self):
        plc = Place()
        with self.assertRaises(TypeError):
            plc.save(None)

    def test_save_updates_file(self):
        plc = Place()
        plc.save()
        plcid = "Place." + plc.id
        with open("file.json", "r") as f:
            self.assertIn(plcid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        plc = Place()
        self.assertIn("id", plc.to_dict())
        self.assertIn("created_at", plc.to_dict())
        self.assertIn("updated_at", plc.to_dict())
        self.assertIn("__class__", plc.to_dict())

    def test_to_dict_contains_added_attributes(self):
        plc = Place()
        plc.middle_name = "Holberton"
        plc.my_number = 98
        self.assertEqual("Holberton", plc.middle_name)
        self.assertIn("my_number", plc.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        plc = Place()
        plc_dict = pl.to_dict()
        self.assertEqual(str, type(plc_dict["id"]))
        self.assertEqual(str, type(plc_dict["created_at"]))
        self.assertEqual(str, type(plc_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        plc = Place()
        plc.id = "123456"
        plc.created_at = plc.updated_at = dt
        hdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(plc.to_dict(), hdict)

    def test_contrast_to_dict_dunder_dict(self):
        plc = Place()
        self.assertNotEqual(plc.to_dict(), plc.__dict__)

    def test_to_dict_with_arg(self):
        plc = Place()
        with self.assertRaises(TypeError):
            plc.to_dict(None)


if __name__ == "__main__":
    unittest.main()

