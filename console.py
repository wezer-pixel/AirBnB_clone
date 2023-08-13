#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage


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


    def do_all(self, arg):
        """Usage: all, or all <class> , or <class>.all()
        Display string representation of all instances of a class.
        Displays object instance if no class specified"""
        ag_ls = parse(arg)
        if len(ag_ls) > 0 and ag_ls[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_ls = []
            for obj in storage.all().values():
                if len(ag_ls) > 0 and ag_ls[0] == obj.__class__.__name__:
                    obj_ls.append(obj.__str__())
                elif len(ag_ls) == 0:
                    obj_ls.append(obj.__str__())
            print(obj_ls)


    def do_count(self, arg):
        """Usage: count <class> , or <class>.count()
        Retrieve the number of instancs of a class"""
        ag_ls = parse(arg)
        i = 0
        for obj in storage.all().values():
            if ag_ls[0] == obj.__class__.__name__:
                i += 1
        print(i)


    def do_update(self, arg):
        """Usage: update <class> <id> <attr_name> <attr_val>
        or,
        <class>.update(<id>, <attr_name>, <attr_val>)
        or,
        <class>.update(<id>, <dictionary>)
        Update a class instance by adding or updating the
        given attribute, key/val pair or dictionary"""
        ag_ls = parse(arg)
        objdict = storage.all()

        if len(ag_ls) == 0:
            print("** class name missing **")
            return False
        if ag_ls[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(ag_ls) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(ag_ls[0], ag_ls[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(ag_ls) == 2:
            print("** attribute name missing **")
            return False
        if len(ag_ls) ==3:
            try:
                type(eval(ag_ls[2])) != dict
            except NameError:
                return False
            
        if len(ag_ls) == 4:
            obj = objdict["{}.{}".format(ag_ls[0], ag_ls[1])]
            if ag_ls[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[ag_ls[2]])
                obj.__dict__[ag_ls[2]] = val_type(ag_ls[3])
            else:
                obj.__dict__[ag_ls[2]] = ag_ls[3]
        elif type(eval(ag_ls[2])) == dict:
            obj = objdict["{}.{}".format(ag_ls[0], ag_ls[1])]
            for key, value in eval(ag_ls[2]).items:
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    val_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = val_type(value)
                else:
                    obj.__dict__[key] = value
        storage.save()            
        


if __name__ == "__main__":
    HBNBCommand().cmdloop()       