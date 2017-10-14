####################################
# Driftwood 2D Folkdance Engine    #
# stdlib/widget.py                 #
# Copyright 2017 Michael D. Reiley #
# & Paul Merrill                   #
####################################

# **********
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# **********

import ast
import json


class InventoryManager:
    """Inventory Manager
    
    Manages an inventory or bag."""
    def __init__(self, size=-1):
        # Maximum weight of items that can be held in the inventory.
        self.size = size
        
        # Amount of items currently being held.
        self.holding = 0

        # A dictionary of item names mapped to item specs.
        self.__inventory = {}

    def __contains__(self, item):
        return self.has(item) is not 0

    def __getitem__(self, item):
        return self.item(item)

    def has(self, item):
        """Return how many of the named item are held currently."""
        if item in self.__inventory:
            return self.__inventory[item]["quantity"]
        return 0

    def item(self, item):
        """Return the data for an item."""
        if item in self.__inventory:
            return self.__inventory[item]
        return None

    def get(self, item, quantity=1):
        """Increment the quantity of an item and increase the holding variable by the appropriate weight. Call the
        item's on_get trigger.

        Returns None if no such item, -1 if too heavy, and quantity now held otherwise."""
        if item not in self.__inventory:
            return None
        if self.holding + self.__inventory[item]["weight"] * quantity > self.size >= 0:
            return -1

        self.__inventory[item]["quantity"] += quantity
        self.holding += self.__inventory[item]["weight"] * quantity

        if "on_get" in self.__inventory[item]["triggers"]:
            Driftwood.script.call(*self.__inventory[item]["triggers"]["on_get"])

        return self.__inventory[item]["quantity"]

    def drop(self, item, quantity=1):
        """Decrement the quantity of an item and decrease the holding variable by the appropriate weight. Call the
        item's on_drop trigger.

        Returns None if no such item, -1 if dropping more than held, and quantity now held otherwise."""
        if item not in self.__inventory:
            return None
        if self.__inventory[item]["quantity"] - quantity < 0:
            return -1

        self.__inventory[item]["quantity"] -= quantity
        self.holding -= self.__inventory[item]["weight"] * quantity

        if "on_drop" in self.__inventory[item]["triggers"]:
            Driftwood.script.call(*self.__inventory[item]["triggers"]["on_drop"])

        return self.__inventory[item]["quantity"]

    def use(self, item, quantity=1):
        """Use an item.

        If the item is not disposable, the value of quantity is meaningless. Otherwise, decrement the quantity
        of an item and decrease the holding variable by the appropriate weight. Call the item's on_use trigger.

        Returns None if no such item, False if disposable and using more than held, or True if succeeded."""
        if item not in self.__inventory:
            return None

        if self.__inventory[item]["disposable"]:
            if self.__inventory[item]["quantity"] - quantity < 0:
                return False

            self.__inventory[item]["quantity"] -= quantity
            self.holding -= self.__inventory[item]["weight"] * quantity

        if "on_use" in self.__inventory[item]["triggers"]:
            Driftwood.script.call(*self.__inventory[item]["triggers"]["on_use"])

        return True

    def load(self, filename):
        """Load a dictionary of item specs from a file.

        Returns True if succeeded, False if failed."""
        data = Driftwood.resource.request_json(filename)
        if not data:
            Driftwood.log.msg("Error", "Folkdance", "Inventory", "load", "could not load items from", filename)
            return False
        for item in data.keys():
            if item in self.__inventory:
                Driftwood.log.msg("WARNING", "Folkdance", "Inventory", "load", "duplicate item", item)
            self.__inventory[item] = data[item]
        return True

    def loads(self, data):
        """Load a dictionary of item specs from a string.

        Returns True if succeeded, False if failed."""
        try:
            data = ast.literal_eval(json.loads(data))
        except:
            Driftwood.log.msg("Error", "Folkdance", "Inventory", "loads", "could not load items")
            return False
        if not data:
            Driftwood.log.msg("Error", "Folkdance", "Inventory", "loads", "could not load items")
            return False
        for item in data.keys():
            if item in self.__inventory:
                Driftwood.log.msg("WARNING", "Folkdance", "Inventory", "loads", "duplicate item", item)
            self.__inventory[item] = data[item]
        return True

    def save(self, varname="inventory"):
        """Save the item dictionary to the currently open database."""
        Driftwood.database.put(varname, str(self.__inventory))
        return True

    def restore(self, varname="inventory"):
        """Restore the item dictionary to from currently open database.

        Returns True if succeeded, False if failed."""
        if varname in Driftwood.database:
            self.loads(Driftwood.database[varname])
            return True
        return False

    def dump(self):
        """Return the item dictionary."""
        return self.__inventory
