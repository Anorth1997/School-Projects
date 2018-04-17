"""
functions to run TOAH tours.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr


# you may want to use time.sleep(delay_between_moves) in your
# solution for 'if __name__ == "main":'
import time
from toah_model import TOAHModel


def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if console_animate is True
    @type animate: bool
        animate the tour or not
    """
    if animate:
        print(model)
        time.sleep(delay_btw_moves)

    # helper function to move cheeses with 3 stools
    def _move(n, source, intermediate, destination):
        # """Move n cheeses from source to destination with 3 stools
        #
        # @param int n: number of cheeses
        # @param int source: source stool index
        # @param int intermediate: intermediate stool index
        # @param int destination: destination stool index
        # """
        if n > 1:
            _move(n - 1, source, destination, intermediate)
            _move(1, source, intermediate, destination)
            _move(n - 1, intermediate, source, destination)
        else:
            print("{} -> {}".format(source, destination))
            model.move(source, destination)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)

    # helper function to move cheeses with 4 stools
    def _move_cheeses(n, source, inter1, inter2, dest):
        # """Move n cheeses from source to destination with 4 stools
        #
        # @param int n: number of cheeses
        # @param int source: source stool index
        # @param int inter1: intermediate 1 stool index
        # @param int inter2: intermediate 2 stool index
        # @param int dest: destination stool index
        # """
        i = n // 2
        if n == 1:
            print("{} -> {}".format(source, dest))
            model.move(source, dest)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
        elif n == 2:
            print("{} -> {}".format(source, inter1))
            model.move(source, inter1)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
            print("{} -> {}".format(source, dest))
            model.move(source, dest)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
            print("{} -> {}".format(inter1, dest))
            model.move(inter1, dest)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
        elif n == 3:
            print("{} -> {}".format(source, inter2))
            model.move(source, inter2)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
            print("{} -> {}".format(source, inter1))
            model.move(source, inter1)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
            print("{} -> {}".format(source, dest))
            model.move(source, dest)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
            print("{} -> {}".format(inter1, dest))
            model.move(inter1, dest)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
            print("{} -> {}".format(inter2, dest))
            model.move(inter2, dest)
            if animate:
                print(model)
                time.sleep(delay_btw_moves)
        else:
            _move_cheeses(i, source, inter2, dest, inter1)
            _move(n - i, source, inter2, dest)
            _move_cheeses(i, inter1, source, inter2, dest)

    _move_cheeses(model.get_number_of_cheeses(), 0, 1, 2, 3)

if __name__ == '__main__':
    num_cheeses = 5
    delay_between_moves = 0.5
    console_animate = True

    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=num_cheeses)

    tour_of_four_stools(four_stools,
                        animate=console_animate,
                        delay_btw_moves=delay_between_moves)

    print(four_stools.number_of_moves())
    import python_ta
    python_ta.check_all(config="tour_pyta.txt")
