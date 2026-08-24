from __future__ import annotations

import random
from dataclasses import dataclass


BOARD_LAYOUT = [
    "###########",
    "#P...#....#",
    "#.#.#.##..#",
    "#.#...#...#",
    "#.###.#.#G#",
    "#.....#...#",
    "###########",
]


@dataclass
class Position:
    row: int
    col: int


class PacmanGame:
    def __init__(self, layout: list[str]) -> None:
        self.board = [list(line) for line in layout]
        self.pacman = self._find("P")
        self.ghost = self._find("G")
        self.score = 0
        self.pellets = sum(cell == "." for row in self.board for cell in row)
        self.game_over = False
        self.win = False

    def _find(self, target: str) -> Position:
        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):
                if cell == target:
                    return Position(row_index, col_index)
        raise ValueError(f"{target!r} not found in board")

    def _is_walkable(self, row: int, col: int) -> bool:
        return self.board[row][col] != "#"

    def _move(self, current: Position, dr: int, dc: int) -> Position:
        next_row = current.row + dr
        next_col = current.col + dc
        if self._is_walkable(next_row, next_col):
            return Position(next_row, next_col)
        return current

    def move_pacman(self, direction: str) -> None:
        deltas = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
        if direction not in deltas:
            return
        dr, dc = deltas[direction]
        self.pacman = self._move(self.pacman, dr, dc)

        cell = self.board[self.pacman.row][self.pacman.col]
        if cell == ".":
            self.board[self.pacman.row][self.pacman.col] = " "
            self.score += 10
            self.pellets -= 1
            if self.pellets == 0:
                self.win = True
                self.game_over = True

    def move_ghost(self) -> None:
        options: list[Position] = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            candidate = self._move(self.ghost, dr, dc)
            if candidate != self.ghost:
                options.append(candidate)
        if options:
            self.ghost = random.choice(options)

    def tick(self, direction: str) -> None:
        if self.game_over:
            return
        self.move_pacman(direction)
        self.move_ghost()
        if self.pacman == self.ghost:
            self.game_over = True

    def render(self) -> str:
        rows = [line[:] for line in self.board]
        rows[self.ghost.row][self.ghost.col] = "G"
        rows[self.pacman.row][self.pacman.col] = "P"
        return "\n".join("".join(row) for row in rows)


def main() -> None:
    game = PacmanGame(BOARD_LAYOUT)
    print("Pac-Man demo: use W/A/S/D, q to quit.")
    while not game.game_over:
        print("\n" + game.render())
        print(f"Score: {game.score}")
        move = input("Move: ").strip().lower()
        if move == "q":
            break
        game.tick(move[:1] if move else "")

    if game.win:
        print(f"You win! Final score: {game.score}")
    elif game.game_over:
        print(f"Caught by the ghost! Final score: {game.score}")
    else:
        print(f"Game ended. Final score: {game.score}")


if __name__ == "__main__":
    main()
