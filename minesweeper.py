import random
import pickle
import os


def print_grid(mine_values, grid_size):
    st = "   "
    for i in range(grid_size):
        st = st + "     " + str(i + 1)
    print(st)

    for row_number in range(grid_size):
        st = "     "
        if row_number == 0:
            for col_number in range(grid_size):
                st = st + "______"
            print(st)

        st = "     "
        for col_number in range(grid_size):
            st = st + "|     "
        print(st + "|")

        st = "  " + str(row_number + 1) + "  "
        for col_number in range(grid_size):
            st = st + "|  " + str(mine_values[row_number][col_number]) + "  "
        print(st + "|")

        st = "     "
        for col_number in range(grid_size):
            st = st + "|_____"
        print(st + '|')
    print()


def set_mines(numbers, num_of_mines, grid_size):
    count = 0
    while count < num_of_mines:
        value = random.randint(0, grid_size * grid_size - 1)

        row_number = value // grid_size
        col_number = value % grid_size

        if numbers[row_number][col_number] != -1:
            count = count + 1
            numbers[row_number][col_number] = -1


def set_values(numbers, grid_size):
    # To count cell value

    for r in range(grid_size):
        for col_number in range(grid_size):

            # Skip, if it contains a mine
            if numbers[r][col_number] == -1:
                continue

            # Check up
            if r > 0 and numbers[r - 1][col_number] == -1:
                numbers[r][col_number] = numbers[r][col_number] + 1
            # Check down
            if r < grid_size - 1 and numbers[r + 1][col_number] == -1:
                numbers[r][col_number] = numbers[r][col_number] + 1
            # Check left
            if col_number > 0 and numbers[r][col_number - 1] == -1:
                numbers[r][col_number] = numbers[r][col_number] + 1
            # Check right
            if col_number < grid_size - 1 and numbers[r][col_number + 1] == -1:
                numbers[r][col_number] = numbers[r][col_number] + 1
            # Check top-left
            if r > 0 and col_number > 0 and numbers[r - 1][col_number - 1] == -1:
                numbers[r][col_number] = numbers[r][col_number] + 1
            # Check top-right
            if r > 0 and col_number < grid_size - 1 and numbers[r - 1][col_number + 1] == -1:
                numbers[r][col_number] = numbers[r][col_number] + 1
            # Check below-left
            if r < grid_size - 1 and col_number > 0 and numbers[r + 1][col_number - 1] == -1:
                numbers[r][col_number] = numbers[r][col_number] + 1
            # Check below-right
            if r < grid_size - 1 and col_number < grid_size - 1 and numbers[r + 1][col_number + 1] == -1:
                numbers[r][col_number] = numbers[r][col_number] + 1


def neighbours(row_number, col_number, mine_values, numbers, grid_size, opened):
    if [row_number, col_number] not in opened:
        opened.append([row_number, col_number])

        if numbers[row_number][col_number] == 0:

            mine_values[row_number][col_number] = numbers[row_number][col_number]

            if row_number > 0:
                neighbours(row_number - 1, col_number, mine_values, numbers, grid_size, opened)
            if row_number < grid_size - 1:
                neighbours(row_number + 1, col_number, mine_values, numbers, grid_size, opened)
            if col_number > 0:
                neighbours(row_number, col_number - 1, mine_values, numbers, grid_size, opened)
            if col_number < grid_size - 1:
                neighbours(row_number, col_number + 1, mine_values, numbers, grid_size, opened)
            if row_number > 0 and col_number > 0:
                neighbours(row_number - 1, col_number - 1, mine_values, numbers, grid_size, opened)
            if row_number > 0 and col_number < grid_size - 1:
                neighbours(row_number - 1, col_number + 1, mine_values, numbers, grid_size, opened)
            if row_number < grid_size - 1 and col_number > 0:
                neighbours(row_number + 1, col_number - 1, mine_values, numbers, grid_size, opened)
            if row_number < grid_size - 1 and col_number < grid_size - 1:
                neighbours(row_number + 1, col_number + 1, mine_values, numbers, grid_size, opened)

        if numbers[row_number][col_number] != 0:
            mine_values[row_number][col_number] = numbers[row_number][col_number]


def game_over_check(mine_values, grid_size, num_of_mines):
    count = 0
    for r in range(grid_size):
        for col_number in range(grid_size):

            if mine_values[r][col_number] != ' ' and mine_values[r][col_number] != 'F':
                count = count + 1

    if count == grid_size * grid_size - num_of_mines:
        return True
    else:
        return False


def show_mines(mine_values, numbers, grid_size):
    for r in range(grid_size):
        for col_number in range(grid_size):
            if numbers[r][col_number] == -1:
                mine_values[r][col_number] = 'M'


def print_instructions():
    print("Instructions:")
    print("1. The grid size must be from 2 to 9")
    print("2. The number or mines must be from 1 to the half of the grid cells")
    print("3. Enter row and column number to select a cell, Example \"2 3\"")
    print("4. In order to flag a mine, enter F after row and column numbers, Example \"2 3 F\"")
    print("5. If you decide to leave during the game, you can save your progress by writing \"s\"")
    print("6. Write \"q\" in order to quit")


def generate_new_game(grid_size, num_of_mines):
    numbers = [[0 for y in range(grid_size)] for x in range(grid_size)]
    mine_values = [[' ' for y in range(grid_size)] for x in range(grid_size)]

    set_mines(numbers, num_of_mines, grid_size)
    set_values(numbers, grid_size)
    return numbers, mine_values


def play(numbers, mine_values, opened, flags, num_of_mines, grid_size):
    print_instructions()

    game_over = False

    # Game loop
    while not game_over:
        print_grid(mine_values, grid_size)

        user_input = input("Enter column and row_number number: ").split()

        if (user_input[0]) == "q":
            quit()

        if user_input[0] == "s":
            file = open('storage.p', 'wb')
            pickle.dump(numbers, file)
            pickle.dump(mine_values, file)
            pickle.dump(opened, file)
            pickle.dump(flags, file)
            pickle.dump(num_of_mines, file)
            file.close()
            print("Game saved\n")

        if len(user_input) == 2:
            try:
                value = list(map(int, user_input))
            except ValueError:
                print("Wrong input!")
                print_instructions()
                continue

        elif len(user_input) == 3:
            if user_input[2] != 'F' and user_input[2] != 'f':
                print("Wrong Input!")
                print_instructions()
                continue

            try:
                value = list(map(int, user_input[:2]))
            except ValueError:
                print("Wrong input!")
                print_instructions()
                continue

            if value[0] > grid_size or value[0] < 1 or value[1] > grid_size or value[1] < 1:
                print("Wrong input!")
                print_instructions()
                continue

            col_number = value[0] - 1
            row_number = value[1] - 1

            if [row_number, col_number] in flags:
                print("Removing flag")
                flags.remove([row_number, col_number])
                mine_values[row_number][col_number] = ' '
                continue

            # Check the number of flags
            if len(flags) < num_of_mines:
                flags.append([row_number, col_number])
                mine_values[row_number][col_number] = 'F'
                print("Flag set")
                continue
            else:
                print("All flags set")
                continue

        else:
            print("Wrong input!")
            print_instructions()
            continue

        # Check if the input fit size of numbers
        if value[0] > grid_size or value[0] < 1 or value[1] > grid_size or value[1] < 1:
            print("Wrong Input!")
            print_instructions()
            continue

        col_number = value[0] - 1
        row_number = value[1] - 1

        if numbers[row_number][col_number] == -1:
            mine_values[row_number][col_number] = 'M'
            show_mines(mine_values, numbers, grid_size)
            print_grid(mine_values, grid_size)
            print("Game over! Landed on mine")
            game_over = True
            continue

        elif numbers[row_number][col_number] == 0:
            mine_values[row_number][col_number] = '0'
            neighbours(row_number, col_number, mine_values, numbers, grid_size, opened)

        else:
            mine_values[row_number][col_number] = numbers[row_number][col_number]

        # Check if all cells are open
        if game_over_check(mine_values, grid_size, num_of_mines):
            show_mines(mine_values, numbers, grid_size)
            print_grid(mine_values, grid_size)
            print("You are the winner!")
            game_over = True
            continue


def choose_game_mode():
    while True:
        try:
            print("\nMINESWEEPER MAIN MENU")
            print("1 - Standard game 5x5")
            print("2 - Custom game")
            print("3 - Load game")
            print("4 - Quit")
            print("Select the game mode: ")
            user_input = int(input())
            # Standard game 5x5
            if user_input == 1:
                grid_size = 5
                num_of_mines = random.randint(2, 5)
                numbers, mine_values = generate_new_game(grid_size, num_of_mines)
                flags = []
                opened = []
                play(numbers, mine_values, opened, flags, num_of_mines, grid_size)

            # Custom game
            elif user_input == 2:
                grid_size = int(input("Print size of grid: "))
                num_of_mines = int(input("Print number of mines: "))
                numbers, mine_values = generate_new_game(grid_size, num_of_mines)
                flags = []
                opened = []
                play(numbers, mine_values, opened, flags, num_of_mines, grid_size)

            # Loaded game
            elif user_input == 3:
                if os.path.isfile('./storage.p'):
                    file = open('storage.p', 'rb')
                    numbers = pickle.load(file)
                    mine_values = pickle.load(file)
                    opened = pickle.load(file)
                    flags = pickle.load(file)
                    num_of_mines = pickle.load(file)
                    grid_size = len(numbers)

                    play(numbers, mine_values, opened, flags, num_of_mines, grid_size)
                else:
                    print("There are no savings available")
                    quit(1)
            elif user_input == 4:
                quit()

        except ValueError:
            print("\nInput error!")
            continue


if __name__ == "__main__":
    choose_game_mode()