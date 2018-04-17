"""
ConsoleController: User interface for manually solving
Anne Hoy's problems from the console.
"""


# Copyright 2014, 2017 Dustin Wehr, Danny Heap, Bogdan Simion,
# Jacqueline Smith, Dan Zingaro
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


from toah_model import TOAHModel, IllegalMoveError


def move(model, origin, dest):
    """ Apply move from origin to destination in model.

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param int origin:
        stool number (index from 0) of cheese to move
    @param int dest:
        stool number you want to move cheese to
    @rtype: None
    """
    model.move(origin, dest)


class ConsoleController:
    """ Controller for text console.
    """

    def __init__(self, number_of_cheeses, number_of_stools):
        """ Initialize a new ConsoleController self.

        @param ConsoleController self: this ConsoleController object
        @param int number_of_cheeses: the number of cheese to start with
        @param int number_of_stools: the number of stools to play with
        @rtype: None
        """
        self._model = TOAHModel(number_of_stools)
        self._stools = number_of_stools
        self._cheese = number_of_cheeses
        self._model.fill_first_stool(number_of_cheeses)

    def play_loop(self):
        """ Play Console-based game.

        @param ConsoleController self: this ConsoleController object
        @rtype: None

        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        """
        print("This is a Tower of Anne Hoy Game\n The rules are the same as"
              " the Tower of Hanoi, you have to move the cheeses to the last"
              " stool.\n Remember that a cheese can only rest upon a "
              "smaller-sized cheese.\n To move a cheese, simply input the "
              "origin stool index followed by the destination stool index "
              "separated by a space. (e.g. 0 1 or 2 3)\n Type 'exit' in the "
              "first question if you which to end the game before completing "
              "it!")
        win_config = TOAHModel(self._stools)
        win_config.fill_last_stool(self._cheese)
        while self._model != win_config:
            print(self._model)
            user_move = input("\nPlease input your moves:\n")
            if user_move == 'exit':
                break
            else:
                moves = user_move.split()
                try:
                    move(self._model, int(moves[0]), int(moves[-1]))
                except ValueError:
                    print("You have not inputted a proper value!")
                except TypeError:
                    print("Please follow the input notation!")
                except KeyError:
                    print("That is not a valid stool index!")
                except IllegalMoveError:
                    print("That is not a valid move")
        if self._model == win_config:
            print("\n \n Congratulations on completing the game! \n")
            print(self._model)
        print("\nThank you for playing!\n")

if __name__ == '__main__':
    game = ConsoleController(5, 4)
    game.play_loop()
    # Leave lines below as they are, so you will know what python_ta checks.
    # You will need consolecontroller_pyta.txt in the same folder.
    import python_ta
    python_ta.check_all(config="consolecontroller_pyta.txt")
