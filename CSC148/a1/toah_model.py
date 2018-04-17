"""
TOAHModel:  Model a game of Tour of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Tour of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro, Ritu Chaturvedi, Samar Sabie
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
#


class TOAHModel:
    """ Model a game of Tour Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.
    """

    def __init__(self, number_of_stools):
        """ Create new TOAHModel with empty stools
        to hold stools of cheese.

        @param TOAHModel self: this TOAHModel object
        @param int number_of_stools: number of stools in game
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> (M.get_number_of_stools(), M.number_of_moves()) == (4,0)
        True
        >>> M.get_number_of_cheeses()
        5
        """
        self._stools = {}
        for i in range(number_of_stools):
            self._stools[i] = []
        self._move_seq = MoveSequence([])

    def get_move_seq(self):
        """ Return the move sequence

        @type self: TOAHModel
        @rtype: MoveSequence

        >>> toah = TOAHModel(2)
        >>> toah.get_move_seq() == MoveSequence([])
        True
        """
        return self._move_seq

    def __eq__(self, other):
        """ Return whether TOAHModel self is equivalent to other.

        Two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other

        @type self: TOAHModel
        @type other: TOAHModel
        @rtype: bool

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(1, 2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0, 3)
        >>> m2.move(0, 2)
        >>> m2.move(3, 2)
        >>> m1 == m2
        True
        """
        for i in self._stools:
            if not self._stools[i] == other._stools[i]:
                return False
        return True

    def _cheese_at(self, stool_index, stool_height):
        """ Return (stool_height)th from stool_index stool, if possible.

        @type self: TOAHModel
        @type stool_index: int
        @type stool_height: int
        @rtype: Cheese | None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """
        if 0 <= stool_height < len(self._stools[stool_index]):
            return self._stools[stool_index][stool_height]
        else:
            return None

    def __str__(self):
        """
        Depicts only the current state of the stools and cheese.

        @param TOAHModel self:
        @rtype: str
        """
        all_cheeses = []
        for height in range(self.get_number_of_cheeses()):
            for stool in range(self.get_number_of_stools()):
                if self._cheese_at(stool, height) is not None:
                    all_cheeses.append(self._cheese_at(stool, height))
        max_cheese_size = max([c.size for c in all_cheeses]) \
            if len(all_cheeses) > 0 else 0
        stool_str = "=" * (2 * max_cheese_size + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.get_number_of_stools()

        def _cheese_str(size):
            # helper for string representation of cheese
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.get_number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.get_number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = _cheese_str(int(c.size))
                else:
                    s = _cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines

    def add(self, cheese, index):
        """ Add a cheese to the the desired stool.

        @param TOAHModel self: this TOAHModel object
        @param Cheese cheese: the cheese to add
        @param int index: the stool index
        @rtype: None
        """
        self._stools[index].append(cheese)

    def get_cheese_location(self, cheese):
        """ Return the stool index of the given cheese.

        @param TOAHModel self: this TOAHModel object
        @param Cheese cheese: the cheese to find
        @rtype: int

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.get_cheese_location(Cheese(2))
        0
        >>> M.move(0, 3)
        >>> M.move(0, 2)
        >>> M.get_cheese_location(Cheese(1))
        3
        >>> M.get_cheese_location(Cheese(2))
        2
        """
        for i in range(len(self._stools)):
            for cheeses in self._stools[i]:
                if cheeses.size == cheese.size:
                    return i

    def get_top_cheese(self, index):
        """ Return the top cheese at the precised stool.

        @param TOAHModel self: this TOAHModel object
        @param int index: the stool index
        @rtype: Cheese | None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> cheese = M.get_top_cheese(0)
        >>> isinstance(cheese, Cheese)
        True
        >>> cheese.size
        1
        >>> cheese_2 = M.get_top_cheese(1)
        >>> cheese_2
        """
        if len(self._stools[index]) == 0:
            return None
        else:
            cheese = self._stools[index][-1]
            return cheese

    def move(self, origin_index, new_index):
        """ Move the top cheese at the stool indexed as origin_index to the
        stool indexed as new_index

        May raise an IllegalMoveError

        @param TOAHModel self: this TOAHModel object
        @param int origin_index: the souce stool
        @param int new_index: the destination stool
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.move(0, 1)
        >>> cheese = M.get_top_cheese(1)
        >>> isinstance(cheese, Cheese)
        True
        >>> cheese.size
        1
        """
        if len(self._stools[origin_index]) == 0:
            pass
        elif len(self._stools[new_index]) == 0:
            self.add(self.get_top_cheese(origin_index), new_index)
            self._stools[origin_index].pop()
            self._move_seq.add_move(origin_index, new_index)
        elif self._stools[origin_index][-1].size < \
                self._stools[new_index][-1].size:
            self.add(self.get_top_cheese(origin_index), new_index)
            self._stools[origin_index].pop()
            self._move_seq.add_move(origin_index, new_index)
        else:
            raise IllegalMoveError

    def number_of_moves(self):
        """ Return the number of moves that have been played since the start of
        the game.

        @param TOAHModel self: this TOAHModel object
        @rtype: int

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.number_of_moves()
        0
        >>> M.move(0, 1)
        >>> M.move(0, 2)
        >>> M.number_of_moves()
        2
        """
        return self._move_seq.length()

    def fill_first_stool(self, number_of_cheeses):
        """ Add a number of cheeses to the first stool.

        @param TOAHModel self: this TOAHModel object
        @param int number_of_cheeses: the number of cheese to add
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> len(M._stools[0])
        5
        """
        for i in range(number_of_cheeses, 0, -1):
            self._stools[0].append(Cheese(i))

# helper function: fill_last_stool()
    def fill_last_stool(self, number_of_cheeses):
        """ Add a number of cheeses to the last stool.

        @param TOAHModel self: this TOAHModel object
        @param int number_of_cheeses: the number of cheese to add
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_last_stool(5)
        >>> len(M._stools[3])
        5
        """
        for i in range(number_of_cheeses, 0, -1):
            self._stools[max(self._stools)].append(Cheese(i))

    def get_number_of_stools(self):
        """ Return the number of stools present in the game.

        @param TOAHModel self: this TOAHModel object
        @rtype: int

        >>> M = TOAHModel(4)
        >>> M.get_number_of_stools()
        4
        """
        return len(self._stools)

    def get_number_of_cheeses(self):
        """ Return the amount of cheeses present in the game.

        @param TOAHModel self: this TOAHModel object
        @rtype: int

        >>> M = TOAHModel(4)
        >>> M.get_number_of_cheeses()
        0
        >>> M.fill_first_stool(6)
        >>> M.get_number_of_cheeses()
        6
        """
        number = 0
        for i in range(len(self._stools)):
            number += len(self._stools[i])
        return number


class Cheese:
    """ A cheese for stacking in a TOAHModel

    === Attributes ===
    @param int size: width of cheese
    """

    def __init__(self, size):
        """ Initialize a Cheese to diameter size.

        @param Cheese self: this Cheese object
        @param int size: the width of the cheese
        @rtype: None

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __eq__(self, other):
        """ Is self equivalent to other?

        We say they are if they're the same
        size.

        @param Cheese self: this Cheese object
        @param Cheese|Any other: object to be compared to
        @rtype: bool

        >>> c = Cheese(3)
        >>> c2 = Cheese(5)
        >>> c == c2
        False
        >>> c3 = Cheese(5)
        >>> c3.__eq__(c2)
        True
        """
        return isinstance(other, type(self)) and self.size == other.size


class IllegalMoveError(Exception):
    """ Exception indicating move that violate TOAHModel
    """
    pass


class MoveSequence(object):
    """ Sequence of moves in TOAH game
    """

    def __init__(self, moves):
        """ Create a new MoveSequence self.

        @param MoveSequence self: this MoveSequence object
        @param list[tuple[int]] moves: a list of integer pairs
        @rtype: None
        """
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self, i):
        """ Return the move at position i in self

        @param MoveSequence self:
        @param int i:
        @rtype: tuple[int]

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.get_move(0) == (1, 2)
        True
        """
        # Exception if not (0 <= i < self.length)
        return self._moves[i]

    def add_move(self, src_stool, dest_stool):
        """ Add move from src_stool to dest_stool to MoveSequence self.

        @param MoveSequence self:
        @param int src_stool:
        @param int dest_stool:
        @rtype: None
        """
        self._moves.append((src_stool, dest_stool))

    def length(self):
        """ Return number of moves in self.

        @param MoveSequence self:
        @rtype: int

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.length()
        1
        """
        return len(self._moves)

    def generate_toah_model(self, number_of_stools, number_of_cheeses):
        """ Construct TOAHModel from number_of_stools and number_of_cheeses
         after moves in self.

        Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in this move sequence.

        @param MoveSequence self:
        @param int number_of_stools:
        @param int number_of_cheeses:
        @rtype: TOAHModel

        >>> ms = MoveSequence([])
        >>> toah = TOAHModel(2)
        >>> toah.fill_first_stool(2)
        >>> toah == ms.generate_toah_model(2, 2)
        True
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    # Leave lines below to see what python_ta checks.
    # File toahmodel_pyta.txt must be in same folder.
    import python_ta
    python_ta.check_all(config="toahmodel_pyta.txt")
