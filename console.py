#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """Takes a single string arg
    Uses reg expp to search patterns in the input string
    cb searches for the content within curly braces {}
    brc searches for content within brackets []  
    returns list of processed items         
    """
    cb = re.search(r"\{(.*?)\}", arg)
    brc = re.search(r"\[(.*?)\]", arg)
    if cb is None:
        if brc is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brc.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brc.group())
            return retl
    else:
        lexer = split(arg[:cb.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(cb.group())
        return retl
    
    
class HBNBCommand(cmd.Cmd):
    """This is the AirBnB commandline interpreter class
    
    Attributes:
        prompt (str): The command prompt
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
        """Do nothing if empty argument received"""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all, # type: ignore
            "show": self.do_show,
            "destroy": self.do_destroy, # type: ignore
            "count": self.do_count, # type: ignore
            "update": self.do_update # type: ignore
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False
    
    def do_quit(self, arg) -> bool:
        """Quit funtion to exit the program"""
        return True
    
    def do_EOF(self, arg) -> bool:
        """EOF characters to exit the program, hold Ctrl+C twice"""
        print("")
        return True
    
    def do_create(self, arg):
        """Usage: create <class>
        Create new class instance and print its id"""
        arg_list = parse(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class does not exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

    
    def do_show(self, arg):
        """Usage : show <class> <id> or <class>.show(<id>)
        Display a class instance
        """

        arg_list = parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])


    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance"""
        arg_list = parse(arg)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesnt exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")  
        else:
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])] 
            storage.save()





if __name__ == "__main__":
    HBNBCommand().cmdloop()       