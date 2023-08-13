#!/usr/bin/python3
"""Defines the hbtn console."""
import cmd
import models
import re
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """overides the default behavir of the emptyline method
            of repeating the last nonempty command entered
            it does nothing upon receiving an empty line.
        """
        pass

    def default(self, arg):
        """Overides the default behaviour of prinint and error
            message when called on an input line when the command is
            not recognized
            Default behavior for cmd module when input is invalid
        """
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argel = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argel[1])
            if match is not None:
                command = [argel[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argel[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        exit()

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        exit()

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argel = parse(arg)
        if len(argel) == 0:
            print("** class name missing **")
        elif argel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argel[0])().id)
            models.storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argel = parse(arg)
        objdict = models.storage.all()
        if len(argel) == 0:
            print("** class name missing **")
        elif argel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argel) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argel[0], argel[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argel[0], argel[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argel = parse(arg)
        objdict = models.storage.all()
        if len(argel) == 0:
            print("** class name missing **")
        elif argel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argel) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argel[0], argel[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argel[0], argel[1])]
            models.storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argel = parse(arg)
        if len(argel) > 0 and argel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in models.storage.all().values():
                if len(argel) > 0 and argel[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argel) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argel = parse(arg)
        count = 0
        for obj in models.storage.all().values():
            if argel[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argel = parse(arg)
        objdict = models.storage.all()

        if len(argel) == 0:
            print("** class name missing **")
            return False
        if argel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argel) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argel[0], argel[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argel) == 2:
            print("** attribute name missing **")
            return False
        if len(argel) == 3:
            try:
                type(eval(argel[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argel) == 4:
            obj = objdict["{}.{}".format(argel[0], argel[1])]
            if argel[2] in obj.__class__.__dict__.keys():
                vtype = type(obj.__class__.__dict__[argel[2]])
                obj.__dict__[argel[2]] = vtype(argel[3])
            else:
                obj.__dict__[argel[2]] = argel[3]
        elif type(eval(argel[2])) == dict:
            obj = objdict["{}.{}".format(argel[0], argel[1])]
            for k, v in eval(argel[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    vtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = vtype(v)
                else:
                    obj.__dict__[k] = v
        models.storage.save()


def parse(arg):
    """Convert argument passed on terminal to a list/dict"""
    brcs = re.search(r"\{(.*?)\}", arg)
    brckts = re.search(r"\[(.*?)\]", arg)
    if brcs is None:
        if brckts is None:
            return [i.strip(",") for i in split(arg)]
        else:
            ass = split(arg[:brckts.span()[0]])
            argel = [i.strip(",") for i in ass]
            argel.append(brckts.group())
            return agrl
    else:
        ass = split(arg[:brcs.span()[0]])
        argel = [i.strip(",") for i in ass]
        argel.append(brcs.group())
        return argel


if __name__ == "__main__":
    HBNBCommand().cmdloop()
