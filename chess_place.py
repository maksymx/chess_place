import itertools


class ChessPlace:
    X = 8
    Y = 8

    def __init__(self, pieces):
        self.pieces = pieces

    def filter_coordinates(self, coordinates):
        """
        Filter iterable `coordinates` from all members who are outisde of `dimensions`.
        """
        return filter(lambda coord: 0 <= coord[0] < self.X and 0 <= coord[1] < self.Y, coordinates)

    def diagonals_iter(self, piece):
        """
        Generate all `coordinate`s on the same diagonals as `piece`.
        """
        piece_x, piece_y = piece["x"], piece["y"]
        directions = itertools.product((1, -1), repeat=2)
        for d_x, d_y in directions:
            new_coord = (piece_x + d_x, piece_y + d_y)
            while 0 <= new_coord[0] < self.X and 0 <= new_coord[1] < self.Y:
                yield new_coord
                new_coord = (new_coord[0] + d_x, new_coord[1] + d_y)

    def process_queen(self, piece):
        return self.process_bishop(piece) | self.process_rook(piece)

    def process_rook(self, piece):
        piece_x, piece_y = piece["x"], piece["y"]
        return set((x, y) for x, y in itertools.chain(
            ((piece_x, y) for y in range(self.Y) if y != piece_y),
            ((x, piece_y) for x in range(self.X) if x != piece_x),
        ))

    def process_bishop(self, piece):
        return set(self.diagonals_iter(piece))

    def process_knight(self, piece):
        """
        Return a set of all `coordinate`s a knight's move away from `piece`.
        """
        piece_x, piece_y = piece["x"], piece["y"]
        potential_attacked = (
            (piece_x + s_x * d_x, piece_y + s_y * d_y)
            for s_x, s_y in itertools.product((-1, 1), repeat=2)
            for d_x, d_y in ((1, 2), (2, 1))
        )
        return set(self.filter_coordinates(potential_attacked))

    def process_king(self, piece):
        """
        Return a set of all `coordinate`s a king's move away from `piece`.
        """
        potential_attacked = ((piece["x"] + d_x, piece["y"] + d_y) for d_x, d_y in
                              itertools.product((-1, 0, 1), repeat=2) if not (d_x == 0 and d_y == 0))
        return set(self.filter_coordinates(potential_attacked))

    def process_pawn(self, piece):
        """
        Return a set of all `coordinate`s a pawn's move away from `piece`.
        """
        potential_attacked = ((piece["x"] + 1, piece["y"]),)
        return set(self.filter_coordinates(potential_attacked))

    def attacked_coordinates_in_position(self, position):
        """
        Return a set of all `coordinate`s that are attacked in `position`.
        """
        placed_pieces = ({"x": coords[0], "y": coords[1], "t": piece_type} for coords, piece_type in position)
        attacked_coordinates = {coords for piece in placed_pieces for coords in
                                getattr(self, "process_{}".format(piece["t"]))(piece)}
        return attacked_coordinates

    def place_pieces(self):
        coordinates = [(x, y) for x in range(self.X) for y in range(self.Y)]
        last_pass = set([(coord, self.pieces[0]) for coord in coordinates])
        current_pass = set()

        for piece in self.pieces[1:]:
            for pos in last_pass:
                if isinstance(pos[1], str):
                    pos = [pos]

                attacked_in_position = self.attacked_coordinates_in_position(pos)
                pos_coordinates = {c[0] for c in pos}
                for coord in coordinates:
                    if coord in pos_coordinates or coord in attacked_in_position:
                        continue
                    placed_piece = {"x": coord[0], "y": coord[1], "t": piece}
                    attacked_by_piece = getattr(self, "process_{}".format(piece))(placed_piece)
                    if set(attacked_by_piece) & pos_coordinates:
                        continue

                    board = [(coord, piece)]
                    board.extend(pos)

                    frozen_board = tuple(board)
                    current_pass.add(frozen_board)
            last_pass, current_pass = current_pass, set()
        return last_pass


if __name__ == "__main__":
    cp = ChessPlace(['knight', 'pawn', 'king'])
    print(cp.place_pieces())
