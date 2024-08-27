###########################################################
#  Crossword Puzzle Game
#  Algorithm
#    load crossword puzzle from a CSV file
#    display the initial state of the puzzle
#    loop to accept user commands (guess, reveal, check solved)
#       if guess command:
#           update the guess on the puzzle board
#           check and display if the guess is correct or not
#       if reveal command:
#           reveal the answer for a clue on the board
#       if check solved command:
#           determine if the puzzle has been fully and correctly solved
#    display closing message when the puzzle is solved or upon exit
###########################################################

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self, clue, new_guess): # fill out the parameters
        """
        Updates the board with new_guess for clue, checking for valid length and characters.
        Raises RuntimeError for invalid inputs.
        """
        # Check if the guess matches the length of the clue's answer
        if len(new_guess) != len(clue.answer):
            raise RuntimeError("Guess length does not match the length of the clue.\n")

        # Check if the guess contains only valid characters
        if not all(char in GUESS_CHARS for char in new_guess):
            raise RuntimeError("Guess contains invalid characters.\n")

        # Update the puzzle board with the new guess
        start_row, start_col = clue.indices
        direction = clue.down_across

        for i, char in enumerate(new_guess):
            if direction == 'A':
                self.board[start_row][start_col + i] = char
            else:  # direction == 'D'
                self.board[start_row + i][start_col] = char

    def reveal_answer(self, clue):  # fill out the parameters
        """
         Reveals the answer for a specified clue on the crossword puzzle board.
        :param clue: A Clue object for which the answer will be revealed.
        """
        # Extracting the starting position and orientation of the clue
        start_row, start_col = clue.indices
        direction = clue.down_across

        # Iterate through the answer characters and place them on the board
        for i, char in enumerate(clue.answer):
            if direction == 'A':  # If the clue is across
                self.board[start_row][start_col + i] = char
            else:  # If the clue is down
                self.board[start_row + i][start_col] = char

    def find_wrong_letter(self, clue):  # fill out the parameters
        """
        Identifies the first incorrect letter in a user's guess for a clue.
        :param clue: A Clue object representing the clue to check against the user's guess.
        :return: The index of the first discrepancy between the guess and the correct answer,
             or -1 if the guess is entirely correct.
        """
        start_row, start_col = clue.indices
        direction = clue.down_across
        answer = clue.answer

        # Iterate through each character in the answer
        for i, correct_char in enumerate(answer):
            if direction == 'A':  # If the clue is across
                board_char = self.board[start_row][start_col + i]
            else:  # If the clue is down
                board_char = self.board[start_row + i][start_col]

            # Compare the character on the board with the correct character from the answer
            if board_char != correct_char:
                # Return the index of the first discrepancy
                return i

        # If no discrepancies are found, return -1
        return -1

    def is_solved(self):  # fill out the parameters
        """
        Checks if the entire crossword puzzle has been successfully solved.
        :return: True if the puzzle is solved (all guesses match the correct answers), False otherwise.
        """
        for clue_key, clue in self.clues.items():
            start_row, start_col = clue.indices
            direction = clue.down_across

            for i, correct_char in enumerate(clue.answer):
                if direction == 'A':
                    board_char = self.board[start_row][start_col + i]
                else:  # direction == 'D'
                    board_char = self.board[start_row + i][start_col]

                if board_char != correct_char:
                    # If any character does not match, the puzzle is not solved.
                    return False

            # If we get through all clues without finding a discrepancy, the puzzle is solved.
        return True
