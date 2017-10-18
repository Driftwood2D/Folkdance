####################################
# Driftwood 2D Folkdance Engine    #
# player.py                        #
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

# Folkdance Player Manager

import ast
import json


class PlayerManager:
    """Player Manager"""
    def __init__(self, entity=None):
        if entity is not None:
            Driftwood.entity.player = entity
        self.__diagonal_movement = False

    def set(self, entity):
        """Set a new entity as the player.

        Returns the previously set player entity.
        """
        oldentity = Driftwood.entity.player
        Driftwood.entity.player = entity
        return oldentity

    def setup_default_keybinds(self, diagonal=False):
        if Driftwood.entity.player is None:
            return False

        if not diagonal:
            Driftwood.input.register("up", self._four_way_keybind_move_up)
            Driftwood.input.register("down", self._four_way_keybind_move_down)
            Driftwood.input.register("left", self._four_way_keybind_move_left)
            Driftwood.input.register("right", self._four_way_keybind_move_right)

            Driftwood.input.register("interact", self._default_keybind_interact)
            Driftwood.input.register("face", self._default_keybind_face)

        else:
            Driftwood.entity.player._move_keys_active = [0, 0, 0, 0]

            Driftwood.input.register("up", self._eight_way_keybind_move_up)
            Driftwood.input.register("down", self._eight_way_keybind_move_down)
            Driftwood.input.register("left", self._eight_way_keybind_move_left)
            Driftwood.input.register("right", self._eight_way_keybind_move_right)

            Driftwood.input.register("interact", self._default_keybind_interact)
            Driftwood.input.register("face", self._default_keybind_face)

        return True

    def _four_way_keybind_move_up(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._walk_stop()
            player.walk(0, -1, dont_stop=True, stance="walk_up", end_stance="face_up")
        elif keyevent == Driftwood.input.ONREPEAT:
            player.walk(0, -1, dont_stop=True, stance="walk_up", end_stance="face_up")
        elif keyevent == Driftwood.input.ONUP:
            player._walk_stop()

    def _four_way_keybind_move_down(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._walk_stop()
            player.walk(0, 1, dont_stop=True, stance="walk_down", end_stance="face_down")
        elif keyevent == Driftwood.input.ONREPEAT:
            player.walk(0, 1, dont_stop=True, stance="walk_down", end_stance="face_down")
        elif keyevent == Driftwood.input.ONUP:
            player._walk_stop()

    def _four_way_keybind_move_left(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._walk_stop()
            player.walk(-1, 0, dont_stop=True, stance="walk_left", end_stance="face_left")
        if keyevent == Driftwood.input.ONREPEAT:
            player.walk(-1, 0, dont_stop=True, stance="walk_left", end_stance="face_left")
        elif keyevent == Driftwood.input.ONUP:
            player._walk_stop()

    def _four_way_keybind_move_right(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._walk_stop()
            player.walk(1, 0, dont_stop=True, stance="walk_right", end_stance="face_right")
        if keyevent == Driftwood.input.ONREPEAT:
            player.walk(1, 0, dont_stop=True, stance="walk_right", end_stance="face_right")
        elif keyevent == Driftwood.input.ONUP:
            player._walk_stop()

    def _default_keybind_interact(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            if not player.interact():
                player.interact("under")

    def _default_keybind_face(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._face_key_active = True
        elif keyevent == Driftwood.input.ONUP:
            player._face_key_active = False

    def _eight_way_keybind_move_up(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._move_keys_active[0] = 1
        elif keyevent == Driftwood.input.ONUP:
            player._move_keys_active[0] = 0
        self._eight_way_update()

    def _eight_way_keybind_move_down(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._move_keys_active[1] = 1
        elif keyevent == Driftwood.input.ONUP:
            player._move_keys_active[1] = 0
        self._eight_way_update()

    def _eight_way_keybind_move_left(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._move_keys_active[2] = 1
        elif keyevent == Driftwood.input.ONUP:
            player._move_keys_active[2] = 0
        self._eight_way_update()

    def _eight_way_keybind_move_right(self, keyevent):
        player = Driftwood.entity.player
        if keyevent == Driftwood.input.ONDOWN:
            player._move_keys_active[3] = 1
        elif keyevent == Driftwood.input.ONUP:
            player._move_keys_active[3] = 0
        self._eight_way_update()

    def _eight_way_update(self):
        eight_way_stance = [
            ["up_left", "up", "up_right"],
            ["left", "none", "right"],
            ["down_left", "down", "down_right"],
        ]

        player = Driftwood.entity.player
        up, down, left, right = player._move_keys_active

        y = down - up
        x = right - left

        base = eight_way_stance[y + 1][x + 1]
        stance = "walk_" + base
        end_stance = "face_" + base

        if x == 0 and y == 0:
            player._walk_stop()
        else:
            player.walk(x, y, dont_stop=True, facing=None, stance=stance, end_stance=end_stance)
