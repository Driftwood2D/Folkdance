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

import json


class InventoryManager:
    def __init__(self, driftwood):
        self.driftwood = driftwood

        self.__inventory = {}

    def __contains__(self, item):
        return self.has(item)

    def __getitem__(self, item):
        return self.item(item)

    def has(self, item):
        if item in self.__inventory:
            return self.__inventory[item]["quantity"]
        return 0

    def item(self, item):
        if item in self.__inventory:
            return self.__inventory[item]
        return None

    def load(self, filename):
        data = self.driftwood.resource.request_json(filename)
        if not data:
            self.driftwood.log("Error", "Folkdance", "Inventory", "load", "could not load items from", filename)
            return False
        for item in data.keys():
            if item in self.__inventory:
                self.driftwood.log("WARNING", "Folkdance", "Inventory", "load", "duplicate item", item)
            self.__inventory[item] = data[item]
        return True

    def loads(self, data):
        try:
            data = json.loads(data)
        except:
            self.driftwood.log("Error", "Folkdance", "Inventory", "loads", "could not load items")
            return False
        if not data:
            self.driftwood.log("Error", "Folkdance", "Inventory", "loads", "could not load items")
            return False
        for item in data.keys():
            if item in self.__inventory:
                self.driftwood.log("WARNING", "Folkdance", "Inventory", "loads", "duplicate item", item)
            self.__inventory[item] = data[item]
        return True
