#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        ame = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", ame.__dict__)

    def test_two_amenities_unique_ids(self):
        ame1 = Amenity()
        ame2 = Amenity()
        self.assertNotEqual(ame1.id, ame2.id)

    def test_two_amenities_different_created_at(self):
        ame1 = Amenity()
        sleep(0.05)
        ame2 = Amenity()
        self.assertLess(ame1.created_at, ame2.created_at)

    def test_two_amenities_different_updated_at(self):
        ame1 = Amenity()
        sleep(0.05)
        ame2 = Amenity()
        self.assertLess(ame1.updated_at, ame2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        ame = Amenity()
        ame.id = "123456"
        ame.created_at = ame.updated_at = dt
        amestr = ame.__str__()
        self.assertIn("[Amenity] (123456)", amestr)
        self.assertIn("'id': '123456'", amestr)
        self.assertIn("'created_at': " + dt_repr, amestr)
        self.assertIn("'updated_at': " + dt_repr, amestr)

    def test_args_unused(self):
        ame = Amenity(None)
        self.assertNotIn(None, ame.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        ame = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(ame.id, "345")
        self.assertEqual(ame.created_at, dt)
        self.assertEqual(ame.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

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
        ame = Amenity()
        sleep(0.05)
        first_updated_at = ame.updated_at
        ame.save()
        self.assertLess(first_updated_at, ame.updated_at)

    def test_two_saves(self):
        ame = Amenity()
        sleep(0.05)
        first_updated_at = ame.updated_at
        ame.save()
        second_updated_at = ame.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ame.save()
        self.assertLess(second_updated_at, ame.updated_at)

    def test_save_with_arg(self):
        ame = Amenity()
        with self.assertRaises(TypeError):
            ame.save(None)

    def test_save_updates_file(self):
        ame = Amenity()
        ame.save()
        amid = "Amenity." + ame.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        ame = Amenity()
        self.assertIn("id", ame.to_dict())
        self.assertIn("created_at", ame.to_dict())
        self.assertIn("updated_at", ame.to_dict())
        self.assertIn("__class__", ame.to_dict())

    def test_to_dict_contains_added_attributes(self):
        ame = Amenity()
        ame.middle_name = "Holberton"
        ame.my_number = 98
        self.assertEqual("Holberton", ame.middle_name)
        self.assertIn("my_number", ame.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        ame = Amenity()
        ame_dict = ame.to_dict()
        self.assertEqual(str, type(ame_dict["id"]))
        self.assertEqual(str, type(ame_dict["created_at"]))
        self.assertEqual(str, type(ame_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        ame = Amenity()
        ame.id = "123456"
        ame.created_at = ame.updated_at = dt
        hdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(ame.to_dict(), hdict)

    def test_contrast_to_dict_dunder_dict(self):
        ame = Amenity()
        self.assertNotEqual(ame.to_dict(), ame.__dict__)

    def test_to_dict_with_arg(self):
        ame = Amenity()
        with self.assertRaises(TypeError):
            ame.to_dict(None)


if __name__ == "__main__":
    unittest.main()

