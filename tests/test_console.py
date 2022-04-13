#!/usr/bin/python3
"""
Test for the console.py
"""

from itertools import count
import os
import unittest
import models
import json
import cmd
from io import StringIO
from console import HBNBCommand
import console
import pycodestyle
from unittest.mock import patch
from models.base_model import BaseModel, storage_Type
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.engine.file_storage import FileStorage


class TestBasicCaseAndDoc(unittest.TestCase):
    """
    Test the whole docs, and basic input
    """

    def test_doc(self):
        """
        Check all the doc of the Amenity Class
        """
        # module documentation
        module = len(console.__doc__)
        self.assertGreater(module, 0)

        # class documentation
        module_class = len(HBNBCommand.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.do_all.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.do_create.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.do_destroy.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.do_quit.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.do_EOF.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.do_count.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.do_destroy.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.do_update.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.emptyline.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.default.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.help_all.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.help_create.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.help_EOF.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.help_destroy.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.help_quit.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.help_show.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(HBNBCommand.help_update.__doc__)
        self.assertGreater(module_class, 0)

    def test_pycodeStyle(self):
        """Test that we conform to PEP-8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(["console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (pycodestyle)."
        )

    def test_prompt(self):
        """
        Test the prompt
        """
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyline(self):
        """
        Check the case of empty line
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual("", f.getvalue().strip())

    def test_UnknowCommand(self):
        """
        Test an unknow command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("fdfdf")
            self.assertEqual("*** Unknown syntax: fdfdf", f.getvalue().strip())


class TestHelpFunction(unittest.TestCase):
    """
    Check all the help functions
    """

    def test_helpCreate(self):
        """
        Test the help function of create
        """
        helpStr = 'Creates a class of any type\n\
[Usage]: create <className>'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertEqual(helpStr, f.getvalue().strip())

    def test_helpShow(self):
        """
        Test the help function of show
        """
        helpStr = 'Shows an individual instance of a class\n\
[Usage]: show <className> <objectId>'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertEqual(helpStr, f.getvalue().strip())

    def test_helpDestroy(self):
        """
        Test the help function of destroy
        """
        helpStr = 'Destroys an individual instance of a class\n\
[Usage]: destroy <className> <objectId>'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertEqual(helpStr, f.getvalue().strip())

    def test_helpAll(self):
        """
        Test the help function of all
        """
        helpStr = "Shows all objects, or all of a class\n\
[Usage]: all <className>"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertEqual(helpStr, f.getvalue().strip())

    def test_helpUpdate(self):
        """
        Test the help function of update
        """
        helpStr = 'Updates an object with new information\n\
Usage: update <className> <id> <attName> <attVal>'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertEqual(helpStr, f.getvalue().strip())

    def test_helpEOF(self):
        """
        Test the help function of EOF
        """
        helpStr = 'Exits the program without formatting'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
            self.assertEqual(helpStr, f.getvalue().strip())

    def test_helpQuit(self):
        """
        Test the help function of quit
        """
        helpStr = 'Exits the program with formatting'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertEqual(helpStr, f.getvalue().strip())

    def test_helpCount(self):
        """
        Test the help function of quit
        """
        helpStr = 'Usage: count <class_name>'
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help count")
            self.assertEqual(helpStr, f.getvalue().strip())


class TestFunctions(unittest.TestCase):
    """
    Test all the functions
    """

    def setUp(self):
        """
        Set up all the test
        """
        try:
            os.rename("file.json", "tmp.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """
        Close all the test
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp.json", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @unittest.skipIf(storage_Type == 'db', "do not test with dbstorage")
    def test_all(self):
        """
        Check the all functions
        Check first all the edges cases, then the creation of
        instances
        """
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all NotAClass")
            self.assertEqual(output, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            bufInstance = f.getvalue().strip()
        allClasses = ["BaseModel",
                      "Amenity",
                      "Place",
                      "City",
                      "Review",
                      "State",
                      "User"]
        for className in allClasses:
            self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all BaseModel")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "BaseModel":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Amenity")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "Amenity":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all City")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "City":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Place")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "Place":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Review")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "Review":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all State")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "State":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all User")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "User":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.all()")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "User":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.all()")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "BaseModel":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Amenity.all()")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "Amenity":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("City.all()")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "City":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Place.all()")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "Place":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Review.all()")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "Review":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("State.all()")
            bufInstance = f.getvalue().strip()
        for className in allClasses:
            if className != "State":
                self.assertNotIn(className, bufInstance)
            else:
                self.assertIn(className, bufInstance)

        output = "*** Unknown syntax: State.all(bablabla)"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("State.all(bablabla)")
            bufInstance = f.getvalue().strip()
            self.assertEqual(bufInstance, output)

    def test_create(self):
        """
        Check the create functions
        Check first all the edges cases, then the creation of
        instances
        """
        output = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(output, f.getvalue().strip())
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create LesTestCesSuicidaire")
            self.assertEqual(output, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            if storage_Type == "db":
                self.skipTest(
                    "Class 'models.base_model.BaseModel' is not mapped")
            HBNBCommand().onecmd("create BaseModel")
            id = f.getvalue().strip()
            className = "BaseModel." + id
            self.assertIn(className, models.storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue().strip()
            className = "User." + id
            self.assertIn(className, models.storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue().strip()
            className = "Amenity." + id
            self.assertIn(className, models.storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            id = f.getvalue().strip()
            className = "City." + id
            self.assertIn(className, models.storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue().strip()
            className = "Place." + id
            self.assertIn(className, models.storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue().strip()
            className = "Review." + id
            self.assertIn(className, models.storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue().strip()
            className = "State." + id
            self.assertIn(className, models.storage.all().keys())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State Useless text")
            id = f.getvalue().strip()
            className = "State." + id
            self.assertIn(className, models.storage.all().keys())

    def test_show(self):
        """
        Check the show functions
        Check first all the edges cases, then the creation of
        instances
        """
        output = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual(output, f.getvalue().strip())
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show NotGoodClasses")
            self.assertEqual(output, f.getvalue().strip())
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(output, f.getvalue().strip())
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            if storage_Type == 'db':
                self.skipTest(
                    "DBStorage' object has no attribute \
'_FileStorage__objects")
            HBNBCommand().onecmd("show BaseModel NotGoodID")
            self.assertEqual(output, f.getvalue().strip())

        output = "*** Unknown syntax: NotGoodClasses.show()"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("NotGoodClasses.show()")
            self.assertEqual(output, f.getvalue().strip())
        output = "*** Unknown syntax: BaseModel.show()"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
            self.assertEqual(output, f.getvalue().strip())
        output = "*** Unknown syntax: BaseModel.show(NotGoodID)"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show(NotGoodID)")
            self.assertEqual(output, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel " + id)
            className = f"[BaseModel] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show BaseModel "{id}"')
            className = f"[BaseModel] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"BaseModel.show({id})")
            className = f"[BaseModel] ({id})"
            # self.assertIn(className, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show User " + id)
            className = f"[User] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show User "{id}"')
            className = f"[User] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"User.show({id})")
            className = f"[User] ({id})"
            # self.assertIn(className, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Amenity " + id)
            className = f"[Amenity] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Amenity "{id}"')
            className = f"[Amenity] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"Amenity.show({id})")
            className = f"[Amenity] ({id})"
            # self.assertIn(className, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show City " + id)
            className = f"[City] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show City "{id}"')
            className = f"[City] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"City.show({id})")
            className = f"[City] ({id})"
            # self.assertIn(className, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Place " + id)
            className = f"[Place] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Place "{id}"')
            className = f"[Place] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"Place.show({id})")
            className = f"[Place] ({id})"
            # self.assertIn(className, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Review " + id)
            className = f"[Review] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Review "{id}"')
            className = f"[Review] ({id})"
            self.assertIn(className, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show State " + id)
            className = f"[State] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show State "{id}"')
            className = f"[State] ({id})"
            self.assertIn(className, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                "show State " + id +
                " Je suis un text inutile show State " + id
            )
            className = f"[State] ({id})"
            self.assertIn(className, f.getvalue().strip())

    def test_destroy(self):
        """
        Test the destroy function
        """
        output = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual(output, f.getvalue().strip())
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy NotGoodClasses")
            self.assertEqual(output, f.getvalue().strip())
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
            self.assertEqual(output, f.getvalue().strip())
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel NotGoodID")
            self.assertEqual(output, f.getvalue().strip())
        output = "*** Unknown syntax: NotGoodClasses.destroy()"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("NotGoodClasses.destroy()")
            self.assertEqual(output, f.getvalue().strip())
        output = "*** Unknown syntax: BaseModel.destroy()"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
            self.assertEqual(output, f.getvalue().strip())
        output = "*** Unknown syntax: BaseModel.destroy(NotGoodID)"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy(NotGoodID)")
            self.assertEqual(output, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            if storage_Type == "db":
                self.skipTest(
                    "Class 'models.base_model.BaseModel' is not mapped")
            HBNBCommand().onecmd("create BaseModel")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel " + id)
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Amenity " + id)
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy City " + id)
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Place " + id)
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Review " + id)
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State " + id)
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User " + id)
            self.assertEqual(models.storage.all(), {})

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'destroy BaseModel "{id}"')
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'destroy Amenity "{id}"')
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'destroy City "{id}"')
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'destroy Place "{id}"')
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'destroy Review "{id}"')
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'destroy State "{id}"')
            self.assertEqual(models.storage.all(), {})
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'destroy User "{id}"')
            self.assertEqual(models.storage.all(), {})

    def test_count(self):
        with patch('sys.stdout', new=StringIO()) as f:
            if storage_Type == "db":
                self.skipTest(
                    "DBStorage' object has no \
attribute '_FileStorage__objects")
            HBNBCommand().onecmd("count BaseModel")
            count = f.getvalue().strip()
            self.assertEqual(count, "0")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count Amenity")
            count = f.getvalue().strip()
            self.assertEqual(count, "0")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count City")
            count = f.getvalue().strip()
            self.assertEqual(count, "0")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count Place")
            count = f.getvalue().strip()
            self.assertEqual(count, "0")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count Review")
            count = f.getvalue().strip()
            self.assertEqual(count, "0")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count State")
            count = f.getvalue().strip()
            self.assertEqual(count, "0")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count User")
            count = f.getvalue().strip()
            self.assertEqual(count, "0")

    def test_update(self):
        """
        Test for update function
        """
        output = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            self.assertEqual(output, f.getvalue().strip())
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update NotAClass")
            self.assertEqual(output, f.getvalue().strip())
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
            self.assertEqual(output, f.getvalue().strip())
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel NotAnId")
            self.assertEqual(output, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            if storage_Type == "db":
                self.skipTest(
                    "Class 'models.base_model.BaseModel' is not mapped")
            HBNBCommand().onecmd("create BaseModel")
            id = f.getvalue().strip()
        output = "** attribute name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"update BaseModel {id}")
            self.assertEqual(output, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel "{id}"')
            self.assertEqual('** attribute name missing **',
                             f.getvalue().strip())
        output = "** value missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"update BaseModel {id} name")
            self.assertEqual(output, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel "{id}" name')
            self.assertEqual('** value missing **', f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'destroy BaseModel "{id}"')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {id} name Betty')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show BaseModel {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {id} name "Betty"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show BaseModel {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {id} id 123')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show BaseModel {id}')
            dictClass = f.getvalue().strip()
        self.assertIn(f"'id': '{id}'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {id} created_at Hier')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show BaseModel {id}')
            dictClass = f.getvalue().strip()
        self.assertNotIn(f"'create_at': 'Hier'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {id} updated_at Demain')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show BaseModel {id}')
            dictClass = f.getvalue().strip()
        self.assertNotIn(f"'updated_at': 'Demain'", dictClass)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update Amenity {id} name Betty')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Amenity {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update Amenity {id} name "Betty"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Amenity {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update City {id} name Betty')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show City {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update City {id} name "Betty"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show City {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update Place {id} name Betty')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Place {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update Place {id} name "Betty"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Place {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update Review {id} name Betty')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Review {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update Review {id} name "Betty"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show Review {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update State {id} name Betty')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show State {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update State {id} name "Betty"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show State {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update User {id} name Betty')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show User {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update User {id} name "Betty"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'show User {id}')
            dictClass = f.getvalue().strip()
        self.assertIn("'name': 'Betty'", dictClass)
