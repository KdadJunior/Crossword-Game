###########################################################
#  Crossword Puzzle Game
#  Algorithm
#    prompt for the filename of a crossword puzzle
#    load the crossword puzzle from the specified file
#    display the initial state of the puzzle and available clues
#    loop to accept and process user commands:
#       if command is 'H', display help menu with available commands
#       if command is 'C n', display 'n' number of clues (or all if 'n' is omitted)
#       if command is 'G i j A/D', prompt for a guess at specified location and direction
#       if command is 'R i j A/D', reveal the answer at specified location and direction
#       if command is 'T i j A/D', provide a hint for the first incorrect letter at specified location and direction
#       if command is 'S', restart the game with a new puzzle
#       if command is 'Q', quit the game
#    display the updated state of the puzzle after each command
#    check if the puzzle is solved after each command; if so, display a congratulations message
#    display closing message upon exiting the game
###########################################################

from crossword import Crossword
import sys


HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
                "\nC n - Display n of the current puzzle's down and across clues" \
                "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
                "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
                "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
                "\nH - Display the menu" \
                "\nS - Restart the game" \
                "\nQ - Quit the program"


OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"
"\nAcross"
"\nDown"
"\nPuzzle solved! Congratulations!"
"Letter {} is wrong, it should be {}"
"Invalid option/arguments. Type 'H' for help."
"Enter your guess (use _ for blanks): "
"This clue is already correct!"

RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")

def input( prompt=None ):
    """
        DO NOT MODIFY: Uncomment this function when submitting to Codio
        or when using the run_file.py to test your code.
        This function is needed for testing in Codio to echo the input to the output
        Function to get user input from the standard input (stdin) with an optional prompt.
        Args:
            prompt (str, optional): A prompt to display before waiting for input. Defaults to None.
        Returns:
            str: The user input received from stdin.
    """

    if prompt:
        print( prompt, end="" )
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip( "\n" )
    print( aaa_str )
    return aaa_str


# DEFINE YOUR FUNCTIONS HERE
def load_puzzle():
    """
    Loads a puzzle from a specified file. Re-prompts if file not found.
    """
    while True:
        filename = input(PUZZLE_PROMPT)
        try:
            puzzle = Crossword(filename)
            return puzzle
        except FileNotFoundError:
            print(PUZZLE_FILE_ERROR)


def display_clues(crossword, number=5):
    """
    Displays a specified number of clues for both across and down directions.
    """
    if not (0 < number < 6):
        raise IndexError("Invalid option/arguments. Type 'H' for help.")

    # Collecting and printing specified number of clues for each direction
    if 0 < number < 6:
        clue_dict = crossword.clues
        across_list = []
        down_list = []
        for key in clue_dict:
            if key[2] == 'A':
                across_list.append(clue_dict[key])
        for key in clue_dict:
            if key[2] == 'D':
                down_list.append(clue_dict[key])
        clues = across_list[:number] + down_list[:number]
        print("\nAcross")
        for clue in [clue for clue in clues if clue.down_across == 'A']:
            print(f"({clue.indices[0]}, {clue.indices[1]}) Across: {clue.clue}")
        print("\nDown")
        for clue in [clue for clue in clues if clue.down_across == 'D']:
            print(f"({clue.indices[0]}, {clue.indices[1]}) Down: {clue.clue}")


def get_and_validate_command(puzzle, input_command):
    """
    Validates user input command and returns it in a structured form.
    """
    # Handling simple commands
    command = list(input_command)
    if command[0] == "S" and len(command) == 1:
        return "S"
    elif command[0] == "Q" and len(command) == 1:
        return "Q"
    elif command[0] == "H" and len(command) == 1:
        return "H"
    elif len(command) == 3 and command[0] == "C" and command[1] == " ":
        # Handling clue display command
        try:
            return ("C",int(command[2]))
        except ValueError:
            return None
    elif command[0] == "G" or command[0] == 'R' or command[0] == 'T' and len(command) == 7:
        try:
            if 0 <= int(command[2]) <= 4 and 0 <= int(command[4]) <= 4:
                if command[6] == 'A' or command[6] == 'D':
                    return (command[0], int(command[2]), int(command[4]), command[6])
        except ValueError:
            return None
    else:
        return None


def main():
    """
    Main function to run the crossword puzzle game.
    """
    control = 0
    while control == 0:
        puzzle = load_puzzle()
        display_clues(puzzle)
        print(puzzle)
        print(HELP_MENU)
        while True:
            if puzzle.is_solved():
                print("\nPuzzle solved! Congratulations!")
                control = 1
                break
            try:
                choice = input('\nEnter option: ')
                command = get_and_validate_command(puzzle, choice)
                if command == None:
                    raise RuntimeError("Invalid option/arguments. Type 'H' for help.")
                elif command == 'Q':
                    control = 1
                    break
                elif command == 'S':
                    control = 0
                    break
                elif command == 'H':
                    print(HELP_MENU)
                    continue
                elif command[0] == 'C':
                    display_clues(puzzle, command[1])
                elif command[0] == 'G' or command[0] == 'R' or command[0] == 'T':
                    row, col, direction = int(command[1]), int(command[2]), command[3]
                    clue = puzzle.clues.get((row, col, direction))
                    if not clue:
                        print("Invalid option/arguments. Type 'H' for help.")
                        continue

                    if command[0] == 'G':
                        while True:
                            guess = input("Enter your guess (use _ for blanks): ").upper()
                            try:
                                puzzle.change_guess(clue, guess)
                                print(puzzle)
                                break
                            except RuntimeError as e:
                                print(e)
                                continue

                    elif command[0] == 'R':
                        puzzle.reveal_answer(clue)
                        print(puzzle)

                    elif command[0] == 'T':
                        wrong_index = puzzle.find_wrong_letter(clue)
                        if wrong_index != -1:
                            correct_letter = clue.answer[wrong_index]
                            print(f"Letter {wrong_index + 1} is wrong, it should be {correct_letter}")
                        else:
                            print("This clue is already correct!")
            except RuntimeError:
                print("Invalid option/arguments. Type 'H' for help.")
                continue

if __name__ == "__main__":
    main()