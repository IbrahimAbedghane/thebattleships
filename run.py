import random

def create_grid(size):
    return [['~' for _ in range(size)] for _ in range(size)]

def display_grid(grid, hide_ships=True):
    size = len(grid)
    print("  " + " ".join(str(i) for i in range(size)))
    for idx, row in enumerate(grid):
        display_row = []
        for cell in row:
            if hide_ships and cell == 'S':
                display_row.append('~')
            else:
                display_row.append(cell)
        print(f"{idx} " + " ".join(display_row))

def place_ships(grid, num_ships):
    size = len(grid)
    ships_placed = 0
    while ships_placed < num_ships:
        orientation = random.choice(['H', 'V'])
        ship_length = random.randint(2, 3)  # Ships of length 2 or 3
        if orientation == 'H':
            row = random.randint(0, size - 1)
            col = random.randint(0, size - ship_length)
            if all(grid[row][col + i] == '~' for i in range(ship_length)):
                for i in range(ship_length):
                    grid[row][col + i] = 'S'
                ships_placed += 1
        else:
            row = random.randint(0, size - ship_length)
            col = random.randint(0, size - 1)
            if all(grid[row + i][col] == '~' for i in range(ship_length)):
                for i in range(ship_length):
                    grid[row + i][col] = 'S'
                ships_placed += 1

def get_user_guess(size):
    while True:
        try:
            x = int(input("Enter column (X coordinate):\n "))
            y = int(input("Enter row (Y coordinate):\n "))
            if 0 <= x < size and 0 <= y < size:
                return x, y
            else:
                print("Coordinates are off-grid. Please try again.")
        except ValueError:
            print("Invalid input. Please enter integer values.")

def process_guess(opponent_grid, display_grid, x, y):
    if display_grid[y][x] in ['X', 'O']:
        print("Location already guessed.")
        return False
    elif opponent_grid[y][x] == 'S':
        print("Hit!")
        display_grid[y][x] = 'X'
        opponent_grid[y][x] = 'X'
        return True
    else:
        print("Miss.")
        display_grid[y][x] = 'O'
        opponent_grid[y][x] = 'O'
        return False

def computer_guess(player_grid, computer_memory):
    size = len(player_grid)
    while True:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if (x, y) not in computer_memory:
            computer_memory.add((x, y))
            if player_grid[y][x] == 'S':
                print(f"Computer guessed ({x}, {y}) - Hit!")
                player_grid[y][x] = 'X'
                return True
            else:
                print(f"Computer guessed ({x}, {y}) - Miss.")
                player_grid[y][x] = 'O'
                return False

def player_place_ships(grid, num_ships):
    size = len(grid)
    ships_placed = 0
    while ships_placed < num_ships:
        print(f"Place ship {ships_placed + 1} of {num_ships}")
        orientation = input("Enter orientation (H for horizontal, V for vertical):\n ").upper()
        if orientation not in ['H', 'V']:
            print("Invalid orientation. Please enter 'H' or 'V'.")
            continue
        try:
            ship_length = int(input("Enter ship length (2 or 3):\n "))
            if ship_length not in [2, 3]:
                print("Invalid ship length. Please enter 2 or 3.")
                continue
            x = int(input("Enter starting column (X coordinate):\n"))
            y = int(input("Enter starting row (Y coordinate):\n "))
            if orientation == 'H':
                if x + ship_length > size:
                    print("Ship goes off-grid. Try again.")
                    continue
                if any(grid[y][x + i] != '~' for i in range(ship_length)):
                    print("Space already occupied. Try again.")
                    continue
                for i in range(ship_length):
                    grid[y][x + i] = 'S'
            else:
                if y + ship_length > size:
                    print("Ship goes off-grid. Try again.")
                    continue
                if any(grid[y + i][x] != '~' for i in range(ship_length)):
                    print("Space already occupied. Try again.")
                    continue
                for i in range(ship_length):
                    grid[y + i][x] = 'S'
            ships_placed += 1
            display_grid(grid, hide_ships=False)
        except ValueError:
            print("Invalid input. Please enter integer values.")

def count_ships(grid):
    return sum(cell == 'S' for row in grid for cell in row)

def play_game():
    print("Welcome to Battleships!")
    grid_size = int(input("Enter the grid size (e.g., 5 for a 5x5 grid):\n "))
    num_ships = int(input("Enter the number of ships:\n "))
    player_grid = create_grid(grid_size)
    computer_grid = create_grid(grid_size)
    player_display_grid = create_grid(grid_size)
    computer_display_grid = create_grid(grid_size)
    computer_memory = set()

    print("\nPlace your ships:")
    player_place_ships(player_grid, num_ships)
    print("\nComputer is placing ships...")
    place_ships(computer_grid, num_ships)

    player_ships_remaining = count_ships(player_grid)
    computer_ships_remaining = count_ships(computer_grid)

    player_turn = True

    while player_ships_remaining > 0 and computer_ships_remaining > 0:
        if player_turn:
            print("\nYour turn:")
            display_grid(player_display_grid, hide_ships=False)
            x, y = get_user_guess(grid_size)
            hit = process_guess(computer_grid, player_display_grid, x, y)
            if hit:
                computer_ships_remaining -= 1
                print(f"Computer ships remaining: {computer_ships_remaining}")
            else:
                print(f"Computer ships remaining: {computer_ships_remaining}")
            player_turn = False
        else:
            print("\nComputer's turn:")
            hit = computer_guess(player_grid, computer_memory)
            if hit:
                player_ships_remaining -= 1
                print(f"Your ships remaining: {player_ships_remaining}")
            else:
                print(f"Your ships remaining: {player_ships_remaining}")
            player_turn = True

    if player_ships_remaining == 0:
        print("\nGame Over! The computer wins.")
    else:
        print("\nCongratulations! You win.")

play_game()