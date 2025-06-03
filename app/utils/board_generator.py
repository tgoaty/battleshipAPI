import random
import json

BOARD_SIZE = 10
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


def generate_board() -> str:
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    def is_valid(x, y, size, horizontal):
        for i in range(size):
            xi = x + i if horizontal else x
            yi = y if horizontal else y + i
            if xi >= BOARD_SIZE or yi >= BOARD_SIZE or board[yi][xi] != 0:
                return False

            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = xi + dx, yi + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if board[ny][nx] != 0:
                            return False
        return True

    def place_ship(size):
        placed = False
        while not placed:
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - 1)
            horizontal = random.choice([True, False])
            if is_valid(x, y, size, horizontal):
                for i in range(size):
                    xi = x + i if horizontal else x
                    yi = y if horizontal else y + i
                    board[yi][xi] = 1
                placed = True

    for size in SHIP_SIZES:
        place_ship(size)

    return json.dumps(board)
